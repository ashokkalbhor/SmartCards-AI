from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, credit_cards, merchants, transactions, rewards, recommendations, card_master_data, card_reviews, community, admin, moderator, user_roles, card_documents
# Temporarily disabled SQL Agent for deployment investigation
# from app.api.v1.endpoints import sql_agent
# Temporarily disabled AI endpoints for deployment
# from app.api.v1.endpoints import chatbot, enhanced_chatbot

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(credit_cards.router, prefix="/credit-cards", tags=["credit-cards"])
api_router.include_router(merchants.router, prefix="/merchants", tags=["merchants"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(rewards.router, prefix="/rewards", tags=["rewards"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(card_master_data.router, prefix="/card-master-data", tags=["card-master-data"])
api_router.include_router(card_reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(community.router, prefix="/community", tags=["community"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(moderator.router, prefix="/moderator", tags=["moderator"])
api_router.include_router(user_roles.router, prefix="/user-roles", tags=["user-roles"])
api_router.include_router(card_documents.router, prefix="/card-documents", tags=["card-documents"])
# Temporarily disabled SQL Agent for deployment investigation
# api_router.include_router(sql_agent.router, prefix="/sql-agent", tags=["sql-agent"])

# Temporarily disabled AI endpoints
# api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
# api_router.include_router(enhanced_chatbot.router, prefix="/enhanced-chatbot", tags=["enhanced-chatbot"]) 
 