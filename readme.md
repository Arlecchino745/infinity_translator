# Infinity Translator

<div align="center">🌐 <a href="/docs/README_zh-Hans.md">简体中文</a> | <a href="/docs/README_zh-Hant.md">繁體中文</a> | <a href="/docs/README_ja.md">日本語</a> | <a href="/docs/README_fr.md">Français</a> | <a href="/docs/README_kr.md">한국어</a> | <a href="/docs/README_ru.md">Русский</a></div>

---
Infinity Translator is a software that utilizes large language models for long text translation, with a modern and beautiful UI interface. It can appropriately chunk and preprocess large documents and translate them into multiple languages.

![image](https://github.com/Arlecchino745/infinity_translator/blob/main/docs/img/screenshot2.png)
![image](https://github.com/Arlecchino745/infinity_translator/blob/main/docs/img/screenshot.png)

## Features ✨

- Supports large document translation with no document length limit 📄
- Preprocesses Markdown documents to optimize the visual appearance of translations 🎨
- Displays translation progress in real-time and automatically saves translation results ⏱️

## Start from the source code (dev)

1. Clone the project and switch to the project folder:
```bash
# Clone the project code from GitHub to your local machine
git clone https://github.com/Arlecchino745/infinity_translator.git
# Switch to the project directory
cd infinity_translator
```

2. Install dependencies: Please pay attention to selecting the appropriate Python version. The project is known to run normally under Python 3.12. 
```bash
# Create a virtual environment named .venv
python -m venv .venv
# Activate the virtual environment (for Windows systems)
.\.venv\Scripts\Activate
# Activate the virtual environment (for Linux&Mac)
source ./.venv/bin/activate
# Install the required dependency libraries for the project
pip install -r requirements.txt
```

3. API Key Configuration: Refer to the `.env.example` file in the project folder. ⚙️
   - Copy the `.env.example` file to `.env` and fill in your API key.

4. (Optional) Create your personalized configuration in the config folder according to the comments in settings.json. 🛠️
   - If you need custom configuration, please refer to the `config/settings.json.example` file.

5. Run after completing the above steps:
```bash
# Start the Web application
python web_app.py
```
Then enter `localhost:8000` or `127.0.0.1:8000` in your browser's address bar and confirm. 🎉

### Application Settings Configuration ⚙️

The project contains two configuration files:
- `config/settings.json` - Default configuration file, should not be modified
- `config/settings.json.example` - Configuration template file for reference

If you need advanced custom configuration (e.g., adding new models or service providers), follow these steps:

1. Copy the `config/settings.json` file and rename it to `config/settings.user.json`:
   ```bash
   # Copy the default configuration file to a user-defined configuration file
   cp config/settings.json config/settings.user.json
   ```

2. Modify the configuration in the `config/settings.user.json` file
   - Edit the `settings.user.json` file according to your needs, such as adding new models or adjusting parameters.

3. The application will prioritize loading settings.user.json, so your custom configuration will not be tracked by Git
   - This avoids custom configurations from being committed to the remote repository by Git.

## Technology Stack 💻

- Backend: FastAPI + Uvicorn
- Frontend: Vue.js + Axios
- Desktop: Flet (based on Flutter)
- Translation: LangChain + OpenAI API
- Build: PyInstaller + Flet packaging tool

## License 📄

The project is licensed under the MIT License.

## AIGC Statement

This project is AI-assisted. Please contact the author if there is any inadvertent infringement.
