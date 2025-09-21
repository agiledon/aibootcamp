from llama_index.core.node_parser import CodeSplitter
from llama_index.core import SimpleDirectoryReader
from langchain_deepseek import ChatDeepSeek

def print_nodes_info(nodes, title="节点信息", max_nodes=None):
    """
    遍历并打印所有节点的信息
    
    Args:
        nodes: 节点列表
        title: 打印标题
        max_nodes: 可选参数，指定要遍历的最大节点数量。如果为None，则遍历所有节点
    """
    print(f"\n{'='*20} {title} {'='*20}")
    print(f"解析得到的Node数量: {len(nodes)}")
    
    # 验证max_nodes参数
    if max_nodes is not None:
        if not isinstance(max_nodes, int) or max_nodes <= 0:
            raise ValueError("max_nodes必须是正整数")
        if max_nodes > len(nodes):
            raise ValueError(f"max_nodes ({max_nodes}) 不能超过节点总数 ({len(nodes)})")
        
        print(f"显示前 {max_nodes} 个节点:")
        nodes_to_show = nodes[:max_nodes]
    else:
        print("显示所有节点:")
        nodes_to_show = nodes
    
    for i, node in enumerate(nodes_to_show):
        print(f"\n--- Node {i+1} ---")
        print(f"Node长度: {len(node.text)} 字符")
        print(f"Node内容:")
        print(node.text)
        print("-" * 50)

llm = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0.1,
            max_tokens=1000,
            timeout=60,
            max_retries=2,
        )

##### CodeSplitter #####

python_code_docs = SimpleDirectoryReader(input_files=["data/multi_head_attention.py"]).load_data()

print(f"加载了 {len(python_code_docs)} 个文档")

splitter = CodeSplitter(
    language="python",
    chunk_lines=40,  # lines per chunk
    chunk_lines_overlap=15,  # lines overlap between chunks
    max_chars=1500,  # max chars per chunk
)
nodes = splitter.get_nodes_from_documents(python_code_docs)

# print_nodes_info(nodes, "CodeSplitter 解析结果")

##### SentenceWindowNodeParser #####

from llama_index.core.node_parser import SentenceWindowNodeParser

node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,
    window_metadata_key="window",
    original_text_metadata_key="original_text",
)
text_docs = SimpleDirectoryReader(input_files=["data/ddd01.txt", "data/ddd02.txt"]).load_data()
print(f"加载了 {len(text_docs)} 个文档")

nodes = node_parser.get_nodes_from_documents(text_docs)

print_nodes_info(nodes, "SentenceWindowNodeParser 解析结果")

##### SemanticSplitterNodeParser #####

from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.ollama import OllamaEmbedding

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    request_timeout=30,  # 减少嵌入请求超时时间
    keep_alive="1m"  # 减少保持连接时间
)
splitter = SemanticSplitterNodeParser(
    buffer_size=2,  # 增加buffer_size，允许更多的句子重叠
    breakpoint_percentile_threshold=20,  # 降低阈值，更容易触发分割点
    embed_model=embed_model
)
nodes = splitter.get_nodes_from_documents(text_docs)

# print_nodes_info(nodes, "SemanticSplitterNodeParser 解析结果")

##### TokenTextSplitter #####

from llama_index.core.node_parser import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=1024,
    chunk_overlap=20,
    separator=" ",
)
nodes = splitter.get_nodes_from_documents(text_docs)

# 显示所有TokenTextSplitter节点
print_nodes_info(nodes, "TokenTextSplitter 解析结果")

# 只显示前2个TokenTextSplitter节点
print_nodes_info(nodes, "TokenTextSplitter 解析结果 - 前2个节点", max_nodes=2)

##### RecursiveCharacterTextSplitter #####
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index.core.node_parser import LangchainNodeParser

parser = LangchainNodeParser(RecursiveCharacterTextSplitter())
nodes = parser.get_nodes_from_documents(text_docs)

# 显示所有RecursiveCharacterTextSplitter节点
print_nodes_info(nodes, "RecursiveCharacterTextSplitter 解析结果")

# 只显示第1个RecursiveCharacterTextSplitter节点
print_nodes_info(nodes, "RecursiveCharacterTextSplitter 解析结果 - 第1个节点", max_nodes=1)