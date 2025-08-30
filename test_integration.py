#!/usr/bin/env python3
"""
Test script to verify SQL Agent integration
"""

import sys
import os

# Add backend to path
sys.path.append('backend')
sys.path.append('backend/app')

def test_imports():
    """Test that all imports work correctly"""
    print("Testing imports...")
    
    try:
        from app.core.sql_agent import SQLAgentService
        print("✅ SQLAgentService import successful")
    except Exception as e:
        print(f"❌ SQLAgentService import failed: {e}")
        return False
    
    try:
        from app.services.vector_service import VectorService
        print("✅ VectorService import successful")
    except Exception as e:
        print(f"❌ VectorService import failed: {e}")
        return False
    
    try:
        from app.services.cache_service import CacheService
        print("✅ CacheService import successful")
    except Exception as e:
        print(f"❌ CacheService import failed: {e}")
        return False
    
    try:
        from app.api.v1.endpoints.sql_agent import router
        print("✅ SQL Agent router import successful")
    except Exception as e:
        print(f"❌ SQL Agent router import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database connectivity"""
    print("\nTesting database...")
    
    try:
        import sqlite3
        conn = sqlite3.connect('smartcards_ai.db')
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"✅ Database connected successfully")
        print(f"✅ Found {len(tables)} tables")
        
        # Check for SQL agent tables
        sql_agent_tables = ['chat_users', 'user_sessions', 'documents']
        found_tables = [table for table in sql_agent_tables if table in tables]
        
        if found_tables:
            print(f"✅ Found SQL agent tables: {found_tables}")
        else:
            print(f"⚠️  SQL agent tables not found: {sql_agent_tables}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    
    try:
        from app.core.config import settings
        
        # Check required settings
        required_settings = [
            'OPENAI_API_KEY',
            'DATABASE_URL',
            'CACHE_ENABLED',
            'SQL_AGENT_TABLES'
        ]
        
        for setting in required_settings:
            if hasattr(settings, setting):
                print(f"✅ {setting} configured")
            else:
                print(f"❌ {setting} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 SQL Agent Integration Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_database,
        test_config
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    
    if all(results):
        print("🎉 All tests passed! Integration is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
