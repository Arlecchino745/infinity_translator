# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Define data files to include
added_files = [
    # Templates directory - make sure it's copied to the correct location
    ('templates', 'templates'),
    # Static assets - make sure they're copied to the correct location
    ('static', 'static'),
    # Configuration files
    ('.env.example', '.'),
    ('config/settings.json', 'config'),
    ('config/settings.json.example', 'config'),
    # Include all Python modules in src and config
    ('src', 'src'),
    ('config', 'config'),
]

# Print the added files for debugging
print("Files to be added to the package:")
for src, dest in added_files:
    print(f"  {src} -> {dest}")

a = Analysis(
    ['debug_wrapper.py'],  # Debug wrapper as main script
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'langchain_openai',
        'langchain_community',
        'langchain_core',
        'langchain_text_splitters',
        'fastapi',
        'uvicorn',
        'jinja2',
        'python-multipart',
        'tiktoken',
        'tenacity',
        'uvicorn.logging',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'uvicorn.lifespan.off',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.protocols.websockets.websockets_impl',
        'uvicorn.protocols.websockets.wsproto_impl',
        'starlette',
        'starlette.routing',
        'starlette.middleware',
        'starlette.middleware.cors',
        'starlette.staticfiles',
        'starlette.templating',
        'starlette.responses',
        'pydantic',
        'asyncio',
        'psutil',
        'dotenv',
        'python_dotenv',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='infinity_translator',
    debug=True,  # Enable debug mode to see error messages
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Keep console window open to see error messages
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='static/favicon.ico',  # Use favicon.ico as the icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='infinity_translator_v2',  # Changed output directory name
)