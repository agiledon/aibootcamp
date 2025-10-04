"""
Milvus向量数据库客户端管理模块
负责Milvus连接、集合管理和向量搜索
"""

import logging
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import config

logger = logging.getLogger(__name__)


class MilvusClient:
    """Milvus向量数据库客户端管理类"""
    
    def __init__(self):
        self.connection = None
        self.collection = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """初始化Milvus连接"""
        try:
            self.connection = connections.connect(
                host=config.MILVUS_HOST,
                port=config.MILVUS_PORT
            )
            logger.info("📡 Connected to Milvus")
        except Exception as e:
            logger.error(f"❌ Milvus连接失败: {e}")
            logger.error("请确保Milvus服务正在运行")
            logger.error("启动命令: docker-compose up -d")
            exit(1)
    
    def get_collection(self):
        """获取或创建集合"""
        if self.collection is None:
            # 检查集合是否存在
            if utility.has_collection(config.COLLECTION_NAME):
                self.collection = Collection(config.COLLECTION_NAME)
                self.collection.load()
            else:
                # 创建新集合
                logger.info(f"创建新集合: {config.COLLECTION_NAME}，维度: {config.EMBEDDING_DIM}")
                try:
                    fields = [
                        FieldSchema("id", DataType.INT64, is_primary=True, auto_id=True),
                        FieldSchema("content", DataType.VARCHAR, max_length=65535),
                        FieldSchema("source_type", DataType.VARCHAR, max_length=50),
                        FieldSchema("source", DataType.VARCHAR, max_length=255),
                        FieldSchema("content_type", DataType.VARCHAR, max_length=50),
                        FieldSchema("embedding", DataType.FLOAT_VECTOR, dim=config.EMBEDDING_DIM)
                    ]
                    schema = CollectionSchema(fields, "Multimodal RAG collection")
                    self.collection = Collection(config.COLLECTION_NAME, schema)
                    self.collection.create_index("embedding", {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 1024}})
                    self.collection.load()
                    logger.info("✅ Collection created, indexed and loaded")
                except Exception as e:
                    logger.error(f"❌ 集合创建失败: {e}")
                    exit(1)
        return self.collection
    
    def search_vectors(self, query_embedding: list, limit: int = 5) -> list:
        """搜索向量数据库"""
        collection = self.get_collection()
        
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=limit,
            output_fields=["content", "source", "content_type"]
        )
        
        # 格式化结果
        search_results = []
        for hits in results:
            for hit in hits:
                search_results.append({
                    "content": hit.entity.get("content"),
                    "source": hit.entity.get("source"),
                    "content_type": hit.entity.get("content_type"),
                    "distance": hit.distance
                })
        
        return search_results
    
    def insert_vectors(self, data: list):
        """插入向量数据"""
        collection = self.get_collection()
        collection.insert(data)
        collection.flush()
    
    def get_entity_count(self):
        """获取集合中的实体数量"""
        try:
            collection = self.get_collection()
            return collection.num_entities
        except Exception as e:
            logger.warning(f"无法获取集合统计信息: {e}")
            return 0
    
    def check_system_status(self):
        """检查系统状态"""
        try:
            # 检查集合是否存在和有数据
            if utility.has_collection(config.COLLECTION_NAME):
                collection = Collection(config.COLLECTION_NAME)
                collection.load()
                try:
                    entity_count = collection.num_entities
                    if entity_count > 0:
                        logger.info(f"✅ System ready with {entity_count} documents")
                        return True
                    else:
                        logger.info("⚠️ Collection exists but is empty")
                except Exception as e:
                    logger.warning(f"无法获取集合统计信息: {e}")
                    logger.info("✅ Collection exists, assuming ready")
                    return True
            else:
                logger.info("⚠️ Collection does not exist")
                return False
        except Exception as e:
            logger.error(f"❌ System check failed: {e}")
            return False

