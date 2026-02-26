from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_recommendations():
    """Get AI recommendations"""
    return {"message": "Recommendations endpoint - coming soon"} 