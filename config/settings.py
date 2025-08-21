import json
import os
import sys
from pathlib import Path

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        print(f"Settings: Using PyInstaller MEIPASS path: {base_path}")
    except AttributeError:
        # Running in development mode
        base_path = Path(__file__).parent.parent.absolute()
        print(f"Settings: Using development path: {base_path}")
    
    full_path = Path(base_path) / relative_path
    print(f"Settings: Resource path for '{relative_path}': {full_path} (exists: {full_path.exists()})")
    return full_path

def load_settings():
    """Load settings from settings.json file"""
    # Try multiple possible locations for settings.json
    settings_paths = [
        get_resource_path('config/settings.user.json'),  # User custom settings (highest priority)
        Path(__file__).parent / 'settings.user.json',
        Path('config/settings.user.json'),
        get_resource_path('config/settings.json'),  # Default settings
        Path(__file__).parent / 'settings.json',
        Path('config/settings.json'),
        Path('settings.json')
    ]
    
    print("Attempting to load settings from the following paths:")
    for settings_path in settings_paths:
        print(f"  - {settings_path} (exists: {settings_path.exists()})")
        if settings_path.exists():
            try:
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    print(f"Successfully loaded settings from {settings_path}")
                    return settings
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load settings from {settings_path}: {e}")
                continue
    
    # Return default settings if no file found
    return get_default_settings()

def get_default_settings():
    """Return default settings structure"""
    return {
        "active_provider": "openrouter",
        "providers": {
            "openrouter": {
                "base_url": "https://openrouter.ai/api/v1",
                "name": "OpenRouter (https://openrouter.ai)",
                "models": [
                    {
                        "id": "google/gemini-2.0-flash-001",
                        "name": "Google/Gemini-2.0-flash"
                    }
                ],
                "model_name": "google/gemini-2.0-flash-001"
            }
        },
        "target_language": "zh-Hans",
        "language_list": [
            {"name": "简体中文", "code": "zh-Hans"},
            {"name": "繁體中文", "code": "zh-Hant"},
            {"name": "English", "code": "en"},
            {"name": "日本語", "code": "ja"},
            {"name": "한국어", "code": "ko"},
            {"name": "Français", "code": "fr"},
            {"name": "Deutsch", "code": "de"},
            {"name": "Español", "code": "es"},
            {"name": "Português", "code": "pt"},
            {"name": "Русский", "code": "ru"},
            {"name": "العربية", "code": "ar"},
            {"name": "हिन्दी", "code": "hi"},
            {"name": "Italiano", "code": "it"},
            {"name": "Türkçe", "code": "tr"},
            {"name": "Tiếng Việt", "code": "vi"},
            {"name": "ไทย", "code": "th"},
            {"name": "Bahasa Indonesia", "code": "id"},
            {"name": "فارسی", "code": "fa"}
        ]
    }

def save_settings(settings):
    """Save settings to settings.user.json file"""
    # Try to save to the user settings file
    settings_paths = [
        get_resource_path('config/settings.user.json'),
        Path(__file__).parent / 'settings.user.json',
        Path('config/settings.user.json')
    ]
    
    # If user settings file doesn't exist, try to create it
    for settings_path in settings_paths:
        try:
            # Ensure directory exists
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return
        except (IOError, OSError) as e:
            print(f"Warning: Could not save settings to {settings_path}: {e}")
            continue
    
    print("Error: Could not save settings to any location")

def get_provider_settings(settings=None):
    """Get settings for the active provider"""
    if settings is None:
        settings = load_settings()
    
    active_provider = settings.get('active_provider', 'openrouter')
    providers = settings.get('providers', {})
    
    if active_provider not in providers:
        # Fallback to first available provider
        active_provider = list(providers.keys())[0] if providers else 'openrouter'
    
    provider_settings = providers.get(active_provider, {})
    
    return active_provider, provider_settings