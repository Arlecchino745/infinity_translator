# Infinity Translator

Infinity Translatorは、大規模言語モデルを利用した長文翻訳ソフトウェアであり、モダンで美しいUIインターフェースを備えています。大規模なドキュメントを適切にチャンク化および前処理し、複数の言語に翻訳できます。
![image](https://github.com/Arlecchino745/infinity_translator/blob/main/docs/img/screenshot2.png)
![image](https://github.com/Arlecchino745/infinity_translator/blob/main/docs/img/screenshot.png)

## 特徴 ✨

- ドキュメントの長さに制限なく、大規模なドキュメントの翻訳をサポート 📄
- Markdownドキュメントを前処理して、翻訳の見栄えを最適化 🎨
- 翻訳の進捗状況をリアルタイムで表示し、翻訳結果を自動的に保存 ⏱️

## クイックスタート 🚀

1. プロジェクトをクローンし、プロジェクトフォルダに切り替えます。
```bash
# GitHubからローカルマシンにプロジェクトコードをクローンします
git clone https://github.com/Arlecchino745/infinity_translator.git
# プロジェクトディレクトリに切り替えます
cd infinity_translator
```

2. 依存関係をインストールします。適切なPythonバージョンを選択するように注意してください。このプロジェクトは、Python 3.12で正常に動作することが確認されています。
```bash
# .venvという名前の仮想環境を作成します
python -m venv .venv
# 仮想環境をアクティブ化します（Windowsシステムの場合）
.\.venv\Scripts\Activate
# 仮想環境をアクティブ化します（Linux＆Macの場合）
source ./.venv/bin/activate
# プロジェクトに必要な依存ライブラリをインストールします
pip install -r requirements.txt
```

3. APIキーの構成：プロジェクトフォルダ内の`.env.example`ファイルを参照してください。 ⚙️
   - `.env.example`ファイルを`.env`にコピーし、APIキーを入力します。

4. （オプション）configフォルダ内のsettings.jsonのコメントに従って、パーソナライズされた構成を作成します。 🛠️
   - カスタム構成が必要な場合は、`config/settings.json.example`ファイルを参照してください。

5. 上記の手順を完了した後、実行します。
```bash
# Webアプリケーションを起動します
python web_app.py
```
次に、ブラウザのアドレスバーに`localhost:8000`または`127.0.0.1:8000`を入力して確認します。 🎉

### アプリケーション設定の構成 ⚙️

プロジェクトには2つの構成ファイルがあります：
- `config/settings.json` - デフォルトの構成ファイル。変更しないでください
- `config/settings.json.example` - 構成テンプレートファイル供参考

高度なカスタム構成（例：新しいモデルやサービスプロバイダーの追加）が必要な場合は、以下の手順に従ってください：

1. `config/settings.json`ファイルをコピーし、`config/settings.user.json`に名前を変更します：
   ```bash
   # デフォルトの構成ファイルをユーザー定義の構成ファイルにコピーします
   cp config/settings.json config/settings.user.json
   ```

2. `config/settings.user.json`ファイル内の構成を変更します
   - 必要に応じて`settings.user.json`ファイルを編集してください（例：新しいモデルの追加やパラメータの調整）。

3. アプリケーションはsettings.user.jsonを優先的に読み込むため、カスタム構成はGitで追跡されません
   - これにより、カスタム構成がGitでリモートリポジトリにコミットされるのを防ぎます。

## 技術スタック 💻

- バックエンド：FastAPI + Uvicorn
- フロントエンド：Vue.js + Axios
- デスクトップ：Flet（Flutterベース）
- 翻訳：LangChain + OpenAI API
- ビルド：PyInstaller + Fletパッケージングツール

## ライセンス 📄

プロジェクトはMITライセンスの下でライセンスされています。

## AIGCステートメント

このプロジェクトはAIによって支援されています。誤って侵害が発生した場合は、著者にお問い合わせください。