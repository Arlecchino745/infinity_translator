import sys
import logging
import traceback
from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import QObject, Signal

class DesktopErrorHandler(QObject):
    """Enhanced error handling for desktop application"""
    
    # Signals for error notification
    error_occurred = Signal(str, str)  # title, message
    critical_error = Signal(str, str)  # title, message
    
    def __init__(self):
        super().__init__()
        self.setup_logging()
        self.setup_exception_handling()
        
    def setup_logging(self):
        """Setup comprehensive logging for desktop application"""
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Setup log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = log_dir / f"infinity_translator_{timestamp}.log"
        
        # Configure logging format
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Configure root logger
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Set specific log levels for different modules
        logging.getLogger('uvicorn').setLevel(logging.WARNING)
        logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
        logging.getLogger('uvicorn.error').setLevel(logging.INFO)
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Desktop error handler initialized")
        
    def setup_exception_handling(self):
        """Setup global exception handling"""
        sys.excepthook = self.handle_exception
        
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions"""
        if issubclass(exc_type, KeyboardInterrupt):
            # Let KeyboardInterrupt pass through
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
            
        # Log the exception
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.logger.error(f"Uncaught exception: {error_msg}")
        
        # Show user-friendly error dialog
        self.show_critical_error(
            "Unexpected Error",
            f"An unexpected error occurred:\n\n{exc_type.__name__}: {exc_value}\n\n"
            "Please check the log files for more details. The application will continue running."
        )
        
    def handle_server_error(self, error):
        """Handle FastAPI server errors"""
        self.logger.error(f"Server error: {error}")
        self.show_error(
            "Server Error",
            f"The translation server encountered an error:\n{error}\n\n"
            "Please try restarting the application."
        )
        
    def handle_translation_error(self, error, filename=None):
        """Handle translation-specific errors"""
        error_msg = f"Translation error for file '{filename}': {error}" if filename else f"Translation error: {error}"
        self.logger.error(error_msg)
        
        self.show_error(
            "Translation Error",
            f"Failed to translate the document:\n{error}\n\n"
            "Please check your API configuration and try again."
        )
        
    def handle_file_error(self, error, operation="file operation"):
        """Handle file-related errors"""
        self.logger.error(f"File error during {operation}: {error}")
        self.show_error(
            "File Error",
            f"A file error occurred during {operation}:\n{error}\n\n"
            "Please check file permissions and try again."
        )
        
    def handle_network_error(self, error):
        """Handle network-related errors"""
        self.logger.error(f"Network error: {error}")
        self.show_error(
            "Network Error",
            f"A network error occurred:\n{error}\n\n"
            "Please check your internet connection and API configuration."
        )
        
    def handle_configuration_error(self, error):
        """Handle configuration-related errors"""
        self.logger.error(f"Configuration error: {error}")
        self.show_error(
            "Configuration Error",
            f"A configuration error occurred:\n{error}\n\n"
            "Please check your settings and API keys."
        )
        
    def show_error(self, title, message):
        """Show non-critical error dialog"""
        self.logger.warning(f"Showing error dialog: {title} - {message}")
        
        if QApplication.instance():
            try:
                QMessageBox.warning(None, title, message)
            except Exception as e:
                self.logger.error(f"Failed to show error dialog: {e}")
                print(f"ERROR: {title} - {message}")
        else:
            print(f"ERROR: {title} - {message}")
            
        # Emit signal for other components
        self.error_occurred.emit(title, message)
        
    def show_critical_error(self, title, message):
        """Show critical error dialog"""
        self.logger.critical(f"Critical error: {title} - {message}")
        
        if QApplication.instance():
            try:
                QMessageBox.critical(None, title, message)
            except Exception as e:
                self.logger.error(f"Failed to show critical error dialog: {e}")
                print(f"CRITICAL ERROR: {title} - {message}")
        else:
            print(f"CRITICAL ERROR: {title} - {message}")
            
        # Emit signal for other components
        self.critical_error.emit(title, message)
        
    def show_info(self, title, message):
        """Show information dialog"""
        self.logger.info(f"Info: {title} - {message}")
        
        if QApplication.instance():
            try:
                QMessageBox.information(None, title, message)
            except Exception as e:
                self.logger.error(f"Failed to show info dialog: {e}")
                print(f"INFO: {title} - {message}")
        else:
            print(f"INFO: {title} - {message}")
            
    def log_performance(self, operation, duration):
        """Log performance metrics"""
        self.logger.info(f"Performance: {operation} took {duration:.2f} seconds")
        
    def log_user_action(self, action, details=None):
        """Log user actions for debugging"""
        if details:
            self.logger.info(f"User action: {action} - {details}")
        else:
            self.logger.info(f"User action: {action}")

# Global error handler instance
_error_handler = None

def get_error_handler():
    """Get the global error handler instance"""
    global _error_handler
    if _error_handler is None:
        _error_handler = DesktopErrorHandler()
    return _error_handler

def handle_error(error_type, error, context=""):
    """Convenience function to handle errors"""
    handler = get_error_handler()
    
    if error_type == "server":
        handler.handle_server_error(error)
    elif error_type == "translation":
        handler.handle_translation_error(error, context)
    elif error_type == "file":
        handler.handle_file_error(error, context)
    elif error_type == "network":
        handler.handle_network_error(error)
    elif error_type == "config":
        handler.handle_configuration_error(error)
    else:
        handler.show_error("Error", f"{context}: {error}" if context else str(error))

def log_info(message):
    """Convenience function to log info messages"""
    get_error_handler().logger.info(message)

def log_error(message):
    """Convenience function to log error messages"""
    get_error_handler().logger.error(message)

def log_warning(message):
    """Convenience function to log warning messages"""
    get_error_handler().logger.warning(message)