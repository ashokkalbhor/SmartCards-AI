import json
import asyncio
from pathlib import Path
from typing import List, Dict, Optional
import logging
from datetime import datetime

from app.core.vector_db import vector_db_service

logger = logging.getLogger(__name__)


class DocumentIngestor:
    def __init__(self):
        self.vector_db = vector_db_service
        self.chunks_path = Path("app/data/documents/chunks")
        self.ingestion_log_path = Path("app/data/ingestion_log.json")
        
        # Create directory if it doesn't exist
        self.chunks_path.mkdir(parents=True, exist_ok=True)
        
        # Load ingestion log
        self.ingestion_log = self._load_ingestion_log()
    
    def _load_ingestion_log(self) -> Dict:
        """Load ingestion log to track processed files"""
        if self.ingestion_log_path.exists():
            try:
                with open(self.ingestion_log_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading ingestion log: {e}")
        
        return {
            "processed_files": {},
            "last_run": None,
            "total_documents_ingested": 0
        }
    
    def _save_ingestion_log(self):
        """Save ingestion log"""
        try:
            with open(self.ingestion_log_path, 'w') as f:
                json.dump(self.ingestion_log, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving ingestion log: {e}")
    
    async def ingest_all_documents(self, force_reingest: bool = False):
        """Ingest all processed document chunks into ChromaDB"""
        print("🗃️ Starting document ingestion into ChromaDB...")
        
        chunk_files = list(self.chunks_path.glob("*_chunks.json"))
        
        if not chunk_files:
            print("⚠️ No chunk files found. Run document processing first.")
            return {
                "status": "no_files",
                "message": "No chunk files found to ingest"
            }
        
        print(f"📁 Found {len(chunk_files)} chunk files to process")
        
        total_ingested = 0
        files_processed = 0
        files_skipped = 0
        
        for chunk_file in chunk_files:
            try:
                result = await self._ingest_chunk_file(chunk_file, force_reingest)
                
                if result["status"] == "ingested":
                    total_ingested += result["chunks_ingested"]
                    files_processed += 1
                elif result["status"] == "skipped":
                    files_skipped += 1
                    
            except Exception as e:
                logger.error(f"Error processing {chunk_file}: {e}")
        
        # Update ingestion log
        self.ingestion_log["last_run"] = datetime.now().isoformat()
        self.ingestion_log["total_documents_ingested"] += total_ingested
        self._save_ingestion_log()
        
        print(f"\n✅ Document ingestion completed!")
        print(f"📊 Summary:")
        print(f"  Files processed: {files_processed}")
        print(f"  Files skipped: {files_skipped}")
        print(f"  Total chunks ingested: {total_ingested}")
        
        return {
            "status": "completed",
            "files_processed": files_processed,
            "files_skipped": files_skipped,
            "total_chunks_ingested": total_ingested
        }
    
    async def _ingest_chunk_file(self, chunk_file: Path, force_reingest: bool = False) -> Dict:
        """Ingest chunks from a single file"""
        file_key = chunk_file.name
        
        # Check if file was already processed
        if not force_reingest and file_key in self.ingestion_log["processed_files"]:
            file_info = self.ingestion_log["processed_files"][file_key]
            file_mtime = chunk_file.stat().st_mtime
            
            if file_mtime <= file_info.get("last_modified", 0):
                print(f"⏭️ Skipping {file_key} (already processed)")
                return {"status": "skipped", "chunks_ingested": 0}
        
        try:
            print(f"📄 Processing {file_key}...")
            
            # Load chunks
            with open(chunk_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            if not chunks:
                print(f"⚠️ No chunks found in {file_key}")
                return {"status": "empty", "chunks_ingested": 0}
            
            # Group chunks by collection
            collections_data = self._group_chunks_by_collection(chunks)
            
            total_ingested = 0
            
            # Ingest into each collection
            for collection_name, collection_chunks in collections_data.items():
                if collection_chunks:
                    success = await self._ingest_into_collection(
                        collection_name, collection_chunks, force_reingest
                    )
                    
                    if success:
                        total_ingested += len(collection_chunks)
                        print(f"  ✅ Added {len(collection_chunks)} chunks to {collection_name}")
                    else:
                        print(f"  ❌ Failed to add chunks to {collection_name}")
            
            # Update ingestion log
            self.ingestion_log["processed_files"][file_key] = {
                "last_processed": datetime.now().isoformat(),
                "last_modified": chunk_file.stat().st_mtime,
                "chunks_ingested": total_ingested,
                "collections": list(collections_data.keys())
            }
            
            return {"status": "ingested", "chunks_ingested": total_ingested}
            
        except Exception as e:
            logger.error(f"Error ingesting {chunk_file}: {e}")
            return {"status": "error", "chunks_ingested": 0, "error": str(e)}
    
    def _group_chunks_by_collection(self, chunks: List[Dict]) -> Dict[str, List[Dict]]:
        """Group chunks by their target collection"""
        collections_data = {}
        
        for chunk in chunks:
            collection_name = self.vector_db.determine_collection_for_document(
                chunk.get("metadata", {})
            )
            
            if collection_name not in collections_data:
                collections_data[collection_name] = []
            
            collections_data[collection_name].append(chunk)
        
        return collections_data
    
    async def _ingest_into_collection(
        self, 
        collection_name: str, 
        chunks: List[Dict], 
        force_reingest: bool = False
    ) -> bool:
        """Ingest chunks into a specific collection"""
        try:
            # Prepare data for ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for chunk in chunks:
                documents.append(chunk['content'])
                metadatas.append(chunk['metadata'])
                ids.append(chunk['id'])
            
            # If force reingest, delete existing documents first
            if force_reingest:
                try:
                    await self.vector_db.delete_documents_from_collection(
                        collection_name, ids=ids
                    )
                except:
                    pass  # Ignore errors if documents don't exist
            
            # Add documents in batches
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i:i + batch_size]
                batch_metadata = metadatas[i:i + batch_size]
                batch_ids = ids[i:i + batch_size]
                
                success = await self.vector_db.add_documents_to_collection(
                    collection_name, batch_docs, batch_metadata, batch_ids
                )
                
                if not success:
                    logger.error(f"Failed to add batch {i//batch_size + 1} to {collection_name}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error ingesting into collection {collection_name}: {e}")
            return False
    
    async def verify_ingestion(self) -> Dict:
        """Verify that documents were ingested correctly"""
        print("\n🔍 Verifying ingestion...")
        
        db_info = self.vector_db.get_database_info()
        
        verification_results = {
            "status": "success",
            "total_documents": db_info["total_documents"],
            "collections": db_info["collections"],
            "tests_passed": 0,
            "tests_failed": 0,
            "test_results": []
        }
        
        # Test each collection
        for collection_name in self.vector_db.collections.keys():
            collection_info = db_info["collections"].get(collection_name, 0)
            
            test_result = {
                "collection": collection_name,
                "document_count": collection_info,
                "search_test": "not_tested"
            }
            
            if collection_info > 0:
                # Test search functionality
                try:
                    search_results = await self.vector_db.search_specific_collection(
                        collection_name, "credit card", n_results=1
                    )
                    
                    if search_results:
                        test_result["search_test"] = "passed"
                        verification_results["tests_passed"] += 1
                        print(f"  ✅ {collection_name}: {collection_info} documents, search working")
                    else:
                        test_result["search_test"] = "no_results"
                        verification_results["tests_failed"] += 1
                        print(f"  ⚠️ {collection_name}: {collection_info} documents, search returned no results")
                        
                except Exception as e:
                    test_result["search_test"] = f"error: {str(e)}"
                    verification_results["tests_failed"] += 1
                    print(f"  ❌ {collection_name}: {collection_info} documents, search failed: {e}")
            else:
                test_result["search_test"] = "empty_collection"
                print(f"  ⚠️ {collection_name}: Empty collection")
            
            verification_results["test_results"].append(test_result)
        
        # Overall status
        if verification_results["tests_failed"] > 0:
            verification_results["status"] = "partial_failure"
        elif verification_results["total_documents"] == 0:
            verification_results["status"] = "empty"
        
        print(f"\n📊 Verification Summary:")
        print(f"  Total documents: {verification_results['total_documents']}")
        print(f"  Tests passed: {verification_results['tests_passed']}")
        print(f"  Tests failed: {verification_results['tests_failed']}")
        print(f"  Status: {verification_results['status']}")
        
        return verification_results
    
    async def cleanup_old_documents(self, days_old: int = 30) -> int:
        """Remove old documents from ChromaDB"""
        print(f"🧹 Cleaning up documents older than {days_old} days...")
        
        cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        cutoff_iso = datetime.fromtimestamp(cutoff_date).isoformat()
        
        total_deleted = 0
        
        for collection_name, collection in self.vector_db.collections.items():
            try:
                # Find old documents
                old_docs = collection.get(
                    where={"processed_at": {"$lt": cutoff_iso}}
                )
                
                if old_docs["ids"]:
                    collection.delete(ids=old_docs["ids"])
                    deleted_count = len(old_docs["ids"])
                    total_deleted += deleted_count
                    print(f"  🗑️ Deleted {deleted_count} old documents from {collection_name}")
                    
            except Exception as e:
                logger.error(f"Error cleaning up {collection_name}: {e}")
        
        print(f"✅ Cleanup completed. Deleted {total_deleted} documents.")
        return total_deleted
    
    async def get_ingestion_stats(self) -> Dict:
        """Get detailed ingestion statistics"""
        stats = {
            "ingestion_log": self.ingestion_log,
            "database_info": self.vector_db.get_database_info(),
            "chunk_files": {
                "available": len(list(self.chunks_path.glob("*_chunks.json"))),
                "processed": len(self.ingestion_log["processed_files"])
            }
        }
        
        return stats


# Async function for easy usage
async def ingest_all_documents(force_reingest: bool = False):
    """Convenience function to ingest all documents"""
    ingestor = DocumentIngestor()
    return await ingestor.ingest_all_documents(force_reingest)


if __name__ == "__main__":
    # Allow command line usage
    import sys
    
    force = "--force" in sys.argv
    result = asyncio.run(ingest_all_documents(force))
    print(f"\nIngestion result: {result}") 