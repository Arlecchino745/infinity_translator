# Infinity Translator

<div align="center">🌐 <a href="/docs/README_zh-Hans.md">简体中文</a> | <a href="/docs/README_zh-Hant.md">繁體中文</a> | <a href="/docs/README_ja.md">日本語</a> | <a href="/docs/README_fr.md">Français</a> | <a href="/docs/README_kr.md">한국어</a> | <a href="/docs/README_ru.md">Русский</a></div>

---
Infinity Translator 是一款利用大型語言模型進行長文本翻譯的軟體，具有現代且美觀的 UI 介面。它可以適當地分塊和預處理大型文檔，並將它們翻譯成多種語言。

![image](https://github.com/Arlecchino745/infinity_translator/blob/main/docs/img/screenshot2.png)
![image](https://github.com/Arlecchino745/infinity_translator/blob/main/docs/img/screenshot.png)

## 功能 ✨

- 支援大型文檔翻譯，沒有文檔長度限制 📄
- 預處理 Markdown 文檔，以優化翻譯的視覺外觀 🎨
- 實時顯示翻譯進度並自動保存翻譯結果 ⏱️

## 快速開始！

**注意：遺憾的是，由於一些技術問題，此版本僅支援透過 OpenRouter 使用 Google Gemini 2.0 Flash 進行翻譯工作。此問題將在後續版本中優先解決。**

1. 從 [Releases](https://github.com/Arlecchino745/infinity_translator/releases) 頁面下載最新版本。
2. 解壓縮下載的 zip 檔案。
3. 開啟 _internal 資料夾，複製 .env.example 並重新命名為 .env，然後填入 API 金鑰。
4. 執行 `infinity_translator.exe` 以啟動應用程式。

## 從原始程式碼開始（開發版）

1. 克隆專案並切換到專案資料夾：
```bash
# 從 GitHub 克隆專案程式碼到您的本地機器
git clone https://github.com/Arlecchino745/infinity_translator.git
# 切換到專案目錄
cd infinity_translator
```

2. 安裝依賴項：請注意選擇合適的 Python 版本。已知該專案在 Python 3.12 下可以正常運行。
```bash
# 建立一個名為 .venv 的虛擬環境
python -m venv .venv
# 啟動虛擬環境（適用於 Windows 系統）
.\.venv\Scripts\Activate
# 啟動虛擬環境（適用於 Linux&Mac）
source ./.venv/bin/activate
# 安裝專案所需的依賴庫
pip install -r requirements.txt
```

3. API 金鑰配置：請參閱專案資料夾中的 `.env.example` 檔案。 ⚙️
   - 將 `.env.example` 檔案複製到 `.env` 並填寫您的 API 金鑰。

4. （可選）根據 config 資料夾中 settings.json 中的註釋，建立您的個人化配置。 🛠️
   - 如果您需要自定義配置，請參閱 `config/settings.json.example` 檔案。

5. 完成上述步驟後運行：
```bash
# 啟動 Web 應用程式
python web_app.py
```
然後在瀏覽器的網址列中輸入 `localhost:8000` 或 `127.0.0.1:8000` 並確認。 🎉

### 應用程式設定配置（僅限從原始程式碼啟動）⚙️

該專案包含兩個配置文件：
- `config/settings.json` - 預設配置文件，不應修改
- `config/settings.json.example` - 配置模板文件供參考

如果您需要高級自定義配置（例如，添加新模型或服務提供商），請按照以下步驟操作：

1. 複製 `config/settings.json` 檔案並重新命名為 `config/settings.user.json`：
   ```bash
   # 複製預設配置文件到用戶定義的配置文件
   cp config/settings.json config/settings.user.json
   ```

2. 修改 `config/settings.user.json` 檔案中的配置
   - 根據您的需要編輯 `settings.user.json` 檔案，例如添加新模型或調整參數。

3. 應用程式將優先加載 settings.user.json，因此您的自定義配置不會被 Git 跟踪
   - 這避免了自定義配置被 Git 提交到遠程倉庫。

## 技術棧 💻

- 後端：FastAPI + Uvicorn
- 前端：Vue.js + Axios
- 翻譯：LangChain + OpenAI API
- 構建：PyInstaller

## 許可證 📄

該專案基於 MIT 許可證。

## AIGC 聲明

該專案由 AI 輔助完成。如有無意侵權，請聯繫作者。