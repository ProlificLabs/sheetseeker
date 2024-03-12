from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
