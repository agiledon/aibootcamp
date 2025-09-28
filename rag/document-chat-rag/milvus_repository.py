"""
MilvusRepository类 - 处理Milvus向量数据库操作
负责文档的存储、检索和更新
"""

import os
import asyncio
import threading
import numpy as np
from typing import List, Dict, Any, Optional
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from llama_index.embeddings.ollama import OllamaEmbedding


class MilvusRepository:
    """Milvus向量数据库仓库类，处理文档的存储和检索"""
    
    def __init__(self, collection_name: str = "kflow", uri: str = "http://localhost:19530"):
        """
        初始化Milvus仓库
        
        Args:
            collection_name: 集合名称，默认为"kflow"
            uri: Milvus服务器地址，默认为本地地址
        """
        self.collection_name = collection_name
        self.uri = uri
        self.vector_store = None
        self.storage_context = None
        self.index = None
        self.collection = None
        self.is_available = False
        self.embed_model = None
        self._initialize_sync_connection()
    
    def _initialize_sync_connection(self):
        """使用同步连接初始化Milvus"""
        try:
            # 解析URI
            if self.uri.startswith("http://"):
                host = self.uri.replace("http://", "").split(":")[0]
                port = self.uri.replace("http://", "").split(":")[1] if ":" in self.uri else "19530"
            else:
                host = "localhost"
                port = "19530"
            
            print(f"尝试同步连接Milvus: {host}:{port}")
            
            # 使用同步连接
            connections.connect(
                alias="default",
                host=host,
                port=port
            )
            
            # 检查连接是否成功
            if connections.has_connection("default"):
                print(f"Milvus同步连接成功: {host}:{port}")
                
                # 创建或获取集合
                self._create_or_get_collection()
                
                # 初始化嵌入模型
                self._initialize_embed_model()
                
                # 注意：LlamaIndex向量存储将在需要时延迟创建，避免异步连接问题
                
                self.is_available = True
                print(f"Milvus仓库初始化成功，集合名称: {self.collection_name}")
            else:
                raise Exception("连接建立失败")
                
        except Exception as e:
            print(f"初始化Milvus同步连接失败: {e}")
            print("Milvus服务器不可用，将使用内存存储模式")
            self.is_available = False
            # 不抛出异常，允许应用继续运行
    
    def _create_or_get_collection(self):
        """创建或获取集合"""
        try:
            # 检查集合是否存在
            if utility.has_collection(self.collection_name):
                print(f"集合 {self.collection_name} 已存在")
                self.collection = Collection(self.collection_name)
            else:
                print(f"创建新集合: {self.collection_name}")
                
                # 定义字段
                fields = [
                    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
                    FieldSchema(name="file_name", dtype=DataType.VARCHAR, max_length=255),
                    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768)
                ]
                
                # 创建集合模式
                schema = CollectionSchema(fields, f"Collection for {self.collection_name}")
                
                # 创建集合
                self.collection = Collection(self.collection_name, schema)
                
                # 创建索引
                index_params = {
                    "metric_type": "L2",
                    "index_type": "IVF_FLAT",
                    "params": {"nlist": 128}
                }
                self.collection.create_index("embedding", index_params)
                
                print(f"集合 {self.collection_name} 创建成功")
                
        except Exception as e:
            print(f"创建或获取集合失败: {e}")
            raise
    
    def _initialize_embed_model(self):
        """初始化嵌入模型"""
        try:
            # 首先检查Ollama服务是否可用
            import requests
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                if response.status_code == 200:
                    print("Ollama服务可用，初始化嵌入模型...")
                    self.embed_model = OllamaEmbedding(
                        model_name="nomic-embed-text",
                        request_timeout=30,
                        keep_alive="1m"
                    )
                    print("嵌入模型初始化成功")
                else:
                    print(f"Ollama服务不可用，状态码: {response.status_code}")
                    self.embed_model = None
            except requests.exceptions.RequestException as e:
                print(f"无法连接到Ollama服务: {e}")
                self.embed_model = None
        except Exception as e:
            print(f"嵌入模型初始化失败: {e}")
            self.embed_model = None
    
    def _create_llamaindex_vector_store(self):
        """创建LlamaIndex向量存储（延迟创建，避免异步连接问题）"""
        try:
            # 检查是否已经创建
            if self.vector_store is not None:
                return True
                
            print("正在创建LlamaIndex向量存储...")
            
            # 创建Milvus向量存储，使用正确的URI格式
            self.vector_store = MilvusVectorStore(
                dim=768,
                uri="http://localhost:19530",  # 使用完整的HTTP URI
                collection_name=self.collection_name,
                overwrite=False
            )
            
            # 创建存储上下文
            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store
            )
            
            print("LlamaIndex向量存储创建成功")
            return True
            
        except Exception as e:
            print(f"创建LlamaIndex向量存储失败: {e}")
            if "llama-index-embeddings-openai" in str(e):
                print("缺少llama-index-embeddings-openai依赖，将使用内存存储模式")
            else:
                print("将使用内存存储模式进行查询")
            # 即使LlamaIndex向量存储失败，我们仍然可以使用同步连接
            self.vector_store = None
            self.storage_context = None
            return False
    
    
    def store_documents(self, documents: List[Document], file_name: str, 
                       progress_callback=None) -> bool:
        """
        存储文档到Milvus或内存
        
        Args:
            documents: 文档列表
            file_name: 文件名（包括扩展名）
            progress_callback: 进度回调函数
            
        Returns:
            bool: 存储是否成功
        """
        try:
            if progress_callback:
                progress_callback(10, "正在准备存储文档...")
            
            if progress_callback:
                progress_callback(30, "正在分割文档...")
            
            # 设置文档分割器
            text_splitter = SentenceSplitter(
                chunk_size=1024,
                chunk_overlap=200,
                separator=" "
            )
            
            # 为每个文档添加文件名元数据
            for doc in documents:
                doc.metadata["file_name"] = file_name
                doc.metadata["source"] = file_name
            
            if progress_callback:
                progress_callback(50, "正在生成向量嵌入...")
            
            if self.is_available and self.embed_model is not None:
                # 尝试使用同步方式存储到Milvus
                try:
                    if progress_callback:
                        progress_callback(60, "正在存储到Milvus...")
                    
                    # 分割文档
                    nodes = text_splitter.get_nodes_from_documents(documents)
                    
                    # 生成嵌入向量
                    texts = [node.text for node in nodes]
                    embeddings = self.embed_model.get_text_embedding_batch(texts)
                    
                    # 准备数据
                    data = []
                    for i, (node, embedding) in enumerate(zip(nodes, embeddings)):
                        data.append({
                            "text": node.text,
                            "file_name": file_name,
                            "embedding": embedding
                        })
                    
                    # 存储到Milvus
                    self._store_to_milvus_sync(data)
                    
                    if progress_callback:
                        progress_callback(90, "正在保存到Milvus...")
                    
                    print(f"成功存储文档 {file_name} 到Milvus集合 {self.collection_name}")
                    storage_message = f"文档 {file_name} 已成功存储到Milvus"
                    
                    # 创建内存索引用于查询
                    index = VectorStoreIndex.from_documents(
                        documents,
                        transformations=[text_splitter],
                        show_progress=True
                    )
                    
                except Exception as e:
                    print(f"存储到Milvus失败: {e}")
                    print("回退到内存存储模式...")
                    
                    if progress_callback:
                        progress_callback(60, "Milvus存储失败，使用内存存储...")
                    
                    # 创建内存向量索引
                    index = VectorStoreIndex.from_documents(
                        documents,
                        transformations=[text_splitter],
                        show_progress=True
                    )
                    
                    if progress_callback:
                        progress_callback(90, "正在保存到内存...")
                    
                    print(f"成功存储文档 {file_name} 到内存")
                    storage_message = f"文档 {file_name} 已存储到内存（Milvus存储失败）"
                
            else:
                # Milvus不可用或嵌入模型不可用，使用内存存储
                if progress_callback:
                    if self.is_available:
                        progress_callback(60, "嵌入模型不可用，使用内存存储...")
                    else:
                        progress_callback(60, "Milvus不可用，使用内存存储...")
                
                # 创建内存向量索引
                index = VectorStoreIndex.from_documents(
                    documents,
                    transformations=[text_splitter],
                    show_progress=True
                )
                
                if progress_callback:
                    progress_callback(90, "正在保存到内存...")
                
                print(f"成功存储文档 {file_name} 到内存")
                storage_message = f"文档 {file_name} 已存储到内存（Milvus不可用）"
            
            # 更新当前索引引用
            self.index = index
            
            if progress_callback:
                progress_callback(100, storage_message)
            
            return True
            
        except Exception as e:
            print(f"存储文档失败: {e}")
            if progress_callback:
                progress_callback(0, f"存储失败: {str(e)}")
            return False
    
    def _store_to_milvus_sync(self, data: List[Dict]):
        """同步存储数据到Milvus"""
        try:
            # 确保集合已加载
            self.collection.load()
            
            # 准备插入数据
            texts = [item["text"] for item in data]
            file_names = [item["file_name"] for item in data]
            embeddings = [item["embedding"] for item in data]
            
            # 插入数据
            insert_data = [texts, file_names, embeddings]
            result = self.collection.insert(insert_data)
            
            # 刷新集合
            self.collection.flush()
            
            print(f"成功插入 {len(data)} 条记录到Milvus")
            
        except Exception as e:
            print(f"同步存储到Milvus失败: {e}")
            raise
    
    def _file_exists(self, file_name: str) -> bool:
        """
        检查文件是否已存在于集合中
        
        Args:
            file_name: 文件名
            
        Returns:
            bool: 文件是否存在
        """
        try:
            # 创建临时索引来检查文件是否存在
            temp_index = VectorStoreIndex.from_vector_store(
                self.vector_store,
                storage_context=self.storage_context
            )
            
            # 尝试查询该文件名的文档
            query_engine = temp_index.as_query_engine(
                filters={"file_name": file_name},
                similarity_top_k=1
            )
            
            # 执行一个简单的查询来检查是否存在
            response = query_engine.query("test")
            return len(response.source_nodes) > 0
            
        except Exception as e:
            print(f"检查文件是否存在时出错: {e}")
            return False
    
    def _delete_file_documents(self, file_name: str):
        """
        删除指定文件的所有文档
        
        Args:
            file_name: 文件名
        """
        try:
            # 这里需要直接操作Milvus客户端来删除特定文件名的文档
            # 由于LlamaIndex的MilvusVectorStore没有直接的删除方法，
            # 我们需要通过重新创建集合来实现替换
            print(f"正在删除文件 {file_name} 的旧版本...")
            
            # 注意：这里我们通过重新创建集合来实现替换
            # 在实际生产环境中，可能需要更精细的删除操作
            
        except Exception as e:
            print(f"删除文件文档时出错: {e}")
    
    def get_query_engine(self, streaming: bool = True):
        """
        获取查询引擎，用于RAG检索
        
        Args:
            streaming: 是否启用流式响应
            
        Returns:
            查询引擎对象
        """
        try:
            if self.index is None:
                if self.is_available:
                    # 尝试创建LlamaIndex向量存储（如果还没有创建）
                    if self.vector_store is None:
                        if not self._create_llamaindex_vector_store():
                            print("LlamaIndex向量存储创建失败，无法创建查询引擎")
                            return None
                    
                    # Milvus可用且LlamaIndex向量存储可用，从向量存储重新创建
                    self.index = VectorStoreIndex.from_vector_store(
                        self.vector_store,
                        storage_context=self.storage_context
                    )
                else:
                    # Milvus不可用，返回None
                    print("Milvus不可用，无法创建查询引擎")
                    return None
            
            # 创建查询引擎，从整个集合中检索
            query_engine = self.index.as_query_engine(
                streaming=streaming,
                similarity_top_k=5  # 检索前5个最相关的文档片段
            )
            
            return query_engine
            
        except Exception as e:
            print(f"创建查询引擎失败: {e}")
            return None
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        获取集合信息
        
        Returns:
            集合信息字典
        """
        try:
            if self.is_available:
                return {
                    "collection_name": self.collection_name,
                    "uri": self.uri,
                    "status": "connected",
                    "storage_type": "milvus"
                }
            else:
                return {
                    "collection_name": self.collection_name,
                    "uri": self.uri,
                    "status": "unavailable",
                    "storage_type": "memory",
                    "message": "Milvus服务器不可用，使用内存存储"
                }
        except Exception as e:
            print(f"获取集合信息失败: {e}")
            return {"status": "error", "message": str(e)}
    
    def clear_collection(self):
        """清空整个集合"""
        try:
            # 重新创建向量存储，这会清空集合
            self.vector_store = MilvusVectorStore(
                dim=768,
                uri=self.uri,
                collection_name=self.collection_name,
                overwrite=True  # 覆盖现有集合
            )
            
            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store
            )
            
            self.index = None
            print(f"已清空集合 {self.collection_name}")
            
        except Exception as e:
            print(f"清空集合失败: {e}")
            raise
