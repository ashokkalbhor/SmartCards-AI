"""
Merchants API endpoints for market research-based popularity data
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.merchant_popularity import merchant_popularity_service, MerchantTier
from app.models.merchant import Merchant

router = APIRouter()

@router.get("/popularity-ranking")
def get_merchant_popularity_ranking(
    limit: int = Query(20, ge=1, le=50, description="Number of merchants to return"),
    category: Optional[str] = Query(None, description="Filter by merchant category"),
    tier: Optional[str] = Query(None, description="Filter by popularity tier"),
    db: Session = Depends(get_db)
):
    """
    Get merchant popularity ranking based on market research data
    """
    try:
        # Get sorted merchants by popularity
        if category:
            merchant_names = merchant_popularity_service.get_top_merchants_by_category(category, limit)
        elif tier:
            # Convert tier string to enum
            tier_enum = None
            for t in MerchantTier:
                if t.value == tier:
                    tier_enum = t
                    break
            
            if tier_enum:
                merchant_names = merchant_popularity_service.get_merchants_by_tier(tier_enum)[:limit]
            else:
                merchant_names = merchant_popularity_service.get_sorted_merchants_by_popularity()[:limit]
        else:
            merchant_names = merchant_popularity_service.get_sorted_merchants_by_popularity()[:limit]
        
        # Get market data for each merchant
        result = []
        for rank, merchant_name in enumerate(merchant_names, 1):
            market_data = merchant_popularity_service.get_merchant_market_data(merchant_name)
            if market_data:
                result.append({
                    "rank": rank,
                    "merchant_name": merchant_name,
                    "display_name": market_data.display_name,
                    "category": market_data.category,
                    "tier": market_data.tier.value,
                    "popularity_score": market_data.popularity_score,
                    "market_share_percent": market_data.market_share_percent,
                    "monthly_active_users_millions": market_data.monthly_active_users_millions,
                    "growth_rate_percent": market_data.growth_rate_percent,
                    "search_volume_index": market_data.search_volume_index,
                    "social_media_followers_millions": market_data.social_media_followers_millions,
                    "app_downloads_millions": market_data.app_downloads_millions,
                    "revenue_impact_score": market_data.revenue_impact_score
                })
        
        return {
            "merchants": result,
            "total_count": len(result),
            "ranking_method": "market_research_based"
        }
        
    except Exception as e:
        return {
            "error": f"Failed to get merchant popularity ranking: {str(e)}",
            "merchants": [],
            "total_count": 0
        }

@router.get("/categories")
def get_merchant_categories():
    """
    Get all merchant categories with their top merchants
    """
    categories = {}
    
    # Get unique categories from market data
    unique_categories = set()
    for merchant_name, market_data in merchant_popularity_service.market_data.items():
        unique_categories.add(market_data.category)
    
    # Get top merchants for each category
    for category in sorted(unique_categories):
        top_merchants = merchant_popularity_service.get_top_merchants_by_category(category, 5)
        categories[category] = {
            "top_merchants": top_merchants,
            "merchant_count": len([m for m in merchant_popularity_service.market_data.values() if m.category == category])
        }
    
    return {
        "categories": categories,
        "total_categories": len(categories)
    }

@router.get("/tiers")
def get_merchant_tiers():
    """
    Get all merchant tiers with their merchants
    """
    tiers = {}
    
    for tier in MerchantTier:
        merchants = merchant_popularity_service.get_merchants_by_tier(tier)
        tiers[tier.value] = {
            "merchants": merchants,
            "merchant_count": len(merchants),
            "description": {
                MerchantTier.TIER_1_SUPER_POPULAR: "Market leaders with 40%+ share",
                MerchantTier.TIER_2_VERY_POPULAR: "Strong players with 20-40% share",
                MerchantTier.TIER_3_POPULAR: "Established players with 10-20% share",
                MerchantTier.TIER_4_MODERATE: "Growing players with 5-10% share",
                MerchantTier.TIER_5_EMERGING: "New/niche players with <5% share"
            }[tier]
        }
    
    return {
        "tiers": tiers,
        "total_tiers": len(tiers)
    }

@router.get("/growth-merchants")
def get_growth_merchants(
    min_growth_rate: float = Query(25.0, ge=0.0, le=100.0, description="Minimum growth rate percentage")
):
    """
    Get merchants with high growth rates (emerging players)
    """
    growth_merchants = merchant_popularity_service.get_growth_merchants(min_growth_rate)
    
    result = []
    for merchant_name in growth_merchants:
        market_data = merchant_popularity_service.get_merchant_market_data(merchant_name)
        if market_data:
            result.append({
                "merchant_name": merchant_name,
                "display_name": market_data.display_name,
                "category": market_data.category,
                "growth_rate_percent": market_data.growth_rate_percent,
                "popularity_score": market_data.popularity_score,
                "market_share_percent": market_data.market_share_percent,
                "tier": market_data.tier.value
            })
    
    return {
        "growth_merchants": result,
        "total_count": len(result),
        "min_growth_rate": min_growth_rate
    }

@router.get("/{merchant_name}/market-data")
def get_merchant_market_data(merchant_name: str):
    """
    Get detailed market data for a specific merchant
    """
    market_data = merchant_popularity_service.get_merchant_market_data(merchant_name)
    
    if not market_data:
        return {
            "error": f"Merchant '{merchant_name}' not found in market data",
            "merchant_name": merchant_name
        }
    
    return {
        "merchant_name": merchant_name,
        "display_name": market_data.display_name,
        "category": market_data.category,
        "tier": market_data.tier.value,
        "popularity_score": market_data.popularity_score,
        "market_share_percent": market_data.market_share_percent,
        "monthly_active_users_millions": market_data.monthly_active_users_millions,
        "growth_rate_percent": market_data.growth_rate_percent,
        "search_volume_index": market_data.search_volume_index,
        "social_media_followers_millions": market_data.social_media_followers_millions,
        "app_downloads_millions": market_data.app_downloads_millions,
        "revenue_impact_score": market_data.revenue_impact_score
    } 