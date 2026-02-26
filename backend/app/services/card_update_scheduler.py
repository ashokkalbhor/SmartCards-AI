"""
Card Update Scheduler - Run automated card updates monthly
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.card_master_data import CardMasterData
from app.models.credit_card import CreditCard
from app.services.card_update_service import CardUpdateService
# from app.services.card_web_discovery_service import CardWebDiscoveryService, WebDiscoveryResult
# from app.services.web_scraping_service import WebScrapingService
from app.core.agent_graph import card_update_graph

logger = logging.getLogger(__name__)


class CardUpdateScheduler:
    """Scheduler for automated monthly card data updates with external source discovery."""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.card_update_service = CardUpdateService()
        # self.scraping_service = WebScrapingService()
        # self._discovery_service: Optional[CardWebDiscoveryService] = None

        self.is_running: bool = False
        self.progress: Dict[str, Any] = {
            "total_cards": 0,
            "processed_cards": 0,
            "current": None,
            "last_completed": None,
        }
        self.last_run_summary: Optional[Dict[str, Any]] = None
        self.last_error: Optional[str] = None
        self._suggestions_created: int = 0
        self._cards_skipped: int = 0
        self._cards_failed: int = 0

    async def process_card_update(self, card: CardMasterData, db: Session, *, position: int, total: int):
        """Process a single card update end-to-end."""
        try:
            self._update_current(card=card, stage="agent_research", position=position, total=total)
            
            # --- AGENT INVOCATION ---
            initial_state = {
                "card_name": card.card_name,
                "bank_name": card.bank_name,
                "official_url": card.terms_and_conditions_url or None, # Use DB URL as seed
                "scraped_content": None,
                "extracted_data": None,
                "errors": [],
                "messages": []
            }
            
            logger.info(f"Invoking Agent for {card.card_name}")
            result = await card_update_graph.ainvoke(initial_state)
            
            # Check for failures
            if result.get("errors") or not result.get("extracted_data"):
                error_msg = "; ".join(result.get("errors", [])) or "Agent returned no data"
                logger.warning(f"Agent failed for {card.card_name}: {error_msg}")
                self._cards_failed += 1
                self._mark_processed(
                    card=card, 
                    status="agent_failed", 
                    suggestions_created=0, 
                    meta={"error": error_msg}
                )
                return

            extracted_data = result["extracted_data"]
            official_url = result.get("official_url")
            
            # --- COMPARISON & SUGGESTIONS ---
            self._update_current(card=card, stage="compare", position=position, total=total)
            
            system_user_id = self.card_update_service.get_or_create_system_user(db)
            
            suggestions = self.card_update_service.compare_and_create_suggestions(
                db,
                card.id,
                extracted_data,
                system_user_id,
            )

            suggestions_created = len(suggestions or [])
            if suggestions_created:
                self._suggestions_created += suggestions_created
                # Attach source metadata
                for suggestion in suggestions:
                    additional = suggestion.additional_data or {}
                    additional["official_source"] = official_url
                    suggestion.additional_data = additional
                db.commit()
                status = "suggestions_created"
            else:
                status = "no_change"

            self._mark_processed(
                card=card,
                status=status,
                suggestions_created=suggestions_created,
                meta={"source_url": official_url},
            )

        except Exception as exc:
            logger.error("Error processing card %s: %s", card.card_name, exc, exc_info=True)
            self._cards_failed += 1
            db.rollback()
            self._mark_processed(
                card=card,
                status="error",
                suggestions_created=0,
                meta={"error": str(exc)},
            )

    async def run_monthly_update(self):
        """Run the monthly card update process sequentially with status tracking.
        Now filters to portfolio cards only (cards with active holders)."""
        if self.is_running:
            logger.warning("Monthly update already running, skipping...")
            return

        logger.info("Starting automated card update process (portfolio cards only)")
        self.is_running = True
        self.last_error = None
        self._suggestions_created = 0
        self._cards_skipped = 0
        self._cards_failed = 0

        # Agent does not need pre-check
        # try:
        #     self._get_discovery_service()
        # except Exception as exc:
        # ...
        pass

        db = SessionLocal()
        try:
            # Query cards that have at least one active holder (portfolio cards)
            from sqlalchemy import func
            
            cards = (
                db.query(CardMasterData)
                .join(CreditCard, CardMasterData.id == CreditCard.card_master_data_id)
                .filter(
                    CardMasterData.is_active.is_(True),
                    CreditCard.is_active == True
                )
                .group_by(CardMasterData.id)
                .order_by(
                    func.count(CreditCard.id).desc(),  # Sort by holder count
                    CardMasterData.updated_at.desc().nullslast(),
                    CardMasterData.id.desc()
                )
                .all()
            )
            total = len(cards)
            self._reset_progress(total_cards=total)
            if total == 0:
                logger.info("No active cards found in user portfolios to process")

            for index, card in enumerate(cards, start=1):
                await self.process_card_update(card, db, position=index, total=total)
                await asyncio.sleep(5.0)  # Respect external API rate limits and allow GPT to cool down

            self.last_run_summary = {
                "total_cards": total,
                "processed_cards": self.progress["processed_cards"],
                "suggestions_created": self._suggestions_created,
                "skipped": self._cards_skipped,
                "failed": self._cards_failed,
                "completed_at": datetime.utcnow().isoformat(),
            }
            logger.info("Card update process completed: %s", self.last_run_summary)

        except Exception as exc:
            self.last_error = str(exc)
            logger.error("Error in monthly update process: %s", exc, exc_info=True)
        finally:
            db.close()
            self.is_running = False
            self.progress["current"] = None

    def start(self):
        """Start the scheduler (1st of every month at midnight)."""
        self.scheduler.add_job(
            self.run_monthly_update,
            CronTrigger(day=1, hour=0, minute=0),
            id="monthly_card_update",
            name="Monthly Card Data Update",
            replace_existing=True,
        )
        self.scheduler.start()
        logger.info("Card update scheduler started - will run monthly")

    def stop(self):
        """Stop the scheduler."""
        self.scheduler.shutdown()
        logger.info("Card update scheduler stopped")

    async def run_now(self):
        """Manually trigger the update process (e.g., via API)."""
        await self.run_monthly_update()

    async def run_portfolio_update(self):
        """Run update process for cards in user portfolios only (cards with active holders)."""
        if self.is_running:
            logger.warning("Portfolio update already running, skipping...")
            return

        logger.info("Starting portfolio-based card update process")
        self.is_running = True
        self.last_error = None
        self._suggestions_created = 0
        self._cards_skipped = 0
        self._cards_failed = 0

        db = SessionLocal()
        try:
            # Query cards that have at least one active holder
            from sqlalchemy import func
            
            cards = (
                db.query(CardMasterData)
                .join(CreditCard, CardMasterData.id == CreditCard.card_master_data_id)
                .filter(
                    CardMasterData.is_active.is_(True),
                    CreditCard.is_active == True
                )
                .group_by(CardMasterData.id)
                .order_by(
                    func.count(CreditCard.id).desc(),  # Sort by holder count
                    CardMasterData.updated_at.desc().nullslast(),
                    CardMasterData.id.desc()
                )
                .all()
            )
            
            total = len(cards)
            self._reset_progress(total_cards=total)
            
            if total == 0:
                logger.info("No cards found in user portfolios to process")
            else:
                logger.info(f"Found {total} cards in user portfolios to update")

            for index, card in enumerate(cards, start=1):
                await self.process_card_update(card, db, position=index, total=total)
                await asyncio.sleep(5.0)  # Respect external API rate limits

            self.last_run_summary = {
                "total_cards": total,
                "processed_cards": self.progress["processed_cards"],
                "suggestions_created": self._suggestions_created,
                "skipped": self._cards_skipped,
                "failed": self._cards_failed,
                "completed_at": datetime.utcnow().isoformat(),
                "update_type": "portfolio"
            }
            logger.info("Portfolio card update process completed: %s", self.last_run_summary)

        except Exception as exc:
            self.last_error = str(exc)
            logger.error("Error in portfolio update process: %s", exc, exc_info=True)
        finally:
            db.close()
            self.is_running = False
            self.progress["current"] = None

    async def run_single_card(self, card: CardMasterData, db: Session) -> Dict[str, Any]:
        """Process a single card outside the bulk workflow."""
        if self.is_running:
            raise RuntimeError("Card update process is already running")

        # Ensure discovery service is ready before mutating scheduler state
        # self._get_discovery_service()

        self.is_running = True
        self.last_error = None
        self._suggestions_created = 0
        self._cards_skipped = 0
        self._cards_failed = 0
        try:
            self._reset_progress(total_cards=1)
            await self.process_card_update(card, db, position=1, total=1)
            summary = {
                "status": self.progress.get("last_completed", {}),
                "suggestions_created": self._suggestions_created,
                "skipped": self._cards_skipped,
                "failed": self._cards_failed,
            }
            self.last_run_summary = {
                "total_cards": 1,
                "processed_cards": self.progress["processed_cards"],
                "suggestions_created": self._suggestions_created,
                "skipped": self._cards_skipped,
                "failed": self._cards_failed,
                "completed_at": datetime.utcnow().isoformat(),
            }
            return summary
        finally:
            self.is_running = False
            self.progress["current"] = None

    def get_status(self) -> Dict[str, Any]:
        """Return a snapshot of the scheduler state for the status endpoint."""
        job = self.scheduler.get_job("monthly_card_update") if self.scheduler else None
        next_run = job.next_run_time.isoformat() if job and job.next_run_time else None
        return {
            "is_running": self.is_running,
            "scheduler_running": self.scheduler.running,
            "next_run": next_run,
            "progress": self.progress,
            "last_run_summary": self.last_run_summary,
            "last_error": self.last_error,
        }



    def _reset_progress(self, *, total_cards: int):
        self.progress = {
            "total_cards": total_cards,
            "processed_cards": 0,
            "current": None,
            "last_completed": None,
        }

    def _update_current(
        self,
        *,
        card: CardMasterData,
        stage: str,
        position: int,
        total: int,
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.progress["current"] = {
            "card_id": card.id,
            "card_name": card.card_name,
            "bank_name": card.bank_name,
            "stage": stage,
            "position": position,
            "total": total,
            **(extra or {}),
        }

    def _mark_processed(
        self,
        *,
        card: CardMasterData,
        status: str,
        suggestions_created: int,
        meta: Optional[Dict[str, Any]] = None,
    ):
        self.progress["processed_cards"] += 1
        self.progress["last_completed"] = {
            "card_id": card.id,
            "card_name": card.card_name,
            "bank_name": card.bank_name,
            "status": status,
            "suggestions_created": suggestions_created,
            "timestamp": datetime.utcnow().isoformat(),
            "meta": meta or {},
        }
        self.progress["current"] = None




# Global scheduler instance
card_update_scheduler = CardUpdateScheduler()
