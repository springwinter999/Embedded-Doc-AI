import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
EMBEDDING_MODEL = "BAAI/bge-base-zh-v1.5"
CHAT_MODEL = "deepseek-chat"

CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "conversations.db")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 5
