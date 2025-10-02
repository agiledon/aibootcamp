"""
自定义查询引擎模块
提供基于文档过滤的查询引擎实现
"""

import logging
from typing import List, Optional, Any
from llama_index.core.query_engine import BaseQueryEngine
from llama_index.core.schema import QueryBundle, NodeWithScore
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.callbacks import CallbackManager
from pydantic import Field

logger = logging.getLogger(__name__)


class FileFilterPostprocessor(BaseNodePostprocessor):
    """基于文件名过滤的后处理器"""
    
    target_files: Optional[List[str]] = Field(default=None, description="目标文件名列表")
    
    def __init__(self, target_files: Optional[List[str]] = None, **kwargs):
        """
        初始化文件过滤后处理器
        
        Args:
            target_files: 目标文件名列表
        """
        super().__init__(target_files=target_files, **kwargs)
        if target_files:
            self.target_files = target_files
        logger.info(f"初始化文件过滤后处理器，目标文件: {self.target_files}")
    
    def _postprocess_nodes(
        self, 
        nodes: List[NodeWithScore], 
        query_bundle: Optional[QueryBundle] = None
    ) -> List[NodeWithScore]:
        """
        过滤节点，只保留目标文件中的节点
        
        Args:
            nodes: 待过滤的节点列表
            query_bundle: 查询包（未使用）
            
        Returns:
            过滤后的节点列表
        """
        if not self.target_files:
            logger.info("无目标文件限制，返回所有节点")
            return nodes
        
        target_files_set = set(self.target_files)
        filtered_nodes = []
        for node in nodes:
            if hasattr(node, 'node') and hasattr(node.node, 'metadata'):
                file_name = node.node.metadata.get('file_name', '')
                if file_name in target_files_set:
                    filtered_nodes.append(node)
                    logger.debug(f"保留节点，文件: {file_name}")
                else:
                    logger.debug(f"过滤节点，文件: {file_name}")
            else:
                # 如果没有元数据，也保留节点（可能是系统节点）
                filtered_nodes.append(node)
                logger.debug("保留无元数据节点")
        
        logger.info(f"节点过滤完成，原始节点数: {len(nodes)}, 过滤后节点数: {len(filtered_nodes)}")
        return filtered_nodes


