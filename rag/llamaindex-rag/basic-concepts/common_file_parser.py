from llama_index.core.node_parser import (
    SimpleFileNodeParser, 
    MarkdownNodeParser, 
    HTMLNodeParser, 
    JSONNodeParser,
    CodeSplitter
)
from llama_index.readers.file import FlatReader
from llama_index.core import SimpleDirectoryReader
from pathlib import Path
import os

def get_parser_by_file_extension(file_path):
    """
    根据文件扩展名返回合适的解析器
    
    Args:
        file_path: 文件路径
    
    Returns:
        对应的解析器实例
    """
    file_extension = Path(file_path).suffix.lower()
    
    parser_map = {
        '.md': MarkdownNodeParser(),
        '.markdown': MarkdownNodeParser(),
        '.html': HTMLNodeParser(),
        '.htm': HTMLNodeParser(),
        '.json': JSONNodeParser(),
        '.py': CodeSplitter(language="python", chunk_lines=40, chunk_lines_overlap=15),
        '.js': CodeSplitter(language="javascript", chunk_lines=40, chunk_lines_overlap=15),
        '.ts': CodeSplitter(language="typescript", chunk_lines=40, chunk_lines_overlap=15),
        '.java': CodeSplitter(language="java", chunk_lines=40, chunk_lines_overlap=15),
        '.cpp': CodeSplitter(language="cpp", chunk_lines=40, chunk_lines_overlap=15),
        '.c': CodeSplitter(language="c", chunk_lines=40, chunk_lines_overlap=15),
        '.cs': CodeSplitter(language="csharp", chunk_lines=40, chunk_lines_overlap=15),
        '.php': CodeSplitter(language="php", chunk_lines=40, chunk_lines_overlap=15),
        '.rb': CodeSplitter(language="ruby", chunk_lines=40, chunk_lines_overlap=15),
        '.go': CodeSplitter(language="go", chunk_lines=40, chunk_lines_overlap=15),
        '.rs': CodeSplitter(language="rust", chunk_lines=40, chunk_lines_overlap=15),
        '.txt': SimpleFileNodeParser(),
    }
    
    return parser_map.get(file_extension, SimpleFileNodeParser())


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

# 加载data文件夹下的所有文件
data_path = Path("data")
all_docs = []
file_doc_mapping = {}  # 存储文件路径到文档的映射

# 获取data文件夹下的所有文件
for file_path in data_path.iterdir():
    if file_path.is_file():
        print(f"发现文件: {file_path}")
        # 使用FlatReader加载单个文件
        file_docs = FlatReader().load_data(file_path)
        
        # 为每个文档添加文件路径信息
        for doc in file_docs:
            # 手动设置文件路径元数据
            doc.metadata['file_path'] = str(file_path)
            doc.metadata['file_name'] = file_path.name
            doc.metadata['file_extension'] = file_path.suffix.lower()
            
            # 存储映射关系
            file_doc_mapping[str(file_path)] = doc
        
        all_docs.extend(file_docs)

print(f"\n总共加载了 {len(all_docs)} 个文档")

# 调试：检查文档元数据
print("\n调试：检查文档元数据")
for i, doc in enumerate(all_docs[:3]):  # 只检查前3个文档
    print(f"文档 {i+1} 元数据:")
    print(f"  file_path: {doc.metadata.get('file_path', '未设置')}")
    print(f"  file_name: {doc.metadata.get('file_name', '未设置')}")
    print(f"  file_extension: {doc.metadata.get('file_extension', '未设置')}")
    print(f"  其他元数据: {doc.metadata}")

# 按文件类型分组处理
file_type_groups = {}

for doc in all_docs:
    # 从文档的metadata中获取文件扩展名
    file_extension = doc.metadata.get('file_extension', '')
    if not file_extension:
        # 如果没有扩展名，尝试从file_path获取
        file_path = doc.metadata.get('file_path', '')
        if file_path:
            file_extension = Path(file_path).suffix.lower()
        else:
            file_extension = '.txt'  # 默认为文本文件
    
    if file_extension not in file_type_groups:
        file_type_groups[file_extension] = []
    
    file_type_groups[file_extension].append(doc)

