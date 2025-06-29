import chromadb
from chromadb.utils import embedding_functions
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging
import json
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)


class ChromaDBService:
    def __init__(self):
        # Ensure the ChromaDB directory exists
        chroma_path = Path(settings.CHROMA_DB_PATH)
        chroma_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 ChromaDB storage path: {chroma_path.absolute()}")
        
        # Initialize PERSISTENT client
        self.client = chromadb.PersistentClient(
            path=str(chroma_path.absolute())
        )
        
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.EMBEDDING_MODEL
        )
        
        # Initialize collections (will create if not exist, load if they do)
        self._initialize_collections()
        
        # Log current state
        self._log_database_status()
    
    def _initialize_collections(self):
        """Initialize or load existing collections"""
        collection_configs = [
            ("credit_card_features", "Card features and reward structures"),
            ("credit_card_terms", "Terms, conditions, and policies"),
            ("merchant_partnerships", "Merchant offers and partnerships"),
            ("credit_card_offers", "Time-limited promotions and offers")
        ]
        
        self.collections = {}
        
        for name, description in collection_configs:
            try:
                # Try to get existing collection first
                collection = self.client.get_collection(
                    name=name,
                    embedding_function=self.embedding_function
                )
                print(f"✅ Loaded existing collection: {name} ({collection.count()} documents)")
                
            except ValueError:
                # Collection doesn't exist, create new one
                collection = self.client.create_collection(
                    name=name,
                    embedding_function=self.embedding_function,
                    metadata={
                        "description": description,
                        "hnsw:space": "cosine",
                        "hnsw:construction_ef": 200,
                        "hnsw:search_ef": 100,
                        "hnsw:M": 16
                    }
                )
                print(f"🆕 Created new collection: {name}")
            
            self.collections[name] = collection
    
    def _log_database_status(self):
        """Log current database status"""
        print("\n📊 ChromaDB Status:")
        print("-" * 30)
        
        total_documents = 0
        for name, collection in self.collections.items():
            count = collection.count()
            total_documents += count
            print(f"  {name}: {count} documents")
        
        print(f"  Total: {total_documents} documents")
        print(f"  Storage: {Path(settings.CHROMA_DB_PATH).absolute()}")
        print("-" * 30)
    
    async def search_all_collections(
        self, 
        query: str, 
        filters: Optional[Dict] = None,
        n_results: int = 5
    ) -> Dict[str, List[Dict]]:
        """Search across all collections and return organized results"""
        results = {}
        
        for collection_name, collection in self.collections.items():
            try:
                search_results = collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    where=filters,
                    include=["documents", "metadatas", "distances"]
                )
                
                # Format results
                formatted_results = []
                if search_results["documents"] and search_results["documents"][0]:
                    for i, doc in enumerate(search_results["documents"][0]):
                        formatted_results.append({
                            "content": doc,
                            "metadata": search_results["metadatas"][0][i],
                            "distance": search_results["distances"][0][i],
                            "similarity": 1 - search_results["distances"][0][i],
                            "collection": collection_name
                        })
                
                results[collection_name] = formatted_results
                
            except Exception as e:
                logger.error(f"Error searching collection {collection_name}: {e}")
                results[collection_name] = []
        
        return results
    
    async def search_specific_collection(
        self,
        collection_name: str,
        query: str,
        filters: Optional[Dict] = None,
        n_results: int = 10
    ) -> List[Dict]:
        """Search a specific collection"""
        if collection_name not in self.collections:
            logger.error(f"Collection {collection_name} not found")
            return []
        
        try:
            collection = self.collections[collection_name]
            search_results = collection.query(
                query_texts=[query],
                n_results=n_results,
                where=filters,
                include=["documents", "metadatas", "distances"]
            )
            
            formatted_results = []
            if search_results["documents"] and search_results["documents"][0]:
                for i, doc in enumerate(search_results["documents"][0]):
                    formatted_results.append({
                        "content": doc,
                        "metadata": search_results["metadatas"][0][i],
                        "distance": search_results["distances"][0][i],
                        "similarity": 1 - search_results["distances"][0][i],
                        "collection": collection_name
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching collection {collection_name}: {e}")
            return []
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database information for health checks"""
        info = {
            "storage_path": str(Path(settings.CHROMA_DB_PATH).absolute()),
            "storage_exists": Path(settings.CHROMA_DB_PATH).exists(),
            "collections": {},
            "total_documents": 0,
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            for name, collection in self.collections.items():
                count = collection.count()
                info["collections"][name] = count
                info["total_documents"] += count
        except Exception as e:
            info["status"] = "error"
            info["error"] = str(e)
        
        return info
    
    async def add_documents_to_collection(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: List[Dict],
        ids: List[str]
    ) -> bool:
        """Add documents to a specific collection"""
        if collection_name not in self.collections:
            logger.error(f"Collection {collection_name} not found")
            return False
        
        try:
            collection = self.collections[collection_name]
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(documents)} documents to {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to {collection_name}: {e}")
            return False
    
    async def delete_documents_from_collection(
        self,
        collection_name: str,
        ids: Optional[List[str]] = None,
        where: Optional[Dict] = None
    ) -> bool:
        """Delete documents from a specific collection"""
        if collection_name not in self.collections:
            logger.error(f"Collection {collection_name} not found")
            return False
        
        try:
            collection = self.collections[collection_name]
            
            if ids:
                collection.delete(ids=ids)
            elif where:
                collection.delete(where=where)
            else:
                logger.error("Either ids or where clause must be provided")
                return False
            
            logger.info(f"Deleted documents from {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting documents from {collection_name}: {e}")
            return False
    
    def determine_collection_for_document(self, metadata: Dict) -> str:
        """Determine which collection a document should go to based on metadata"""
        doc_type = metadata.get('document_type', '').lower()
        
        if doc_type in ['terms', 'conditions', 'tc']:
            return 'credit_card_terms'
        elif doc_type in ['features', 'benefits', 'rewards']:
            return 'credit_card_features'
        elif doc_type in ['offers', 'promotions', 'campaigns']:
            return 'credit_card_offers'
        elif doc_type in ['merchants', 'partnerships']:
            return 'merchant_partnerships'
        else:
            return 'credit_card_features'  # Default collection
    
    async def cleanup_expired_documents(self) -> int:
        """Remove expired documents from all collections"""
        total_deleted = 0
        current_time = datetime.now().isoformat()
        
        for collection_name, collection in self.collections.items():
            try:
                # Find expired documents
                expired_docs = collection.get(
                    where={"expires_at": {"$lt": current_time}}
                )
                
                if expired_docs["ids"]:
                    collection.delete(ids=expired_docs["ids"])
                    deleted_count = len(expired_docs["ids"])
                    total_deleted += deleted_count
                    logger.info(f"Deleted {deleted_count} expired documents from {collection_name}")
                    
            except Exception as e:
                logger.error(f"Error cleaning up expired documents from {collection_name}: {e}")
        
        return total_deleted


# Create global instance
vector_db_service = ChromaDBService() 