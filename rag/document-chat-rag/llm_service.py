"""
LLM和嵌入模型服务模块
负责管理语言模型和嵌入模型的创建和配置
"""

import logging
from typing import Optional, Any
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

logger = logging.getLogger(__name__)


class LLMService:
    """LLM服务类，负责语言模型的创建和管理"""
    
    def __init__(self):
        """初始化LLM服务"""
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """初始化语言模型"""
        try:
            logger.info("正在初始化DeepSeek语言模型...")
            self.llm = DeepSeek(
                model="deepseek-chat",
                temperature=0.1,
                max_tokens=1000,
                timeout=120,
                max_retries=3
            )
            
            # 设置全局LLM
            Settings.llm = self.llm
            logger.info("✅ DeepSeek语言模型初始化成功")
            
        except Exception as e:
            logger.error(f"❌ DeepSeek语言模型初始化失败: {e}")
            self.llm = None
    
    def get_llm(self) -> Optional[DeepSeek]:
        """获取语言模型实例"""
        return self.llm
    
    def is_available(self) -> bool:
        """检查LLM是否可用"""
        return self.llm is not None


class EmbeddingService:
    """嵌入模型服务类，负责嵌入模型的创建和管理"""
    
    def __init__(self):
        """初始化嵌入模型服务"""
        self.embed_model = None
        self._initialize_embed_model()
    
    def _initialize_embed_model(self):
        """初始化嵌入模型"""
        try:
            logger.info("正在初始化Ollama嵌入模型...")
            self.embed_model = OllamaEmbedding(
                model_name="nomic-embed-text",
                request_timeout=60,
                keep_alive="5m"
            )
            
            # 设置全局嵌入模型
            Settings.embed_model = self.embed_model
            
            # 测试嵌入模型是否可用
            test_embedding = self.embed_model.get_text_embedding("test")
            if test_embedding:
                logger.info("✅ Ollama嵌入模型初始化成功")
            else:
                logger.error("❌ Ollama嵌入模型测试失败")
                self.embed_model = None
                
        except Exception as e:
            logger.error(f"❌ Ollama嵌入模型初始化失败: {e}")
            self.embed_model = None
    
    def get_embed_model(self) -> Optional[OllamaEmbedding]:
        """获取嵌入模型实例"""
        return self.embed_model
    
    def is_available(self) -> bool:
        """检查嵌入模型是否可用"""
        return self.embed_model is not None


class ModelService:
    """模型服务管理器，统一管理LLM和嵌入模型"""
    
    def __init__(self):
        """初始化模型服务管理器"""
        self.llm_service = LLMService()
        self.embedding_service = EmbeddingService()
        
        # 检查服务状态
        self._check_services_status()
    
    def _check_services_status(self):
        """检查所有服务的状态"""
        llm_status = self.llm_service.is_available()
        embedding_status = self.embedding_service.is_available()
        
        logger.info(f"模型服务状态 - LLM: {'✅' if llm_status else '❌'}, 嵌入模型: {'✅' if embedding_status else '❌'}")
        
        if not llm_status:
            logger.warning("⚠️ LLM服务不可用，可能影响查询功能")
        
        if not embedding_status:
            logger.warning("⚠️ 嵌入模型服务不可用，可能影响文档索引功能")
    
    def get_llm(self) -> Optional[DeepSeek]:
        """获取语言模型"""
        return self.llm_service.get_llm()
    
    def get_embed_model(self) -> Optional[OllamaEmbedding]:
        """获取嵌入模型"""
        return self.embedding_service.get_embed_model()
    
    def is_llm_available(self) -> bool:
        """检查LLM是否可用"""
        return self.llm_service.is_available()
    
    def is_embedding_available(self) -> bool:
        """检查嵌入模型是否可用"""
        return self.embedding_service.is_available()
    
    def is_fully_available(self) -> bool:
        """检查所有服务是否都可用"""
        return self.is_llm_available() and self.is_embedding_available()
    
    def get_status_info(self) -> dict:
        """获取服务状态信息"""
        return {
            "llm_available": self.is_llm_available(),
            "embedding_available": self.is_embedding_available(),
            "fully_available": self.is_fully_available()
        }
