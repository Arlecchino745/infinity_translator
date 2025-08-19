import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QMenuBar, QStatusBar, QMessageBox, QApplication,
                               QSystemTrayIcon, QMenu, QFileDialog)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PySide6.QtCore import Qt, QUrl, QTimer, Signal, QThread
from PySide6.QtGui import QIcon, QAction, QPixmap
from server_manager import ServerManager

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Main window for the Infinity Translator desktop application"""
    
    # Signals
    server_started = Signal(str)
    server_error = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.server_manager = None
        self.web_view = None
        self.system_tray = None
        self.is_fullscreen = False
        
        self.init_ui()
        self.setup_web_engine()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.setup_system_tray()
        self.setup_server()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Infinity Translator")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set application icon if it exists
        icon_path = Path(__file__).parent / "static" / "favicon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        else:
            # Create a default icon if favicon doesn't exist
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.GlobalColor.blue)
            self.setWindowIcon(QIcon(pixmap))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create web view
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # Set fullscreen by default
        self.showFullScreen()
        self.is_fullscreen = True
        
    def setup_web_engine(self):
        """Configure the web engine settings"""
        if not self.web_view:
            return
            
        # Get the default profile
        profile = QWebEngineProfile.defaultProfile()
        
        # Configure settings
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        
        # Enable high DPI scaling for web content (handle possible exception)
        try:
            settings.setAttribute(QWebEngineSettings.WebAttribute.HighDpiScalingEnabled, True)
        except Exception as e:
            logger.warning(f"Failed to enable HighDpiScalingEnabled: {e}")
        
        # Set user agent
        profile.setHttpUserAgent(
            "Infinity Translator Desktop App (PySide6 WebEngine)"
        )
        
    def setup_menu_bar(self):
        """Setup the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open File", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        refresh_action = QAction("Refresh", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_page)
        view_menu.addAction(refresh_action)
        
        fullscreen_action = QAction("Toggle Fullscreen", self)
        fullscreen_action.setShortcut("F11")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Initializing...")
        
    def setup_system_tray(self):
        """Setup system tray icon and menu"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            logger.warning("System tray is not available")
            return
            
        # Create system tray icon
        icon_path = Path(__file__).parent / "static" / "favicon.ico"
        if icon_path.exists():
            icon = QIcon(str(icon_path))
        else:
            # Create a default icon if favicon doesn't exist
            pixmap = QPixmap(16, 16)
            pixmap.fill(Qt.GlobalColor.blue)
            icon = QIcon(pixmap)
            
        self.system_tray = QSystemTrayIcon(icon, self)
        
    def setup_server(self):
        """Initialize and start the FastAPI server"""
        try:
            self.server_manager = ServerManager()
            self.server_manager.start_server()
            
            # Load the web interface after server starts
            QTimer.singleShot(1000, self.load_web_interface)
            
        except Exception as e:
            logger.error(f"Failed to setup server: {e}")
            self.show_error_message("Server Error", f"Failed to start the application server: {e}")
            
    def load_web_interface(self):
        """Load the web interface in the web view"""
        if self.server_manager and self.server_manager.is_server_running():
            url = self.server_manager.get_url()
            self.web_view.setUrl(QUrl(url))
            self.status_bar.showMessage(f"Connected to {url}")
            logger.info(f"Loading web interface from {url}")
        else:
            self.status_bar.showMessage("Server not available")
            self.show_error_message("Connection Error", "Cannot connect to the application server")
            
    def open_file_dialog(self):
        """Open file dialog for selecting files to translate"""
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Text files (*.txt *.md *.json *.csv)")
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                # Here you could inject JavaScript to handle the file
                # For now, just show a message
                self.status_bar.showMessage(f"Selected file: {Path(file_path).name}")
                
    def refresh_page(self):
        """Refresh the web page"""
        if self.web_view:
            self.web_view.reload()
            
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Infinity Translator",
            "Infinity Translator\n\n"
            "AI-Powered Document Translation\n"
            "Break through document length limitations with advanced LLM technology.\n\n"
            "Desktop version powered by PySide6"
        )
        
    def show_error_message(self, title, message):
        """Show error message dialog"""
        QMessageBox.critical(self, title, message)
        
    def show_window(self):
        """Show and raise the main window"""
        self.show()
        self.raise_()
        self.activateWindow()
        
    def tray_icon_activated(self, reason):
        """Handle system tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window()
            
    def quit_application(self):
        """Quit the application properly"""
        self.close()
        
    def closeEvent(self, event):
        """Handle application close event"""
        try:
            # Stop the server
            if self.server_manager:
                self.server_manager.stop_server()
                
            # Hide system tray icon
            if self.system_tray:
                self.system_tray.hide()
                
            event.accept()
            logger.info("Application closed successfully")
            
        except Exception as e:
            logger.error(f"Error during application shutdown: {e}")
            event.accept()
            
    def changeEvent(self, event):
        """Handle window state changes"""
        if event.type() == event.Type.WindowStateChange:
            if self.isMinimized() and self.system_tray and self.system_tray.isVisible():
                # Hide to system tray when minimized
                self.hide()
                if hasattr(self.system_tray, 'showMessage'):
                    self.system_tray.showMessage(
                        "Infinity Translator",
                        "Application was minimized to tray",
                        QSystemTrayIcon.MessageIcon.Information,
                        2000
                    )
                event.ignore()
                return
        super().changeEvent(event)