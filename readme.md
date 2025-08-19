# Infinite Translator

基于langchain的长文本翻译工具，具有简洁美观的网页GUI界面。
网页LOGO来自[https://icon-sets.iconify.design/](https://icon-sets.iconify.design/)。

![image](https://github.com/Arlecchino745/infinity_translator/blob/main/img/screenshot2.png)

![image](https://github.com/Arlecchino745/infinity_translator/blob/main/img/screenshot.png)

## 使用方法
若需使用，请:
1. 克隆仓库(git clone)，并安装依赖。这需要您的计算机上安装了Python。个人建议不要使用最新或太老的python版本。在克隆仓库后，依次运行(Windows系统的示例，其他系统类似)：
```powershell
cd "infinity_translator"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
2. 将.env.example复制并重命名为.env，然后填写好您的API密钥。这可以通过计算机的记事本或VS Code等编辑器完成。
   如果您没有API key,您可以在.env.example中查看如何获取。
3. 此后运行main.py，在您的浏览器中输入`localhost:8000`或`127.0.0.1:8000`即可。
4. 尚未完成完整的应用程序，目前依赖网页端。

## 注意
注意，目前翻译的效果很差，很有可能出现排版混乱、内容缺失等各种各样的bug。
这只是一个远远没有完成的项目，目前还无法在实际工作中帮助到您。