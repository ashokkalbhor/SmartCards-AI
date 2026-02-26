"""
Card Update Service - GenAI-powered automated card data updates
Fetches latest card information from official bank sources and creates edit suggestions.
"""
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
import asyncio

from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.config import settings
from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward
from app.models.edit_suggestion import EditSuggestion
from app.models.community import CommunityPost
from app.models.user import User

logger = logging.getLogger(__name__)


class CardUpdateService:
    """Service for automated card data updates using GenAI"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0,  # Deterministic for factual extraction
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.system_admin_user_id = None  # Will be set to system admin user
    
    def _get_extraction_prompt(self, card_name: str, bank_name: str, variant: str = None) -> str:
        """Generate the structured extraction prompt for card data"""
        card_full_name = f"{bank_name} {card_name}"
        if variant:
            card_full_name += f" {variant}"
        
        return f"""You are a precise data extraction assistant. Extract credit card details ONLY from the provided official bank webpage content.

Extract the following details for "{card_full_name}" as structured JSON. If a field is not present, use null.

Return ONLY valid JSON in this exact structure:
{{
  "bank_name": string,
  "card_name": string,
  "card_variant": string or null,
  "card_network": string (Visa/Mastercard/Amex/RuPay),
  "card_tier": string (basic/premium/super_premium/elite),
  "fees": {{
    "joining_fee": number or null,
    "annual_fee": number or null,
    "is_lifetime_free": boolean,
    "annual_fee_waiver_spend": number or null,
    "foreign_transaction_fee": number or null,
    "late_payment_fee": number or null,
    "overlimit_fee": number or null,
    "cash_advance_fee": number or null
  }},
  "lounge_benefits": {{
    "domestic_lounge_visits": number or null,
    "international_lounge_visits": number or null,
    "lounge_spend_requirement": number or null,
    "lounge_spend_period": string or null (quarterly/monthly/yearly)
  }},
  "welcome_benefits": {{
    "welcome_bonus_points": number or null,
    "welcome_bonus_spend_requirement": number or null,
    "welcome_bonus_timeframe": number or null (days)
  }},
  "credit_limit": {{
    "minimum_credit_limit": number or null,
    "maximum_credit_limit": number or null
  }},
  "eligibility": {{
    "minimum_salary": number or null,
    "minimum_age": number or null,
    "maximum_age": number or null
  }},
  "features": {{
    "contactless_enabled": boolean,
    "chip_enabled": boolean,
    "mobile_wallet_support": [string] or null
  }},
  "insurance_benefits": [string] or null,
  "concierge_service": boolean,
  "milestone_benefits": [string] or null,
  "reward_program": {{
    "reward_program_name": string or null,
    "reward_expiry_period": number or null (months),
    "reward_conversion_rate": number or null,
    "minimum_redemption_points": number or null
  }},
  "spending_categories": [
    {{
      "category_name": string,
      "category_display_name": string,
      "reward_rate": number,
      "reward_type": string (cashback/points/miles),
      "reward_cap": number or null,
      "reward_cap_period": string or null (monthly/quarterly/yearly),
      "minimum_transaction_amount": number or null,
      "additional_conditions": string or null
    }}
  ],
  "merchant_rewards": [
    {{
      "merchant_name": string,
      "merchant_display_name": string,
      "merchant_category": string or null,
      "reward_rate": number,
      "reward_type": string (cashback/points/miles),
      "reward_cap": number or null,
      "reward_cap_period": string or null,
      "minimum_transaction_amount": number or null,
      "requires_registration": boolean,
      "additional_conditions": string or null
    }}
  ],
  "description": string or null,
  "terms_and_conditions_url": string or null,
  "application_url": string or null,
  "additional_features": [string] or null,
  "source_url": string (the URL of the page this data was extracted from)
}}

