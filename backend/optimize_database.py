#!/usr/bin/env python3
"""
Database optimization script for SmartCards AI
- VACUUM the database to reclaim space from deleted data
- ANALYZE tables for better query performance
- Check database integrity
"""

import sqlite3
import os
import sys
from pathlib import Path

def optimize_database(db_path: str):
    """Optimize SQLite database by vacuuming and analyzing"""
    print(f"🔧 Optimizing database: {db_path}")
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False
    
    # Get initial size
    initial_size = os.path.getsize(db_path)
    print(f"📊 Initial database size: {initial_size / 1024:.1f} KB")
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check database integrity first
        print("🔍 Checking database integrity...")
        cursor.execute("PRAGMA integrity_check")
        integrity_result = cursor.fetchone()
        if integrity_result[0] != "ok":
            print(f"❌ Database integrity check failed: {integrity_result[0]}")
            return False
        print("✅ Database integrity check passed")
        
        # Get table information before optimization
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Found {len(tables)} tables: {', '.join(tables)}")
        
        # VACUUM the database to reclaim space
        print("🧹 Running VACUUM to reclaim space...")
        cursor.execute("VACUUM")
        print("✅ VACUUM completed")
        
        # ANALYZE tables for better query performance
        print("📈 Running ANALYZE for query optimization...")
        cursor.execute("ANALYZE")
        print("✅ ANALYZE completed")
        
        # Update database statistics
        print("📊 Updating database statistics...")
        cursor.execute("PRAGMA optimize")
        print("✅ Database statistics updated")
        
        # Close connection
        conn.close()
        
        # Get final size
        final_size = os.path.getsize(db_path)
        space_saved = initial_size - final_size
        space_saved_percent = (space_saved / initial_size * 100) if initial_size > 0 else 0
        
        print(f"📊 Final database size: {final_size / 1024:.1f} KB")
        print(f"💾 Space saved: {space_saved / 1024:.1f} KB ({space_saved_percent:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error optimizing database: {e}")
        return False

def main():
    """Main function"""
    # Get database path
    backend_dir = Path(__file__).parent
    db_path = backend_dir / "smartcards_ai.db"
    
    print("🚀 SmartCards AI Database Optimization")
    print("=" * 50)
    
    success = optimize_database(str(db_path))
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Database optimization completed successfully!")
    else:
        print("❌ Database optimization failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
