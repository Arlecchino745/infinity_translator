import flet as ft
import os
import sys
import zipfile
from pathlib import Path

def build_desktop_app():
    """Build the Flet desktop application"""
    try:
        # 确保在正确的目录中
        os.chdir(Path(__file__).parent.parent)
        
        print("Building Infinity Translator desktop app...")
        
        # 使用flet pack命令打包应用
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "flet", "pack", 
            "app/desktop_app.py",  # 更新为desktop_app.py
            "--name", "InfinityTranslator",
            "--product-name", "Infinity Translator",
            "--product-version", "1.0.0",
            "--file-description", "Infinity Translator - AI Powered Document Translation Tool",
            "--copyright", "Copyright (c) 2025 Infinity Translator Project"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Desktop app built successfully!")
            print("📦 Output location: dist/InfinityTranslator.exe")
            
            # 创建完整包
            create_full_package()
        else:
            print("❌ Build failed!")
            print("Error output:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False
    
    return True

def create_full_package():
    """Create a full package with all necessary files"""
    try:
        package_dir = Path("dist/InfinityTranslator_Package")
        package_dir.mkdir(exist_ok=True)
        
        # 复制主程序
        main_exe = Path("dist/InfinityTranslator.exe")
        if main_exe.exists():
            import shutil
            shutil.copy2(main_exe, package_dir)
        
        # 需要包含的目录和文件
        assets = [
            "config",
            "static",
            "templates",
            "src",
            "requirements.txt",
            "web_app.py",  # 更新为web_app.py
            "README.md"
        ]
        
        for asset in assets:
            asset_path = Path(asset)
            if asset_path.exists():
                if asset_path.is_dir():
                    # 复制目录
                    import shutil
                    dest_path = package_dir / asset_path.name
                    if dest_path.exists():
                        shutil.rmtree(dest_path)
                    shutil.copytree(asset_path, dest_path, 
                                  ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git', '.venv'))
                else:
                    # 复制文件
                    import shutil
                    shutil.copy2(asset_path, package_dir)
        
        # 创建ZIP包
        zip_path = Path("dist/InfinityTranslator_Package.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in package_dir.rglob('*'):
                if file_path.is_file():
                    arc_path = file_path.relative_to(package_dir.parent)
                    zipf.write(file_path, arc_path)
        
        print("📦 Full package created successfully!")
        print("📁 Package location: dist/InfinityTranslator_Package/")
        print("💾 ZIP package: dist/InfinityTranslator_Package.zip")
        
    except Exception as e:
        print(f"❌ Package creation error: {e}")

if __name__ == "__main__":
    build_desktop_app()