CRITICAL RULES:
- Only use information from the provided content
- Return valid JSON only, no markdown or explanation
- Use null for missing fields, never guess or hallucinate
- Ensure all numeric values are numbers, not strings
- All URLs must be complete and valid"""
    
    async def extract_card_data(self, page_content: str, card_name: str, 
                                bank_name: str, variant: str = None) -> Dict[str, Any]:
        """Extract structured card data from webpage content using GenAI"""
        try:
            system_prompt = self._get_extraction_prompt(card_name, bank_name, variant)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract data from this content:\n\n{page_content}"}
            ]
            
            response = await self.llm.ainvoke(messages)

            raw_content = self._normalize_response_content(response.content)
            payload = self._extract_json_block(raw_content)
            if payload is None:
                logger.error("Failed to parse JSON response: could not locate JSON block")
                logger.error(f"Response content: {raw_content[:500]}")
                raise json.JSONDecodeError("No JSON object found", raw_content, 0)

            extracted_data = json.loads(payload)
            
            logger.info(f"Successfully extracted data for {bank_name} {card_name}")
            return extracted_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response content: {raw_content[:500]}")
            raise
        except Exception as e:
            logger.error(f"Error extracting card data: {e}")
            raise

    @staticmethod
    def _normalize_response_content(content: Any) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    value = item.get("text")
                    if isinstance(value, dict):
                        parts.append(value.get("value", ""))
                    elif isinstance(value, str):
                        parts.append(value)
                else:
                    parts.append(str(item))
            return "\n".join(parts)
        return str(content or "")

    @staticmethod
    def _extract_json_block(text: str) -> Optional[str]:
        text = text.strip()

        if text.startswith("```"):
            first_newline = text.find("\n")
            if first_newline != -1:
                closing = text.find("```", first_newline + 1)
                if closing != -1:
                    text = text[first_newline + 1:closing].strip()

        start = text.find("{")
        if start == -1:
            return None
        stack = 0
        for idx in range(start, len(text)):
            char = text[idx]
            if char == "{":
                stack += 1
            elif char == "}":
                stack -= 1
                if stack == 0:
                    return text[start:idx + 1]
        return None
    
    def compare_and_create_suggestions(self, db: Session, card_id: int, 
                                      extracted_data: Dict[str, Any],
                                      system_user_id: int) -> List[EditSuggestion]:
        """Compare extracted data with current DB and create edit suggestions for changes"""
        suggestions = []
        
        # Get current card data
        card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
        if not card:
            logger.error(f"Card {card_id} not found")
            return suggestions
        
        # Compare card-level fields
        card_field_mapping = {
            "joining_fee": ("fees", "joining_fee"),
            "annual_fee": ("fees", "annual_fee"),
            "is_lifetime_free": ("fees", "is_lifetime_free"),
            "annual_fee_waiver_spend": ("fees", "annual_fee_waiver_spend"),
            "foreign_transaction_fee": ("fees", "foreign_transaction_fee"),
            "late_payment_fee": ("fees", "late_payment_fee"),
            "overlimit_fee": ("fees", "overlimit_fee"),
            "cash_advance_fee": ("fees", "cash_advance_fee"),
            "domestic_lounge_visits": ("lounge_benefits", "domestic_lounge_visits"),
            "international_lounge_visits": ("lounge_benefits", "international_lounge_visits"),
            "lounge_spend_requirement": ("lounge_benefits", "lounge_spend_requirement"),
            "lounge_spend_period": ("lounge_benefits", "lounge_spend_period"),
            "welcome_bonus_points": ("welcome_benefits", "welcome_bonus_points"),
            "welcome_bonus_spend_requirement": ("welcome_benefits", "welcome_bonus_spend_requirement"),
            "welcome_bonus_timeframe": ("welcome_benefits", "welcome_bonus_timeframe"),
            "minimum_credit_limit": ("credit_limit", "minimum_credit_limit"),
            "maximum_credit_limit": ("credit_limit", "maximum_credit_limit"),
            "minimum_salary": ("eligibility", "minimum_salary"),
            "minimum_age": ("eligibility", "minimum_age"),
            "maximum_age": ("eligibility", "maximum_age"),
            "contactless_enabled": ("features", "contactless_enabled"),
            "chip_enabled": ("features", "chip_enabled"),
            "concierge_service": ("concierge_service",),
            "reward_program_name": ("reward_program", "reward_program_name"),
            "reward_expiry_period": ("reward_program", "reward_expiry_period"),
            "reward_conversion_rate": ("reward_program", "reward_conversion_rate"),
            "minimum_redemption_points": ("reward_program", "minimum_redemption_points"),
            "description": ("description",),
            "terms_and_conditions_url": ("terms_and_conditions_url",),
            "application_url": ("application_url",),
        }
        
        for db_field, path in card_field_mapping.items():
            old_value = getattr(card, db_field)
            
            # Navigate nested structure
            new_value = extracted_data
            for key in path:
                new_value = new_value.get(key) if isinstance(new_value, dict) else None
                if new_value is None:
                    break
            
            # Compare values
            if old_value != new_value and new_value is not None:
                suggestion = EditSuggestion(
                    user_id=system_user_id,
                    card_master_id=card_id,
                    field_type="card_field",
                    field_name=db_field,
                    old_value=str(old_value) if old_value is not None else None,
                    new_value=str(new_value),
                    status="pending",
                    suggestion_reason=f"Automated update from official source",
                    additional_data={
                        "source_url": extracted_data.get("source_url"),
                        "extraction_date": datetime.utcnow().isoformat()
                    }
                )
                suggestions.append(suggestion)
                logger.info(f"Created suggestion for {db_field}: {old_value} -> {new_value}")
        
        # Compare spending categories
        current_categories = {cat.category_name: cat for cat in card.spending_categories}
        new_categories = extracted_data.get("spending_categories", [])
        
        for new_cat in new_categories:
            cat_name = new_cat.get("category_name")
            if cat_name in current_categories:
                old_cat = current_categories[cat_name]
                if old_cat.reward_rate != new_cat.get("reward_rate"):
                    suggestion = EditSuggestion(
                        user_id=system_user_id,
                        card_master_id=card_id,
                        field_type="spending_category",
                        field_name=cat_name,
                        old_value=str(old_cat.reward_rate),
                        new_value=str(new_cat.get("reward_rate")),
                        status="pending",
                        suggestion_reason=f"Automated update: reward rate changed",
                        additional_data={
                            "source_url": extracted_data.get("source_url"),
                            "extraction_date": datetime.utcnow().isoformat(),
                            "category_data": new_cat
                        }
                    )
                    suggestions.append(suggestion)
            else:
                # New category
                suggestion = EditSuggestion(
                    user_id=system_user_id,
                    card_master_id=card_id,
                    field_type="spending_category",
                    field_name=cat_name,
                    old_value=None,
                    new_value=json.dumps(new_cat),
                    status="pending",
                    suggestion_reason=f"Automated update: new category added",
                    additional_data={
                        "source_url": extracted_data.get("source_url"),
                        "extraction_date": datetime.utcnow().isoformat()
                    }
                )
                suggestions.append(suggestion)
        
        # Compare merchant rewards
        current_merchants = {merch.merchant_name: merch for merch in card.merchant_rewards}
        new_merchants = extracted_data.get("merchant_rewards", [])
        
        for new_merch in new_merchants:
            merch_name = new_merch.get("merchant_name")
            if merch_name in current_merchants:
                old_merch = current_merchants[merch_name]
                if old_merch.reward_rate != new_merch.get("reward_rate"):
                    suggestion = EditSuggestion(
                        user_id=system_user_id,
                        card_master_id=card_id,
                        field_type="merchant_reward",
                        field_name=merch_name,
                        old_value=str(old_merch.reward_rate),
                        new_value=str(new_merch.get("reward_rate")),
                        status="pending",
                        suggestion_reason=f"Automated update: reward rate changed",
                        additional_data={
                            "source_url": extracted_data.get("source_url"),
                            "extraction_date": datetime.utcnow().isoformat(),
                            "merchant_data": new_merch
                        }
                    )
                    suggestions.append(suggestion)
            else:
                # New merchant
                suggestion = EditSuggestion(
                    user_id=system_user_id,
                    card_master_id=card_id,
                    field_type="merchant_reward",
                    field_name=merch_name,
                    old_value=None,
                    new_value=json.dumps(new_merch),
                    status="pending",
                    suggestion_reason=f"Automated update: new merchant added",
                    additional_data={
                        "source_url": extracted_data.get("source_url"),
                        "extraction_date": datetime.utcnow().isoformat()
                    }
                )
                suggestions.append(suggestion)
        
        # Save all suggestions
        if suggestions:
            db.add_all(suggestions)
            db.commit()
            logger.info(f"Created {len(suggestions)} edit suggestions for card {card_id}")
        
        return suggestions
    
    def create_community_post_for_approval(self, db: Session, suggestion: EditSuggestion) -> Optional[int]:
        """Create a community post announcing an approved card update"""
        try:
            card = db.query(CardMasterData).filter(
                CardMasterData.id == suggestion.card_master_id
            ).first()
            
            if not card:
                logger.error(f"Card {suggestion.card_master_id} not found")
                return None
            
            # Generate post title and body based on change type
            if suggestion.field_type == "spending_category":
                title = f"🎉 Update: {card.display_name} - {suggestion.field_name} Rewards Changed"
                if suggestion.old_value and suggestion.new_value:
                    body = f"Good news everyone! The **{card.display_name}** has updated rewards for **{suggestion.field_name}** category.\n\n"
                    body += f"**Previous Rate:** {suggestion.old_value}%\n"
                    body += f"**New Rate:** {suggestion.new_value}%\n\n"
                else:
                    body = f"Good news everyone! The **{card.display_name}** now offers rewards for **{suggestion.field_name}** category.\n\n"
                    body += f"**Reward Rate:** {suggestion.new_value}%\n\n"
            elif suggestion.field_type == "merchant_reward":
                title = f"🎉 Update: {card.display_name} - {suggestion.field_name} Rewards Changed"
                if suggestion.old_value and suggestion.new_value:
                    body = f"Great news! The **{card.display_name}** has updated rewards for **{suggestion.field_name}**.\n\n"
                    body += f"**Previous Rate:** {suggestion.old_value}%\n"
                    body += f"**New Rate:** {suggestion.new_value}%\n\n"
                else:
                    body = f"Great news! The **{card.display_name}** now offers special rewards at **{suggestion.field_name}**.\n\n"
                    body += f"**Reward Rate:** {suggestion.new_value}%\n\n"
            else:
                title = f"ℹ️ Update: {card.display_name} - {suggestion.field_name.replace('_', ' ').title()} Changed"
                body = f"The **{card.display_name}** has been updated.\n\n"
                body += f"**Field:** {suggestion.field_name.replace('_', ' ').title()}\n"
                if suggestion.old_value:
                    body += f"**Previous Value:** {suggestion.old_value}\n"
                body += f"**New Value:** {suggestion.new_value}\n\n"
            
            # Add source if available
            if suggestion.additional_data and suggestion.additional_data.get("source_url"):
                body += f"\n**Source:** {suggestion.additional_data['source_url']}\n"
            
            body += f"\n_This update was automatically detected and approved._"
            
            # Create the community post
            post = CommunityPost(
                user_id=suggestion.reviewed_by or suggestion.user_id,
                card_master_id=card.id,
                title=title,
                body=body,
                upvotes=0,
                downvotes=0,
                comment_count=0
            )
            
            db.add(post)
            db.commit()
            db.refresh(post)
            
            logger.info(f"Created community post {post.id} for suggestion {suggestion.id}")
            return post.id
            
        except Exception as e:
            logger.error(f"Error creating community post: {e}")
            db.rollback()
            return None
    
    def get_or_create_system_user(self, db: Session) -> int:
        """Get or create the system admin user for automated updates"""
        system_email = "system@smartcardsai.internal"
        
        user = db.query(User).filter(User.email == system_email).first()
        if not user:
            from app.core.security import get_password_hash
            user = User(
                email=system_email,
                hashed_password=get_password_hash("system_automated_password_not_for_login"),
                first_name="System",
                last_name="Admin",
                is_active=True,
                is_verified=True,
                country="India"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created system user with ID {user.id}")
        
        self.system_admin_user_id = user.id
        return user.id
