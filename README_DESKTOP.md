# Infinity Translator Desktop Application

Transform your FastAPI-based translation web application into a standalone desktop application with PySide6 WebEngine.

## 🎯 Overview

This desktop version of Infinity Translator provides:
- **No Browser Required**: Embedded web engine eliminates the need for manual browser navigation
- **System Integration**: Native file dialogs, system tray, and desktop notifications
- **Auto-Server Management**: FastAPI server runs automatically in the background
- **Professional Look**: Native window styling and desktop application behavior
- **Offline-Ready**: All resources bundled in the executable

## 🚀 Quick Start

### Option 1: Use Build Script (Recommended)
```bash
# Windows
build.bat

# Linux/Mac
python build_desktop.py
```

### Option 2: Manual Build
```bash
# Install dependencies
pip install -r requirements.txt pyinstaller

# Build the application
python build_desktop.py
```

### Option 3: Run in Development Mode
```bash
# Install desktop dependencies
pip install PySide6 PySide6-WebEngine

# Run desktop version
python desktop_app.py
```

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux with Qt support
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB free space for installation

### Python Dependencies
```
PySide6>=6.5.0
PySide6-WebEngine>=6.5.0
fastapi>=0.100.0
uvicorn>=0.22.0
langchain-openai
langchain-community
python-dotenv
tiktoken
tqdm
jinja2
python-multipart
psutil
```

## 🔧 Configuration

### API Keys Setup
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your API keys:
   ```env
   # Choose one or both providers
   SILICONFLOW_API_KEY=your_siliconflow_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

### Provider Configuration
The application supports multiple AI providers configured in `config/settings.json`:
- **OpenRouter**: Access to multiple models through OpenRouter API
- **SiliconFlow**: Direct access to SiliconFlow models

## 🏗️ Build Process

### Build Options
```bash
# Standard build (single executable)
python build_desktop.py

# Debug build (with console output)
python build_desktop.py --debug --console

# Clean build artifacts only
python build_desktop.py --clean-only

# Build without distribution package
python build_desktop.py --no-package
```

### Build Artifacts
- `dist/InfinityTranslator.exe` - Main executable
- `dist/InfinityTranslator_Package/` - Complete distribution package
- `build/` - Temporary build files (can be deleted)

## 🖥️ Desktop Features

### Window Management
- **Main Window**: Full-featured web interface in native window
- **System Tray**: Minimize to system tray functionality
- **Fullscreen Mode**: Toggle with F11
- **Window State**: Remembers size and position

### Menu System
- **File Menu**: Open files, exit application
- **View Menu**: Refresh, fullscreen toggle
- **Help Menu**: About dialog and help information

### Keyboard Shortcuts
- `Ctrl+O` - Open file dialog
- `Ctrl+Q` - Quit application
- `F5` - Refresh page
- `F11` - Toggle fullscreen
- `Esc` - Close dropdowns and dialogs

### Enhanced File Handling
- **Drag & Drop**: Enhanced drag-and-drop support
- **Native Dialogs**: System file dialogs for better UX
- **File Association**: Can be configured to open supported file types

## 🔍 Troubleshooting

### Common Issues

#### Application Won't Start
- **Check Python Version**: Ensure Python 3.8+ is installed
- **Missing Dependencies**: Run `pip install -r requirements.txt`
- **Port Conflicts**: Application automatically finds free ports
- **Check Logs**: Look in `logs/` directory for error details

#### Translation Errors
- **API Keys**: Verify API keys are correctly set in `.env`
- **Network Connection**: Check internet connectivity
- **Model Availability**: Ensure selected model is available
- **File Format**: Verify file is in supported format (TXT, MD, JSON, CSV)

#### Performance Issues
- **Memory Usage**: Close other applications if system is low on memory
- **Large Files**: Break large documents into smaller chunks
- **System Resources**: Check task manager for resource usage

### Debug Mode
Run with console output to see detailed logs:
```bash
python build_desktop.py --debug --console
```

### Log Files
Application logs are saved in:
- `logs/infinity_translator_YYYYMMDD.log`
- `infinity_translator.log` (in application directory)

## 🏗️ Architecture

### Component Overview
```
Desktop Application
├── desktop_app.py          # Main entry point
├── main_window.py          # PySide6 main window
├── server_manager.py       # FastAPI server management
├── error_handler.py        # Error handling and logging
├── main.py                 # FastAPI application
├── config/
│   ├── config.py          # Configuration management
│   └── settings.py        # Settings persistence
└── src/
    ├── translator.py      # Translation engine
    ├── progress.py        # Progress tracking
    └── output.py          # Output formatting
