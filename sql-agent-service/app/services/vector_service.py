import chromadb
from chromadb.utils import embedding_functions
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging
import json
import yaml
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)


class VectorService:
    """Vector database service for document storage and retrieval"""
    
    def __init__(self):
        # Ensure the ChromaDB directory exists
        chroma_path = Path(settings.CHROMA_DB_PATH)
        chroma_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize persistent client
        self.client = chromadb.PersistentClient(
            path=str(chroma_path.absolute())
        )
        
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.EMBEDDING_MODEL
        )
        
        # Initialize collections
        self._initialize_collections()
    
    def _initialize_collections(self):
        """Initialize or load existing collections"""
        try:
            # Main collection for credit card knowledge
            self.main_collection = self.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                embedding_function=self.embedding_function,
                metadata={"description": "Credit card knowledge base"}
            )
            
            # User-specific collection for personal documents
            self.user_collection = self.client.get_or_create_collection(
                name="user_documents",
                embedding_function=self.embedding_function,
                metadata={"description": "User-specific documents"}
            )
            
            logger.info("✅ Vector database collections initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize vector collections: {e}")
            raise
    
    async def add_document(
        self,
        content: str,
        metadata: Dict[str, Any],
        collection_name: str = "main"
    ) -> str:
        """Add a document to the vector database"""
        try:
            collection = self._get_collection(collection_name)
            
            # Generate unique ID
            doc_id = f"doc_{datetime.now().timestamp()}_{hash(content) % 10000}"
            
            # Add document
            collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.info(f"✅ Added document {doc_id} to {collection_name}")
            return doc_id
            
        except Exception as e:
            logger.error(f"❌ Failed to add document: {e}")
            raise
    
    async def search(
        self,
        query: str,
        user_id: Optional[int] = None,
        limit: int = 5,
        collection_name: str = "main"
    ) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        try:
            collection = self._get_collection(collection_name)
            
            # Search in main collection
            results = collection.query(
                query_texts=[query],
                n_results=limit,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            formatted_results = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    formatted_results.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i],
                        "similarity": 1 - results["distances"][0][i]  # Convert distance to similarity
                    })
            
            # If user_id provided, also search user-specific collection
            if user_id:
                user_results = await self._search_user_documents(query, user_id, limit)
                formatted_results.extend(user_results)
            
            # Sort by similarity and return top results
            formatted_results.sort(key=lambda x: x["similarity"], reverse=True)
            return formatted_results[:limit]
            
        except Exception as e:
            logger.error(f"❌ Failed to search documents: {e}")
            return []
    
    async def _search_user_documents(
        self,
        query: str,
        user_id: int,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Search user-specific documents"""
        try:
            results = self.user_collection.query(
                query_texts=[query],
                n_results=limit,
                where={"user_id": user_id},
                include=["documents", "metadatas", "distances"]
            )
            
            formatted_results = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    formatted_results.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i],
                        "similarity": 1 - results["distances"][0][i]
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"❌ Failed to search user documents: {e}")
            return []
    
    async def delete_document(
        self,
        document_id: str,
        collection_name: str = "main"
    ) -> bool:
        """Delete a document from the vector database"""
        try:
            collection = self._get_collection(collection_name)
            collection.delete(ids=[document_id])
            
            logger.info(f"✅ Deleted document {document_id} from {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to delete document: {e}")
            return False
    
    async def delete_user_documents(self, user_id: int) -> bool:
        """Delete all documents for a specific user"""
        try:
            # Get all documents for user
            results = self.user_collection.get(
                where={"user_id": user_id},
                include=["ids"]
            )
            
            if results["ids"]:
                self.user_collection.delete(ids=results["ids"])
                logger.info(f"✅ Deleted {len(results['ids'])} documents for user {user_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to delete user documents: {e}")
            return False
    
    async def get_collection_stats(self, collection_name: str = "main") -> Dict[str, Any]:
        """Get statistics about a collection"""
        try:
            collection = self._get_collection(collection_name)
            count = collection.count()
            
            return {
                "collection_name": collection_name,
                "document_count": count,
                "status": "healthy"
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get collection stats: {e}")
            return {
                "collection_name": collection_name,
                "document_count": 0,
                "status": "error",
                "error": str(e)
            }
    
    def _get_collection(self, collection_name: str):
        """Get collection by name"""
        if collection_name == "main":
            return self.main_collection
        elif collection_name == "user":
            return self.user_collection
        else:
            raise ValueError(f"Unknown collection: {collection_name}")

    async def load_tuning_data(self) -> bool:
        """Load tuning data from YAML file and store in vector database"""
        try:
            # Path to tuning data file
            tuning_file = Path(__file__).parent.parent / "data" / "tuning_data.yaml"
            
            if not tuning_file.exists():
                logger.warning(f"Tuning data file not found: {tuning_file}")
                return False
            
            # Load YAML data
            with open(tuning_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Create or recreate tuning collection to ensure fresh data
            try:
                self.client.delete_collection(name="tuning_examples")
            except:
                pass  # Collection doesn't exist
            
            self.tuning_collection = self.client.create_collection(
                name="tuning_examples",
                embedding_function=self.embedding_function,
                metadata={"description": "Tuning examples for credit card recommendations"}
            )
            
            # Add each example to the vector database
            for i, example in enumerate(data.get('tuning_examples', [])):
                # Combine question, SQL query, and answer for embedding
                content = f"Question: {example['question']}\nSQL Query: {example['sql_query']}\nAnswer: {example['answer']}"
                
                # Add to vector database
                self.tuning_collection.add(
                    documents=[content],
                    metadatas=[{
                        "type": "tuning_example",
                        "category": example.get('category', 'general'),
                        "question": example['question'],
                        "sql_query": example['sql_query'],
                        "answer": example['answer']
                    }],
                    ids=[f"tuning_{i}"]
                )
            
            logger.info(f"✅ Loaded {len(data.get('tuning_examples', []))} tuning examples")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load tuning data: {e}")
            return False

    async def get_tuning_examples(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Get relevant tuning examples for a query"""
        try:
            if not hasattr(self, 'tuning_collection'):
                return []
            
            # Search for relevant examples
            results = self.tuning_collection.query(
                query_texts=[query],
                n_results=limit,
                include=["documents", "metadatas", "distances"]
            )
            
            formatted_results = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    formatted_results.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i],
                        "similarity": 1 - results["distances"][0][i]
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"❌ Failed to get tuning examples: {e}")
            return []


# Create global instance
vector_service = VectorService()
