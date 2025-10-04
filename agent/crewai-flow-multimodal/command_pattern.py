"""
Command模式实现
负责处理用户输入的不同操作
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import Optional

from multimodal_rag_flow import MultimodalRAGFlow

logger = logging.getLogger(__name__)


class Command(ABC):
    """命令模式基类"""
    
    @abstractmethod
    def execute(self) -> str:
        """执行命令"""
        pass


class TextQueryCommand(Command):
    """文本查询命令"""
    
    def __init__(self, query: str):
        self.query = query
    
    def execute(self) -> str:
        """执行文本查询"""
        try:
            logger.info(f"Processing text query: {self.query}")
            rag_flow = MultimodalRAGFlow()
            
            # Manually execute the flow steps (same as original implementation)
            # This ensures the same behavior as before refactoring
            initial_state = rag_flow.transcribe_audio_if_needed(inputs={"query": self.query, "audio_file": None})
            
            # Manually execute the remaining steps since Flow isn't auto-executing
            search_state = rag_flow.search_knowledge_base(initial_state)
            final_state = rag_flow.generate_response(search_state)
            
            # Handle different result types
            result = final_state.final_response
            if hasattr(result, 'raw'):
                return result.raw
            elif hasattr(result, 'data'):
                return result.data
            else:
                return str(result)
        except Exception as e:
            logger.error(f"Error processing text query: {e}")
            return f"Sorry, I encountered an error while processing your query: {str(e)}"


class AudioQueryCommand(Command):
    """音频查询命令"""
    
    def __init__(self, audio_file: str):
        self.audio_file = audio_file
    
    def execute(self) -> str:
        """执行音频查询"""
        try:
            logger.info(f"Processing audio query from file: {self.audio_file}")
            rag_flow = MultimodalRAGFlow()
            
            # Manually execute the flow steps (same as original implementation)
            # This ensures the same behavior as before refactoring
            initial_state = rag_flow.transcribe_audio_if_needed(inputs={"query": "", "audio_file": self.audio_file})
            
            # Manually execute the remaining steps since Flow isn't auto-executing
            search_state = rag_flow.search_knowledge_base(initial_state)
            final_state = rag_flow.generate_response(search_state)
            
            # Clean up audio file
            try:
                os.unlink(self.audio_file)
                logger.info(f"Cleaned up audio file: {self.audio_file}")
            except Exception as cleanup_error:
                logger.warning(f"Failed to clean up audio file: {cleanup_error}")
            
            # Handle different result types
            result = final_state.final_response
            if hasattr(result, 'raw'):
                return result.raw
            elif hasattr(result, 'data'):
                return result.data
            else:
                return str(result)
        except Exception as e:
            logger.error(f"Error processing audio query: {e}")
            # Still try to clean up audio file
            try:
                os.unlink(self.audio_file)
            except:
                pass
            return f"Sorry, I encountered an error while processing your audio: {str(e)}"


class SystemSetupCommand(Command):
    """系统设置命令"""
    
    def execute(self) -> str:
        """执行系统设置"""
        try:
            logger.info("Setting up system...")
            from data_ingestion_flow import DataIngestionFlow
            
            # Use the DataIngestionFlow to set up the system
            ingestion_flow = DataIngestionFlow()
            initial_state = ingestion_flow.discover_files()
            
            # Manually execute the flow steps
            setup_state = ingestion_flow.setup_vector_database(initial_state)
            process_state = ingestion_flow.process_multimodal_data(setup_state)
            
            if len(process_state.chunks) > 0:
                embed_state = ingestion_flow.generate_embeddings_flow(process_state)
                final_state = ingestion_flow.store_in_vector_database(embed_state)
                return "✅ System setup completed!"
            else:
                return "⚠️ No data to process"
                
        except Exception as e:
            logger.error(f"Error setting up system: {e}")
            return f"❌ System setup failed: {str(e)}"


class ExitCommand(Command):
    """退出命令"""
    
    def execute(self) -> str:
        """执行退出操作"""
        return "EXIT"
