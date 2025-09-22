from pathlib import Path
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Settings
)

from llama_index.core.schema import MetadataMode
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.readers.file import (
    PDFReader,
    DocxReader,
    PandasExcelReader,
    MarkdownReader
)
import chromadb
import datetime
from langchain_deepseek import ChatDeepSeek

class DeepSeekRAGSystem:
    def __init__(self,
                 model_name: str = "deepseek-chat",
                 embed_model: str = "nomic-embed-text",
                 chroma_path: str = "./chroma_db",
                 document_dir: str = "./documents"):

        Settings.llm = ChatDeepSeek(
            model=model_name,
            temperature=0.1,
            max_tokens=1000,
            timeout=60,
            max_retries=2,
        )

        # 初始化嵌入模型 - 使用更轻量级的配置
        Settings.embed_model = OllamaEmbedding(
            model_name=embed_model,
            request_timeout=30,  # 减少嵌入请求超时时间
            keep_alive="1m"  # 减少保持连接时间
        )

        # 配置文档解析器
        self.reader_config = {
            ".pdf": PDFReader(),
            ".docx": DocxReader(),
            ".xlsx": PandasExcelReader(sheet_name=None, concat_rows=True),
            ".xls": PandasExcelReader(sheet_name="Sheet1"),
            ".md": MarkdownReader()
        }

        # 初始化向量数据库
        chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.vector_store = ChromaVectorStore(
            chroma_collection=chroma_client.get_or_create_collection("deepseek_rag_epl")
        )
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )

        # 初始化节点分割器 - 使用更大的块以减少节点数量
        from llama_index.core.node_parser import SentenceSplitter
        Settings.node_parser = SentenceSplitter(
            chunk_size=1024,  # 更大的块大小以减少节点数量
            chunk_overlap=100,  # 适度的重叠
            separator="\n"
        )

        # 加载文档
        self.document_dir = document_dir
        self._load_documents()

    def _load_documents(self):
        """加载多格式文档"""
        documents = []

        print(f"开始加载文档...{self.document_dir}")
        
        file_count = 0
        for file_path in Path(self.document_dir).glob("*"):
            file_count += 1
            print(f"发现文件 {file_count}: {file_path}")
            print(f"文件后缀: {file_path.suffix.lower()}")
            print(f"支持的文件类型: {list(self.reader_config.keys())}")

            if file_path.suffix.lower() in self.reader_config:
                print(f"开始加载文档：{file_path}")
                try:
                    loader = self.reader_config[file_path.suffix.lower()]
                    docs = loader.load_data(file=file_path)
                    print(f"成功加载 {len(docs)} 个文档片段")

                    for i, doc in enumerate(docs):
                        doc.metadata = {"filename": str(file_path)}
                        content = doc.get_content(metadata_mode=MetadataMode.LLM)
                    documents.extend(docs)
                except Exception as e:
                    print(f"加载文档 {file_path} 时出错: {e}")
            else:
                print(f"不支持的文件类型: {file_path.suffix}")

        print(f"总共加载了 {len(documents)} 个文档")
        print("文档加载完成")

        # 构建索引
        print("开始分割文档...")
        nodes = Settings.node_parser.get_nodes_from_documents(documents)
        print(f"文档分割完成，共生成 {len(nodes)} 个节点")

        print("开始构建向量索引...")
        self.storage_context.docstore.add_documents(nodes)
        
        # 使用向量存储索引
        self.vector_index = VectorStoreIndex(
            nodes=nodes,
            storage_context=self.storage_context,
            embed_model=Settings.embed_model,
            show_progress=True  # 显示进度
        )
        print("向量索引构建完成")

    def query(self, question: str, similarity_top_k: int = 5) -> str:
        """执行增强检索"""
        try:
            print(f"开始执行增强检索，问题: {question[:100]}...")
            
            query_engine = self.vector_index.as_query_engine(
                similarity_top_k=similarity_top_k,  # 减少检索数量
                response_mode="compact",  # 使用compact模式减少响应时间
                streaming=False,  # 关闭流式响应
                similarity_threshold=0.6  # 降低相似度阈值
            )

            print("查询引擎创建成功，开始查询...")
            response = query_engine.query(question)
            
            if hasattr(response, 'response') and response.response:
                return str(response.response)
            elif hasattr(response, 'message') and response.message:
                return str(response.message)
            else:
                return str(response)
                
        except Exception as e:
            print(f"查询过程中出现错误: {e}")
            return f"查询出错: {str(e)}"

# 使用示例
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    start_time = datetime.datetime.now()
    print(f"开始时间: {start_time}")

    rag = DeepSeekRAGSystem(
        model_name="deepseek-chat",  # 使用更轻量级的模型
        document_dir="./documents"
    )

    # 使用更简单的问题进行测试
    question = "你是编写书评的作者，请总结这篇文章的主题，并以要点形式给出。"
    answer = rag.query(question)
    print(f"问题：{question}\n回答：{answer}")
    #
    # question = "什么是领域驱动架构？它的特征是什么？它和领域驱动设计的关系是什么？"
    # answer = rag.query(question)
    # print(f"问题：{question}\n回答：{answer}")