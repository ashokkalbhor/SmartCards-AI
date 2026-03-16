import logging
import json
from typing import TypedDict, Annotated, Optional, List, Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from app.core.config import settings
from app.core.agent_tools import search_web, scrape_web_page, parse_pdf
from app.services.card_web_discovery_service import CardWebDiscoveryService

logger = logging.getLogger(__name__)

# --- State Definition ---
class CardUpdateState(TypedDict):
    card_name: str
    bank_name: str
    official_url: Optional[str]
    scraped_content: Optional[str]
    research_summary: Optional[str]
    extracted_data: Optional[Dict]
    verification_flags: Optional[Dict]
    errors: List[str]
    messages: Annotated[List[BaseMessage], add_messages]


def _apply_points_conversion(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Layer 2: Deterministic override of reward_rate for points-based cards.
    If points_per_100 and rupee_value_per_point are both present and non-zero,
    calculate effective_cashback = points_per_100 * rupee_value_per_point
    and override the LLM's reward_rate with this value.
    """
    for entry in extracted_data.get("spending_categories", []):
        p = entry.get("points_per_100")
        v = entry.get("rupee_value_per_point")
        if p is not None and v is not None and float(p) > 0 and float(v) > 0:
            calculated = round(float(p) * float(v), 2)
            logger.info(
                f"Points conversion: {entry.get('category_name')} "
                f"{p} pts × ₹{v}/pt = {calculated}% (was {entry.get('reward_rate')}%)"
            )
            entry["reward_rate"] = calculated
    for entry in extracted_data.get("merchant_rewards", []):
        p = entry.get("points_per_100")
        v = entry.get("rupee_value_per_point")
        if p is not None and v is not None and float(p) > 0 and float(v) > 0:
            calculated = round(float(p) * float(v), 2)
            logger.info(
                f"Points conversion: {entry.get('merchant_name')} "
                f"{p} pts × ₹{v}/pt = {calculated}% (was {entry.get('reward_rate')}%)"
            )
            entry["reward_rate"] = calculated
    return extracted_data

# --- Node 1 (New): Deep Research ---
async def deep_research_node(state: CardUpdateState):
    """
    Perform deep research using GPT-5-Search to find detailed reward rates.
    """
    logger.info(f"Node: Deep Research for {state['bank_name']} {state['card_name']}")
    
    discovery_service = CardWebDiscoveryService()
    
    try:
        summary = await discovery_service.perform_deep_research(
            bank_name=state['bank_name'],
            card_name=state['card_name']
        )
        
        return {
            "research_summary": summary,
            "messages": [SystemMessage(content=f"Deep Research Completed. Summary length: {len(summary)}")]
        }
    except Exception as e:
        return {
            "errors": [f"Deep Research failed: {str(e)}"],
            "messages": [SystemMessage(content=f"Deep Research Error: {str(e)}")]
        }

# --- Node 3: Extract Data ---
async def extract_structured_data(state: CardUpdateState):
    """
    Use LLM to parse the raw text into the strict JSON schema.
    """
    content = state.get('research_summary')
    if not content:
        # Fallback to scraped content if research failed?
        content = state.get('scraped_content')
        
    if not content:
        return {"errors": ["No content (Research/Scrape) to extract from"]}
        
    logger.info(f"Node: Extracting data for {state['card_name']}")
    
    # Using GPT-5 (configured in .env)
    llm = ChatOpenAI(model=settings.OPENAI_MODEL, temperature=0, openai_api_key=settings.OPENAI_API_KEY)
    
    user_msg = f"""
    Card: {state['bank_name']} {state['card_name']}
    
    Research Summary / Content:
    {content}
    
    Task: Map this data EXACTLY into the JSON structure.
    
    Rules for Merchant Rewards:
    - Explicit Matches: If research says '5% Cashback on Amazon', create a `merchant_reward` entry for 'Amazon'.
    - Inference: If card gives '5% on all Online Spend' AND research confirms no exclusions for Amazon/Flipkart, you MAY create entries for 'Amazon' and 'Flipkart' with 5% rate.
    - Caps: Always populate `reward_cap` if mentioned (e.g., 'Max 1000 cashback per month').
    """
    
    # To ensure JSON, we can use json_mode if model supports it (GPT-4-turbo does)
    llm_json = llm.bind(response_format={"type": "json_object"})
    
    try:
        # We need to construct the full messages
        # Using a proper prompt that mimics the original service's robust schema
        # I will define a helper method or just put the big schema here.
        # For 'implementation correctness', I should make sure it matches what `CardUpdateService` expects.
        # The `CardUpdateService.compare_and_create_suggestions` expects keys like "fees", "spending_categories".
        
        full_json_schema = """
        {
          "fees": {
            "joining_fee": number or null,
            "annual_fee": number or null,
            "is_lifetime_free": boolean,
            "annual_fee_waiver_spend": number or null
          },
          "lounge_benefits": {
            "domestic_lounge_visits": number or null,
            "international_lounge_visits": number or null,
            "lounge_spend_requirement": number or null,
            "lounge_spend_period": string or null
          },
          "spending_categories": [
            {
              "category_name": string — MUST be one of exactly these 15 values:
                online shopping, offline spends, fuel, dining, food delivery, grocery,
                travel, utilities, rent, insurance, education, government payments,
                international, entertainment, wallets. Never invent new names. If no match, omit.
              "reward_rate": number — effective cashback %. For points cards: your best estimate.
                The system will recalculate and override this using points_per_100 × rupee_value_per_point when available.
              "points_per_100": number or null — REQUIRED for points-based cards: raw points earned per ₹100 spend.
                Set null for direct cashback cards.
              "rupee_value_per_point": number or null — REQUIRED for points-based cards: rupee value of 1 point.
                Find this on the bank's reward redemption/catalogue page. Set null if not found.
              "reward_cap": number or null,
              "reward_cap_period": string or null
            }
          ],
          "merchant_rewards": [
            {
              "merchant_name": string — MUST be one of exactly these 15 values:
                amazon, flipkart, swiggy, zomato, bigbasket, blinkit, myntra,
                uber, ola, bookmyshow, phonepe, airtel, netflix, nykaa, ajio.
                Only include if the card explicitly rewards this merchant. Never invent.
              "reward_rate": number — effective cashback %. For points cards: your best estimate.
              "points_per_100": number or null — same rule as spending_categories above.
              "rupee_value_per_point": number or null — same rule as spending_categories above.
              "reward_cap": number or null,
              "reward_cap_period": string or null
            }
          ],
          "source_urls": [string] — all URLs from Section 5, empty array if none
        }
        """

        msgs = [
            SystemMessage(content=f"Extract credit card data from the text into this JSON structure: {full_json_schema}. Only return JSON."),
            HumanMessage(content=user_msg)
        ]
        
        response = await llm_json.ainvoke(msgs)
        json_data = json.loads(response.content)
        
        # Inject the official URL into source_urls if the model returned none
        if not json_data.get("source_urls") and state.get("official_url"):
            json_data["source_urls"] = [state["official_url"]]

        # Layer 2: deterministic points → cashback conversion
        json_data = _apply_points_conversion(json_data)

        return {
            "extracted_data": json_data,
            "messages": [SystemMessage(content="Extraction successful")]
        }
        
    except Exception as e:
        return {"errors": [f"Extraction failed: {str(e)}"]}


# --- Node 3: Verify Extracted Data ---
async def verify_extracted_data(state: CardUpdateState):
    """
    Layer 3: Independent verification of extracted data using gpt-4.1-mini with web search.
    Flags fields where verifier disagrees with extractor → status becomes 'needs_review'.
    Fails open: if verification errors, pipeline continues with flags = {}.
    """
    extracted_data = state.get("extracted_data")
    if not extracted_data:
        return {"verification_flags": {}}

    logger.info(f"Node: Verifying data for {state['bank_name']} {state['card_name']}")

    discovery_service = CardWebDiscoveryService()
    flags = await discovery_service.verify_card_data(
        bank_name=state["bank_name"],
        card_name=state["card_name"],
        extracted_data=extracted_data,
    )

    flagged_count = sum(1 for v in flags.values() if v.get("flagged"))
    return {
        "verification_flags": flags,
        "messages": [SystemMessage(content=f"Verification complete. {flagged_count} field(s) flagged.")],
    }


# --- Graph Construction ---
def build_card_update_graph():
    workflow = StateGraph(CardUpdateState)

    workflow.add_node("deep_research", deep_research_node)
    workflow.add_node("extract_data", extract_structured_data)
    workflow.add_node("verify_data", verify_extracted_data)

    workflow.set_entry_point("deep_research")

    workflow.add_edge("deep_research", "extract_data")
    workflow.add_edge("extract_data", "verify_data")
    workflow.add_edge("verify_data", END)

    return workflow.compile()

# Singleton accessor
card_update_graph = build_card_update_graph()
