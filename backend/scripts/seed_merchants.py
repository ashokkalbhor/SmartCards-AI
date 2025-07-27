#!/usr/bin/env python3
"""
Seed merchants table with common merchants
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_async_db
from app.models.merchant import Merchant

# Common merchants data
MERCHANTS_DATA = [
    # Online Shopping
    ("amazon", "Amazon", "online_shopping"),
    ("flipkart", "Flipkart", "online_shopping"),
    ("myntra", "Myntra", "online_shopping"),
    ("nykaa", "Nykaa", "online_shopping"),
    ("ajio", "AJIO", "online_shopping"),
    ("snapdeal", "Snapdeal", "online_shopping"),
    ("paytmmall", "Paytm Mall", "online_shopping"),
    ("shopclues", "ShopClues", "online_shopping"),
    
    # Food Delivery
    ("swiggy", "Swiggy", "dining"),
    ("zomato", "Zomato", "dining"),
    ("dunzo", "Dunzo", "dining"),
    ("bigbasket", "BigBasket", "groceries"),
    ("grofers", "Grofers", "groceries"),
    ("zepto", "Zepto", "groceries"),
    ("blinkit", "Blinkit", "groceries"),
    ("instamart", "Instamart", "groceries"),
    
    # Travel & Transport
    ("uber", "Uber", "travel"),
    ("ola", "Ola", "travel"),
    ("makemytrip", "MakeMyTrip", "travel"),
    ("goibibo", "Goibibo", "travel"),
    ("booking.com", "Booking.com", "travel"),
    ("airbnb", "Airbnb", "travel"),
    ("irctc", "IRCTC", "travel"),
    ("redbus", "RedBus", "travel"),
    
    # Fuel
    ("reliance", "Reliance", "fuel"),
    ("hp", "HP", "fuel"),
    ("bp", "BP", "fuel"),
    ("shell", "Shell", "fuel"),
    ("indian oil", "Indian Oil", "fuel"),
    ("bharat petroleum", "Bharat Petroleum", "fuel"),
    
    # Entertainment
    ("netflix", "Netflix", "entertainment"),
    ("prime", "Amazon Prime", "entertainment"),
    ("hotstar", "Disney+ Hotstar", "entertainment"),
    ("bookmyshow", "BookMyShow", "entertainment"),
    ("spotify", "Spotify", "entertainment"),
    ("youtube", "YouTube", "entertainment"),
    
    # Utilities
    ("airtel", "Airtel", "utilities"),
    ("jio", "Jio", "utilities"),
    ("vodafone", "Vodafone", "utilities"),
    ("bsnl", "BSNL", "utilities"),
    ("tata power", "Tata Power", "utilities"),
    ("adani electricity", "Adani Electricity", "utilities"),
    
    # Healthcare
    ("pharmeasy", "PharmEasy", "healthcare"),
    ("1mg", "1mg", "healthcare"),
    ("netmeds", "NetMeds", "healthcare"),
    ("apollo", "Apollo Pharmacy", "healthcare"),
    ("medplus", "MedPlus", "healthcare"),
    
    # Education
    ("coursera", "Coursera", "education"),
    ("udemy", "Udemy", "education"),
    ("byju's", "BYJU'S", "education"),
    ("unacademy", "Unacademy", "education"),
    ("vedantu", "Vedantu", "education"),
    
    # Gaming
    ("steam", "Steam", "gaming"),
    ("epic games", "Epic Games", "gaming"),
    ("playstation", "PlayStation", "gaming"),
    ("xbox", "Xbox", "gaming"),
    ("nintendo", "Nintendo", "gaming"),
]

async def seed_merchants():
    """Seed merchants table with common merchants"""
    async for db in get_async_db():
        try:
            # Check if merchants already exist
            existing_count = await db.execute(
                text("SELECT COUNT(*) FROM merchants")
            )
            count = existing_count.scalar()
            
            if count > 0:
                print(f"Merchants table already has {count} records. Skipping seeding.")
                return
            
            # Insert merchants
            for merchant_name, display_name, category in MERCHANTS_DATA:
                merchant = Merchant(
                    name=merchant_name,
                    display_name=display_name,
                    primary_category=category,
                    is_active=True
                )
                db.add(merchant)
            
            await db.commit()
            print(f"Successfully seeded {len(MERCHANTS_DATA)} merchants")
            
        except Exception as e:
            print(f"Error seeding merchants: {e}")
            await db.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(seed_merchants()) 