import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.core import SummaryIndex

# load documents
documents = SimpleDirectoryReader(input_files=["data/paul_graham_essay.txt"]).load_data()

# get nodes
from llama_index.core import Settings
# Set LLM and embedding to avoid OpenAI defaults
from langchain_deepseek import ChatDeepSeek
from llama_index.embeddings.ollama import OllamaEmbedding

Settings.llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.1,
    max_tokens=1000,
    timeout=60,
    max_retries=2,
)
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    request_timeout=30,
    keep_alive="1m",
)

# initialize settings (set chunk size)
Settings.chunk_size = 1024
nodes = Settings.node_parser.get_nodes_from_documents(documents)

# initialize storage context (by default it's in-memory)
storage_context = StorageContext.from_defaults()
storage_context.docstore.add_documents(nodes)

# define summary index & vector index on the same data
summary_index = SummaryIndex(nodes, storage_context=storage_context)
vector_index = VectorStoreIndex(nodes, storage_context=storage_context)

from llama_index.core.tools import QueryEngineTool

list_query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize", use_async=True
)
vector_query_engine = vector_index.as_query_engine(
    response_mode="tree_summarize", use_async=True
)

# wrap query engine by using QueryEngineTool
list_tool = QueryEngineTool.from_defaults(
    query_engine=list_query_engine,
    description="Useful for questions asking for a biography of the author.",
)
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description=(
        "Useful for retrieving specific snippets from the author's life, like"
        " his time in college, his time in YC, or more."
    ),
)

# define Object Index
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex

obj_index = ObjectIndex.from_objects(
    [list_tool, vector_tool],
    index_cls=VectorStoreIndex,
)

from llama_index.core.query_engine import ToolRetrieverRouterQueryEngine

query_engine = ToolRetrieverRouterQueryEngine(obj_index.as_retriever())

# response = query_engine.query("What is a biography of the author?")
response = query_engine.query("What is specific snippets from the author's life?")
print("response:", response)