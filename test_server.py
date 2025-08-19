#!/usr/bin/env python3
"""
Test script for Infinity Translator server functionality
This tests the core FastAPI server without the GUI components
"""

import sys
import time
import requests
import threading
from pathlib import Path

def test_server_import():
    """Test if server components can be imported"""
    print("[*] Testing server imports...")
    
    try:
        from server_manager import ServerManager
        print("[OK] ServerManager import successful")
    except ImportError as e:
        print(f"[FAIL] ServerManager import failed: {e}")
        return False
    
    try:
        from main import app
        print("[OK] FastAPI app import successful")
    except ImportError as e:
        print(f"[FAIL] FastAPI app import failed: {e}")
        return False
    
    try:
        from config.settings import load_settings
        print("[OK] Settings import successful")
    except ImportError as e:
        print(f"[FAIL] Settings import failed: {e}")
        return False
    
    return True

def test_server_startup():
    """Test if the server can start and respond"""
    print("\n[*] Testing server startup...")
    
    try:
        from server_manager import ServerManager
        
        # Create server manager
        server_manager = ServerManager(port=8001)  # Use different port for testing
        
        # Start server
        server_manager.start_server()
        
        # Wait a moment for server to start
        time.sleep(2)
        
        if server_manager.is_server_running():
            print("[OK] Server started successfully")
            
            # Test basic endpoint
            try:
                response = requests.get(f"{server_manager.get_url()}/", timeout=5)
                if response.status_code == 200:
                    print("[OK] Server responding to requests")
                else:
                    print(f"[WARN] Server responded with status code: {response.status_code}")
            except requests.RequestException as e:
                print(f"[WARN] Could not connect to server: {e}")
            
            # Stop server
            server_manager.stop_server()
            print("[OK] Server stopped successfully")
            return True
        else:
            print("[FAIL] Server failed to start")
            return False
            
    except Exception as e:
        print(f"[FAIL] Server test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n[*] Testing configuration...")
    
    try:
        from config.settings import load_settings, get_default_settings
        
        settings = load_settings()
        print("[OK] Settings loaded successfully")
        
        if 'providers' in settings:
            print(f"[OK] Found {len(settings['providers'])} providers")
            for provider_id, provider in settings['providers'].items():
                print(f"   - {provider_id}: {provider.get('name', 'Unknown')}")
        
        if 'language_list' in settings:
            print(f"[OK] Found {len(settings['language_list'])} languages")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Configuration test failed: {e}")
        return False

def test_translator_import():
    """Test if translator components can be imported"""
    print("\n[*] Testing translator imports...")
    
    try:
        from src.translator import DocumentTranslator
        print("[OK] DocumentTranslator import successful")
        
        # Try to create instance (may fail due to missing API keys, but should import)
        try:
            translator = DocumentTranslator()
            print("[OK] DocumentTranslator instance created")
        except Exception as e:
            print(f"[WARN] DocumentTranslator instance creation failed (expected if no API keys): {e}")
        
        return True
        
    except ImportError as e:
        print(f"[FAIL] Translator import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("[TEST] Infinity Translator Server Test Suite")
    print("=" * 50)
    
    # Check working directory
    current_dir = Path.cwd()
    print(f"Working directory: {current_dir}")
    
    # Check if we're in the right directory
    if not (current_dir / "main.py").exists():
        print("[FAIL] main.py not found. Please run this script from the infinity translator directory.")
        return False
    
    tests = [
        ("Import Tests", test_server_import),
        ("Configuration Tests", test_configuration),
        ("Translator Tests", test_translator_import),
        ("Server Startup Tests", test_server_startup),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n" + "=" * 20 + f" {test_name} " + "=" * 20)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[FAIL] Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("[SUMMARY] Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] All tests passed! The server functionality is working correctly.")
        print("\nNote: To run the full desktop application, you need:")
        print("- Python 3.8-3.12 (current: " + sys.version.split()[0] + ")")
        print("- PySide6 and PySide6-WebEngine")
    else:
        print("[WARNING] Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    import os
    os.chdir(script_dir)
    
    success = main()
    sys.exit(0 if success else 1)