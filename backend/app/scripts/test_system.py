#!/usr/bin/env python3
"""
Test script for SmartCards AI system
Tests vector database, AI service, and API endpoints
"""

import asyncio
import sys
import os
from pathlib import Path
import json
import time
from typing import Dict, List, Any

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from core.vector_db import vector_db_service
from core.ai_service import ai_service


class SystemTester:
    def __init__(self):
        self.test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "tests": []
        }
    
    def log_test(self, test_name: str, status: str, details: str = "", error: str = ""):
        """Log test result"""
        self.test_results["total_tests"] += 1
        
        if status == "PASS":
            self.test_results["passed_tests"] += 1
            print(f"✅ {test_name}: {status}")
        else:
            self.test_results["failed_tests"] += 1
            print(f"❌ {test_name}: {status}")
            if error:
                print(f"   Error: {error}")
        
        if details:
            print(f"   Details: {details}")
        
        self.test_results["tests"].append({
            "name": test_name,
            "status": status,
            "details": details,
            "error": error
        })
    
    async def run_all_tests(self):
        """Run all system tests"""
        print("🧪 SmartCards AI System Test Suite")
        print("=" * 50)
        
        # Test 1: Vector Database Connection
        await self.test_vector_db_connection()
        
        # Test 2: Vector Database Content
        await self.test_vector_db_content()
        
        # Test 3: Vector Search Functionality
        await self.test_vector_search()
        
        # Test 4: AI Service Integration
        await self.test_ai_service()
        
        # Test 5: End-to-End Query Processing
        await self.test_end_to_end_queries()
        
        # Test 6: Performance Test
        await self.test_performance()
        
        # Print summary
        self.print_summary()
        
        return self.test_results
    
    async def test_vector_db_connection(self):
        """Test vector database connection"""
        try:
            db_info = vector_db_service.get_database_info()
            
            if db_info["status"] == "healthy":
                self.log_test(
                    "Vector DB Connection",
                    "PASS",
                    f"Connected to {len(vector_db_service.collections)} collections"
                )
            else:
                self.log_test(
                    "Vector DB Connection",
                    "FAIL",
                    error=db_info.get("error", "Unknown error")
                )
        except Exception as e:
            self.log_test("Vector DB Connection", "FAIL", error=str(e))
    
    async def test_vector_db_content(self):
        """Test if vector database has content"""
        try:
            db_info = vector_db_service.get_database_info()
            total_docs = db_info["total_documents"]
            
            if total_docs > 0:
                self.log_test(
                    "Vector DB Content",
                    "PASS", 
                    f"{total_docs} documents loaded"
                )
            else:
                self.log_test(
                    "Vector DB Content",
                    "FAIL",
                    error="No documents found in vector database"
                )
        except Exception as e:
            self.log_test("Vector DB Content", "FAIL", error=str(e))
    
    async def test_vector_search(self):
        """Test vector search functionality"""
        test_queries = [
            "credit card rewards",
            "HDFC Regalia",
            "online shopping benefits",
            "dining cashback"
        ]
        
        passed_searches = 0
        
        for query in test_queries:
            try:
                results = await vector_db_service.search_all_collections(query, n_results=3)
                
                # Check if any collection returned results
                has_results = any(len(collection_results) > 0 for collection_results in results.values())
                
                if has_results:
                    passed_searches += 1
                
            except Exception as e:
                print(f"   Search error for '{query}': {e}")
        
        if passed_searches == len(test_queries):
            self.log_test(
                "Vector Search",
                "PASS",
                f"All {len(test_queries)} test queries returned results"
            )
        elif passed_searches > 0:
            self.log_test(
                "Vector Search",
                "PARTIAL",
                f"{passed_searches}/{len(test_queries)} queries successful"
            )
        else:
            self.log_test(
                "Vector Search",
                "FAIL",
                error="No search queries returned results"
            )
    
    async def test_ai_service(self):
        """Test AI service functionality"""
        try:
            # Test basic vector search through AI service
            query = "What are the best credit cards for online shopping?"
            results = await ai_service._search_vector_db(query)
            
            if results and len(results) > 0:
                best_similarity = max(result["similarity"] for result in results)
                self.log_test(
                    "AI Service Vector Search",
                    "PASS",
                    f"Found {len(results)} results, best similarity: {best_similarity:.3f}"
                )
            else:
                self.log_test(
                    "AI Service Vector Search", 
                    "FAIL",
                    error="No results returned from AI service"
                )
        except Exception as e:
            self.log_test("AI Service Vector Search", "FAIL", error=str(e))
    
    async def test_end_to_end_queries(self):
        """Test end-to-end query processing"""
        test_queries = [
            {
                "query": "Which credit card is best for Myntra purchases?",
                "expected_keywords": ["myntra", "online", "shopping", "reward", "cashback"]
            },
            {
                "query": "What are the annual fees for premium credit cards?",
                "expected_keywords": ["annual", "fee", "premium", "cost"]
            },
            {
                "query": "Tell me about HDFC credit card benefits",
                "expected_keywords": ["hdfc", "benefit", "feature", "reward"]
            }
        ]
        
        passed_queries = 0
        
        for test_case in test_queries:
            try:
                # Test without user context first
                response = await ai_service.process_user_query(
                    user_id=1,  # Mock user ID
                    query=test_case["query"],
                    conversation_id=None,
                    db=None
                )
                
                # Check response quality
                if (response and 
                    response.get("response") and 
                    len(response["response"]) > 50 and
                    response.get("confidence", 0) > 0.3):
                    
                    passed_queries += 1
                    
            except Exception as e:
                print(f"   Query error for '{test_case['query'][:30]}...': {e}")
        
        if passed_queries == len(test_queries):
            self.log_test(
                "End-to-End Queries",
                "PASS",
                f"All {len(test_queries)} queries processed successfully"
            )
        elif passed_queries > 0:
            self.log_test(
                "End-to-End Queries",
                "PARTIAL",
                f"{passed_queries}/{len(test_queries)} queries successful"
            )
        else:
            self.log_test(
                "End-to-End Queries",
                "FAIL", 
                error="No queries processed successfully"
            )
    
    async def test_performance(self):
        """Test system performance"""
        try:
            query = "best credit card for dining"
            
            # Measure response time
            start_time = time.time()
            results = await ai_service._search_vector_db(query)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response_time < 2.0:  # Less than 2 seconds
                self.log_test(
                    "Performance Test",
                    "PASS",
                    f"Query processed in {response_time:.3f}s"
                )
            elif response_time < 5.0:  # Less than 5 seconds
                self.log_test(
                    "Performance Test",
                    "PARTIAL",
                    f"Query processed in {response_time:.3f}s (acceptable but slow)"
                )
            else:
                self.log_test(
                    "Performance Test",
                    "FAIL",
                    error=f"Query took {response_time:.3f}s (too slow)"
                )
        except Exception as e:
            self.log_test("Performance Test", "FAIL", error=str(e))
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("🎯 Test Summary")
        print("-" * 25)
        print(f"Total Tests: {self.test_results['total_tests']}")
        print(f"Passed: {self.test_results['passed_tests']}")
        print(f"Failed: {self.test_results['failed_tests']}")
        
        if self.test_results['failed_tests'] == 0:
            print("\n🎉 All tests passed! System is ready to use.")
            print("\n📖 Next steps:")
            print("1. Start the FastAPI server:")
            print("   uvicorn app.main:app --reload")
            print("2. Visit http://localhost:8000/docs for API documentation")
            print("3. Test the chatbot endpoints")
        elif self.test_results['passed_tests'] > self.test_results['failed_tests']:
            print("\n⚠️ Most tests passed, but some issues detected.")
            print("The system should work but may have reduced functionality.")
        else:
            print("\n❌ System has significant issues that need to be resolved.")
            print("Please check the setup and try running the setup script again.")


