import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# LLM Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
LLM_API_BASE = os.getenv("LLM_API_BASE", "https://api.deepseek.com")

# Milvus Configuration
MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = int(os.getenv("MILVUS_PORT", "19530"))
COLLECTION_NAME = os.getenv("MILVUS_COLLECTION_NAME", "multimodal_rag")

# Embeddings Configuration
# 使用Ollama本地嵌入模型
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text:latest")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIMENSION", "768"))  # nomic-embed-text的维度是768
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Data Directory
DATA_DIR = "data" 