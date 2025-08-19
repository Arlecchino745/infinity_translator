import sys
import os
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QIcon
from main_window import MainWindow

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

class InfinityTranslatorApp:
    """Desktop application for Infinity Translator"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.splash_screen = None
        
    def setup_application(self):
        """Setup the QApplication with proper configuration"""
        # Set application properties
        QApplication.setApplicationName("Infinity Translator")
        QApplication.setApplicationVersion("1.0.0")
        QApplication.setOrganizationName("Infinity Translator")
        QApplication.setOrganizationDomain("infinity-translator.local")
        
        # Enable high DPI scaling before creating QApplication
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL, True)
        
        # Create application instance
        self.app = QApplication(sys.argv)
        
        # Additional high DPI settings
        self.app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        
        # Set application icon if it exists
        icon_path = Path(__file__).parent / "static" / "favicon.ico"
        if icon_path.exists():
            self.app.setWindowIcon(QIcon(str(icon_path)))
        else:
            # Create a default icon if favicon doesn't exist
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.GlobalColor.blue)
            self.app.setWindowIcon(QIcon(pixmap))
        
        # Enable high DPI scaling
        self.app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        self.app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        # Try to set high DPI scaling for WebEngine (handle possible exception)
        try:
            self.app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        except Exception as e:
            logger.warning(f"Failed to set AA_UseHighDpiPixmaps: {e}")
            
    def show_splash_screen(self):
        """Show splash screen while application loads"""
        try:
            # Try to load logo as splash screen
            logo_path = Path(__file__).parent / "static" / "logo.png"
            if logo_path.exists():
                pixmap = QPixmap(str(logo_path))
                # Scale the pixmap to a reasonable size
                pixmap = pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio, 
                                     Qt.TransformationMode.SmoothTransformation)
            else:
                # Create a simple splash screen
                pixmap = QPixmap(400, 300)
                pixmap.fill(Qt.GlobalColor.white)
                
            self.splash_screen = QSplashScreen(pixmap)
            self.splash_screen.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | 
                                            Qt.WindowType.FramelessWindowHint)
            
            # Show splash screen
            self.splash_screen.show()
            self.splash_screen.showMessage(
                "Starting Infinity Translator...", 
                Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
                Qt.GlobalColor.black
            )
            
            # Process events to show splash screen
            self.app.processEvents()
            
        except Exception as e:
            logger.warning(f"Failed to show splash screen: {e}")
            
    def hide_splash_screen(self):
        """Hide the splash screen"""
        if self.splash_screen:
            self.splash_screen.close()
            self.splash_screen = None
            
    def create_main_window(self):
        """Create and configure the main window"""
        try:
            self.main_window = MainWindow()
            
            # Hide splash screen when main window is ready
            if self.splash_screen:
                QTimer.singleShot(2000, self.hide_splash_screen)
            
            # Show main window
            self.main_window.show()
            
            logger.info("Main window created and shown")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to create main window: {error_msg}")
            self.show_error_and_exit("Initialization Error", 
                                   f"Failed to initialize the application: {error_msg}")
            
    def show_error_and_exit(self, title, message):
        """Show error message and exit application"""
        try:
            if self.splash_screen:
                self.splash_screen.hide()
                
            QMessageBox.critical(None, title, message)
        except:
            print(f"Critical Error: {title} - {message}")
        finally:
            sys.exit(1)
            
    def setup_exception_handling(self):
        """Setup global exception handling"""
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
                
            logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
            
            if self.app:
                QMessageBox.critical(
                    None, 
                    "Unexpected Error",
                    f"An unexpected error occurred:\n{exc_type.__name__}: {exc_value}\n\n"
                    "Please check the log file for more details."
                )
                
        sys.excepthook = handle_exception
        
    def run(self):
        """Run the desktop application"""
        try:
            logger.info("Starting Infinity Translator Desktop Application")
            
            # Setup exception handling
            self.setup_exception_handling()
            
            # Setup application
            self.setup_application()
            
            # Show splash screen
            self.show_splash_screen()
            
            # Create main window
            self.create_main_window()
            
            # Start the application event loop
            logger.info("Starting application event loop")
            exit_code = self.app.exec()
            
            logger.info(f"Application exited with code: {exit_code}")
            return exit_code
            
        except Exception as e:
            logger.error(f"Failed to start application: {e}")
            self.show_error_and_exit("Startup Error", 
                                   f"Failed to start the application: {e}")
            
    def cleanup(self):
        """Cleanup resources before exit"""
        try:
            if self.main_window:
                self.main_window.close()
                
            if self.splash_screen:
                self.splash_screen.close()
                
            logger.info("Application cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

def main():
    """Main entry point"""
    # Ensure we're in the correct directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Create and run the application
    app = InfinityTranslatorApp()
    
    try:
        return app.run()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Application failed: {e}")
        return 1
    finally:
        app.cleanup()

if __name__ == "__main__":
    sys.exit(main())