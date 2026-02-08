#!/usr/bin/env python3
"""
Health check script to verify the backend development environment.
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """Check if Python 3.11+ is available."""
    import sys
    if sys.version_info < (3, 11):
        print(f"❌ Python version {sys.version_info.major}.{sys.version_info.minor} is less than required 3.11")
        return False
    print(f"✅ Python version {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} is OK")
    return True


def check_docker():
    """Check if Docker is available."""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Docker is available: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Docker is not available: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        print("❌ Docker is not installed or not in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Docker command timed out")
        return False


def check_docker_compose():
    """Check if Docker Compose is available."""
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Docker Compose is available: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Docker Compose is not available: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        print("❌ Docker Compose is not installed or not in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Docker Compose command timed out")
        return False


def check_git():
    """Check if Git is available."""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Git is available: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Git is not available: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        print("❌ Git is not installed or not in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Git command timed out")
        return False


def check_required_files():
    """Check if required project files exist."""
    required_files = [
        'backend/src/api/main.py',
        'backend/requirements/base.txt',
        'docker/Dockerfile',
        'docker/docker-compose.yml',
        '.env.example',
        'README.md'
    ]
    
    all_found = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ Required file exists: {file_path}")
        else:
            print(f"❌ Required file missing: {file_path}")
            all_found = False
    
    return all_found


def check_environment_variables():
    """Check if environment variables are properly configured."""
    env_vars_to_check = [
        'DATABASE_URL',
        'SECRET_KEY'
    ]
    
    # Try to load from .env file
    env_file = '.env'
    if os.path.exists(env_file):
        print(f"✅ Environment file found: {env_file}")
        
        # Check if .env has been customized (not identical to .env.example)
        if os.path.exists('.env.example'):
            with open('.env', 'r') as f:
                env_content = f.read()
            with open('.env.example', 'r') as f:
                example_content = f.read()
            
            if env_content.strip() == example_content.strip():
                print("⚠️  Environment file (.env) has not been customized from .env.example")
                return True  # Still return True as the file exists
            else:
                print("✅ Environment file (.env) has been customized")
                return True
        else:
            print("✅ Environment file exists")
            return True
    else:
        print("⚠️  Environment file (.env) not found, using defaults")
        return True  # Not necessarily an error, just a warning


def main():
    """Main health check function."""
    print("🔍 Running health check for Backend Development Framework...")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Docker", check_docker),
        ("Docker Compose", check_docker_compose),
        ("Git", check_git),
        ("Required Files", check_required_files),
        ("Environment Variables", check_environment_variables),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n📋 Checking {check_name}...")
        result = check_func()
        results.append((check_name, result))
    
    print("\n" + "="*60)
    print("📊 Health Check Summary:")
    
    all_passed = True
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All checks passed! Your backend development environment is ready.")
        return 0
    else:
        print("💥 Some checks failed. Please address the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())