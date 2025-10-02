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
            
            # 如果有目标文件过滤需求，手动应用过滤
            if self.target_files:
                logger.info(f"🔍 手动应用文件过滤，目标文件: {self.target_files}")
                
                # 先尝试从目标文件中检索更多节点
                target_nodes = self._retrieve_from_target_files(query_bundle)
                logger.info(f"🔍 从目标文件检索到 {len(target_nodes)} 个节点")
                
                # 如果目标文件节点不够，尝试关键词检索
                if len(target_nodes) < self.similarity_top_k:
                    logger.info(f"🔍 目标文件节点不足，尝试关键词检索")
                    
                    # 从目标文件名中提取关键词
                    keywords = self._extract_keywords_from_target_files()
                    logger.info(f"🔍 提取的关键词: {keywords}")
                    
                    # 尝试使用关键词检索
                    keyword_nodes = []
                    for keyword in keywords:
                        if keyword and len(keyword) > 1:  # 过滤掉太短的词
                            logger.info(f"🔍 尝试关键词检索: '{keyword}'")
                            keyword_query = QueryBundle(keyword)
                            nodes = self._retrieve(keyword_query)
                            filtered_nodes = self._apply_file_filter(nodes)
                            keyword_nodes.extend(filtered_nodes)
                            logger.info(f"🔍 关键词 '{keyword}' 找到 {len(filtered_nodes)} 个目标文件节点")
                    
                    # 合并并去重
                    all_target_nodes = self._merge_nodes(target_nodes, keyword_nodes)
                    
                    # 如果还是没有足够的节点，进行全局检索
                    if len(all_target_nodes) < self.similarity_top_k:
                        logger.info(f"🔍 关键词检索后仍不足，进行全局检索补充")
                        global_nodes = self._retrieve(query_bundle)
                        filtered_global_nodes = self._apply_file_filter(global_nodes)
                        all_target_nodes = self._merge_nodes(all_target_nodes, filtered_global_nodes)
                else:
                    all_target_nodes = target_nodes
                
                logger.info(f"🔍 最终目标文件节点数: {len(all_target_nodes)}")
                
                if not all_target_nodes:
                    logger.warning("⚠️ 目标文件中没有相关节点，返回空响应")
                    # 返回一个空的响应
                    from llama_index.core import Response
                    return Response(response="根据提供的文档，我无法找到相关信息。", source_nodes=[])
                
                # 手动构建响应
                from llama_index.core import Response
                response = Response(
                    response="",  # 这里需要调用 LLM 生成回答
                    source_nodes=all_target_nodes
                )
                
                # 如果有 LLM，生成回答
                if self.llm:
                    # 构建上下文
                    context_str = "\n\n".join([node.node.text for node in all_target_nodes])
                    prompt = f"基于以下上下文信息回答问题：\n\n上下文：\n{context_str}\n\n问题：{query_bundle.query_str}\n\n回答："
                    
                    llm_response = self.llm.complete(prompt)
                    response.response = str(llm_response)
                
                logger.info("✅ 查询执行成功（手动过滤）")
                return response
            else:
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
            
            # 使用检索器的 retrieve 方法
            if hasattr(self._base_query_engine, '_retriever'):
                nodes = self._base_query_engine._retriever.retrieve(query_bundle)
            else:
                # 如果没有 _retriever 属性，尝试直接调用 retrieve
                nodes = self._base_query_engine.retrieve(query_bundle)
            
            logger.info(f"✅ 检索完成，找到 {len(nodes)} 个节点")
            return nodes
            
        except Exception as e:
            logger.error(f"❌ 节点检索失败: {e}")
            raise e
    
    def _retrieve_from_target_files(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """
        专门从目标文件中检索节点
        
        Args:
            query_bundle: 查询包
            
        Returns:
            从目标文件中检索到的节点列表
        """
        try:
            logger.info(f"🔍 从目标文件检索节点: {query_bundle.query_str[:50]}...")
            
            if not self.target_files:
                logger.info("无目标文件限制，返回空列表")
                return []
            
            # 增加检索数量，确保能获取到足够的节点
            increased_top_k = max(self.similarity_top_k * 3, 20)
            
            # 使用检索器检索更多节点
            if hasattr(self._base_query_engine, '_retriever'):
                nodes = self._base_query_engine._retriever.retrieve(query_bundle)
            else:
                nodes = self._base_query_engine.retrieve(query_bundle)
            
            logger.info(f"🔍 检索到 {len(nodes)} 个节点")
            
            # 过滤出目标文件的节点
            target_nodes = self._apply_file_filter(nodes)
            
            # 只返回前 similarity_top_k 个节点
            final_nodes = target_nodes[:self.similarity_top_k]
            
            logger.info(f"✅ 从目标文件检索完成，找到 {len(final_nodes)} 个节点")
            return final_nodes
            
        except Exception as e:
            logger.error(f"❌ 从目标文件检索失败: {e}")
            return []
    
    def _merge_nodes(self, nodes1: List[NodeWithScore], nodes2: List[NodeWithScore]) -> List[NodeWithScore]:
        """
        合并两个节点列表，去除重复
        
        Args:
            nodes1: 第一个节点列表
            nodes2: 第二个节点列表
            
        Returns:
            合并后的节点列表
        """
        # 使用节点ID去重
        seen_ids = set()
        merged_nodes = []
        
        # 先添加第一个列表的节点
        for node in nodes1:
            node_id = node.node.id_
            if node_id not in seen_ids:
                seen_ids.add(node_id)
                merged_nodes.append(node)
        
        # 再添加第二个列表的节点
        for node in nodes2:
            node_id = node.node.id_
            if node_id not in seen_ids:
                seen_ids.add(node_id)
                merged_nodes.append(node)
        
        # 按分数排序
        merged_nodes.sort(key=lambda x: x.score, reverse=True)
        
        logger.info(f"合并节点完成，节点1: {len(nodes1)}, 节点2: {len(nodes2)}, 合并后: {len(merged_nodes)}")
        return merged_nodes
    
    def _apply_file_filter(self, nodes: List[NodeWithScore]) -> List[NodeWithScore]:
        """
        应用文件过滤
        
        Args:
            nodes: 待过滤的节点列表
            
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
    
    def _extract_keywords_from_target_files(self) -> List[str]:
        """
        从目标文件名中提取关键词
        
        Returns:
            提取的关键词列表
        """
        keywords = []
        
        for file_name in self.target_files:
            # 移除文件扩展名
            name_without_ext = file_name.replace('.pdf', '').replace('.md', '').replace('.txt', '')
            
            # 简单的关键词提取逻辑
            # 对于中文文件名，可以按字符分割或使用常见分隔符
            if '及' in name_without_ext:
                parts = name_without_ext.split('及')
                keywords.extend([part.strip() for part in parts if part.strip()])
            elif '与' in name_without_ext:
                parts = name_without_ext.split('与')
                keywords.extend([part.strip() for part in parts if part.strip()])
            elif '和' in name_without_ext:
                parts = name_without_ext.split('和')
                keywords.extend([part.strip() for part in parts if part.strip()])
            else:
                # 如果没有分隔符，尝试提取关键词
                # 对于"软件工程及DDD大模型"，提取"软件工程"、"DDD"、"大模型"
                if '软件工程' in name_without_ext:
                    keywords.append('软件工程')
                if 'DDD' in name_without_ext:
                    keywords.append('DDD')
                if '大模型' in name_without_ext:
                    keywords.append('大模型')
                if 'Agent' in name_without_ext:
                    keywords.append('Agent')
                if '架构' in name_without_ext:
                    keywords.append('架构')
            
            # 添加完整文件名作为关键词
            keywords.append(name_without_ext)
        
        # 去重并过滤
        unique_keywords = list(set(keywords))
        filtered_keywords = [kw for kw in unique_keywords if kw and len(kw) > 1]
        
        logger.info(f"从目标文件 {self.target_files} 提取关键词: {filtered_keywords}")
        return filtered_keywords
    
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
