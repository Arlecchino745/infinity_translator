import os
from dotenv import load_dotenv

load_dotenv()

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not SILICONFLOW_API_KEY and not OPENROUTER_API_KEY:
    print("Please configure the API key correctly in the .env file."); exit(1)
