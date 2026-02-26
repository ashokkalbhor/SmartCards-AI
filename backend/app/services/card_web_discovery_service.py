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
            "tools": [{"type": "web_search"}],
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
            "You are a Senior Credit Card Researcher. "
            "Your goal is to find EXACT reward rates (in percentage) for specific merchants and categories. "
            "Use the 'web_search' tool to find authoritative sources (official bank pages + reputable blogs like Technofino/CardExpert). "
            "Synthesize valid data into a detailed summary."
        )
        
        user_prompt = (
            f"Perform a comprehensive deep-dive search for the '{bank_name} {card_name}' credit card.\n"
            "**Crucial Goal**: Find exact reward rates (%) for specific Spending Categories and VIP Merchants.\n\n"
            "**Search Targets**:\n"
            "1. **VIP Merchants**: Specifically look for reward rates (%) for:\n"
            "   - **Amazon, Flipkart, Swiggy, Zomato, Myntra, Uber, Ola, BigBasket, BookMyShow**.\n"
            "2. **Categories**: Dining, Travel, Fuel, Utilities, Rent, Insurance.\n"
            "3. **Exclusions**: Check 'Terms and Conditions' or 'Fair Usage Policy' for excluded MCCs.\n"
            "4. **Caps**: Look for monthly/daily capping on these rewards.\n\n"
            "**Output**: Return a detailed textual summary of these specific reward rates. "
            "If a merchant is getting benefits via a category (e.g., 'Amazon gets 5% because it falls under Online Spend'), EXPLICITLY state that.\n"
            "Format the summary clearly."
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
        
        # Only add web_search tool if NOT using the specialized search API model (which implies search)
        # Or if the model is standard GPT-4/5 which needs the tool.
        # The error said 'web_search_preview' not supported with 'gpt-5-search-api'.
        if "search-api" not in self.model: 
             payload["tools"] = [{"type": "web_search"}]

        try:
            # We call _request directly to avoid JSON parsing in _invoke
            response_json = await self._request(payload)
            content = self._extract_text_from_response(response_json)
            return content
        except Exception as exc:
            logger.error(f"Deep research failed: {exc}")
            return f"Research failed: {str(exc)}"

