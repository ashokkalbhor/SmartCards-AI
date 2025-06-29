from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_credit_cards():
    """Get user's credit cards"""
    return {"message": "Credit cards endpoint - coming soon"} 