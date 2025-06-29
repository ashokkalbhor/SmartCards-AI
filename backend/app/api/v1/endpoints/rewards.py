from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_rewards():
    """Get user's rewards"""
    return {"message": "Rewards endpoint - coming soon"} 