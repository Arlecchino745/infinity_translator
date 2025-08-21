# Infinity Translator

Infinity Translator 是一款利用大语言模型进行长文本翻译的软件，拥有现代且美观的 UI 界面。它可以适当地对大型文档进行分块和预处理，并将其翻译成多种语言。
![image](https://github.com/Arlecchino745/infinity_translator/blob/main/img/screenshot2.png)
![image](https://github.com/Arlecchino745/infinity_translator/blob/main/img/screenshot.png)

## 特性

- 支持大型文档翻译，无文档长度限制
- 预处理 Markdown 文档以优化翻译的视觉效果
- 实时显示翻译进度并自动保存翻译结果

## 快速开始

1. 克隆项目并切换到项目文件夹：
```bash
# 从 GitHub 克隆项目代码到您的本地机器
git clone https://github.com/Arlecchino745/infinity_translator.git
# 切换到项目目录
cd infinity_translator
```

2. 安装依赖：请注意选择合适的 Python 版本。已知该项目在 Python 3.12 下运行正常。
```bash
# 创建一个名为 .venv 的虚拟环境
python -m venv .venv
# 激活虚拟环境（对于 Windows 系统）
.\.venv\Scripts\Activate
# 激活虚拟环境（对于 Linux&Mac）
source ./.venv/bin/activate
# 安装项目所需的依赖库
pip install -r requirements.txt
```

3. API 密钥配置：请参考项目文件夹中的 `.env.example` 文件。
   - 复制 `.env.example` 文件到 `.env` 并填写您的 API 密钥。

4. （可选）根据 config 文件夹中 settings.json 的注释创建您的个性化配置。
   - 如果您需要自定义配置，请参考 `config/settings.json.example` 文件。

5. 完成以上步骤后运行：
```bash
# 启动 Web 应用程序
python web_app.py
```
然后在浏览器的地址栏中输入 `localhost:8000` 或 `127.0.0.1:8000` 并确认。

### 应用程序设置配置

该项目包含两个配置文件：
- `config/settings.json` - 默认配置文件，不应修改
- `config/settings.json.example` - 用于参考的配置模板文件

如果您需要高级自定义配置（例如，添加新模型或服务提供商），请按照以下步骤操作：

1. 复制 `config/settings.json` 文件并将其重命名为 `config/settings.user.json`：
   ```bash
   # 将默认配置文件复制到用户定义的配置文件
   cp config/settings.json config/settings.user.json
   ```

2. 修改 `config/settings.user.json` 文件中的配置
   - 根据您的需求编辑 `settings.user.json` 文件，例如添加新模型或调整参数。

3. 应用程序将优先加载 settings.user.json，因此您的自定义配置不会被 Git 跟踪
   - 这避免了自定义配置被 Git 提交到远程仓库。

## 技术栈

- 后端: FastAPI + Uvicorn
- 前端: Vue.js + Axios
- 桌面端: Flet (基于 Flutter)
- 翻译: LangChain + OpenAI API
- 构建: PyInstaller + Flet 打包工具

## 许可证

该项目采用 MIT 许可证。

## AIGC声明

本项目含有人工智能辅助生成的内容。如有无意侵犯了您的权益，请联系作者。
