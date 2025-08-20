import sys
import os
import logging
from pathlib import Path

# Add the parent directory to the path so we can import the main FastAPI app
sys.path.append(str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('infinity_translator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the application"""
    try:
        logger.info("Starting Infinity Translator Application")
        
        # Import and run the Flet desktop app
        import flet as ft
        from app.ui.desktop_app import main as flet_main
        
        logger.info("Launching Flet application")
        ft.app(target=flet_main)
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()