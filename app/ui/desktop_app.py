import flet as ft
from app.ui.main_window import MainWindow
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InfinityTranslatorApp:
    """Flet-based desktop application for Infinity Translator"""
    
    def __init__(self):
        self.main_window = None
        
    def run(self, page: ft.Page):
        """Run the Flet desktop application"""
        try:
            logger.info("Starting Infinity Translator Desktop Application with Flet")
            
            # Create main window
            self.main_window = MainWindow(page)
            
            # Show main window
            self.main_window.show()
            
            logger.info("Application started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start application: {e}")
            # In a real application, we would show an error dialog here
            raise

def main(page: ft.Page):
    """Main entry point for the Flet application"""
    app = InfinityTranslatorApp()
    app.run(page)

if __name__ == "__main__":
    ft.app(target=main)