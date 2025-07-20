import os
from pathlib import Path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings
)
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.schema import MetadataMode
from llama_index.llms.ollama import Ollama
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

        # 初始化Ollama模型 - 使用更轻量级的配置
        # Settings.llm = Ollama(
        #     model=model_name,
        #     request_timeout=120,  # 减少超时时间到2分钟
        #     keep_alive="2m",  # 减少保持连接时间
        #     num_thread=4,  # 减少线程数
        #     temperature=0.1,  # 降低温度以获得更稳定的回答
        #     system_prompt="你是一个专业的知识助手。请基于提供的上下文给出精准、简洁的回答。"
        # )

        Settings.llm = ChatDeepSeek(
            model=model_name,
            temperature=0.1,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            cache=True,
        )

        # 初始化嵌入模型 - 使用更轻量级的配置
        Settings.embed_model = OllamaEmbedding(
            model_name=embed_model,
            request_timeout=30,  # 减少嵌入请求超时时间
            keep_alive="1m"  # 减少保持连接时间
        )

        # # 设置全局超时时间（单位：秒）
        # Settings.global_timeout = 120  # 默认通常为60秒
        #
        # # 同时调整HTTP相关参数
        # Settings.http_retry_attempts = 5  # 重试次数
        # Settings.http_retry_delay = 10  # 重试间隔
        # Settings.http_timeout = (10.0, 120.0)  # (连接超时, 读取超时)

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
        print(f"文档目录是否存在: {Path(self.document_dir).exists()}")
        
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
                        print(f"文档片段 {i+1} 内容长度: {len(doc.get_content(metadata_mode=MetadataMode.LLM))}")
                        print("文档内容预览:")
                        content = doc.get_content(metadata_mode=MetadataMode.LLM)
                        print(f"{content[:200]}..." if len(content) > 200 else content)
                        print("文档的元数据:")
                        print(f"{doc.metadata}\n")
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
        
        # 使用更高效的索引构建方式
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
            print(f"向量索引中的节点数量: {len(self.vector_index.docstore.docs)}")
            
            # 简化查询问题，提取核心问题
            core_question = self._extract_core_question(question)
            print(f"核心问题: {core_question}")
            
            query_engine = self.vector_index.as_query_engine(
                similarity_top_k=3,  # 减少检索数量
                response_mode="compact",  # 使用compact模式减少响应时间
                streaming=False,  # 关闭流式响应
                similarity_threshold=0.5  # 降低相似度阈值
            )

            print("查询引擎创建成功，开始查询...")
            response = query_engine.query(core_question)
            
            print(f"查询完成，响应类型: {type(response)}")
            
            if hasattr(response, 'response') and response.response:
                return str(response.response)
            elif hasattr(response, 'message') and response.message:
                return str(response.message)
            else:
                return str(response)
                
        except Exception as e:
            print(f"查询过程中出现错误: {e}")
            return f"查询出错: {str(e)}"
    
    def _extract_core_question(self, question: str) -> str:
        """提取问题的核心部分"""
        # 如果问题包含任务描述，提取核心问题
        if "阅读以下文章内容并执行任务" in question:
            # 提取任务描述中的核心要求
            lines = question.split('\n')
            core_parts = []
            for line in lines:
                if line.strip().startswith('- **主要目标**') or line.strip().startswith('- **目标**'):
                    core_parts.append(line.strip())
            if core_parts:
                return "请分析文章结构并详细说明每个部分的内容和作用"
        
        # 如果问题太长，截取前200个字符
        if len(question) > 200:
            return question[:200] + "..."
        
        return question


# 使用示例
if __name__ == "__main__":
    # 初始化前需要确保Ollama服务已启动并下载模型
    # 终端执行：ollama pull deepseek-r1:7b
    from dotenv import load_dotenv
    load_dotenv()

    start_time = datetime.datetime.now()
    print(f"开始时间: {start_time}")

    rag = DeepSeekRAGSystem(
        model_name="deepseek-chat",  # 使用更轻量级的模型
        document_dir="./documents"
    )

    # question = "首先显示上传文档的全部数据，" \
    #            "然后为客户东风佛吉亚汽车内饰有限公司成都分公司统计承诺交期从2024年1月到2025年2月的产品订货数情况。" \
    #            "统计时，先筛选客户名称为东风佛吉亚汽车内饰有限公司成都分公司，并且承诺交期在2024年1月到2025年2月期间的数据，" \
    #            "然后在这些数据基础上，针对物料名称对订购数S进行分类统计，从而得到产品订货数情况。"
    # answer = rag.query(question)
    # print(f"问题：{question}\n回答：{answer}")

    # question = "请根据我提供的当前联赛排名进行数据分析，然后预测英格兰超级足球联赛24-25赛季可能的最终排名"
    # answer = rag.query(question)
    # print(f"问题：{question}\n回答：{answer}")

    # question = "净胜球为进球数减去失球数，请问哪一只队伍的净胜球为0"
    # answer = rag.query(question)
    # print(f"问题：{question}\n回答：{answer}")

    # 使用更简单的问题进行测试
    question = "这篇文章主要讲了什么内容？"
    answer = rag.query(question)
    print(f"问题：{question}\n回答：{answer}")
    #
    # question = "什么是领域驱动架构？它的特征是什么？它和领域驱动设计的关系是什么？"
    # answer = rag.query(question)
    # print(f"问题：{question}\n回答：{answer}")

    end_time = datetime.datetime.now()
    print(f"结束时间: {end_time}")

    duration = end_time - start_time
    print(f"消耗时间: {duration}")

    # 如果需要单独提取微秒
    total_seconds = duration.total_seconds()
    print(f"总秒数: {total_seconds} 秒")
    print(f"微秒: {duration.microseconds} 微秒")