```

### Threading Model
- **Main Thread**: PySide6 GUI and event handling
- **Server Thread**: FastAPI server (uvicorn)
- **Translation Thread**: LLM processing (when active)

### Resource Management
- **Bundled Resources**: All static files, templates, and configs
- **Dynamic Configs**: User settings saved to writable locations
- **Temporary Files**: Cleaned up automatically on exit

## 🚀 Deployment

### Single Executable Distribution
The build process creates a single executable containing:
- Python runtime
- All dependencies
- Static files and templates
- Configuration files
- WebEngine runtime

### Distribution Package
Includes:
- `InfinityTranslator.exe` - Main executable
- `.env.example` - Configuration template
- `README.txt` - User instructions

### System Requirements for End Users
- **Windows**: Windows 10 or higher
- **No Python Required**: Completely standalone
- **No Installation**: Run directly from any location
- **Portable**: Can be run from USB drive

## 🔄 Migration from Web Version

### Existing Users
1. **Keep Configuration**: Copy your existing `.env` and `config/settings.json`
2. **Same Interface**: Web interface remains identical
3. **Enhanced Features**: Gain desktop-specific functionality
4. **Backward Compatible**: Can still run web version separately

### Development Workflow
```bash
# Web development (unchanged)
python main.py

# Desktop testing
python desktop_app.py

# Production build
python build_desktop.py
```

## 🆘 Support

### Getting Help
1. **Check Logs**: Review log files for error details
2. **GitHub Issues**: Report bugs and feature requests
3. **Documentation**: Refer to this README and code comments
4. **Community**: Join discussions and get help

### Reporting Issues
When reporting issues, please include:
- Operating system and version
- Python version (if running from source)
- Log files (`logs/` directory)
- Steps to reproduce the issue
- Expected vs actual behavior

## 📈 Performance Optimization

### Startup Time
- **Splash Screen**: Shows loading progress
- **Lazy Loading**: Components load as needed
- **Resource Caching**: Static files cached in memory

### Memory Usage
- **Efficient Threading**: Minimal thread overhead
- **Resource Cleanup**: Automatic cleanup on exit
- **Memory Monitoring**: Built-in memory usage tracking

### Translation Performance
- **Chunk Optimization**: Intelligent text chunking
- **Progress Tracking**: Real-time progress updates
- **Error Recovery**: Automatic retry on failures

## 🔮 Future Enhancements

### Planned Features
- **Auto-Updates**: Automatic application updates
- **Plugin System**: Extensible translation providers
- **Batch Processing**: Multiple file processing
- **OCR Integration**: Image and PDF text extraction
- **Cloud Sync**: Settings synchronization across devices

### Customization Options
- **Themes**: Light/dark mode support
- **Shortcuts**: Customizable keyboard shortcuts
- **Window Layouts**: Flexible window arrangements
- **Provider Plugins**: Custom AI provider integrations

---

## 📝 License

This desktop application maintains the same license as the original Infinity Translator project.

## 🙏 Acknowledgments

- **PySide6**: Qt for Python framework
- **FastAPI**: Modern web framework for APIs
- **PyInstaller**: Python to executable converter
- **Original Infinity Translator**: Base translation engine and web interface