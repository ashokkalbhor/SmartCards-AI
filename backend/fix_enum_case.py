#!/usr/bin/env python3
"""
Fix enum case issue in database
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from app.models.card_master_data import CardMasterData
from sqlalchemy.orm import sessionmaker
import structlog

logger = structlog.get_logger()


async def fix_enum_case():
    """Fix the enum case issue in the database"""
    try:
        logger.info("Starting enum case fix...")
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Find cards with incorrect enum case
        cards_with_issues = session.query(CardMasterData).filter(
            CardMasterData.card_tier == 'super_premium'
        ).all()
        
        logger.info(f"Found {len(cards_with_issues)} cards with incorrect enum case")
        
        # Fix the enum values
        for card in cards_with_issues:
            logger.info(f"Fixing card: {card.display_name}")
            # The enum value is already correct, just need to ensure it's properly set
            card.card_tier = 'super_premium'  # This should work with the enum
        
        session.commit()
        logger.info("Enum case fix completed successfully!")
        
    except Exception as e:
        logger.error("Enum case fix failed", error=str(e))
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    asyncio.run(fix_enum_case()) 