import json
import os

def load_settings():
    """Load settings from settings.json file"""
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    return settings

def get_provider_settings(settings=None):
    """Get settings for the active provider"""
    if settings is None:
        settings = load_settings()
    
    active_provider = settings['active_provider']
    provider_settings = settings['providers'][active_provider]
    
    return active_provider, provider_settings
