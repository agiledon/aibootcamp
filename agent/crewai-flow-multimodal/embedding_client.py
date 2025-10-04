"""
嵌入模型客户端管理模块
负责Ollama嵌入模型的初始化和配置
"""

import logging
from llama_index.embeddings.ollama import OllamaEmbedding
import config

logger = logging.getLogger(__name__)


class EmbeddingClient:
    """Ollama嵌入模型客户端管理类"""
    
    def __init__(self):
        self.embed_model = None
        self._initialize_embed_model()
    
    def _initialize_embed_model(self):
        """初始化Ollama嵌入模型"""
        try:
            self.embed_model = OllamaEmbedding(
                model_name=config.EMBEDDING_MODEL,
                request_timeout=60,
                keep_alive="5m"
            )
            logger.info(f"✅ Ollama嵌入模型初始化成功: {config.EMBEDDING_MODEL}")
        except Exception as e:
            logger.error(f"❌ Ollama嵌入模型初始化失败: {e}")
            logger.error("请确保Ollama服务正在运行，且模型nomic-embed-text:latest已安装")
            logger.error("安装命令: ollama pull nomic-embed-text:latest")
            exit(1)
    
    def get_embeddings(self, texts: list) -> list:
        """
        获取文本嵌入向量，使用Ollama本地模型
        """
        try:
            embeddings = []
            for text in texts:
                # 检查文本是否为空或只包含空白字符
                if not text or not text.strip():
                    logger.warning(f"跳过空文本，使用零向量代替")
                    # 使用零向量代替空文本的嵌入
                    embedding = [0.0] * config.EMBEDDING_DIM
                else:
                    embedding = self.embed_model.get_text_embedding(text.strip())
                embeddings.append(embedding)
            return embeddings
        except Exception as e:
            logger.error(f"❌ Ollama嵌入失败: {e}")
            logger.error("请检查Ollama服务状态和模型可用性")
            exit(1)
    
    def get_embed_model(self):
        """获取嵌入模型实例"""
        return self.embed_model
    
    def get_embedding_dimension(self):
        """获取嵌入维度"""
        return config.EMBEDDING_DIM

