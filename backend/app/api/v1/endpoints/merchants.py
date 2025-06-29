from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_merchants():
    """Get merchants"""
    return {"message": "Merchants endpoint - coming soon"} 