print(f"\n按文件类型分组:")
for ext, docs in file_type_groups.items():
    print(f"  {ext}: {len(docs)} 个文件")

# 对每种文件类型使用对应的解析器
all_nodes = []

for file_extension, docs in file_type_groups.items():
    if not docs:
        continue
    
    print(f"\n处理 {file_extension} 文件...")
    print(f"文件列表: {[doc.metadata.get('file_name', 'unknown') for doc in docs]}")
    
    # 获取对应的解析器
    parser = get_parser_by_file_extension(f"dummy{file_extension}")
    parser_name = parser.__class__.__name__
    
    print(f"使用解析器: {parser_name}")
    
    try:
        # 使用对应的解析器解析文档
        nodes = parser.get_nodes_from_documents(docs)
        all_nodes.extend(nodes)
        
        print(f"解析得到 {len(nodes)} 个节点")
        
        # 显示前2个节点的信息
        if nodes:
            print_nodes_info(nodes, f"{parser_name} 解析结果 - {file_extension} 文件", max_nodes=2)
        
    except Exception as e:
        print(f"解析 {file_extension} 文件时出错: {e}")
        print(f"错误详情: {type(e).__name__}")
        
        # 如果专用解析器失败，回退到SimpleFileNodeParser
        print(f"回退到 SimpleFileNodeParser")
        try:
            fallback_parser = SimpleFileNodeParser()
            nodes = fallback_parser.get_nodes_from_documents(docs)
            all_nodes.extend(nodes)
            print(f"回退解析成功，得到 {len(nodes)} 个节点")
            print_nodes_info(nodes, f"SimpleFileNodeParser 解析结果 - {file_extension} 文件", max_nodes=2)
        except Exception as fallback_error:
            print(f"回退解析也失败: {fallback_error}")
            print(f"跳过 {file_extension} 文件的处理")

print(f"\n所有解析器总共产生了 {len(all_nodes)} 个节点")

# 显示所有节点的统计信息
print(f"\n{'='*50}")
print("最终统计信息")
print(f"{'='*50}")
print(f"总文件数: {len(all_docs)}")
print(f"总节点数: {len(all_nodes)}")
print(f"支持的文件类型: {list(file_type_groups.keys())}")

# 备用方法：使用SimpleDirectoryReader
# print(f"\n{'='*50}")
# print("备用方法：使用SimpleDirectoryReader")
# print(f"{'='*50}")

# try:
#     # 使用SimpleDirectoryReader加载所有文件
#     simple_docs = SimpleDirectoryReader("data").load_data()
#     print(f"SimpleDirectoryReader加载了 {len(simple_docs)} 个文档")
    
#     # 检查SimpleDirectoryReader的元数据
#     print("\nSimpleDirectoryReader的文档元数据:")
#     for i, doc in enumerate(simple_docs[:3]):
#         print(f"文档 {i+1} 元数据:")
#         print(f"  {doc.metadata}")
        
#     # 使用SimpleFileNodeParser解析所有文档
#     simple_parser = SimpleFileNodeParser()
#     simple_nodes = simple_parser.get_nodes_from_documents(simple_docs)
#     print(f"\nSimpleDirectoryReader + SimpleFileNodeParser 解析得到 {len(simple_nodes)} 个节点")
    
#     # 显示前2个节点
#     print_nodes_info(simple_nodes, "SimpleDirectoryReader 解析结果", max_nodes=2)
    
# except Exception as e:
#     print(f"SimpleDirectoryReader方法失败: {e}")


from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

from langchain_deepseek import ChatDeepSeek

Settings.llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.1,
    max_tokens=1000,
    timeout=60,
    max_retries=2,
)

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    request_timeout=30,  # 减少嵌入请求超时时间
    keep_alive="1m"  # 减少保持连接时间
)

from llama_index.core import VectorStoreIndex

index = VectorStoreIndex(all_nodes)

# response = index.as_query_engine().query("DDD的价值包括哪些，请给出详细的解释。如果文档中有相关内容，请给出具体内容。")
response = index.as_query_engine().query("请分析MultiHeadAttention类的主要作用和实现原理。")
print(response)