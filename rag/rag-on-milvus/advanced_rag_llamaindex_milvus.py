from dotenv import load_dotenv
load_dotenv()

# 启动Milvus Server
from milvus import MilvusServer
import time

print("Starting Milvus Server...")
milvus_server = MilvusServer()
milvus_server.start()
print("Milvus Server started successfully!")

# 等待服务完全启动
time.sleep(3)

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

# 将LLM和embed_model设置到LlamaIndex的全局Settings中
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

from llama_index.core import SimpleDirectoryReader

# Load data
documents = SimpleDirectoryReader(
        input_files=["./data/milvus_doc.md"]
).load_data()

print("Document ID:", documents[0].doc_id)

from llama_index.core.node_parser import SentenceWindowNodeParser

# Create the sentence window node parser 
node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,
    window_metadata_key="window",
    original_text_metadata_key="original_text",
)

# Extract nodes from documents
nodes = node_parser.get_nodes_from_documents(documents)

print("len(nodes):", len(nodes))

from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.milvus import  MilvusVectorStore
from llama_index.core import StorageContext

vector_store = MilvusVectorStore(dim=768,  # nomic-embed-text模型的维度
                                 uri="http://localhost:19530",  # Milvus默认端口
                                 collection_name='advance_rag',
                                 overwrite=True)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex(
    nodes, 
    storage_context=storage_context
)

from llama_index.core.postprocessor import MetadataReplacementPostProcessor

# The target key defaults to `window` to match the node_parser's default
postproc = MetadataReplacementPostProcessor(
    target_metadata_key="window"
)

from llama_index.core.postprocessor import SentenceTransformerRerank

# BAAI/bge-reranker-base is a cross-encoder model
# link: https://huggingface.co/BAAI/bge-reranker-base
rerank = SentenceTransformerRerank(
    top_n = 3, 
    model = "BAAI/bge-reranker-base" 
)

# The QueryEngine class is equipped with the generator and facilitates the retrieval and generation steps
query_engine = index.as_query_engine(
    similarity_top_k = 3, 
    node_postprocessors = [postproc, rerank],
)

response = query_engine.query(
    "Can user delete milvus entities through non-primary key filtering?"
)
print(str(response))

# 程序结束时优雅关闭Milvus Server
print("\nShutting down Milvus Server...")
milvus_server.stop()
print("Milvus Server stopped successfully!")