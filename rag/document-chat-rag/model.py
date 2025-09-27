"""
Model类 - 处理业务逻辑和数据管理
包含PDF处理、LLM配置、向量索引等核心功能
"""

import os
import tempfile
import uuid
from typing import List, Dict, Any, Optional
from llama_index.readers.file import PDFReader
from llama_index.core import Settings, VectorStoreIndex, PromptTemplate
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.ollama import OllamaEmbedding


class DocumentChatModel:
    """文档聊天模型类，处理PDF文档和LLM交互的核心业务逻辑"""
    
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.file_cache: Dict[str, Any] = {}
        self.messages: List[Dict[str, str]] = []
        self._llm = None
        self._embed_model = None
        
    @property
    def llm(self):
        """懒加载LLM模型"""
        if self._llm is None:
            self._llm = DeepSeek(
                model="deepseek-chat", 
                temperature=0.1, 
                max_tokens=1000, 
                timeout=60, 
                max_retries=2
            )
        return self._llm
    
    @property
    def embed_model(self):
        """懒加载嵌入模型"""
        if self._embed_model is None:
            self._embed_model = OllamaEmbedding(
                model_name="nomic-embed-text",
                request_timeout=30,
                keep_alive="1m"
            )
        return self._embed_model
    
    def process_pdf_file(self, uploaded_file) -> tuple[bool, str, Optional[Any]]:
        """
        处理上传的PDF文件
        
        Args:
            uploaded_file: Streamlit上传的文件对象
            
        Returns:
            tuple: (success, message, query_engine)
        """
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                
                # 保存上传的文件
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                file_key = f"{self.session_id}-{uploaded_file.name}"
                
                # 检查缓存
                if file_key in self.file_cache:
                    return True, "文件已缓存，直接使用", self.file_cache[file_key]
                
                # 加载PDF文档
                if not os.path.exists(file_path):
                    return False, "无法找到上传的文件", None
                
                loader = PDFReader()
                docs = loader.load_data(file=file_path)
                
                # 设置嵌入模型
                Settings.embed_model = self.embed_model
                
                # 创建向量索引
                index = VectorStoreIndex.from_documents(docs, show_progress=True)
                
                # 设置LLM
                Settings.llm = self.llm
                
                # 创建查询引擎
                query_engine = index.as_query_engine(streaming=True)
                
                # 自定义提示模板
                qa_prompt_tmpl_str = (
                    "Context information is below.\n"
                    "---------------------\n"
                    "{context_str}\n"
                    "---------------------\n"
                    "Given the context information above I want you to think step by step to answer the query in a crisp manner, incase case you don't know the answer say 'I don't know!'.\n"
                    "Query: {query_str}\n"
                    "Answer: "
                )
                qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
                
                query_engine.update_prompts(
                    {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
                )
                
                # 缓存查询引擎
                self.file_cache[file_key] = query_engine
                
                return True, "文档处理完成", query_engine
                
        except Exception as e:
            return False, f"处理文件时发生错误: {e}", None
    
    def query_document(self, query_engine, prompt: str):
        """
        查询文档
        
        Args:
            query_engine: 查询引擎
            prompt: 用户查询
            
        Returns:
            流式响应生成器
        """
        if query_engine is None:
            return None
        
        try:
            streaming_response = query_engine.query(prompt)
            return streaming_response.response_gen
        except Exception as e:
            print(f"查询时发生错误: {e}")
            return None
    
    def add_message(self, role: str, content: str):
        """添加消息到聊天历史"""
        self.messages.append({"role": role, "content": content})
    
    def get_messages(self) -> List[Dict[str, str]]:
        """获取聊天历史"""
        return self.messages
    
    def clear_messages(self):
        """清空聊天历史"""
        self.messages = []
    
    def get_session_id(self) -> str:
        """获取会话ID"""
        return self.session_id
