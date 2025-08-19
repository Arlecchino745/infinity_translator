import threading
import time
import logging
import uvicorn
import socket
from pathlib import Path
import sys
import os

# 修复uvicorn在PyInstaller环境下的日志问题
if getattr(sys, 'frozen', False):
    # 在PyInstaller环境中，确保stdout/stderr有isatty方法
    if hasattr(sys.stdout, 'isatty'):
        sys.stdout.isatty = lambda: False
    else:
        sys.stdout = type('StdoutProxy', (), {
            'isatty': lambda self: False,
            'write': lambda self, data: None,
            'flush': lambda self: None
        })()
        
    if hasattr(sys.stderr, 'isatty'):
        sys.stderr.isatty = lambda: False
    else:
        sys.stderr = type('StderrProxy', (), {
            'isatty': lambda self: False,
            'write': lambda self, data: None,
            'flush': lambda self: None
        })()

logger = logging.getLogger(__name__)

class ServerManager:
    """Manages the FastAPI server in a separate thread for the desktop application"""
    
    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port
        self.server_thread = None
        self.server = None
        self.is_running = False
        
    def find_free_port(self, start_port=8000, max_attempts=10):
        """Find a free port starting from start_port"""
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((self.host, port))
                    return port
            except OSError:
                continue
        raise RuntimeError(f"Could not find a free port in range {start_port}-{start_port + max_attempts}")
    
    def start_server(self):
        """Start the FastAPI server in a separate thread"""
        if self.is_running:
            logger.warning("Server is already running")
            return
        
        try:
            # Find a free port if the default is occupied
            self.port = self.find_free_port(self.port)
            logger.info(f"Starting server on {self.host}:{self.port}")
            
            # Import the FastAPI app
            from main import app
            
            # Configure uvicorn server
            config = uvicorn.Config(
                app,
                host=self.host,
                port=self.port,
                log_level="info",
                access_log=False,  # Disable access logs for cleaner output
                log_config=None,   # Disable uvicorn's logging configuration to prevent formatter conflicts
                loop="asyncio"
            )
            
            self.server = uvicorn.Server(config)
            
            # Start server in a separate thread
            self.server_thread = threading.Thread(
                target=self._run_server,
                daemon=True,
                name="FastAPI-Server"
            )
            self.server_thread.start()
            
            # Wait for server to start
            self._wait_for_server()
            self.is_running = True
            
            logger.info(f"Server started successfully on http://{self.host}:{self.port}")
            
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            raise
    
    def _run_server(self):
        """Run the uvicorn server"""
        try:
            self.server.run()
        except Exception as e:
            logger.error(f"Server error: {e}")
    
    def _wait_for_server(self, timeout=10):
        """Wait for the server to become available"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex((self.host, self.port))
                    if result == 0:
                        return True
            except Exception:
                pass
            time.sleep(0.1)
        
        raise TimeoutError(f"Server failed to start within {timeout} seconds")
    
    def stop_server(self):
        """Stop the FastAPI server"""
        if not self.is_running:
            return
        
        try:
            logger.info("Stopping server...")
            if self.server:
                self.server.should_exit = True
            
            if self.server_thread and self.server_thread.is_alive():
                self.server_thread.join(timeout=5)
            
            self.is_running = False
            logger.info("Server stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping server: {e}")
    
    def get_url(self):
        """Get the server URL"""
        return f"http://{self.host}:{self.port}"
    
    def is_server_running(self):
        """Check if the server is running"""
        return self.is_running and self.server_thread and self.server_thread.is_alive()