#!/usr/bin/env python3
"""
Build script for Infinity Translator Desktop Application
This script automates the build process using PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import argparse

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'PySide6',
        'fastapi',
        'uvicorn',
        'langchain_openai',
        'pyinstaller'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PySide6':
                import PySide6
            elif package == 'fastapi':
                import fastapi
            elif package == 'uvicorn':
                import uvicorn
            elif package == 'langchain_openai':
                import langchain_openai
            elif package == 'pyinstaller':
                import PyInstaller
        except ImportError:
            missing_packages.append(package)
            # 尝试另一种导入方式
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                try:
                    __import__(package.replace('-', '').lower())
                except ImportError:
                    pass
                else:
                    missing_packages.remove(package)
            else:
                missing_packages.remove(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt pyinstaller")
        return False
    
    print("✅ All required packages are installed")
    return True

def clean_build_directories():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous build artifacts...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))
        
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
    
    print("✅ Build directories cleaned")

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        print("📄 Creating .env file from .env.example...")
        shutil.copy(env_example, env_file)
        print("⚠️  Please edit .env file with your API keys before running the application")
    elif not env_file.exists():
        print("📄 Creating default .env file...")
        with open(env_file, 'w') as f:
            f.write("# Infinity Translator API Configuration\n")
            f.write("# Uncomment and fill in your API keys\n\n")
            f.write("#SILICONFLOW_API_KEY=your_siliconflow_api_key_here\n")
            f.write("#OPENROUTER_API_KEY=your_openrouter_api_key_here\n")
        print("⚠️  Please edit .env file with your API keys before running the application")

def build_application(debug=False, console=False):
    """Build the desktop application using PyInstaller"""
    print("🔨 Building desktop application...")
    
    # Check if icon file exists
    icon_path = 'static/favicon.ico'
    if not Path(icon_path).exists():
        print("⚠️  Icon file not found, building without icon")
        icon_path = None
    
    # PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--onefile' if not debug else '--onedir',
        '--windowed' if not console else '--console',
        '--name', 'InfinityTranslator',
    ]
    
    # Add icon only if it exists
    if icon_path:
        cmd.extend(['--icon', icon_path])
    
    cmd.extend([
        '--add-data', 'static;static',
        '--add-data', 'templates;templates',
        '--add-data', 'config;config',
        '--add-data', 'src;src',
        '--add-data', '.env.example;.',
        '--hidden-import', 'uvicorn.lifespan.on',
        '--hidden-import', 'uvicorn.lifespan.off',
        '--hidden-import', 'uvicorn.protocols.websockets.auto',
        '--hidden-import', 'uvicorn.protocols.websockets.websockets_impl',
        '--hidden-import', 'uvicorn.protocols.http.auto',
        '--hidden-import', 'uvicorn.protocols.http.h11_impl',
        '--hidden-import', 'uvicorn.protocols.http.httptools_impl',
        '--hidden-import', 'uvicorn.loops.auto',
        '--hidden-import', 'uvicorn.loops.asyncio',
        '--hidden-import', 'PySide6.QtWebEngineWidgets',
        '--hidden-import', 'PySide6.QtWebEngineCore',
        '--hidden-import', 'langchain_openai',
        '--hidden-import', 'langchain_community',
        '--hidden-import', 'langchain_core',
        '--hidden-import', 'langchain_text_splitters',
        '--exclude-module', 'tkinter',
        '--exclude-module', 'matplotlib',
        '--exclude-module', 'numpy',
        '--exclude-module', 'scipy',
        '--exclude-module', 'pandas',
        'desktop_app.py'
    ])
    
    if debug:
        cmd.extend(['--debug', 'all'])
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        
        # Show build artifacts
        dist_dir = Path('dist')
        if dist_dir.exists():
            print(f"\n📦 Build artifacts in {dist_dir.absolute()}:")
            for item in dist_dir.iterdir():
                if item.is_file():
                    size = item.stat().st_size / (1024 * 1024)  # MB
                    print(f"   {item.name} ({size:.1f} MB)")
                elif item.is_dir():
                    print(f"   {item.name}/ (directory)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error code {e.returncode}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def create_distribution_package():
    """Create a distribution package with necessary files"""
    print("📦 Creating distribution package...")
    
    dist_dir = Path('dist')
    package_dir = dist_dir / 'InfinityTranslator_Package'
    
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy executable
    exe_file = dist_dir / 'InfinityTranslator.exe'
    if exe_file.exists():
        shutil.copy(exe_file, package_dir)
    
    # Copy .env.example if it exists
    env_example = Path('.env.example')
    if env_example.exists():
        shutil.copy('.env.example', package_dir)
    else:
        # Create a default .env file
        with open(package_dir / '.env', 'w') as f:
            f.write("# Infinity Translator API Configuration\n")
            f.write("# Uncomment and fill in your API keys\n\n")
            f.write("#SILICONFLOW_API_KEY=your_siliconflow_api_key_here\n")
            f.write("#OPENROUTER_API_KEY=your_openrouter_api_key_here\n")
    
    # Create README for distribution
    readme_content = """# Infinity Translator Desktop Application

## Quick Start
1. Edit .env with your API keys
2. Run InfinityTranslator.exe

## API Keys Required
- SiliconFlow API Key OR OpenRouter API Key
- Get your keys from:
  - SiliconFlow: https://siliconflow.cn
  - OpenRouter: https://openrouter.ai

## Support
For issues and support, please check the application logs in the logs/ directory.
"""
    
    with open(package_dir / 'README.txt', 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Distribution package created in {package_dir}")

def main():
    parser = argparse.ArgumentParser(description='Build Infinity Translator Desktop Application')
    parser.add_argument('--debug', action='store_true', help='Build in debug mode')
    parser.add_argument('--console', action='store_true', help='Show console window')
    parser.add_argument('--clean-only', action='store_true', help='Only clean build directories')
    parser.add_argument('--no-package', action='store_true', help='Skip distribution package creation')
    
    args = parser.parse_args()
    
    print("🚀 Infinity Translator Desktop Build Script")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    print(f"Working directory: {script_dir}")
    
    # Clean build directories
    clean_build_directories()
    
    if args.clean_only:
        print("✅ Clean completed")
        return 0
    
    # Check requirements
    if not check_requirements():
        return 1
    
    # Create .env file
    create_env_file()
    
    # Build application
    if not build_application(debug=args.debug, console=args.console):
        return 1
    
    # Create distribution package
    if not args.no_package:
        create_distribution_package()
    
    print("\n🎉 Build process completed successfully!")
    print("\nNext steps:")
    print("1. Test the executable in dist/ directory")
    print("2. Configure API keys in .env file")
    print("3. Distribute the package to users")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())