from fastapi import FastAPI, Request, UploadFile, File, Form, Response
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from src.translator import DocumentTranslator
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from pathlib import Path
import json

# 创建FastAPI实例
app = FastAPI(title="Infinity Translator")

# 允许CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import settings functions
from config.settings import load_settings, save_settings

# Alias for compatibility
def get_settings():
    return load_settings()

# 挂载静态文件目录
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# 配置favicon
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(str(static_path / 'favicon.ico'))

# 设置模板目录
templates_path = Path(__file__).parent / "templates"
templates_path.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_path))

class TranslationRequest(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/providers")
async def get_providers():
    settings = get_settings()
    return JSONResponse(content={
        "active_provider": settings["active_provider"],
        "providers": settings["providers"]
    })

@app.get("/api/languages")
async def get_languages():
    settings = get_settings()
    return JSONResponse(content={
        "target_language": settings["target_language"],
        "language_list": settings["language_list"]
    })

@app.post("/api/set-provider")
async def set_provider(request: Request):
    data = await request.json()
    provider = data.get("provider")
    if not provider:
        return JSONResponse(status_code=400, content={"message": "Provider is required"})
    
    settings = get_settings()
    if provider not in settings["providers"]:
        return JSONResponse(status_code=400, content={"message": "Invalid provider"})
    
    settings["active_provider"] = provider
    save_settings(settings)
    
    return JSONResponse(content={"status": "success"})

@app.post("/api/set-language")
async def set_language(request: Request):
    data = await request.json()
    language = data.get("language")
    if not language:
        return JSONResponse(status_code=400, content={"message": "Language is required"})
    
    settings = get_settings()
    # 验证语言是否在语言列表中
    language_codes = [lang["code"] for lang in settings["language_list"]]
    if language not in language_codes:
        return JSONResponse(status_code=400, content={"message": "Invalid language"})
    
    settings["target_language"] = language
    save_settings(settings)
    
    return JSONResponse(content={"status": "success"})

@app.get("/translate-progress")
async def translation_progress():
    """获取翻译进度的 Server-Sent Events 端点"""
    from src.progress import TranslationProgress
    import asyncio
    import json
    
    progress = await TranslationProgress.get_instance()
    queue = await progress.subscribe()
    
    async def event_generator():
        try:
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
        except asyncio.CancelledError:
            await progress.unsubscribe(queue)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

@app.post("/translate")
async def translate(file: UploadFile = File(...), model_name: str = Form(...)):
    try:
        content = await file.read()
        text = content.decode('utf-8')
        
        # 获取设置并更新模型名称
        settings = get_settings()
        active_provider = settings["active_provider"]
        provider_info = settings["providers"][active_provider]
        provider_info["model_name"] = model_name
        
        # 保存更新后的设置
        save_settings(settings)
        
        # 获取翻译器实例并执行翻译
        translator = DocumentTranslator()
        content_bytes, output_filename = await translator.translate_document(text, file.filename)
        
        # 返回翻译后的文件
        headers = {
            'Content-Disposition': f'attachment; filename="{output_filename}"'
        }
        return Response(content_bytes, headers=headers, media_type='text/markdown')
        
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return JSONResponse(status_code=500, content={"message": f"Translation failed: {str(e)}"})

def start_web_server():
    """Start the web server (for standalone web mode)"""
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    start_web_server()