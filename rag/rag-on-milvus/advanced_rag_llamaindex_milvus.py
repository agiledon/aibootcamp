from dotenv import load_dotenv
load_dotenv()

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

# 将LLM和embed_model设置到LlamaIndex的全局Settings中
Settings.llm = OpenAI(
            model='deepseek-chat',
            temperature=0.1,
            max_tokens=1000,
            timeout=60,
            max_retries=2,
            # DeepSeek API配置
            api_base="https://api.deepseek.com/v1",  # DeepSeek API基础URL
        )
Settings.embed_model = OllamaEmbedding(
            model_name="nomic-embed-text",
            request_timeout=30,  # 减少嵌入请求超时时间
            keep_alive="1m"  # 减少保持连接时间
        )
