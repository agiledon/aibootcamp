import logging
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

import nest_asyncio

nest_asyncio.apply()

from llama_index.llms.ollama import Ollama
from llama_index.core import SimpleDirectoryReader, get_response_synthesizer
from llama_index.core import DocumentSummaryIndex
from llama_index.core.node_parser import SentenceSplitter

# 更新为中国城市
city_titles = ["北京", "上海", "广州", "深圳", "杭州"]

from pathlib import Path

# 预定义的城市信息，避免网络请求问题
city_info = {
    "北京": """北京是中华人民共和国的首都，直辖市，国家中心城市，超大城市，全国政治中心、文化中心、国际交往中心、科技创新中心。
北京位于华北平原北部，背靠燕山，毗邻天津市和河北省。北京是世界著名古都和现代化国际城市。
北京拥有众多历史文化古迹，如故宫、天坛、颐和园、长城等。北京还是中国的教育、科技、文化中心，拥有北京大学、清华大学等著名高校。
北京的经济以服务业为主，金融、科技、文化创意等产业发达。北京举办过2008年夏季奥运会和2022年冬季奥运会。""",
    
    "上海": """上海是中华人民共和国直辖市，国家中心城市，超大城市，中国国际经济、金融、贸易、航运、科技创新中心。
上海位于长江三角洲地区，东临东海，南临杭州湾，西接江苏、浙江两省。上海是中国最大的经济中心和港口城市。
上海拥有外滩、东方明珠、豫园等著名景点。上海的经济以金融、贸易、制造业为主，是中国最重要的金融中心。
上海拥有复旦大学、上海交通大学等著名高校。上海举办过2010年世界博览会。""",
    
    "广州": """广州是广东省省会，副省级市，国家中心城市，超大城市，中国重要的国际大都市、国际商贸中心、国际综合交通枢纽。
广州位于珠江三角洲北部，濒临南海，是华南地区的政治、经济、文化中心。广州有"花城"的美誉。
广州拥有陈家祠、沙面岛、广州塔等著名景点。广州的经济以商贸、制造业、服务业为主，是中国重要的对外贸易港口。
广州拥有中山大学、华南理工大学等著名高校。广州是海上丝绸之路的重要起点。""",
    
    "深圳": """深圳是广东省副省级市，国家计划单列市，超大城市，中国设立的第一个经济特区，中国改革开放的窗口。
深圳位于珠江三角洲东部，毗邻香港，是中国最年轻的大城市之一。深圳从一个小渔村发展成为现代化国际大都市。
深圳拥有世界之窗、欢乐谷、大梅沙等著名景点。深圳的经济以高新技术产业为主，拥有华为、腾讯等知名企业。
深圳拥有深圳大学、南方科技大学等高校。深圳是中国改革开放的象征和成功典范。""",
    
    "杭州": """杭州是浙江省省会，副省级市，国家历史文化名城，中国重要的电子商务中心，互联网经济发达。
杭州位于浙江省北部，钱塘江下游，是中国著名的旅游城市。杭州有"人间天堂"的美誉。
杭州拥有西湖、灵隐寺、千岛湖等著名景点。杭州的经济以互联网、电子商务、旅游业为主，阿里巴巴总部位于杭州。
杭州拥有浙江大学、杭州电子科技大学等著名高校。杭州是G20峰会举办城市。"""
}

for title in city_titles:
    print(f"正在处理{title}的信息...")
    
    # 获取预定义的城市信息
    city_text = city_info[title]
    
    # 创建数据目录
    data_path = Path("data")
    if not data_path.exists():
        data_path.mkdir()

    # 保存城市信息到文件
    with open(data_path / f"{title}.txt", "w", encoding="utf-8") as fp:
        fp.write(city_text)
    
    print(f"{title}信息已保存")

# Load all city documents
city_docs = []
for city_title in city_titles:
    docs = SimpleDirectoryReader(
        input_files=[f"data/{city_title}.txt"]
    ).load_data()
    docs[0].doc_id = city_title
    city_docs.extend(docs)

# llm = Ollama(
#     model="deepseek-r1:7b",
#     request_timeout=300,  # 减少超时时间到2分钟
#     keep_alive="5m",  # 减少保持连接时间
#     num_thread=4,  # 减少线程数
#     temperature=0.1,  # 降低温度以获得更稳定的回答
# )

from langchain_deepseek import ChatDeepSeek
from llama_index.llms.langchain import LangChainLLM

lc_llm = ChatDeepSeek(
            model="deepseek-chat",
            api_key=os.getenv("DEEPSEEK_API_KEY"),  # 从环境变量获取API密钥
            temperature=0.1,
            max_tokens=1000,
            timeout=60,
            max_retries=2,
        )
llm = LangChainLLM(lc_llm)

# 配置嵌入模型
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

# Set global LLM and embedding model settings
Settings.llm = llm
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    request_timeout=300,
    keep_alive="5m"
)

embed_model = Settings.embed_model

splitter = SentenceSplitter(chunk_size=1024)

# default mode of building the index
response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize", use_async=True, llm=llm
)
doc_summary_index = DocumentSummaryIndex.from_documents(
    city_docs,
    llm=llm,
    embed_model=embed_model,
    transformations=[splitter],
    response_synthesizer=response_synthesizer,
    show_progress=True,
)

doc_summary_index.get_document_summary("北京")

doc_summary_index.storage_context.persist("city_index")

from llama_index.core import load_index_from_storage
from llama_index.core import StorageContext

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="city_index")
doc_summary_index = load_index_from_storage(storage_context)

# using Query Engine to query the index
query_engine = doc_summary_index.as_query_engine(
    response_mode="tree_summarize", use_async=True
)
response = query_engine.query("北京有哪些著名的旅游景点？")
print("########################################################")
print("通过Tree Summarize获取的response:", response)

# Retrieve the summary of the index on LLM
from llama_index.core.indices.document_summary import (
    DocumentSummaryIndexLLMRetriever,
)
retriever = DocumentSummaryIndexLLMRetriever(
    doc_summary_index,
    # choice_select_prompt=None,
    # choice_batch_size=10,
    # choice_top_k=1,
    # format_node_batch_fn=None,
    # parse_choice_select_answer_fn=None,
)
retrieved_nodes = retriever.retrieve("北京有哪些著名的旅游景点？")
print("########################################################")
print("length of retrieved_nodes:", len(retrieved_nodes))
print(retrieved_nodes[0].score)
print("通过LLM Retriever获取的response:", retrieved_nodes[0].node.get_text())

# use retriever as part of a query engine
from llama_index.core.query_engine import RetrieverQueryEngine

# configure response synthesizer
response_synthesizer = get_response_synthesizer(response_mode="tree_summarize")

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)

# query
response = query_engine.query("北京有哪些著名的旅游景点？")
print("########################################################")
print("通过RetrieverQueryEngine获取的response:", response)

from llama_index.core.indices.document_summary import (
    DocumentSummaryIndexEmbeddingRetriever,
)
retriever = DocumentSummaryIndexEmbeddingRetriever(
    doc_summary_index,
    # similarity_top_k=1,
)
retrieved_nodes = retriever.retrieve("北京有哪些著名的旅游景点？")
print("length of retrieved_nodes:", len(retrieved_nodes))

print("########################################################")
print("通过DocumentSummaryIndexEmbeddingRetriever获取的response:", retrieved_nodes[0].node.get_text())