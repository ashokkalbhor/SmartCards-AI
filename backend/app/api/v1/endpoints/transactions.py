from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_transactions():
    """Get user's transactions"""
    return {"message": "Transactions endpoint - coming soon"} 