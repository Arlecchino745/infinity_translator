import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running in development mode
        base_path = Path(__file__).parent.parent.absolute()
    
    return Path(base_path) / relative_path

def load_environment():
    """Load environment variables from .env file"""
    # Try to load from multiple possible locations
    env_paths = [
        get_resource_path('.env'),
        get_resource_path('.env.example'),
        Path('.env'),
        Path('.env.example')
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break

# Load environment variables
load_environment()

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not SILICONFLOW_API_KEY and not OPENROUTER_API_KEY:
    print("Warning: No API keys found. Please configure API keys in the .env file or environment variables.")
