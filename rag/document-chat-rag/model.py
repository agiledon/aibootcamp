"""
Model类 - 处理业务逻辑和数据管理
包含PDF处理、LLM配置、向量索引等核心功能
"""

import os
import tempfile
import uuid
from typing import List, Dict, Any, Optional
from llama_index.readers.file import PDFReader, DocxReader, MarkdownReader, CSVReader
from llama_index.core import Settings, VectorStoreIndex, PromptTemplate
from llama_index.core.readers import SimpleDirectoryReader
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
    
    def _get_file_loader(self, file_extension: str):
        """
        根据文件扩展名获取对应的加载器
        
        Args:
            file_extension: 文件扩展名
            
        Returns:
            对应的文档加载器
        """
        extension_mapping = {
            '.pdf': PDFReader(),
            '.docx': DocxReader(),
            '.doc': DocxReader(),
            '.md': MarkdownReader(),
            '.markdown': MarkdownReader(),
            '.csv': CSVReader(),
            '.txt': None,  # 使用SimpleDirectoryReader处理txt文件
        }
        
        return extension_mapping.get(file_extension.lower())
    
    def _load_document(self, file_path: str, file_extension: str):
        """
        根据文件类型加载文档
        
        Args:
            file_path: 文件路径
            file_extension: 文件扩展名
            
        Returns:
            加载的文档列表
        """
        loader = self._get_file_loader(file_extension)
        
        if loader is None:
            # 对于txt文件或其他未明确支持的文件，使用SimpleDirectoryReader
            reader = SimpleDirectoryReader(
                input_files=[file_path],
                required_exts=[file_extension]
            )
            return reader.load_data()
        else:
            # 使用专门的加载器
            return loader.load_data(file=file_path)
    
    def process_document_file(self, uploaded_file) -> tuple[bool, str, Optional[Any]]:
        """
        处理上传的文档文件（支持PDF、Word、Markdown、CSV、TXT）
        
        Args:
            uploaded_file: Streamlit上传的文件对象
            
        Returns:
            tuple: (success, message, query_engine)
        """
        try:
            # 获取文件扩展名
            file_extension = os.path.splitext(uploaded_file.name)[1]
            supported_extensions = ['.pdf', '.docx', '.doc', '.md', '.markdown', '.csv', '.txt']
            
            if file_extension.lower() not in supported_extensions:
                return False, f"不支持的文件类型: {file_extension}。支持的类型: {', '.join(supported_extensions)}", None
            
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                
                # 保存上传的文件
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                file_key = f"{self.session_id}-{uploaded_file.name}"
                
                # 检查缓存
                if file_key in self.file_cache:
                    return True, "文件已缓存，直接使用", self.file_cache[file_key]
                
                # 检查文件是否存在
                if not os.path.exists(file_path):
                    return False, "无法找到上传的文件", None
                
                # 根据文件类型加载文档
                docs = self._load_document(file_path, file_extension)
                
                if not docs:
                    return False, "文档加载失败，请检查文件格式", None
                
                # 记录文档加载信息
                total_chars = sum(len(doc.text) for doc in docs)
                print(f"成功加载 {len(docs)} 个文档片段，总字符数: {total_chars}")
                
                # 设置嵌入模型
                Settings.embed_model = self.embed_model
                
                # 创建向量索引，设置合适的文档分割参数
                from llama_index.core.node_parser import SentenceSplitter
                
                # 设置文档分割器，避免过度分割
                text_splitter = SentenceSplitter(
                    chunk_size=1024,
                    chunk_overlap=200,
                    separator=" "
                )
                
                index = VectorStoreIndex.from_documents(
                    docs, 
                    transformations=[text_splitter],
                    show_progress=True
                )
                
                # 设置LLM
                Settings.llm = self.llm
                
                # 创建查询引擎
                query_engine = index.as_query_engine(streaming=True)
                
                # 自定义提示模板
                qa_prompt_tmpl_str = (
                    "你是一个专业的文档问答助手。请基于以下提供的上下文信息来回答用户的问题。\n\n"
                    "上下文信息：\n"
                    "---------------------\n"
                    "{context_str}\n"
                    "---------------------\n\n"
                    "请按照以下要求回答问题：\n"
                    "1. 仔细阅读并理解上下文信息\n"
                    "2. 基于上下文信息提供准确、详细的回答\n"
                    "3. 如果上下文信息中包含相关数据、代码或具体细节，请准确引用\n"
                    "4. 如果上下文信息不足以回答问题，请明确说明\"根据提供的文档，我无法找到相关信息\"\n"
                    "5. 回答要结构清晰，逻辑性强\n"
                    "6. 如果问题涉及多个方面，请分别说明\n\n"
                    "用户问题：{query_str}\n\n"
                    "回答："
                )
                qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
                
                query_engine.update_prompts(
                    {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
                )
                
                # 缓存查询引擎
                self.file_cache[file_key] = query_engine
                
                file_type_name = {
                    '.pdf': 'PDF',
                    '.docx': 'Word',
                    '.doc': 'Word',
                    '.md': 'Markdown',
                    '.markdown': 'Markdown',
                    '.csv': 'CSV',
                    '.txt': 'TXT'
                }.get(file_extension.lower(), '文档')
                
                return True, f"{file_type_name}文档处理完成", query_engine
                
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
