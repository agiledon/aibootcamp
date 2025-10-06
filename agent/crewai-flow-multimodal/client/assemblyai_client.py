"""
AssemblyAI客户端管理模块
负责音频转录功能
"""

import logging
import assemblyai as aai
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


class AssemblyAIClient:
    """AssemblyAI客户端管理类"""
    
    def __init__(self):
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化AssemblyAI客户端"""
        try:
            aai.settings.api_key = config.ASSEMBLYAI_API_KEY
            if not config.ASSEMBLYAI_API_KEY:
                raise ValueError("ASSEMBLYAI_API_KEY未配置")
            logger.info("✅ AssemblyAI客户端初始化成功")
        except Exception as e:
            logger.error(f"❌ AssemblyAI客户端初始化失败: {e}")
            logger.error("请检查ASSEMBLYAI_API_KEY配置")
            exit(1)
    
    def transcribe_audio_file(self, audio_file: str) -> str:
        """转录音频文件"""
        try:
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(audio_file)
            return transcript.text
        except Exception as e:
            logger.error(f"❌ 音频转录失败: {e}")
            logger.error("请检查AssemblyAI API密钥和网络连接")
            exit(1)

