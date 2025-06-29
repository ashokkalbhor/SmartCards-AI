from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, credit_cards, merchants, transactions, rewards, recommendations, chatbot, card_master_data

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(credit_cards.router, prefix="/credit-cards", tags=["credit-cards"])
api_router.include_router(merchants.router, prefix="/merchants", tags=["merchants"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(rewards.router, prefix="/rewards", tags=["rewards"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(card_master_data.router, prefix="/card-master-data", tags=["card-master-data"]) 
 