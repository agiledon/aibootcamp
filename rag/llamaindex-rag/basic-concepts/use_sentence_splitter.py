from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import MetadataMode

# 使用 SimpleDirectoryReader 读取 data 文件夹中的 ddd01.txt 文件
reader = SimpleDirectoryReader(input_files=["data/ddd01.txt"])
documents = reader.load_data()

print(f"加载了 {len(documents)} 个文档")
print(f"第一个文档的内容长度: {len(documents[0].text)}")
print(f"第一个文档的前100个字符: {documents[0].text[:100]}...")

node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=20)

nodes = node_parser.get_nodes_from_documents(
    documents, show_progress=True
)
print("len(nodes):", len(nodes))
print("nodes[0]:", nodes[0])
print("nodes[0].text:", nodes[0].text)
print("nodes[0].metadata:", nodes[0].metadata)
print("nodes[0].excluded_llm_metadata_keys:", nodes[0].excluded_llm_metadata_keys)
print("nodes[0].metadata_seperator:", nodes[0].metadata_seperator)
print("nodes[0].metadata_template:", nodes[0].metadata_template)
print("nodes[0].text_template:", nodes[0].text_template)
print("nodes[0].get_content(metadata_mode=MetadataMode.LLM):", nodes[0].get_content(metadata_mode=MetadataMode.LLM))
print("nodes[0].get_content(metadata_mode=MetadataMode.EMBED):", nodes[0].get_content(metadata_mode=MetadataMode.EMBED))