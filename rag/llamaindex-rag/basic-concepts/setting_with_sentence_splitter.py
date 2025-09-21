from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.ollama import Ollama
from langchain_deepseek import ChatDeepSeek
from llama_index.embeddings.ollama import OllamaEmbedding

documents = SimpleDirectoryReader("./data").load_data()

print(f"加载了 {len(documents)} 个文档")

# global
from llama_index.core import Settings

Settings.text_splitter = SentenceSplitter(chunk_size=10240, chunk_overlap=20)

Settings.llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.1,
    max_tokens=1000,
    timeout=60,
    max_retries=2,
)

# 初始化Ollama模型 - 使用更轻量级的配置
# Settings.llm = Ollama(
#     model="qwen:7b",
#     request_timeout=120,  # 减少超时时间到2分钟
#     keep_alive="2m",  # 减少保持连接时间
#     num_thread=4,  # 减少线程数
#     temperature=0.1,  # 降低温度以获得更稳定的回答
#     system_prompt="你是一个专业的知识助手。请基于提供的上下文给出精准、简洁的回答。"
# )

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    request_timeout=30,  # 减少嵌入请求超时时间
    keep_alive="1m"  # 减少保持连接时间
)

# per-index
index = VectorStoreIndex.from_documents(
    documents
)

print(f"索引中的节点数量: {len(index.docstore.docs)}")

response = index.as_query_engine().query("文档的主题是什么?")
print(response)