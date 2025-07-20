import os
from pathlib import Path
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.ollama import Ollama
from llama_index.readers.file import DocxReader
import datetime
import re
from langchain_deepseek import ChatDeepSeek
from llama_index.embeddings.openai import OpenAIEmbedding


class MemoryRAGSystem:
    def __init__(self,
                 model_name: str = "deepseek-chat",
                 document_dir: str = "./documents"):

        # 初始化Ollama模型
        # Settings.llm = Ollama(
        #     model=model_name,
        #     request_timeout=60,
        #     temperature=0.1
        # )

        Settings.llm = ChatDeepSeek(
            model=model_name,
            temperature=0.1,
            max_tokens=1000,  # 限制最大token数
            timeout=60,  # 设置超时时间
            max_retries=2,
        )
        
        # 使用DeepSeek的嵌入模型
        Settings.embed_model = OpenAIEmbedding(
            model="text-embedding-3-small",  # 使用OpenAI兼容的嵌入模型
            api_base="https://api.deepseek.com/v1",  # DeepSeek API地址
            api_key=os.getenv("DEEPSEEK_API_KEY"),  # 从环境变量获取API密钥
            embed_batch_size=100,  # 批量处理以提高速度
        )

        # 配置文档解析器
        self.reader_config = {
            ".docx": DocxReader(),
        }

        # 初始化节点分割器
        self.node_parser = SentenceSplitter(
            chunk_size=512,
            chunk_overlap=50,
            separator="\n"
        )

        # 加载文档
        self.document_dir = document_dir
        self.document_chunks = []
        self._load_documents()

    def _load_documents(self):
        """加载多格式文档"""
        documents = []

        print(f"开始加载文档...{self.document_dir}")
        
        for file_path in Path(self.document_dir).glob("*"):
            print(f"发现文件: {file_path}")

            if file_path.suffix.lower() in self.reader_config:
                print(f"开始加载文档：{file_path}")
                try:
                    loader = self.reader_config[file_path.suffix.lower()]
                    docs = loader.load_data(file=file_path)
                    print(f"成功加载 {len(docs)} 个文档片段")

                    for doc in docs:
                        doc.metadata = {"filename": str(file_path)}
                    documents.extend(docs)
                except Exception as e:
                    print(f"加载文档 {file_path} 时出错: {e}")

        print(f"总共加载了 {len(documents)} 个文档")
        print("文档加载完成")

        # 分割文档
        print("开始分割文档...")
        nodes = self.node_parser.get_nodes_from_documents(documents)
        print(f"文档分割完成，共生成 {len(nodes)} 个节点")

        # 存储文档块
        for node in nodes:
            self.document_chunks.append({
                'content': node.get_content(),
                'metadata': node.metadata
            })
        
        print("文档块存储完成")

    def _simple_search(self, question: str, top_k: int = 2):
        """简单的关键词搜索"""
        # 提取问题中的关键词（过滤掉停用词）
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        keywords = [word for word in re.findall(r'\b\w+\b', question.lower()) if word not in stop_words and len(word) > 1]
        
        print(f"提取的关键词: {keywords}")
        
        # 计算每个文档块的相关性分数
        scores = []
        for i, chunk in enumerate(self.document_chunks):
            content_lower = chunk['content'].lower()
            score = sum(1 for keyword in keywords if keyword in content_lower)
            if score > 0:
                scores.append((score, i, chunk))
        
        # 如果没有找到匹配，返回前几个文档块
        if not scores:
            print("没有找到关键词匹配，返回前几个文档块")
            return self.document_chunks[:top_k]
        
        # 按分数排序并返回前top_k个
        scores.sort(reverse=True)
        return [chunk for score, i, chunk in scores[:top_k]]

    def query(self, question: str) -> str:
        """执行检索"""
        try:
            print(f"开始执行检索，问题: {question[:100]}...")
            
            # 使用简单搜索找到相关文档块
            relevant_chunks = self._simple_search(question, top_k=2)
            print(f"找到 {len(relevant_chunks)} 个相关文档块")
            
            if not relevant_chunks:
                return "抱歉，没有找到相关的文档内容来回答您的问题。"
            
            # 构建上下文（限制长度）
            context_parts = []
            total_length = 0
            for chunk in relevant_chunks:
                content = chunk['content']
                if total_length + len(content) > 2000:  # 限制上下文长度
                    break
                context_parts.append(content)
                total_length += len(content)
            
            context = "\n\n".join(context_parts)
            
            # 构建简化的提示
            prompt = f"""文档内容：{context}

问题：{question}

请简要回答这个问题。"""

            print("开始生成回答...")
            
            # 使用LLM生成回答
            response = Settings.llm.complete(prompt)
            
            print("回答生成完成")
            
            return str(response)
                
        except Exception as e:
            print(f"查询过程中出现错误: {e}")
            return f"查询出错: {str(e)}"


# 使用示例
if __name__ == "__main__":
    start_time = datetime.datetime.now()

    from dotenv import load_dotenv
    load_dotenv()

    print(f"开始时间: {start_time}")

    rag = MemoryRAGSystem(
        model_name="deepseek-chat",  # 使用更轻量级的模型
        document_dir="./documents"
    )

    question = "这篇文章主要讲了什么内容？"
    answer = rag.query(question)
    print(f"问题：{question}\n回答：{answer}")

    end_time = datetime.datetime.now()
    print(f"结束时间: {end_time}")

    duration = end_time - start_time
    print(f"消耗时间: {duration}")
    print(f"总秒数: {duration.total_seconds()} 秒") 