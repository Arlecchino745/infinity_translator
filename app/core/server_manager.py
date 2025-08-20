import threading
import time
import uvicorn
import socket
import sys
import os
from pathlib import Path

# Add parent directory to path so we can import from the root
sys.path.append(str(Path(__file__).parent.parent.parent))

class ServerManager:
    """Manages the FastAPI server in a separate thread for the desktop application"""
    
    def __init__(self, port=None):
        # 修复PyInstaller环境下的日志问题
        self._fix_pyinstaller_logging()
        
        self.port = port or self._find_free_port()
        self.server_thread = None
        self.is_running = False
        
    def _find_free_port(self):
        """查找可用端口"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    def start_server(self):
        """启动FastAPI服务器"""
        if self.is_running:
            return
            
        def run():
            try:
                # 导入FastAPI应用
                from web_app import app  # 修改为web_app.py
                
                config = uvicorn.Config(
                    app=app,
                    host="127.0.0.1",
                    port=self.port,
                    log_level="info"
                )
                server = uvicorn.Server(config)
                self.is_running = True
                server.run()
            except Exception as e:
                print(f"Server error: {e}")
                self.is_running = False
        
        self.server_thread = threading.Thread(target=run, daemon=True)
        self.server_thread.start()
        
        # 等待服务器启动
        timeout = 10
        while timeout > 0 and not self.is_running:
            time.sleep(0.1)
            timeout -= 0.1
    
    
    def stop_server(self):
        """停止服务器"""
        self.is_running = False
        if self.server_thread:
            self.server_thread.join(timeout=5)
    
    def get_url(self):
        """获取服务器URL"""
        return f"http://127.0.0.1:{self.port}"