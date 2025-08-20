# Infinity Translator

Infinity Translator 是一个基于 LangChain 的长文本翻译工具，可以将大型文档翻译成多种语言。它支持网页和桌面两种运行模式，现在使用 Flet 作为桌面应用框架。

## 特性

- 支持大型文档翻译（最大支持10万字）
- 支持多种翻译提供商（OpenRouter、SiliconFlow）
- 提供网页和桌面两种使用方式
- 支持拖拽上传文件
- 实时显示翻译进度
- 自动保存翻译结果

## 新项目结构

```
infinity_translator/
├── app/                    # 应用核心代码
│   ├── __init__.py
│   ├── desktop_app.py      # 桌面应用入口点
│   ├── core/               # 核心功能模块
│   │   ├── __init__.py
│   │   └── server_manager.py  # 服务器管理
│   ├── ui/                 # 用户界面
│   │   ├── __init__.py
│   │   ├── desktop_app.py  # 桌面应用入口
│   │   └── main_window.py  # 主窗口界面
│   ├── config/             # 配置管理
│   └── utils/              # 工具函数
├── src/                    # 翻译核心模块
│   ├── __init__.py
│   ├── translator.py       # 翻译器核心
│   ├── progress.py         # 进度跟踪
│   └── output.py           # 输出处理
├── config/                 # 配置文件
│   ├── config.py           # 环境配置
│   ├── settings.py         # 应用设置加载逻辑
│   ├── settings.json       # 默认应用设置 (会被版本控制)
│   └── settings.json.example  # 应用设置模板 (供用户自定义)
├── static/                 # 静态资源
├── templates/              # HTML模板
├── scripts/                # 构建和辅助脚本
│   ├── build_flet.py       # Flet构建脚本
│   ├── build_desktop.py    # 原PySide6构建脚本
│   ├── build.bat           # Windows构建脚本
│   └── ...                 # 其他脚本文件
├── tools/                  # 工具模块
│   └── error_handler.py    # 错误处理模块
├── docs/                   # 文档
│   ├── README_DESKTOP.md   # 桌面版说明
│   └── ...                 # 其他文档
├── requirements.txt        # 依赖列表
├── web_app.py              # FastAPI应用
└── readme.md              # 项目说明
```

## 安装

1. 克隆项目：
   ```
   git clone <repository-url>
   cd infinity_translator
   ```

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

## 使用方式

### 网页模式

```
python web_app.py
```

然后在浏览器中打开 `http://localhost:8000`

### 桌面模式

```
python app/desktop_app.py
```

## 构建桌面应用

```
python scripts/build_flet.py
```

构建后的应用将位于 `dist/` 目录中。

## 配置

### API 密钥配置

在项目根目录创建 `.env` 文件，添加以下配置：

```
# 支持的提供商: openrouter, siliconflow

# OpenRouter 配置
OPENROUTER_API_KEY=your_openrouter_api_key

# SiliconFlow 配置
SILICONFLOW_API_KEY=your_siliconflow_api_key
```

### 应用设置配置

项目包含两个配置文件：
- [config/settings.json](file:///e:/HelloWorld/infinity_translator/config/settings.json) - 默认配置文件，用于版本控制，不应被修改
- [config/settings.json.example](file:///e:/HelloWorld/infinity_translator/config/settings.json.example) - 配置模板文件，供参考

如果需要自定义配置（例如添加新的模型或服务商），请按照以下步骤操作：

1. 复制 [config/settings.json](file:///e:/HelloWorld/infinity_translator/config/settings.json) 文件并重命名为 [config/settings.user.json](file:///e:/HelloWorld/infinity_translator/config/settings.json)
2. 修改 [config/settings.user.json](file:///e:/HelloWorld/infinity_translator/config/settings.json) 文件中的配置
3. 应用会优先加载 [settings.user.json](file:///e:/HelloWorld/infinity_translator/config/settings.json)，这样您的自定义配置就不会被 Git 跟踪

注意：不要直接修改 [config/settings.json](file:///e:/HelloWorld/infinity_translator/config/settings.json) 文件，因为这会导致 Git 冲突。

## 技术栈

- 后端：FastAPI + Uvicorn
- 前端：Vue.js + Axios
- 桌面：Flet (基于 Flutter)
- 翻译：LangChain + OpenAI API
- 构建：PyInstaller + Flet打包工具

## 许可证

MIT