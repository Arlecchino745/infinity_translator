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
import sys
import os

# Function to get the correct path for resources, works for both development and PyInstaller
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running in development mode
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Create FastAPI instance
app = FastAPI(title="Infinity Translator")

# Allow CORS
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

# Get paths for static and templates directories
static_dir = get_resource_path("static")
templates_dir = get_resource_path("templates")

# Ensure directories exist
if not os.path.exists(static_dir):
    print(f"Warning: Static directory not found at {static_dir}")
if not os.path.exists(templates_dir):
    print(f"Warning: Templates directory not found at {templates_dir}")

# Mount static files directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Setup templates
templates = Jinja2Templates(directory=templates_dir)

# Load settings
settings = get_settings()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "settings": settings})

@app.get("/api/providers")
async def get_providers():
    return {"providers": settings["providers"], "active_provider": settings["active_provider"]}

@app.get("/api/languages")
async def get_languages():
    return {"language_list": settings["language_list"], "target_language": settings.get("target_language", "zh-Hans")}

@app.post("/api/settings")
async def update_settings(new_settings: dict):
    # Update model information
    active_provider = new_settings.get("active_provider", settings["active_provider"])
    model_name = new_settings.get("model_name")
    
    if model_name:
        settings["providers"][active_provider]["model_name"] = model_name
    
    # Update target language
    target_language = new_settings.get("target_language")
    if target_language:
        settings["target_language"] = target_language
    
    # Save settings
    save_settings(settings)
    return {"message": "Settings updated successfully"}

@app.post("/api/set-language")
async def set_language(request: Request):
    data = await request.json()
    language = data.get("language")
    if not language:
        return JSONResponse(status_code=400, content={"message": "Language is required"})
    
    # Verify that the language is in the language list
    language_codes = [lang["code"] for lang in settings["language_list"]]
    if language not in language_codes:
        return JSONResponse(status_code=400, content={"message": "Invalid language"})
    
    settings["target_language"] = language
    save_settings(settings)
    
    return JSONResponse(content={"status": "success"})

# Import TranslationProgress
from src.progress import TranslationProgress

@app.get("/translate-progress")
async def translation_progress():
    """Server-Sent Events endpoint for getting translation progress"""
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
        
        # Get settings and update model name
        settings = get_settings()
        active_provider = settings["active_provider"]
        provider_info = settings["providers"][active_provider]
        provider_info["model_name"] = model_name
        
        # Save updated settings
        save_settings(settings)
        
        # Get translator instance and perform translation
        translator = DocumentTranslator()
        content_bytes, output_filename = await translator.translate_document(text, file.filename)
        
        # Return translated file
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