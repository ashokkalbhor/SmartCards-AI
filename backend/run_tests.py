#!/usr/bin/env python3
"""
Test runner script for SmartCards AI backend
"""

import subprocess
import sys
import os

def run_tests():
    """Run the test suite"""
    print("🧪 Running SmartCards AI Backend Tests")
    print("=" * 50)
    
    # Install test dependencies
    print("📦 Installing test dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"], check=True)
    
    # Run tests with coverage
    print("🚀 Running tests with coverage...")
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-report=xml",
        "--cov-fail-under=90",
        "-v"
    ], cwd=os.path.dirname(__file__))
    
    if result.returncode == 0:
        print("✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/")
        print("📈 Coverage report generated in coverage.xml")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    run_tests() 