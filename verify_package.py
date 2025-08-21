"""
Verification script for the packaged Infinity Translator application.
This script checks if all required files are present in the packaged application.
"""

import os
import sys
from pathlib import Path

def check_file(file_path, required=True):
    """Check if a file exists and print the result."""
    exists = os.path.exists(file_path)
    status = "✅ Found" if exists else "❌ Missing"
    if not exists and required:
        status += " (REQUIRED)"
    print(f"{status}: {file_path}")
    return exists

def main():
    # Determine the base directory
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = "dist/infinity_translator"
    
    if not os.path.isdir(base_dir):
        print(f"Error: Directory '{base_dir}' not found.")
        print("Usage: python verify_package.py [path_to_package_directory]")
        return False
    
    print(f"Verifying package in: {base_dir}\n")
    
    # Required files
    required_files = [
        "infinity_translator.exe",  # Main executable
        ".env.example",             # Environment variables example
        "config/settings.json",     # Default settings
        "config/settings.json.example",  # Settings example
        "templates/index.html",     # Main template
        "static/favicon.ico",       # Favicon/icon
        "static/logo.png",          # Logo
        "static/app.js",            # Frontend JavaScript
        "static/css/main.css"       # Main CSS
    ]
    
    # Check for required files
    print("Checking required files:")
    all_required_found = True
    for file_path in required_files:
        full_path = os.path.join(base_dir, file_path)
        if not check_file(full_path, required=True):
            all_required_found = False
    
    # Files that should NOT be included
    excluded_files = [
        ".env",                     # Environment variables with API keys
        ".git",                     # Git directory
        ".gitignore",               # Git ignore file
        "__pycache__",              # Python cache
        "build.bat",                # Build script
        "build.sh",                 # Build script
        "infinity_translator.spec"  # PyInstaller spec file
    ]
    
    print("\nChecking excluded files (these should NOT be present):")
    all_excluded_absent = True
    for file_path in excluded_files:
        full_path = os.path.join(base_dir, file_path)
        if check_file(full_path, required=False):
            all_excluded_absent = False
            print(f"  ⚠️ Warning: {file_path} should not be included in the package")
    
    # Summary
    print("\nVerification Summary:")
    if all_required_found:
        print("✅ All required files are present")
    else:
        print("❌ Some required files are missing")
    
    if all_excluded_absent:
        print("✅ No excluded files were found")
    else:
        print("⚠️ Some files that should be excluded were found")
    
    if all_required_found and all_excluded_absent:
        print("\n✅ Package verification PASSED")
        return True
    else:
        print("\n⚠️ Package verification FAILED")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)