async def run_quick_test():
    """Run a quick functionality test"""
    print("🚀 Quick System Test")
    print("-" * 20)
    
    try:
        # Test vector DB
        db_info = vector_db_service.get_database_info()
        print(f"📊 Vector DB: {db_info['total_documents']} documents loaded")
        
        # Test search
        results = await vector_db_service.search_all_collections(
            "credit card benefits", n_results=1
        )
        result_count = sum(len(collection_results) for collection_results in results.values())
        print(f"🔍 Search: Found {result_count} results for test query")
        
        # Test AI service  
        response = await ai_service._search_vector_db("HDFC credit card")
        print(f"🤖 AI Service: {len(response)} results returned")
        
        if db_info['total_documents'] > 0 and result_count > 0 and len(response) > 0:
            print("\n✅ Quick test passed! System appears to be working.")
            return True
        else:
            print("\n❌ Quick test failed. Run full test for details.")
            return False
            
    except Exception as e:
        print(f"\n❌ Quick test error: {e}")
        return False


async def interactive_test():
    """Interactive test mode"""
    print("🔍 Interactive Test Mode")
    print("Type queries to test the system. Type 'quit' to exit.")
    print("-" * 50)
    
    while True:
        try:
            query = input("\n💬 Your query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
            
            if not query:
                continue
            
            print("🔍 Searching...")
            start_time = time.time()
            
            # Test vector search
            vector_results = await ai_service._search_vector_db(query)
            
            end_time = time.time()
            
            print(f"⏱️ Response time: {end_time - start_time:.3f}s")
            print(f"📊 Found {len(vector_results)} results")
            
            if vector_results:
                print("\n📋 Top result:")
                top_result = vector_results[0]
                print(f"   Similarity: {top_result['similarity']:.3f}")
                print(f"   Source: {top_result['metadata'].get('bank', 'Unknown')}")
                print(f"   Content: {top_result['content'][:200]}...")
            else:
                print("❌ No results found")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Interactive test session ended")


async def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SmartCards AI System Tester")
    parser.add_argument("--quick", action="store_true", help="Run quick test only")
    parser.add_argument("--interactive", action="store_true", help="Run interactive test mode")
    parser.add_argument("--output", help="Save test results to JSON file")
    
    args = parser.parse_args()
    
    if args.quick:
        success = await run_quick_test()
        sys.exit(0 if success else 1)
    elif args.interactive:
        await interactive_test()
    else:
        # Run full test suite
        tester = SystemTester()
        results = await tester.run_all_tests()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Test results saved to {args.output}")
        
        # Exit with appropriate code
        success_rate = results["passed_tests"] / results["total_tests"] if results["total_tests"] > 0 else 0
        sys.exit(0 if success_rate >= 0.8 else 1)


if __name__ == "__main__":
    asyncio.run(main()) 