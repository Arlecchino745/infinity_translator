import flet as ft
import logging
import webbrowser
from app.core.server_manager import ServerManager

logger = logging.getLogger(__name__)

class MainWindow:
    """Main window for the Flet-based Infinity Translator desktop application"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.server_manager = ServerManager()
        self.web_view = None
        self.url = None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.page.title = "Infinity Translator"
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.window.center()
        
        # Set application theme
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.colors.BLUE,
        )
        
        # Create app bar
        self.appbar = ft.AppBar(
            title=ft.Text("Infinity Translator"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.SETTINGS, on_click=self.open_settings),
                ft.IconButton(ft.icons.HELP, on_click=self.show_help),
            ],
        )
        
        # Create main content
        self.content = ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Infinity Translator", size=24, weight=ft.FontWeight.BOLD),
                            ft.Text("Starting server...", size=16),
                            ft.ProgressBar(),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    expand=True,
                )
            ],
            expand=True,
        )
        
        # Set page content
        self.page.appbar = self.appbar
        self.page.add(self.content)
        
    def show(self):
        """Display the main window and start the server"""
        try:
            # Start server
            self.server_manager.start_server()
            self.url = self.server_manager.get_url()
            
            # Update UI to show web view
            self.content.controls.clear()
            self.content.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Infinity Translator", size=24, weight=ft.FontWeight.BOLD),
                            ft.ElevatedButton(
                                "Open Web Interface",
                                icon=ft.icons.OPEN_IN_BROWSER,
                                on_click=self.open_web_interface
                            ),
                            ft.Text(f"Server is running at: {self.url}", size=14),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    expand=True,
                )
            )
            
            self.page.update()
            logger.info(f"Server started successfully at {self.url}")
            
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            self.content.controls.clear()
            self.content.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Error", size=24, color=ft.colors.RED),
                            ft.Text(f"Failed to start server: {str(e)}", size=16),
                            ft.ElevatedButton("Retry", on_click=self.retry_start),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    expand=True,
                )
            )
            self.page.update()
            
    def open_web_interface(self, e):
        """Open the web interface in the default browser"""
        if self.url:
            webbrowser.open(self.url)
            
    def open_settings(self, e):
        """Open settings dialog"""
        # For now, just show a simple dialog
        dlg = ft.AlertDialog(
            title=ft.Text("Settings"),
            content=ft.Text("Settings would be implemented here"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.page.close_dialog()),
            ],
        )
        self.page.open_dialog(dlg)
        
    def show_help(self, e):
        """Show help dialog"""
        dlg = ft.AlertDialog(
            title=ft.Text("Help"),
            content=ft.Text("Infinity Translator - Help content would be here"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.page.close_dialog()),
            ],
        )
        self.page.open_dialog(dlg)
        
    def retry_start(self, e):
        """Retry starting the application"""
        self.content.controls.clear()
        self.content.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Infinity Translator", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Starting server...", size=16),
                        ft.ProgressBar(),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True,
            )
        )
        self.page.update()
        self.show()