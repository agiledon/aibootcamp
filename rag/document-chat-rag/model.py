"""
Model类 - 处理业务逻辑和数据管理
包含PDF处理、LLM配置、向量索引等核心功能
"""

import os
import tempfile
import uuid
import logging
from typing import List, Dict, Any, Optional
from llama_index.readers.file import PDFReader, DocxReader, MarkdownReader, CSVReader
from llama_index.core import Settings, VectorStoreIndex, PromptTemplate
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.readers import SimpleDirectoryReader
from chroma_repository import ChromaRepository
from config import get_llm, get_embed_model, verify_settings

# 配置日志
logger = logging.getLogger(__name__)


class DocumentChatModel:
    """KFlow RAG模型类，处理多种文档格式和LLM交互的核心业务逻辑"""
    
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.file_cache: Dict[str, Any] = {}
        self.messages: List[Dict[str, str]] = []
        
        # 验证Settings配置
        if not verify_settings():
            raise RuntimeError("Settings配置验证失败，请检查config.py")
        
        # 初始化ChromaDB仓库
        self.chroma_repo = ChromaRepository(collection_name="kflow")
        
        logger.info("DocumentChatModel初始化完成")
        
    @property
    def llm(self):
        """获取LLM模型"""
        return get_llm()
    
    @property
    def embed_model(self):
        """获取嵌入模型"""
        return get_embed_model()
    
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
    
    def process_document_file(self, uploaded_file, progress_callback=None) -> tuple[bool, str, Optional[Any]]:
        """
        处理上传的文档文件（支持PDF、Word、Markdown、CSV、TXT）
        
        Args:
            uploaded_file: Streamlit上传的文件对象
            progress_callback: 进度回调函数，接收(progress, message)参数
            
        Returns:
            tuple: (success, message, query_engine)
        """
        try:
            if progress_callback:
                progress_callback(0, "开始处理文档...")
            
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
                    if progress_callback:
                        progress_callback(100, "使用缓存文件")
                    return True, "文件已缓存，直接使用", self.file_cache[file_key]
                
                # 检查文件是否存在
                if not os.path.exists(file_path):
                    return False, "无法找到上传的文件", None
                
                # 阶段1：解析文档 (0% - 20%)
                if progress_callback:
                    progress_callback(5, "正在解析文档...")
                
                # 根据文件类型加载文档
                docs = self._load_document(file_path, file_extension)
                
                if not docs:
                    return False, "文档加载失败，请检查文件格式", None
                
                # 记录文档加载信息
                total_chars = sum(len(doc.text) for doc in docs)
                print(f"成功加载 {len(docs)} 个文档片段，总字符数: {total_chars}")
                
                if progress_callback:
                    progress_callback(20, "文档解析完成")
                
                # 嵌入模型已在config.py中统一配置
                
                # 阶段2：存储到ChromaDB (20% - 80%)
                if progress_callback:
                    progress_callback(30, "正在存储到ChromaDB向量数据库...")
                
                # 嵌入模型已在config.py中统一配置
                
                # 存储文档到ChromaDB
                storage_success = self.chroma_repo.store_documents(
                    docs, 
                    uploaded_file.name, 
                    progress_callback
                )
                
                if not storage_success:
                    return False, "存储到ChromaDB失败", None
                
                if progress_callback:
                    progress_callback(80, "ChromaDB存储完成")
                
                # 阶段3：更新向量存储 (80% - 100%)
                if progress_callback:
                    progress_callback(85, "正在更新向量存储...")
                
                # 更新向量存储以包含新文档
                update_success = self.chroma_repo.update_vector_store_with_new_documents()
                
                if not update_success:
                    logger.warning("向量存储更新失败，但不影响基本功能")
                
                # 从ChromaDB获取查询引擎（从整个集合中检索）
                query_engine = self.chroma_repo.get_query_engine(streaming=True)
                
                if query_engine is None:
                    return False, "创建查询引擎失败", None
                
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
                
                # 尝试更新提示模板，如果失败则跳过
                try:
                    query_engine.update_prompts(
                        {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
                    )
                    logger.info("✅ 成功更新查询引擎提示模板")
                except Exception as e:
                    logger.warning(f"⚠️ 更新提示模板失败，但不影响基本功能: {e}")
                    # 如果更新提示模板失败，我们仍然可以使用查询引擎
                
                # 缓存查询引擎
                self.file_cache[file_key] = query_engine
                
                if progress_callback:
                    progress_callback(100, "文档加载完成")
                
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
            if progress_callback:
                progress_callback(0, f"处理失败: {str(e)}")
            return False, f"处理文件时发生错误: {e}", None
    
    def query_document(self, query_engine, prompt: str):
        """
        查询文档（从Milvus集合中检索）
        
        Args:
            query_engine: 查询引擎
            prompt: 用户查询
            
        Returns:
            流式响应生成器
        """
        if query_engine is None:
            # 如果查询引擎为空，尝试从ChromaDB重新获取
            query_engine = self.chroma_repo.get_query_engine(streaming=True)
            if query_engine is None:
                return None
        
        try:
            logger.info(f"🔍 开始执行查询，提示: {prompt[:50]}...")
            streaming_response = query_engine.query(prompt)
            
            if streaming_response is None:
                logger.error("❌ 查询引擎返回空响应")
                return None
            
            # 如果有目标文件过滤需求，在响应中进行过滤
            if hasattr(query_engine, 'target_files') and query_engine.target_files:
                logger.info(f"🔍 过滤特定文件: {query_engine.target_files}")
                if hasattr(streaming_response, 'source_nodes') and streaming_response.source_nodes:
                    filtered_nodes = []
                    for node in streaming_response.source_nodes:
                        if hasattr(node, 'metadata') and node.metadata:
                            file_name = node.metadata.get('file_name', '')
                            if file_name in query_engine.target_files:
                                filtered_nodes.append(node)
                                logger.info(f"✅ 保留节点，文件: {file_name}")
                            else:
                                logger.info(f"❌ 过滤节点，文件: {file_name}")
                        else:
                            # 如果没有元数据，也保留节点
                            filtered_nodes.append(node)
                    
                    streaming_response.source_nodes = filtered_nodes
                    logger.info(f"✅ 过滤完成，保留 {len(filtered_nodes)} 个节点")
                
            if hasattr(streaming_response, 'response_gen'):
                logger.info("✅ 查询成功，返回流式响应")
                return streaming_response.response_gen
            elif hasattr(streaming_response, 'response'):
                logger.info("✅ 查询成功，返回非流式响应")
                # 对于非流式响应，创建一个生成器来模拟流式输出
                response_text = str(streaming_response.response)
                def response_generator():
                    yield response_text
                return response_generator()
            else:
                logger.error("❌ 查询响应格式不正确")
                logger.error(f"响应对象类型: {type(streaming_response)}")
                logger.error(f"响应对象属性: {dir(streaming_response)}")
                return None
                
        except IndexError as e:
            if "pop from empty list" in str(e):
                logger.error(f"❌ 查询时发生回调管理器错误: {e}")
                logger.error("❌ 这通常是由于 llama_index 回调管理器状态不一致导致的")
                logger.error("❌ 建议重启应用程序以重置回调管理器状态")
                return None
            else:
                logger.error(f"❌ 查询时发生索引错误: {e}")
                logger.error(f"❌ 错误类型: {type(e).__name__}")
                import traceback
                logger.error(f"❌ 详细错误堆栈: {traceback.format_exc()}")
                return None
        except Exception as e:
            logger.error(f"❌ 查询时发生错误: {e}")
            logger.error(f"❌ 错误类型: {type(e).__name__}")
            import traceback
            logger.error(f"❌ 详细错误堆栈: {traceback.format_exc()}")
            return None
    
    def get_query_engine(self):
        """
        获取查询引擎（全知识库检索）
        
        Returns:
            查询引擎对象
        """
        try:
            logger.info("创建全知识库查询引擎")
            return self.chroma_repo.get_query_engine(
                llm=self.llm,
                streaming=True
            )
        except Exception as e:
            logger.error(f"获取查询引擎失败: {e}")
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
    
    def get_chroma_info(self) -> Dict[str, Any]:
        """获取ChromaDB集合信息"""
        return self.chroma_repo.get_collection_info()
    
    def get_existing_documents(self) -> List[Dict[str, Any]]:
        """获取已有文档列表"""
        # 从ChromaDB集合信息中获取文档列表，包含完整的元数据
        collection_info = self.chroma_repo.get_collection_info()
        if collection_info.get("status") == "available" and collection_info.get("file_info"):
            documents = []
            file_info = collection_info["file_info"]
            for file_name, info in file_info.items():
                documents.append({
                    "file_name": file_name,
                    "file_type": info["file_type"],
                    "document_count": info["count"]
                })
            return documents
        return []
    
    def delete_document(self, file_name: str) -> tuple[bool, str]:
        """
        删除指定文档
        
        Args:
            file_name: 要删除的文件名
            
        Returns:
            tuple[bool, str]: (是否成功, 消息)
        """
        try:
            logger.info(f"开始删除文档: {file_name}")
            
            # 从ChromaDB中删除文档
            success = self.chroma_repo.delete_file_documents(file_name)
            
            if success:
                # 清除文件缓存
                file_key = f"{file_name}_{self.session_id}"
                if file_key in self.file_cache:
                    del self.file_cache[file_key]
                    logger.info(f"已清除文件缓存: {file_key}")
                
                # 重新创建向量存储和索引以反映删除操作
                update_success = self.chroma_repo.update_vector_store_with_new_documents()
                
                if update_success:
                    logger.info(f"✅ 文档 '{file_name}' 删除成功")
                    return True, f"文档 '{file_name}' 已成功删除"
                else:
                    logger.warning(f"⚠️ 文档 '{file_name}' 已删除，但向量存储更新失败")
                    return True, f"文档 '{file_name}' 已删除，但向量存储更新失败"
            else:
                logger.error(f"❌ 删除文档 '{file_name}' 失败")
                return False, f"删除文档 '{file_name}' 失败"
                
        except Exception as e:
            logger.error(f"❌ 删除文档时发生错误: {e}")
            return False, f"删除文档时发生错误: {str(e)}"
    
    def clear_chroma_collection(self):
        """清空ChromaDB集合"""
        self.chroma_repo.clear_collection()
    
    def check_services_status(self):
        """
        检查服务状态
        
        Returns:
            tuple: (chroma_status, ollama_status)
        """
        # 检查ChromaDB状态
        chroma_info = self.chroma_repo.get_collection_info()
        chroma_status = chroma_info.get("status", "error")
        
        # 检查Ollama状态
        ollama_status = "unavailable"
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                ollama_status = "available"
        except:
            ollama_status = "unavailable"
        
        return chroma_status, ollama_status