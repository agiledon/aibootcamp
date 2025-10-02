"""
ChromaRepository类 - 处理ChromaDB向量数据库操作
专注于向量存储的创建、访问和文档管理
保持纯粹的向量存储访问职责
"""

import os
import logging
from typing import List, Dict, Any, Optional
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter
import chromadb

from .custom_query_engine import FilteredQueryEngine

# 配置日志
logger = logging.getLogger(__name__)


class ChromaRepository:
    """ChromaDB向量数据库仓库类，专注于向量存储的创建和访问"""
    
    def __init__(self, collection_name: str = "kflow", persist_directory: str = "./chroma_db"):
        """
        初始化ChromaDB仓库
        
        Args:
            collection_name: 集合名称，默认为"kflow"
            persist_directory: ChromaDB数据持久化目录
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.vector_store = None
        self.storage_context = None
        self.index = None
        self.chroma_client = None
        self.chroma_collection = None
        self.is_available = False
        
        self._initialize_chroma_connection()
        logger.info("ChromaRepository初始化完成")
    
    def _initialize_chroma_connection(self):
        """初始化ChromaDB连接"""
        try:
            logger.info("正在初始化ChromaDB连接...")
            
            # 创建ChromaDB客户端，数据将持久化到指定目录
            self.chroma_client = chromadb.PersistentClient(path=self.persist_directory)
            
            # 获取或创建集合
            try:
                self.chroma_collection = self.chroma_client.get_or_create_collection(self.collection_name)
                logger.info(f"获取现有ChromaDB集合: {self.collection_name}")
            except Exception as e:
                self.chroma_collection = self.chroma_client.create_collection(self.collection_name)
                logger.info(f"创建新ChromaDB集合: {self.collection_name}")
            
            self.is_available = True
            logger.info(f"ChromaDB仓库初始化成功，集合名称: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"初始化ChromaDB连接失败: {e}")
            self.is_available = False
    
    def store_documents(self, documents: List[Document], file_name: str, embed_model=None, progress_callback=None) -> bool:
        """
        存储文档到ChromaDB
        
        Args:
            documents: LlamaIndex Document对象列表
            file_name: 原始文件名
            embed_model: 嵌入模型实例
            progress_callback: 进度回调函数
            
        Returns:
            bool: 是否成功存储
        """
        try:
            if not self.is_available or not self.chroma_collection:
                logger.error("ChromaDB不可用，无法存储文档")
                return False
            
            logger.info(f"正在存储 {len(documents)} 个文档片段到ChromaDB...")
            
            # 使用文档分割器
            text_splitter = SentenceSplitter(
                chunk_size=1024,
                chunk_overlap=200,
                separator=" "
            )
            nodes = text_splitter.get_nodes_from_documents(documents)
            
            # 准备数据以存储到ChromaDB
            ids = [node.id_ for node in nodes]
            texts = [node.text for node in nodes]
            metadatas = [node.metadata for node in nodes]
            
            # 添加文件名为元数据
            for metadata in metadatas:
                metadata["file_name"] = file_name
                metadata["source"] = file_name
            
            # 批量添加文档到ChromaDB
            self.chroma_collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"成功存储{len(documents)}个文档片段到ChromaDB")
            return True
            
        except Exception as e:
            logger.error(f"存储文档到ChromaDB失败: {e}")
            if progress_callback:
                progress_callback(0, f"存储失败: {str(e)}")
            return False
    
    def _create_vector_store(self):
        """创建ChromaDB向量存储"""
        try:
            logger.info("正在创建ChromaDB向量存储...")
            
            self.vector_store = ChromaVectorStore(
                chroma_collection=self.chroma_collection
            )
            
            # 创建存储上下文
            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store
            )
            
            logger.info("ChromaDB向量存储创建成功")
            return True
            
        except Exception as e:
            logger.error(f"创建ChromaDB向量存储失败: {e}")
            self.vector_store = None
            self.storage_context = None
            return False
    
    def _create_index(self, embed_model=None):
        """创建向量存储索引"""
        try:
            logger.info("=== 开始创建索引 ===")
            logger.info(f"向量存储状态: {self.vector_store is not None}")
            logger.info(f"存储上下文状态: {self.storage_context is not None}")
            logger.info(f"嵌入模型状态: {embed_model is not None}")
            
            if self.vector_store is None or self.storage_context is None:
                logger.error("❌ 向量存储或存储上下文未初始化，无法创建索引")
                return False
            
            # 检查向量存储中是否有数据
            try:
                # 获取ChromaDB集合中的数据
                results = self.chroma_collection.get()
                logger.info(f"✅ ChromaDB集合中有 {len(results.get('ids', []))} 条记录")
                
                if len(results.get('ids', [])) == 0:
                    logger.error("❌ ChromaDB集合中没有数据，无法创建索引")
                    return False
                    
            except Exception as e:
                logger.error(f"❌ 检查ChromaDB数据失败: {e}")
                return False
            
            # 从向量存储创建索引
            logger.info("✅ 开始从向量存储创建索引...")
            if embed_model:
                self.index = VectorStoreIndex.from_vector_store(
                    self.vector_store,
                    storage_context=self.storage_context,
                    embed_model=embed_model
                )
            else:
                self.index = VectorStoreIndex.from_vector_store(
                    self.vector_store,
                    storage_context=self.storage_context
                )
            
            logger.info("✅ 索引创建成功！")
            return True
            
        except Exception as e:
            logger.error(f"❌ 创建索引失败: {e}")
            logger.error(f"错误类型: {type(e).__name__}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            self.index = None
            return False
    
    def get_query_engine(self, file_names: Optional[List[str]] = None, llm=None, streaming: bool = True):
        """
        获取查询引擎，用于RAG检索
        
        Args:
            file_names: 指定要检索的文件名列表，None表示检索所有文件
            llm: 语言模型实例
            streaming: 是否启用流式响应
            
        Returns:
            查询引擎对象
        """
        try:
            logger.info(f"=== 开始获取查询引擎 ===")
            logger.info(f"ChromaDB可用状态: {self.is_available}")
            logger.info(f"索引状态: {self.index is not None}")
            logger.info(f"向量存储状态: {self.vector_store is not None}")
            logger.info(f"目标文件: {file_names}")
            
            # 如果没有索引，尝试创建或重新创建
            if self.index is None:
                logger.info("索引为空，开始创建索引...")
                if self.is_available:
                    # 尝试创建ChromaDB向量存储（如果还没有创建）
                    if self.vector_store is None:
                        logger.info("向量存储为空，开始创建...")
                        if not self._create_vector_store():
                            logger.error("❌ ChromaDB向量存储创建失败")
                            return None
                        logger.info("✅ ChromaDB向量存储创建成功")
                    
                    try:
                        # 创建索引（这里需要传入embed_model，但我们在外部处理）
                        logger.info("开始创建索引...")
                        if not self._create_index():
                            logger.error("❌ 创建索引失败")
                            return None
                        logger.info("✅ 成功从ChromaDB向量存储创建索引")
                    except Exception as e:
                        logger.error(f"❌ 从ChromaDB向量存储创建索引失败: {e}")
                        import traceback
                        logger.error(f"详细错误信息: {traceback.format_exc()}")
                        return None
                else:
                    logger.error("❌ ChromaDB不可用，无法创建查询引擎")
                    return None
            
            # 创建自定义过滤查询引擎
            try:
                logger.info("开始创建自定义过滤查询引擎...")
                query_engine = FilteredQueryEngine(
                    index=self.index,
                    target_files=file_names,
                    similarity_top_k=5,
                    streaming=streaming,
                    llm=llm
                )
                logger.info("✅ 自定义过滤查询引擎创建成功")
                return query_engine
                
            except Exception as e:
                logger.error(f"❌ 创建自定义过滤查询引擎时发生错误: {e}")
                import traceback
                logger.error(f"详细错误信息: {traceback.format_exc()}")
                return None
            
        except Exception as e:
            logger.error(f"❌ 获取查询引擎失败: {e}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            return None
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        获取集合信息
        
        Returns:
            集合信息字典
        """
        try:
            if not self.is_available or not self.chroma_collection:
                return {
                    "status": "unavailable",
                    "collection_name": self.collection_name,
                    "document_count": 0,
                    "message": "ChromaDB不可用或集合未初始化"
                }
            
            # 获取集合统计信息
            results = self.chroma_collection.get()
            document_count = len(results.get('ids', []))
            
            # 获取文件列表和统计信息
            file_info = {}  # {file_name: {count: int, file_type: str}}
            if results.get('metadatas'):
                for metadata in results['metadatas']:
                    if metadata and 'file_name' in metadata:
                        file_name = metadata['file_name']
                        if file_name not in file_info:
                            file_info[file_name] = {'count': 0, 'file_type': '未知'}
                        file_info[file_name]['count'] += 1
                        
                        # 尝试从文件名推断文件类型
                        if '.' in file_name:
                            ext = file_name.split('.')[-1].lower()
                            type_map = {
                                'pdf': 'PDF',
                                'docx': 'Word',
                                'doc': 'Word', 
                                'md': 'Markdown',
                                'markdown': 'Markdown',
                                'csv': 'CSV',
                                'txt': 'TXT'
                            }
                            file_info[file_name]['file_type'] = type_map.get(ext, ext.upper())
            
            return {
                "status": "available",
                "collection_name": self.collection_name,
                "document_count": document_count,
                "file_count": len(file_info),
                "file_names": list(file_info.keys()),
                "file_info": file_info,  # 包含每个文件的详细信息
                "persist_directory": self.persist_directory,
                "message": f"ChromaDB集合'{self.collection_name}'包含{document_count}个文档片段，来自{len(file_info)}个文件"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "collection_name": self.collection_name,
                "document_count": 0,
                "message": f"获取集合信息失败: {e}"
            }
    
    def clear_collection(self):
        """清空集合中的所有数据"""
        try:
            if not self.is_available or not self.chroma_collection:
                logger.error("ChromaDB不可用，无法清空集合")
                return False
            
            self.chroma_client.delete_collection(self.collection_name)
            self.chroma_collection = self.chroma_client.create_collection(self.collection_name)
            self.index = None  # 清空索引
            self.vector_store = None
            self.storage_context = None
            logger.info(f"ChromaDB集合 '{self.collection_name}' 已清空")
            return True
        except Exception as e:
            logger.error(f"清空ChromaDB集合失败: {e}")
            return False
    
    def delete_file_documents(self, file_name: str) -> bool:
        """
        从ChromaDB中删除指定文件的所有文档片段
        
        Args:
            file_name: 要删除的文件名
            
        Returns:
            bool: 是否成功删除
        """
        try:
            if not self.is_available or not self.chroma_collection:
                logger.error("ChromaDB不可用，无法删除文档")
                return False
            
            logger.info(f"正在从ChromaDB删除文件 '{file_name}' 的文档片段...")
            
            # 获取与该文件相关的所有文档ID
            results = self.chroma_collection.get(
                where={"file_name": file_name},
                output_fields=["ids"]
            )
            
            ids_to_delete = results.get('ids', [])
            
            if ids_to_delete:
                self.chroma_collection.delete(ids=ids_to_delete)
                logger.info(f"成功从ChromaDB删除 {len(ids_to_delete)} 个文档片段，来自文件 '{file_name}'")
                return True
            else:
                logger.info(f"未找到文件 '{file_name}' 的文档片段")
                return False
            
        except Exception as e:
            logger.error(f"删除文件文档时出错: {e}")
            return False
    
    def update_vector_store_with_new_documents(self, embed_model=None):
        """
        当新文档上传后，更新向量存储和查询引擎
        这个方法会在文档上传完成后调用
        
        Args:
            embed_model: 嵌入模型实例
        """
        try:
            logger.info("正在更新ChromaDB向量存储和查询引擎...")
            
            # 重新创建向量存储，这会自动包含新文档
            if self._create_vector_store():
                # 重新创建索引
                if self._create_index(embed_model):
                    logger.info("ChromaDB向量存储和查询引擎更新成功")
                    return True
                else:
                    logger.error("重新创建索引失败")
                    return False
            else:
                logger.error("ChromaDB向量存储更新失败")
                return False
                
        except Exception as e:
            logger.error(f"更新ChromaDB向量存储失败: {e}")
            return False
