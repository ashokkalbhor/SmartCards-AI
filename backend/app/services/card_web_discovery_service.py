"""
Card Web Discovery Service - calls the OpenAI Responses API with web search tool support.
"""
import json
import logging
from typing import Any, Awaitable, Callable, Dict, List, Optional

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

API_URL = "https://api.openai.com/v1/responses"


class WebDiscoveryResult:
    def __init__(self, official_url: Optional[str] = None, reddit_threads: Optional[List[str]] = None):
        self.official_url = official_url
        self.reddit_threads = reddit_threads or []


def _safe_strip(value: Any) -> Optional[str]:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _normalise_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if isinstance(item, str) and item.strip()]
    return []


class CardWebDiscoveryService:
    """
    Uses OpenAI's Responses API (via httpx) to search for official credit card pages and Reddit discussions.
    """

    def __init__(
        self,
        *,
        request_func: Optional[Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]] = None,
        timeout: float = 90.0,
    ):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be configured for web discovery")

        configured_model = settings.OPENAI_BROWSE_MODEL or settings.OPENAI_MODEL or "gpt-4.1-mini"
        if configured_model.lower() in {"gpt-5", "gpt5", "gpt-4-turbo-preview"}:
            configured_model = "gpt-4.1-mini"

        self.model = configured_model
        self.timeout = timeout
        self._request = request_func or self._perform_request
        self._headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        # gpt-4.1 family uses 'web_search'; gpt-4o family requires 'web_search_preview'
        self._web_search_tool = (
            {"type": "web_search"}
            if any(x in configured_model for x in ("4.1", "4-1"))
            else {"type": "web_search_preview"}
        )

    async def discover_sources(self, *, bank_name: str, card_name: str) -> WebDiscoveryResult:
        primary_messages = self._build_prompt(bank_name=bank_name, card_name=card_name)
        data = await self._invoke(primary_messages)

        if not data.get("official_url"):
            logger.info(
                "Primary browse found no official URL for %s %s; retrying with simpler query",
                bank_name,
                card_name,
            )
            fallback_messages = self._build_retry_prompt(bank_name=bank_name, card_name=card_name)
            retry_data = await self._invoke(fallback_messages)
            if retry_data:
                data = {
                    "official_url": retry_data.get("official_url") or data.get("official_url"),
                    "reddit_threads": retry_data.get("reddit_threads") or data.get("reddit_threads", []),
                }

        return WebDiscoveryResult(
            official_url=_safe_strip(data.get("official_url")),
            reddit_threads=_normalise_list(data.get("reddit_threads")),
        )

    async def _invoke(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "input": messages,
            "tools": [self._web_search_tool],
        }

        try:
            response_json = await self._request(payload)
        except Exception as exc:
            logger.error("Web discovery request failed: %s", exc)
            return {}

        content = self._extract_text_from_response(response_json)
        if not content:
            logger.warning("Web discovery returned empty content")
            return {}

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning("Failed to parse discovery JSON: %s", content[:200])
            return {}

    async def _perform_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(API_URL, headers=self._headers, json=payload)
            if response.status_code >= 400:
                detail = response.json()
                raise RuntimeError(f"OpenAI error {response.status_code}: {detail}")
            return response.json()

    @staticmethod
    def _extract_text_from_response(response_json: Dict[str, Any]) -> str:
        texts: List[str] = []

        outputs = response_json.get("output") or response_json.get("choices") or []
        for output in outputs:
            content_items = output.get("content", [])
            for item in content_items:
                text_block = item.get("text")
                if isinstance(text_block, dict):
                    value = text_block.get("value")
                    if value:
                        texts.append(value)
                elif isinstance(text_block, str):
                    texts.append(text_block)

        if not texts:
            output_text = response_json.get("output_text")
            if output_text:
                texts.append(output_text)

        return "\n".join(texts)

    def _build_prompt(self, *, bank_name: str, card_name: str) -> List[Dict[str, str]]:
        system = (
            "Use live web search to identify authoritative information about Indian credit cards. "
            "Prefer official bank domains such as hdfcbank.com, axisbank.com, icicibank.com, sbi.co.in, kotakbank.com. "
            "Return concise JSON only."
        )
        user = (
            "1. Find the official bank webpage (product or terms page) for the following credit card.\n"
            "2. Provide up to three recent Reddit discussion URLs about the card.\n"
            "3. If no official page is found, set official_url to null but still list Reddit threads if available.\n\n"
            f"Bank: {bank_name}\n"
            f"Card: {card_name}\n\n"
            "Respond strictly in JSON with this structure:\n"
            "{\n"
            '  \"official_url\": string | null,\n'
            '  \"reddit_threads\": [string]\n'
            "}\n"
            "Always include full URLs. Only use trusted domains for official_url."
        )
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

    def _build_retry_prompt(self, *, bank_name: str, card_name: str) -> List[Dict[str, str]]:
        query = f"{bank_name} {card_name} credit card official site terms conditions"
        system = "Perform a focused web search and respond with JSON (official_url + reddit_threads)."
        user = (
            f"Search the web for: \"{query}\".\n"
            "Return JSON: {\"official_url\": string | null, \"reddit_threads\": [string]}.\n"
            "Prefer official bank domains for official_url."
        )
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

    async def perform_deep_research(self, *, bank_name: str, card_name: str) -> str:
        """
        Perform a comprehensive deep-dive search using the configured search model (GPT-5 Search).
        Returns a detailed textual summary of findings, focusing on specific merchant rewards.
        """
        system_prompt = (
            "You are a Senior Credit Card Researcher for the Indian market. "
            "Your goal is to find EXACT, current data for a specific credit card using web search. "
            "Prefer official bank websites, then reputable sources like Technofino, CardExpert, BankBazaar. "
            "Prefer pages dated within the last 12 months. Never guess — if data is not found, say 'Not found'."
        )

        user_prompt = (
            f"Perform a comprehensive research for the '{bank_name} {card_name}' credit card.\n\n"
            "Search and report ALL of the following. Organise your response into these exact sections:\n\n"
            "**SECTION 1 — FEES**\n"
            "  - Joining fee (₹) — state 0 if none\n"
            "  - Annual fee (₹) — state 0 if none\n"
            "  - Annual fee waiver spend threshold (₹) — state 'Not found' if no waiver\n"
            "  - Is it lifetime free? (yes/no)\n\n"
            "**SECTION 2 — LOUNGE ACCESS**\n"
            "  - Domestic airport lounge visits (count per year or per quarter)\n"
            "  - International airport lounge visits (count per year or per quarter) — state 'Not found' if not offered\n"
            "  - Minimum spend required to retain lounge access (₹ per quarter) — state 'Not found' if no requirement\n\n"
            "**SECTION 3 — SPENDING CATEGORY RATES**\n"
            "For each category below, report the EFFECTIVE CASHBACK PERCENTAGE (not raw multipliers).\n"
            "IMPORTANT — Reward Points Conversion Rule:\n"
            "  Many Indian cards use reward points (e.g. FIRST Coins, Edge Reward Points, RBL Coins).\n"
            "  If the card uses points, you MUST find:\n"
            "    (a) Points earned per ₹100 spend\n"
            "    (b) Rupee value per point from the bank's reward redemption/catalogue page\n"
            "  Then calculate: effective_% = (points_per_100 × rupee_value_per_point)\n"
            "  Example: 30 FIRST Coins per ₹100 × ₹0.25/coin = 7.5% effective cashback — report 7.5%, NOT 30%.\n"
            "  Never report a raw multiplier (e.g. '10X', '30X', '5 points') as a percentage.\n"
            "  If you cannot find the rupee value per point, state 'Not found'.\n"
            "Also report monthly or quarterly cap (₹ and period) where applicable.\n"
            "State 'Not found' if the card has no specific rate for that category.\n"
            "  Online Shopping, Offline Spends, Fuel, Dining, Food Delivery, Grocery,\n"
            "  Travel, Utilities, Rent, Insurance, Education, Government Payments,\n"
            "  International, Entertainment, Wallets\n\n"
            "**SECTION 4 — MERCHANT RATES**\n"
            "For each merchant below, report the EFFECTIVE CASHBACK PERCENTAGE using the same\n"
            "points-to-rupee conversion rule described in Section 3 above.\n"
            "Never report raw multipliers as percentages.\n"
            "If a merchant earns via a category rate (e.g. 'Amazon earns 5% under Online Shopping'), state that explicitly.\n"
            "State 'Not found' if not specifically mentioned.\n"
            "  Amazon, Flipkart, Swiggy, Zomato, BigBasket, Blinkit, Myntra,\n"
            "  Uber, Ola, BookMyShow, PhonePe, Airtel, Netflix, Nykaa, Ajio\n\n"
            "**SECTION 5 — SOURCE URLS**\n"
            "  List every URL you used to gather the above data (one per line).\n"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        logger.info(f"Starting Deep Research for {bank_name} {card_name} with model {self.model}")
        
        payload = {
            "model": self.model,
            "input": messages,
        }

        # Add the correct web search tool unless model has built-in search (search-api variants)
        if "search-api" not in self.model:
            payload["tools"] = [self._web_search_tool]

        try:
            # We call _request directly to avoid JSON parsing in _invoke
            response_json = await self._request(payload)
            content = self._extract_text_from_response(response_json)
            return content
        except Exception as exc:
            logger.error(f"Deep research failed: {exc}")
            return f"Research failed: {str(exc)}"

    async def verify_card_data(
        self, *, bank_name: str, card_name: str, extracted_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Independently verify extracted card data using the configured verify model (gpt-4.1-mini)
        with web search. Returns a dict of verification flags keyed by
        "<field_type>:<field_name>" with structure:
          { "extracted_value": ..., "verified_value": ..., "flagged": bool, "reason": str }
        """
        verify_model = settings.OPENAI_VERIFY_MODEL or "gpt-4.1-mini"
        # gpt-4.1 family uses 'web_search'; gpt-4o family uses 'web_search_preview'
        web_tool = (
            {"type": "web_search"}
            if any(x in verify_model for x in ("4.1", "4-1"))
            else {"type": "web_search_preview"}
        )

        # Build a compact summary of what was extracted so verifier can check each value
        lines = [f"Card: {bank_name} {card_name}", ""]
        fees = extracted_data.get("fees", {})
        if fees:
            lines.append("Fees:")
            for k, v in fees.items():
                if v is not None:
                    lines.append(f"  {k}: {v}")
        lounge = extracted_data.get("lounge_benefits", {})
        if lounge:
            lines.append("Lounge:")
            for k, v in lounge.items():
                if v is not None:
                    lines.append(f"  {k}: {v}")
        for cat in extracted_data.get("spending_categories", []):
            lines.append(f"spending_category:{cat['category_name']} = {cat.get('reward_rate')}%")
        for merch in extracted_data.get("merchant_rewards", []):
            lines.append(f"merchant_reward:{merch['merchant_name']} = {merch.get('reward_rate')}%")

        extracted_summary = "\n".join(lines)

        system_prompt = (
            "You are an independent credit card data verifier for the Indian market. "
            "Search the web to verify the accuracy of extracted card data. "
            "Use official bank pages and trusted sources (Technofino, CardExpert, BankBazaar). "
            "For reward rates on points-based cards, always convert to effective cashback %: "
            "effective_% = (points_per_100_spend × rupee_value_per_point). "
            "Never report raw multipliers as percentages. "
            "Return ONLY a JSON object — no markdown, no explanation outside JSON."
        )

        user_prompt = (
            f"Verify the following extracted data for the '{bank_name} {card_name}' credit card "
            f"by searching the web:\n\n{extracted_summary}\n\n"
            "For EACH item listed, search and confirm whether the value is correct.\n"
            "Return JSON in this exact format:\n"
            "{\n"
            '  "verified_fields": {\n'
            '    "<field_key>": {\n'
            '      "extracted_value": <number or string>,\n'
            '      "verified_value": <your finding>,\n'
            '      "flagged": true or false,\n'
            '      "reason": "<brief explanation>"\n'
            "    }\n"
            "  }\n"
            "}\n\n"
            "Field key format: 'spending_category:<name>', 'merchant_reward:<name>', 'fees:<field>'\n"
            "Set flagged=true only when you have high confidence the extracted value is WRONG."
        )

        payload = {
            "model": verify_model,
            "input": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "tools": [web_tool],
        }

        try:
            response_json = await self._request(payload)
            content = self._extract_text_from_response(response_json)
            # Strip markdown fences if present
            content = content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            result = json.loads(content)
            flags = result.get("verified_fields", {})
            logger.info(
                f"Verification complete for {bank_name} {card_name}: "
                f"{sum(1 for v in flags.values() if v.get('flagged'))} field(s) flagged"
            )
            return flags
        except Exception as exc:
            logger.error(f"Verification failed for {bank_name} {card_name}: {exc}")
            return {}  # Fail open — pipeline continues with pending status