class FilteredQueryEngine(BaseQueryEngine):
    """自定义查询引擎，支持文档过滤"""
    
    def __init__(
        self,
        index: VectorStoreIndex,
        target_files: Optional[List[str]] = None,
        similarity_top_k: int = 5,
        streaming: bool = True,
        llm: Optional[Any] = None,
        callback_manager: Optional[CallbackManager] = None
    ):
        """
        初始化过滤查询引擎
        
        Args:
            index: 向量存储索引
            target_files: 目标文件名列表，None表示全知识库
            similarity_top_k: 相似度检索的top-k数量
            streaming: 是否启用流式响应
            llm: 语言模型实例
            callback_manager: 回调管理器
        """
        # 如果没有提供回调管理器，创建一个新的，避免回调栈状态问题
        if callback_manager is None:
            from llama_index.core.callbacks import CallbackManager
            callback_manager = CallbackManager()
        
        super().__init__(callback_manager=callback_manager)
        self.index = index
        self.target_files = target_files
        self.similarity_top_k = similarity_top_k
        self.streaming = streaming
        self.llm = llm
        
        # 创建基础查询引擎
        self._base_query_engine = None
        self._create_base_query_engine()
        
        logger.info(f"初始化过滤查询引擎，目标文件: {self.target_files}, top_k: {self.similarity_top_k}")
    
    def query(self, query_str: str):
        """
        同步查询方法
        
        Args:
            query_str: 查询字符串
            
        Returns:
            查询响应
        """
        from llama_index.core.schema import QueryBundle
        query_bundle = QueryBundle(query_str)
        return self._query(query_bundle)
    
    def _create_base_query_engine(self):
        """创建基础查询引擎"""
        try:
            # 创建后处理器列表
            postprocessors = []
            
            # 如果有目标文件，添加文件过滤后处理器
            if self.target_files:
                file_filter = FileFilterPostprocessor(self.target_files)
                postprocessors.append(file_filter)
                logger.info(f"添加文件过滤后处理器，目标文件: {self.target_files}")
            
            # 创建查询引擎（不传递 callback_manager，避免重复参数错误）
            if self.llm:
                self._base_query_engine = self.index.as_query_engine(
                    similarity_top_k=self.similarity_top_k,
                    node_postprocessors=postprocessors,
                    streaming=self.streaming,
                    llm=self.llm
                )
            else:
                self._base_query_engine = self.index.as_query_engine(
                    similarity_top_k=self.similarity_top_k,
                    node_postprocessors=postprocessors,
                    streaming=self.streaming
                )
            
            logger.info("✅ 基础查询引擎创建成功")
            
        except Exception as e:
            logger.error(f"❌ 创建基础查询引擎失败: {e}")
            raise e
    
    def _query(self, query_bundle: QueryBundle):
        """
        执行查询
        
        Args:
            query_bundle: 查询包
            
        Returns:
            查询响应
        """
        try:
            logger.info(f"🔍 执行查询: {query_bundle.query_str[:50]}...")
            
            if self._base_query_engine is None:
                raise RuntimeError("基础查询引擎未初始化")
            
            # 执行查询（过滤由后处理器自动处理）
            response = self._base_query_engine._query(query_bundle)
            
            logger.info("✅ 查询执行成功")
            return response
            
        except IndexError as e:
            if "pop from empty list" in str(e):
                logger.warning(f"⚠️ 检测到回调管理器栈状态问题，尝试重置回调管理器: {e}")
                # 重置回调管理器状态
                try:
                    from llama_index.core.callbacks import CallbackManager
                    self.callback_manager = CallbackManager()
                    # 重新创建基础查询引擎
                    self._create_base_query_engine()
                    # 重试查询
                    response = self._base_query_engine._query(query_bundle)
                    logger.info("✅ 查询执行成功（重试后）")
                    return response
                except Exception as retry_e:
                    logger.error(f"❌ 重试查询失败: {retry_e}")
                    raise e
            else:
                logger.error(f"❌ 查询执行失败: {e}")
                raise e
        except Exception as e:
            logger.error(f"❌ 查询执行失败: {e}")
            raise e
    
    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """
        检索相关节点
        
        Args:
            query_bundle: 查询包
            
        Returns:
            检索到的节点列表
        """
        try:
            logger.info(f"🔍 检索节点: {query_bundle.query_str[:50]}...")
            
            if self._base_query_engine is None:
                raise RuntimeError("基础查询引擎未初始化")
            
            nodes = self._base_query_engine._retrieve(query_bundle)
            
            logger.info(f"✅ 检索完成，找到 {len(nodes)} 个节点")
            return nodes
            
        except Exception as e:
            logger.error(f"❌ 节点检索失败: {e}")
            raise e
    
    def get_target_files(self) -> Optional[List[str]]:
        """获取目标文件列表"""
        return self.target_files
    
    def set_target_files(self, target_files: Optional[List[str]]):
        """设置目标文件列表"""
        self.target_files = target_files
        logger.info(f"更新目标文件列表: {self.target_files}")
        
        # 重新创建基础查询引擎以应用新的过滤条件
        self._create_base_query_engine()
    
    async def _aquery(self, query_bundle: QueryBundle):
        """
        异步查询方法
        
        Args:
            query_bundle: 查询包
            
        Returns:
            查询响应
        """
        # 对于我们的用例，直接调用同步方法
        return self._query(query_bundle)
    
    def _get_prompt_modules(self):
        """
        获取提示模块
        
        Returns:
            提示模块字典
        """
        return {}
