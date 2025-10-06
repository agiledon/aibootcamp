"""
LLM客户端管理模块
负责DeepSeek LLM客户端的初始化和配置
"""

import logging
import openai
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


class LLMClient:
    """DeepSeek LLM客户端管理类"""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化LLM客户端"""
        try:
            self.client = openai.OpenAI(
                api_key=config.DEEPSEEK_API_KEY,
                base_url=config.LLM_API_BASE
            )
            logger.info(f"✅ DeepSeek LLM客户端初始化成功: {config.LLM_MODEL}")
        except Exception as e:
            logger.error(f"❌ DeepSeek LLM客户端初始化失败: {e}")
            logger.error("请检查DEEPSEEK_API_KEY配置和网络连接")
            exit(1)
    
    def get_client(self):
        """获取LLM客户端实例"""
        return self.client
    
    def get_model_name(self):
        """获取模型名称"""
        return config.LLM_MODEL

