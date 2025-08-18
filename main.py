from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from pathlib import Path
import json
from src.translator import translate_document

# 创建FastAPI实例
app = FastAPI(title="Infinity Translator")

# 读取设置文件
def get_settings():
    settings_path = Path(__file__).parent / "config" / "settings.json"
    with open(settings_path, 'r', encoding='utf-8') as f:
        return json.load(f)

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
    settings_path = Path(__file__).parent / "config" / "settings.json"
    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
    
    return JSONResponse(content={"status": "success"})

@app.post("/translate")
async def translate(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode('utf-8')
        translated_text = translate_document(text)
        return {"status": "success", "translated_text": translated_text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
