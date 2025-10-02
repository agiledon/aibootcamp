"""
ChromaRepository类 - 处理ChromaDB向量数据库操作
负责文档的存储、检索和更新
保持与MilvusRepository完全相同的功能接口
"""

import os
import tempfile
import numpy as np
import logging
from typing import List, Dict, Any, Optional
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
import chromadb
from chromadb.config import Settings

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ChromaRepository:
    """ChromaDB向量数据库仓库类，处理文档的存储和检索"""
    
    def __init__(self, collection_name: str = "kflow", persist_directory: str = "./chroma_db"):
        """
        初始化ChromaDB仓库
        
        Args:
            collection_name: 集合名称，默认为"kflow"
            persist_directory: 数据持久化目录，默认为"./chroma_db"
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.vector_store = None
        self.storage_context = None
        self.index = None
        self.chroma_client = None
        self.chroma_collection = None
        self.is_available = False
        self.embed_model = None
        self._initialize_chroma_connection()
    
    def _initialize_chroma_connection(self):
        """初始化ChromaDB连接"""
        try:
            print(f"正在初始化ChromaDB连接...")
            
            # 创建ChromaDB客户端
            self.chroma_client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # 创建或获取集合
            self._create_or_get_collection()
            
            # 初始化嵌入模型
            self._initialize_embed_model()
            
            self.is_available = True
            print(f"ChromaDB仓库初始化成功，集合名称: {self.collection_name}")
                
        except Exception as e:
            print(f"初始化ChromaDB连接失败: {e}")
            print("ChromaDB服务器不可用，将使用内存存储模式")
            self.is_available = False
    
    def _create_or_get_collection(self):
        """创建或获取集合"""
        try:
            # 尝试获取现有集合
            try:
                self.chroma_collection = self.chroma_client.get_collection(
                    name=self.collection_name
                )
                print(f"获取现有ChromaDB集合: {self.collection_name}")
            except Exception:
                # 集合不存在，创建新集合
                self.chroma_collection = self.chroma_client.create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
                )
                print(f"创建新ChromaDB集合: {self.collection_name}")
                
        except Exception as e:
            print(f"创建或获取ChromaDB集合失败: {e}")
            raise
    
    def _initialize_embed_model(self):
        """初始化嵌入模型"""
        try:
            # 检查Ollama服务是否可用
            import requests
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [model.get("name", "") for model in models]
                    
                    if any("nomic-embed-text" in name for name in model_names):
                        self.embed_model = OllamaEmbedding(
                            model_name="nomic-embed-text",
                            request_timeout=60,
                            keep_alive="5m"
                        )
                        print("Ollama嵌入模型初始化成功")
                    else:
                        print("未找到nomic-embed-text模型")
                        self.embed_model = None
                else:
                    print(f"Ollama服务响应异常: {response.status_code}")
                    self.embed_model = None
            except requests.exceptions.RequestException as e:
                print(f"无法连接到Ollama服务: {e}")
                self.embed_model = None
        except Exception as e:
            print(f"嵌入模型初始化失败: {e}")
            self.embed_model = None
    
    def store_documents(self, documents: List[Document], file_name: str, progress_callback=None) -> bool:
        """
        存储文档到ChromaDB
        
        Args:
            documents: 文档列表
            file_name: 文件名
            progress_callback: 进度回调函数
            
        Returns:
            是否存储成功
        """
        try:
            if not self.is_available:
                print("ChromaDB不可用，无法存储文档")
                return False
            
            if progress_callback:
                progress_callback(10, "开始存储文档到ChromaDB...")
            
            # 文档分割
            text_splitter = SentenceSplitter(
                chunk_size=1024,
                chunk_overlap=200,
                separator=" "
            )
            
            nodes = text_splitter.get_nodes_from_documents(documents)
            
            if progress_callback:
                progress_callback(30, f"文档分割完成，共{len(nodes)}个片段")
            
            # 准备存储数据
            texts = []
            metadatas = []
            ids = []
            
            for i, node in enumerate(nodes):
                texts.append(node.text)
                metadata = {
                    "file_name": file_name,
                    "chunk_id": i,
                    "source": file_name
                }
                metadatas.append(metadata)
                ids.append(f"{file_name}_{i}")
            
            if progress_callback:
                progress_callback(50, "正在生成嵌入向量...")
            
            # 生成嵌入向量
            if self.embed_model is None:
                print("嵌入模型不可用，无法生成向量")
                return False
            
            embeddings = []
            batch_size = 32
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_embeddings = self.embed_model.get_text_embedding_batch(batch_texts)
                embeddings.extend(batch_embeddings)
                
                if progress_callback:
                    progress = 50 + int(40 * i / len(texts))
                    progress_callback(progress, f"生成嵌入向量进度: {i+len(batch_texts)}/{len(texts)}")
            
            if progress_callback:
                progress_callback(90, "正在存储到ChromaDB...")
            
            # 存储到ChromaDB
            self.chroma_collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            if progress_callback:
                progress_callback(100, "文档存储完成")
            
            print(f"成功存储{len(texts)}个文档片段到ChromaDB")
            return True
            
        except Exception as e:
            print(f"存储文档到ChromaDB失败: {e}")
            if progress_callback:
                progress_callback(0, f"存储失败: {str(e)}")
            return False
    
    def _create_chroma_vector_store(self):
        """创建ChromaDB向量存储"""
        try:
            print("正在创建ChromaDB向量存储...")
            
            self.vector_store = ChromaVectorStore(
                chroma_collection=self.chroma_collection
            )
            
            # 创建存储上下文
            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store
            )
            
            print("ChromaDB向量存储创建成功")
            return True
            
        except Exception as e:
            print(f"创建ChromaDB向量存储失败: {e}")
            self.vector_store = None
            self.storage_context = None
            return False
    
    def _create_index_with_embed_model(self):
        """使用正确的嵌入模型创建索引"""
        try:
            print("=== 开始创建索引 ===")
            print(f"向量存储状态: {self.vector_store is not None}")
            print(f"存储上下文状态: {self.storage_context is not None}")
            print(f"嵌入模型状态: {self.embed_model is not None}")
            
            if self.vector_store is None or self.storage_context is None:
                print("❌ 向量存储或存储上下文未初始化，无法创建索引")
                return False
            
            # 确保嵌入模型已初始化
            if self.embed_model is None:
                print("❌ 嵌入模型未初始化，无法创建索引")
                return False
            
            print("✅ 正在使用Ollama嵌入模型创建索引...")
            
            # 设置LlamaIndex的全局嵌入模型
            from llama_index.core import Settings
            Settings.embed_model = self.embed_model
            print("✅ 已设置全局嵌入模型")
            
            # 检查向量存储中是否有数据
            try:
                # 获取ChromaDB集合中的数据
                results = self.chroma_collection.get()
                print(f"✅ ChromaDB集合中有 {len(results.get('ids', []))} 条记录")
                
                if len(results.get('ids', [])) == 0:
                    print("❌ ChromaDB集合中没有数据，无法创建索引")
                    return False
                    
            except Exception as e:
                print(f"❌ 检查ChromaDB数据失败: {e}")
                return False
            
            # 从向量存储创建索引
            print("✅ 开始从向量存储创建索引...")
            self.index = VectorStoreIndex.from_vector_store(
                self.vector_store,
                storage_context=self.storage_context,
                embed_model=self.embed_model  # 显式指定嵌入模型
            )
            
            print("✅ 索引创建成功！")
            return True
            
        except Exception as e:
            print(f"❌ 创建索引失败: {e}")
            print(f"错误类型: {type(e).__name__}")
            import traceback
            print(f"详细错误信息: {traceback.format_exc()}")
            self.index = None
            return False
    
    def get_query_engine(self, streaming: bool = True, file_names: List[str] = None):
        """
        获取查询引擎，用于RAG检索
        
        Args:
            streaming: 是否启用流式响应
            file_names: 指定要检索的文件名列表，None表示检索所有文件
            
        Returns:
            查询引擎对象
        """
        try:
            print(f"=== 开始获取查询引擎 ===")
            print(f"ChromaDB可用状态: {self.is_available}")
            print(f"索引状态: {self.index is not None}")
            print(f"向量存储状态: {self.vector_store is not None}")
            
            # 如果没有索引，尝试创建或重新创建
            if self.index is None:
                print("索引为空，开始创建索引...")
                if self.is_available:
                    # 尝试创建ChromaDB向量存储（如果还没有创建）
                    if self.vector_store is None:
                        print("向量存储为空，开始创建...")
                        if not self._create_chroma_vector_store():
                            print("❌ ChromaDB向量存储创建失败")
                            return None
                        print("✅ ChromaDB向量存储创建成功")
                    
                    try:
                        # 使用新的方法创建索引，确保使用正确的嵌入模型
                        print("开始创建索引...")
                        if not self._create_index_with_embed_model():
                            print("❌ 使用嵌入模型创建索引失败")
                            return None
                        print("✅ 成功从ChromaDB向量存储创建索引")
                    except Exception as e:
                        print(f"❌ 从ChromaDB向量存储创建索引失败: {e}")
                        import traceback
                        print(f"详细错误信息: {traceback.format_exc()}")
                        # 尝试检查是否有文档存在
                        try:
                            # 查询集合中是否有数据
                            results = self.chroma_collection.get()
                            if len(results.get('ids', [])) == 0:
                                print("❌ ChromaDB集合中没有文档数据")
                                return None
                            else:
                                print(f"❌ ChromaDB集合中有 {len(results['ids'])} 条记录，但无法创建索引")
                                return None
                        except Exception as query_e:
                            print(f"❌ 检查ChromaDB集合数据失败: {query_e}")
                        return None
                else:
                    # ChromaDB不可用
                    print("❌ ChromaDB不可用，无法创建查询引擎")
                    return None
            
            # 创建查询引擎
            try:
                print("开始创建查询引擎...")
                
                # 设置全局LLM模型，避免在查询引擎创建时使用OpenAI
                try:
                    from llama_index.llms.deepseek import DeepSeek
                    from llama_index.core import Settings
                    
                    # 创建DeepSeek LLM实例
                    llm = DeepSeek(
                        model="deepseek-chat",
                        temperature=0.1,
                        max_tokens=1000,
                        timeout=120,
                        max_retries=3
                    )
                    
                    # 设置全局LLM
                    Settings.llm = llm
                    print("✅ 成功设置全局LLM模型")
                except Exception as e:
                    print(f"❌ 设置LLM模型失败: {e}")
                    llm = None
                
                if file_names and len(file_names) > 0:
                    # 指定文件名的检索
                    
                    # 对于ChromaDB，我们使用简单的全知识库查询，然后在应用层过滤
                    logger.info(f"创建针对特定文件的查询引擎: {file_names}")
                    
                    try:
                        # 创建全知识库查询引擎，增加检索数量
                        if llm:
                            query_engine = self.index.as_query_engine(
                                streaming=streaming,
                                similarity_top_k=50,  # 增加检索数量以便后续过滤
                                llm=llm
                            )
                        else:
                            query_engine = self.index.as_query_engine(
                                streaming=streaming,
                                similarity_top_k=50,  # 增加检索数量以便后续过滤
                            )
                        
                        # 将目标文件名存储在查询引擎对象上，供后续过滤使用
                        query_engine.target_files = file_names
                        logger.info("✅ 成功创建带文件过滤的查询引擎")
                        
                    except Exception as e:
                        logger.error(f"❌ 创建过滤查询引擎失败: {e}")
                        logger.error(f"❌ 错误类型: {type(e).__name__}")
                        import traceback
                        logger.error(f"❌ 详细错误堆栈: {traceback.format_exc()}")
                        raise e
                else:
                    # 从整个集合中检索
                    logger.info("创建全知识库查询引擎")
                    try:
                        if llm:
                            query_engine = self.index.as_query_engine(
                                streaming=streaming,
                                similarity_top_k=5,
                                llm=llm  # 明确指定LLM
                            )
                        else:
                            # 如果没有LLM，先创建基础的查询引擎
                            query_engine = self.index.as_query_engine(
                                streaming=streaming,
                                similarity_top_k=5
                            )
                    except Exception as e:
                        logger.error(f"❌ 创建全知识库查询引擎失败: {e}")
                        logger.error(f"❌ 错误类型: {type(e).__name__}")
                        import traceback
                        logger.error(f"❌ 详细错误堆栈: {traceback.format_exc()}")
                        raise e
                
                logger.info("✅ 查询引擎创建成功")
                return query_engine
                
            except Exception as e:
                logger.error(f"❌ 创建查询引擎时发生错误: {e}")
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
                "file_info": file_info,  # 新增：包含每个文件的详细信息
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
                print("ChromaDB不可用，无法清空集合")
                return False
            
            # 删除集合
            self.chroma_client.delete_collection(self.collection_name)
            
            # 重新创建空集合
            self._create_or_get_collection()
            
            # 重置相关对象
            self.vector_store = None
            self.storage_context = None
            self.index = None
            
            print(f"成功清空ChromaDB集合: {self.collection_name}")
            return True
            
        except Exception as e:
            print(f"清空ChromaDB集合失败: {e}")
            return False
    
    def delete_file_documents(self, file_name: str):
        """
        删除指定文件的所有文档片段
        
        Args:
            file_name: 要删除的文件名
        """
        try:
            if not self.is_available or not self.chroma_collection:
                print("ChromaDB不可用，无法删除文档")
                return False
            
            # 查询该文件的所有文档ID
            results = self.chroma_collection.get(
                where={"file_name": file_name}
            )
            
            if results.get('ids'):
                # 删除这些文档
                self.chroma_collection.delete(ids=results['ids'])
                print(f"成功删除文件 {file_name} 的 {len(results['ids'])} 个文档片段")
                
                # 重置索引，因为数据已更改
                self.index = None
                self.vector_store = None
                self.storage_context = None
                
                return True
            else:
                print(f"未找到文件 {file_name} 的文档")
                return False
            
        except Exception as e:
            print(f"删除文件文档时出错: {e}")
            return False
    
    def update_vector_store_with_new_documents(self):
        """
        当新文档上传后，更新向量存储和查询引擎
        这个方法会在文档上传完成后调用
        """
        try:
            print("正在更新ChromaDB向量存储和查询引擎...")
            
            # 重新创建向量存储，这会自动包含新文档
            if self._create_chroma_vector_store():
                # 使用新的方法重新创建索引
                if self._create_index_with_embed_model():
                    print("ChromaDB向量存储和查询引擎更新成功")
                    return True
                else:
                    print("重新创建索引失败")
                    return False
            else:
                print("ChromaDB向量存储更新失败")
                return False
                    
        except Exception as e:
            print(f"更新ChromaDB向量存储失败: {e}")
            return False
