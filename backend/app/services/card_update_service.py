"""
Card Update Service - GenAI-powered automated card data updates
Fetches latest card information from official bank sources and creates edit suggestions.
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from sqlalchemy.orm import Session

from app.models.card_master_data import CardMasterData, CardSpendingCategory, CardMerchantReward
from app.models.edit_suggestion import EditSuggestion
from app.models.card_document import CardDocument
from app.models.community import CommunityPost
from app.models.user import User

logger = logging.getLogger(__name__)


class CardUpdateService:
    """Service for automated card data updates using GenAI"""
    
    def __init__(self):
        self.system_admin_user_id = None  # Will be set to system admin user

    def compare_and_create_suggestions(self, db: Session, card_id: int,
                                      extracted_data: Dict[str, Any],
                                      system_user_id: int,
                                      verification_flags: Optional[Dict[str, Any]] = None) -> List[EditSuggestion]:
        """Compare extracted data with current DB and create edit suggestions for changes.

        verification_flags format (from verify_card_data):
          { "<field_type>:<field_name>": { "extracted_value", "verified_value", "flagged", "reason" } }
        Flagged suggestions get status='needs_review' with verifier details in additional_data.
        """
        suggestions = []
        verification_flags = verification_flags or {}

        # Get current card data
        card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
        if not card:
            logger.error(f"Card {card_id} not found")
            return suggestions

        # Fetch existing pending/needs_review suggestions to avoid duplicates
        existing_pending = db.query(EditSuggestion).filter(
            EditSuggestion.card_master_id == card_id,
            EditSuggestion.status.in_(["pending", "needs_review"])
        ).all()
        pending_keys = {(s.field_type, s.field_name) for s in existing_pending}

        def _is_duplicate(field_type: str, field_name: str) -> bool:
            return (field_type, field_name) in pending_keys

        def _suggestion_status(field_type: str, field_name: str, base_additional: Dict) -> tuple:
            """Return (status, additional_data) — needs_review when verifier flagged this field."""
            flag_key = f"{field_type}:{field_name}"
            flag = verification_flags.get(flag_key, {})
            if flag.get("flagged"):
                additional = {**base_additional, "verifier": {
                    "verified_value": flag.get("verified_value"),
                    "reason": flag.get("reason", ""),
                    "model": "gpt-4.1-mini",
                }}
                return "needs_review", additional
            return "pending", base_additional

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
            if old_value != new_value and new_value is not None and not _is_duplicate("card_field", db_field):
                base_additional = {
                    "source_url": (extracted_data.get("source_urls") or [None])[0],
                    "extraction_date": datetime.utcnow().isoformat()
                }
                status, additional = _suggestion_status("card_field", db_field, base_additional)
                suggestion = EditSuggestion(
                    user_id=system_user_id,
                    card_master_id=card_id,
                    field_type="card_field",
                    field_name=db_field,
                    old_value=str(old_value) if old_value is not None else None,
                    new_value=str(new_value),
                    status=status,
                    suggestion_reason="Automated update from official source",
                    additional_data=additional,
                )
                suggestions.append(suggestion)
                logger.info(f"Created suggestion ({status}) for {db_field}: {old_value} -> {new_value}")
        
        # Compare spending categories
        current_categories = {cat.category_name: cat for cat in card.spending_categories}
        new_categories = extracted_data.get("spending_categories", [])
        
        MAX_SANE_REWARD_RATE = 30.0  # anything above 30% is almost certainly a raw multiplier, not effective cashback

        for new_cat in new_categories:
            cat_name = new_cat.get("category_name")
            raw_rate = new_cat.get("reward_rate")
            if raw_rate is not None and raw_rate > MAX_SANE_REWARD_RATE:
                logger.warning(
                    f"Skipping spending_category '{cat_name}' for card {card_id}: "
                    f"reward_rate {raw_rate}% exceeds sanity cap {MAX_SANE_REWARD_RATE}% — "
                    f"likely a raw points multiplier, not effective cashback."
                )
                continue
            if cat_name in current_categories:
                old_cat = current_categories[cat_name]
                if old_cat.reward_rate != new_cat.get("reward_rate") and not _is_duplicate("spending_category", cat_name):
                    base_additional = {
                        "source_url": (extracted_data.get("source_urls") or [None])[0],
                        "extraction_date": datetime.utcnow().isoformat(),
                        "category_data": new_cat,
                    }
                    status, additional = _suggestion_status("spending_category", cat_name, base_additional)
                    suggestion = EditSuggestion(
                        user_id=system_user_id,
                        card_master_id=card_id,
                        field_type="spending_category",
                        field_name=cat_name,
                        old_value=str(old_cat.reward_rate),
                        new_value=str(new_cat.get("reward_rate")),
                        status=status,
                        suggestion_reason="Automated update: reward rate changed",
                        additional_data=additional,
                    )
                    suggestions.append(suggestion)
            elif not _is_duplicate("spending_category", cat_name):
                # New category
                base_additional = {
                    "source_url": (extracted_data.get("source_urls") or [None])[0],
                    "extraction_date": datetime.utcnow().isoformat(),
                }
                status, additional = _suggestion_status("spending_category", cat_name, base_additional)
                suggestion = EditSuggestion(
                    user_id=system_user_id,
                    card_master_id=card_id,
                    field_type="spending_category",
                    field_name=cat_name,
                    old_value=None,
                    new_value=json.dumps(new_cat),
                    status=status,
                    suggestion_reason="Automated update: new category added",
                    additional_data=additional,
                )
                suggestions.append(suggestion)
        
        # Compare merchant rewards
        current_merchants = {merch.merchant_name: merch for merch in card.merchant_rewards}
        new_merchants = extracted_data.get("merchant_rewards", [])
        
        for new_merch in new_merchants:
            merch_name = new_merch.get("merchant_name")
            raw_merch_rate = new_merch.get("reward_rate")
            if raw_merch_rate is not None and raw_merch_rate > MAX_SANE_REWARD_RATE:
                logger.warning(
                    f"Skipping merchant_reward '{merch_name}' for card {card_id}: "
                    f"reward_rate {raw_merch_rate}% exceeds sanity cap {MAX_SANE_REWARD_RATE}% — "
                    f"likely a raw points multiplier, not effective cashback."
                )
                continue
            if merch_name in current_merchants:
                old_merch = current_merchants[merch_name]
                if old_merch.reward_rate != new_merch.get("reward_rate") and not _is_duplicate("merchant_reward", merch_name):
                    base_additional = {
                        "source_url": (extracted_data.get("source_urls") or [None])[0],
                        "extraction_date": datetime.utcnow().isoformat(),
                        "merchant_data": new_merch,
                    }
                    status, additional = _suggestion_status("merchant_reward", merch_name, base_additional)
                    suggestion = EditSuggestion(
                        user_id=system_user_id,
                        card_master_id=card_id,
                        field_type="merchant_reward",
                        field_name=merch_name,
                        old_value=str(old_merch.reward_rate),
                        new_value=str(new_merch.get("reward_rate")),
                        status=status,
                        suggestion_reason="Automated update: reward rate changed",
                        additional_data=additional,
                    )
                    suggestions.append(suggestion)
            elif not _is_duplicate("merchant_reward", merch_name):
                # New merchant
                base_additional = {
                    "source_url": (extracted_data.get("source_urls") or [None])[0],
                    "extraction_date": datetime.utcnow().isoformat(),
                }
                status, additional = _suggestion_status("merchant_reward", merch_name, base_additional)
                suggestion = EditSuggestion(
                    user_id=system_user_id,
                    card_master_id=card_id,
                    field_type="merchant_reward",
                    field_name=merch_name,
                    old_value=None,
                    new_value=json.dumps(new_merch),
                    status=status,
                    suggestion_reason="Automated update: new merchant added",
                    additional_data=additional,
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
    
    def save_source_urls_as_documents(self, db: Session, card_id: int,
                                      source_urls: List[str], system_user_id: int) -> None:
        """Save research source URLs as approved CardDocument link entries, skipping duplicates."""
        if not source_urls:
            return

        existing_urls = {
            doc.content for doc in db.query(CardDocument).filter(
                CardDocument.card_master_id == card_id,
                CardDocument.document_type == "link"
            ).all()
        }

        new_docs = []
        for url in source_urls:
            url = url.strip() if url else ""
            if not url or url in existing_urls:
                continue
            new_docs.append(CardDocument(
                user_id=system_user_id,
                card_master_id=card_id,
                title="Research Source",
                document_type="link",
                content=url,
                submission_reason="Auto-added by card update pipeline",
                status="approved",
            ))
            existing_urls.add(url)

        if new_docs:
            db.add_all(new_docs)
            db.commit()
            logger.info(f"Saved {len(new_docs)} source URL(s) as documents for card {card_id}")

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
