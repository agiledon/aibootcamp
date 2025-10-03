"""
配置文件 - 统一管理LlamaIndex的全局设置
确保整个程序中使用统一的LLM和嵌入模型配置
"""

import logging
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

logger = logging.getLogger(__name__)


def initialize_settings():
    """
    初始化LlamaIndex的全局设置
    确保整个程序使用统一的LLM和嵌入模型配置
    """
    try:
        logger.info("开始初始化LlamaIndex全局设置...")
        
        # 1. 初始化DeepSeek语言模型
        logger.info("正在初始化DeepSeek语言模型...")
        llm = DeepSeek(
            model="deepseek-chat",
            temperature=0.1,
            max_tokens=1000,
            timeout=120,
            max_retries=3
        )
        
        # 2. 初始化Ollama嵌入模型
        logger.info("正在初始化Ollama嵌入模型...")
        embed_model = OllamaEmbedding(
            model_name="nomic-embed-text",
            request_timeout=60,
            keep_alive="5m"
        )
        
        # 3. 设置全局Settings
        Settings.llm = llm
        Settings.embed_model = embed_model
        
        # 4. 验证配置
        logger.info("正在验证配置...")
        
        # 测试LLM
        try:
            test_response = llm.complete("Hello")
            logger.info("✅ LLM配置验证成功")
        except Exception as e:
            logger.error(f"❌ LLM配置验证失败: {e}")
            raise
        
        # 测试嵌入模型
        try:
            test_embedding = embed_model.get_text_embedding("test")
            logger.info(f"✅ 嵌入模型配置验证成功，维度: {len(test_embedding)}")
        except Exception as e:
            logger.error(f"❌ 嵌入模型配置验证失败: {e}")
            raise
        
        logger.info("✅ LlamaIndex全局设置初始化完成")
        logger.info(f"   - LLM: {llm.model}")
        logger.info(f"   - 嵌入模型: {embed_model.model_name}")
        logger.info(f"   - 嵌入维度: {len(test_embedding)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ LlamaIndex全局设置初始化失败: {e}")
        return False


def get_llm():
    """
    获取全局LLM实例
    """
    return Settings.llm


def get_embed_model():
    """
    获取全局嵌入模型实例
    """
    return Settings.embed_model


def verify_settings():
    """
    验证Settings是否正确配置
    """
    try:
        llm = Settings.llm
        embed_model = Settings.embed_model
        
        if llm is None:
            logger.error("❌ LLM未配置")
            return False
            
        if embed_model is None:
            logger.error("❌ 嵌入模型未配置")
            return False
        
        # 测试嵌入模型维度
        test_embedding = embed_model.get_text_embedding("test")
        logger.info(f"✅ Settings验证通过 - LLM: {llm.model}, 嵌入模型: {embed_model.model_name}, 维度: {len(test_embedding)}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Settings验证失败: {e}")
        return False


# 在模块导入时自动初始化设置
if __name__ != "__main__":
    # 只有在作为模块导入时才自动初始化
    initialize_settings()
