# Infinity Translator

Infinity Translator 是一款利用大型語言模型進行長文本翻譯的軟體，具有現代且美觀的 UI 介面。它可以適當地分塊和預處理大型文檔，並將它們翻譯成多種語言。
![image](https://github.com/Arlecchino745/infinity_translator/blob/main/img/screenshot2.png)
![image](https://github.com/Arlecchino745/infinity_translator/blob/main/img/screenshot.png)

## 功能

- 支援大型文檔翻譯，沒有文檔長度限制
- 預處理 Markdown 文檔，以優化翻譯的視覺外觀
- 實時顯示翻譯進度並自動保存翻譯結果

## 快速開始

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

3. API 金鑰配置：請參閱專案資料夾中的 `.env.example` 檔案。
   - 將 `.env.example` 檔案複製到 `.env` 並填寫您的 API 金鑰。

4. （可選）根據 config 資料夾中 settings.json 中的註釋，建立您的個人化配置。
   - 如果您需要自定義配置，請參閱 `config/settings.json.example` 檔案。

5. 完成上述步驟後運行：
```bash
# 啟動 Web 應用程式
python web_app.py
```
然後在瀏覽器的網址列中輸入 `localhost:8000` 或 `127.0.0.1:8000` 並確認。

### 應用程式設定配置

該專案包含兩個配置文件：
- `config/settings.json` - 預設配置文件，不應修改
- `config/settings.json.example` - 參考用的配置範本檔案

如果您需要進階的自定義配置（例如，新增模型或服務提供商），請按照以下步驟操作：

1. 複製 `config/settings.json` 檔案並將其重新命名為 `config/settings.user.json`：
   ```bash
   # 將預設配置文件複製到用戶定義的配置文件
   cp config/settings.json config/settings.user.json
   ```

2. 修改 `config/settings.user.json` 檔案中的配置
   - 根據您的需求編輯 `settings.user.json` 檔案，例如新增模型或調整參數。

3. 應用程式將優先載入 settings.user.json，因此您的自定義配置不會被 Git 追蹤
   - 這可以避免自定義配置被 Git 提交到遠端儲存庫。

## 技術堆疊

- 後端：FastAPI + Uvicorn
- 前端：Vue.js + Axios
- 桌面：Flet (基於 Flutter)
- 翻譯：LangChain + OpenAI API
- 建置：PyInstaller + Flet 打包工具

## 許可證

該專案採用 MIT 許可證。
