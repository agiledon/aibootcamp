import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine import RouterQueryEngine, RetrieverQueryEngine
from llama_index.core.selectors import PydanticSingleSelector
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.postprocessor import SimilarityPostprocessor
# from llama_index.llms.openai import OpenAI
# from llama_index.embeddings.openai import OpenAIEmbedding

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# # 设置你的OpenAI API密钥
# os.environ["OPENAI_API_KEY"] = "你的OPENAI_API_KEY"

# # 初始化LLM和嵌入模型（使用最新API）
# llm = OpenAI(model="gpt-3.5-turbo")
# embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# from langchain_deepseek import ChatDeepSeek
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

# llm = ChatDeepSeek(
#     model="deepseek-chat",
#     temperature=0.1,
#     max_tokens=1000,
#     timeout=60,
#     max_retries=2,
# )
llm = DeepSeek(
    model="deepseek-chat",  # 使用支持函数调用的模型
    temperature=0.1,
    max_tokens=1000,
    timeout=60,
    max_retries=2,
)
embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    request_timeout=30,
    keep_alive="1m",
)

# 设置全局 Settings 确保所有组件使用正确的模型
Settings.llm = llm
Settings.embed_model = embed_model

# 1. 加载文档并构建索引
documents = SimpleDirectoryReader("./data").load_data()  # 确保你的文档放在项目目录下的'data'文件夹中

# 使用节点解析器进行文档分块
node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
nodes = node_parser.get_nodes_from_documents(documents)

# 创建向量索引
vector_index = VectorStoreIndex(nodes, embed_model=embed_model)

# 2. 配置检索器 - 使用VectorIndexRetriever[6,10](@ref)
vector_retriever = VectorIndexRetriever(
    index=vector_index,
    similarity_top_k=5,  # 检索最相关的5个节点
)

# 3. 配置节点后处理器 - 使用SimilarityPostprocessor进行相似度过滤[7,10](@ref)
similarity_postprocessor = SimilarityPostprocessor(similarity_cutoff=0.7)  # 过滤相似度低于0.7的节点

# 4. 配置响应合成器 - 使用get_response_synthesizer[6,9](@ref)
response_synthesizer = get_response_synthesizer(
    llm=llm,
    response_mode="compact",  # 响应模式：'compact', 'refine', 'tree_summarize'等[6,9](@ref)
)

# 5. 组装基础查询引擎（组合了检索器、后处理器和响应合成器）[6,9,10](@ref)
base_query_engine = RetrieverQueryEngine(
    retriever=vector_retriever,
    node_postprocessors=[similarity_postprocessor],
    response_synthesizer=response_synthesizer,
)

# 6. 创建另一个不同配置的查询引擎作为路由候选（例如：用于摘要的引擎）[3](@ref)
summary_index = VectorStoreIndex(nodes, embed_model=embed_model)  # 明确指定嵌入模型
summary_query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize",  # 使用树状摘要模式进行总结[3,9](@ref)
    llm=llm
)

# 7. 将两个查询引擎封装成工具，并提供清晰的描述以便路由选择[3](@ref)
query_engine_tools = [
    QueryEngineTool.from_defaults(
        query_engine=base_query_engine,
        description="适用于从文档中检索具体事实、细节和上下文的查询。例如：询问特定的事件、人物、概念或关系。",
    ),
    QueryEngineTool.from_defaults(
        query_engine=summary_query_engine,
        description="适用于对文档或特定主题进行摘要、概述或获取高层次观点的查询。例如：总结文档主要内容或某个章节的大意。",
    ),
]

# 8. 创建路由查询引擎（组合了路由器）[3](@ref)
router_query_engine = RouterQueryEngine(
    selector=PydanticSingleSelector.from_defaults(llm=llm),  # 使用Pydantic选择器进行路由决策[3](@ref)
    query_engine_tools=query_engine_tools,
)

# 9. 执行查询
# response = router_query_engine.query("文档中提到的关键技术有哪些？")
response = router_query_engine.query("文档中提到的分析模式该如何运用？")
print(response)

# 打印来源节点信息以验证后处理效果
print("\n来源信息:")
for idx, node in enumerate(response.source_nodes):
    print(f"{idx + 1}. 文档片段: {node.text[:100]}... | 相似度得分: {node.score:.4f}")