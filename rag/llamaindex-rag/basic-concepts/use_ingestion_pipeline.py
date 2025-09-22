from llama_index.core import Document
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline
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

# create the pipeline with transformations
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=25, chunk_overlap=0),
        TitleExtractor(),
    ]
)

# run the pipeline
nodes = pipeline.run(documents=[Document.example()])
print("len(nodes):", len(nodes))

# transformations with index building
from llama_index.core import VectorStoreIndex
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
)
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter

# transformations = [
#     TokenTextSplitter(chunk_size=512, chunk_overlap=128),
#     TitleExtractor(nodes=5),
#     QuestionsAnsweredExtractor(questions=3),
# ]

text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=128)
title_extractor = TitleExtractor(nodes=5)
qa_extractor = QuestionsAnsweredExtractor(questions=3)

Settings.transformations = [text_splitter, title_extractor, qa_extractor]

# per-index
index = VectorStoreIndex.from_documents(
    documents=[Document.example()]
)
print("len(index.docstore.docs):", len(index.docstore.docs))