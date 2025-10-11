from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from tqdm import tqdm
from qdrant_client import models
from qdrant_client import QdrantClient

faq_text = """Question 1: What is the first step before building a machine learning model?
Answer 1: Understand the problem, define the objective, and identify the right metrics for evaluation.

Question 2: How important is data cleaning in ML?
Answer 2: Extremely important. Clean data improves model performance and reduces the chance of misleading results.

Question 3: Should I normalize or standardize my data?
Answer 3: Yes, especially for models sensitive to feature scales like SVMs, KNN, and neural networks.

Question 4: When should I use feature engineering?
Answer 4: Always consider it. Well-crafted features often yield better results than complex models.

Question 5: How to handle missing values?
Answer 5: Use imputation techniques like mean/median imputation, or model-based imputation depending on the context.

Question 6: Should I balance my dataset for classification tasks?
Answer 6: Yes, especially if the classes are imbalanced. Techniques include resampling, SMOTE, and class-weighting.

Question 7: How do I select features for my model?
Answer 7: Use domain knowledge, correlation analysis, or techniques like Recursive Feature Elimination or SHAP values.

Question 8: Is it good to use all features available?
Answer 8: Not always. Irrelevant or redundant features can reduce performance and increase overfitting.

Question 9: How do I avoid overfitting?
Answer 9: Use techniques like cross-validation, regularization, pruning (for trees), and dropout (for neural nets).

Question 10: Why is cross-validation important?
Answer 10: It provides a more reliable estimate of model performance by reducing bias from a single train-test split.

Question 11: What’s a good train-test split ratio?
Answer 11: Common ratios are 80/20 or 70/30, but use cross-validation for more robust evaluation.

Question 12: Should I tune hyperparameters?
Answer 12: Yes. Use grid search, random search, or Bayesian optimization to improve model performance.

Question 13: What’s the difference between training and validation sets?
Answer 13: Training set trains the model, validation set tunes hyperparameters, and test set evaluates final performance.

Question 14: How do I know if my model is underfitting?
Answer 14: It performs poorly on both training and test sets, indicating it hasn’t learned patterns well.

Question 15: What are signs of overfitting?
Answer 15: High accuracy on training data but poor generalization to test or validation data.

Question 16: Is ensemble modeling useful?
Answer 16: Yes. Ensembles like Random Forests or Gradient Boosting often outperform individual models.

Question 17: When should I use deep learning?
Answer 17: Use it when you have large datasets, complex patterns, or tasks like image and text processing.

Question 18: What is data leakage and how to avoid it?
Answer 18: Data leakage is using future or target-related information during training. Avoid by carefully splitting and preprocessing.

Question 19: How do I measure model performance?
Answer 19: Choose appropriate metrics: accuracy, precision, recall, F1, ROC-AUC for classification; RMSE, MAE for regression.

Question 20: Why is model interpretability important?
Answer 20: It builds trust, helps debug, and ensures compliance—especially important in high-stakes domains like healthcare.
"""

# 将faq_text按行分割，并去掉空行
new_faq_text = [i.replace("\n", " ") for i in faq_text.split("\n\n")]
def batch_iterate(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i : i + batch_size]

class EmbedData:
    
    def __init__(self, 
                 embed_model_name="nomic-ai/nomic-embed-text-v1.5",
                 batch_size=32):
        
        self.embed_model_name = embed_model_name
        self.embed_model = self._load_embed_model()
        self.batch_size = batch_size
        self.embeddings = []

    def _load_embed_model(self):
        embed_model = HuggingFaceEmbedding(model_name=self.embed_model_name,
                                           trust_remote_code=True,
                                           cache_folder='./hf_cache'
                                           )
        return embed_model
    
    def generate_embedding(self, context):
        return self.embed_model.get_text_embedding_batch(context)
    
    def embed(self, contexts):
        self.contexts = contexts
        
        for batch_context in tqdm(batch_iterate(contexts, self.batch_size),
                                  total=len(contexts)//self.batch_size,
                                  desc="Embedding data in batches"):
                                  
            batch_embeddings = self.generate_embedding(batch_context)
            
            self.embeddings.extend(batch_embeddings)



class QdrantVDB:
    # vector_dim: 768  是向量维度
    def __init__(self, collection_name, vector_dim=768, batch_size=512):
        self.collection_name = collection_name
        self.batch_size = batch_size
        self.vector_dim = vector_dim
        self.define_client()

    def define_client(self):
        self.client = QdrantClient(url="http://localhost:6333",
                                   prefer_grpc=True)
        
    def create_collection(self):
        
        if not self.client.collection_exists(collection_name=self.collection_name):

            self.client.create_collection(collection_name=self.collection_name,
                                          
                                          vectors_config=models.VectorParams(
                                                              size=self.vector_dim,
                                                              distance=models.Distance.DOT, # 点积（DOT）作为距离度量
                                                              on_disk=True),
                                          
                                          optimizers_config=models.OptimizersConfigDiff(
                                                                            default_segment_number=5,
                                                                            indexing_threshold=0)
                                         )
            
    def ingest_data(self, embeddata):
        
        for batch_context, batch_embeddings in tqdm(zip(batch_iterate(embeddata.contexts, self.batch_size), 
                                                        batch_iterate(embeddata.embeddings, self.batch_size)), 
                                                    total=len(embeddata.contexts)//self.batch_size, 
                                                    desc="Ingesting in batches"):
        
            self.client.upload_collection(collection_name=self.collection_name,
                                        vectors=batch_embeddings,
                                        payload=[{"context": context} for context in batch_context])

        self.client.update_collection(collection_name=self.collection_name,
                                    optimizer_config=models.OptimizersConfigDiff(indexing_threshold=20000)
                                    )
        
class Retriever:

    def __init__(self, vector_db, embeddata):
        
        self.vector_db = vector_db
        self.embeddata = embeddata

    def search(self, query):
        query_embedding = self.embeddata.embed_model.get_query_embedding(query)

        # select the top 3 results
        result = self.vector_db.client.search(
            collection_name=self.vector_db.collection_name,
            
            query_vector=query_embedding,
            
            search_params=models.SearchParams(
                quantization=models.QuantizationSearchParams(
                    ignore=True,
                    rescore=True,
                    oversampling=2.0,
                )
            ),
            limit=3,
            timeout=1000,
        )

        context = [dict(data) for data in result]
        combined_prompt = []

        for entry in context[:3]:
            context = entry["payload"]["context"]

            combined_prompt.append(context)

        final_output = "\n\n---\n\n".join(combined_prompt)
        return final_output


from abc import ABC, abstractmethod


class WebSearcher(ABC):
    """
    Web搜索器抽象基类
    定义了web搜索的通用接口
    """
    
    @abstractmethod
    def search(self, query, num_results=50):
        """
        搜索给定查询的网络信息
        
        Args:
            query: 搜索查询字符串
            num_results: 返回结果数量（默认50）
            
        Returns:
            list[dict]: 搜索结果列表
        """
        pass


class BrightDataSearcher(WebSearcher):
    """
    使用Bright Data进行网络搜索的实现
    """
    
    def __init__(self, username=None, password=None, env_file=None):
        """
        初始化Web搜索器
        
        Args:
            username: Bright Data用户名（如果为None，则从.env文件读取）
            password: Bright Data密码（如果为None，则从.env文件读取）
            env_file: .env文件路径（如果为None，则使用当前项目目录下的.env）
        """
        import os
        from pathlib import Path
        from dotenv import load_dotenv
        
        # 确定.env文件路径
        if env_file is None:
            # 使用当前文件所在目录的.env文件
            current_dir = Path(__file__).parent
            env_file = current_dir / ".env"
        else:
            env_file = Path(env_file)
        
        # 加载项目的.env文件
        if env_file.exists():
            load_dotenv(dotenv_path=env_file)
        else:
            # 如果.env文件不存在，尝试创建示例文件
            env_example = env_file.parent / ".env.example"
            if not env_example.exists():
                self._create_env_example(env_example)
            raise FileNotFoundError(
                f".env file not found at {env_file}. "
                f"Please copy .env.example to .env and configure your Bright Data credentials."
            )
        
        # Bright Data配置
        self.host = 'brd.superproxy.io'
        self.port = 33335
        self.username = username or os.getenv("BRIGHT_DATA_USERNAME")
        self.password = password or os.getenv("BRIGHT_DATA_PASSWORD")
        
        if not self.username or not self.password:
            raise ValueError(
                "Bright Data credentials not provided. "
                "Please set BRIGHT_DATA_USERNAME and BRIGHT_DATA_PASSWORD in your .env file."
            )
        
        # 配置代理
        self.proxy_url = f'http://{self.username}:{self.password}@{self.host}:{self.port}'
        self.proxies = {
            'http': self.proxy_url,
            'https': self.proxy_url
        }
    
    @staticmethod
    def _create_env_example(env_example_path):
        """创建.env.example示例文件"""
        example_content = """# Bright Data Configuration
# Get your credentials from https://brightdata.com/

BRIGHT_DATA_USERNAME=your_brightdata_username
BRIGHT_DATA_PASSWORD=your_brightdata_password
"""
        with open(env_example_path, 'w', encoding='utf-8') as f:
            f.write(example_content)
    
    def search(self, query, num_results=50):
        """
        搜索给定查询的网络信息
        
        Args:
            query: 搜索查询字符串
            num_results: 返回结果数量（默认50）
            
        Returns:
            list[dict]: 有机搜索结果列表
        """
        import ssl
        import requests
        
        # 配置SSL
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # 格式化查询并发起请求
        formatted_query = "+".join(query.split(" "))
        url = f"https://www.google.com/search?q={formatted_query}&brd_json=1&num={num_results}"
        
        try:
            response = requests.get(url, proxies=self.proxies, verify=False)
            response.raise_for_status()
            
            # 返回有机搜索结果
            return response.json().get('organic', [])
        
        except requests.RequestException as e:
            raise RuntimeError(f"Web search failed: {str(e)}")


class DuckDuckGoSearcher(WebSearcher):
    """
    使用DuckDuckGo进行网络搜索的实现（免费、开源、无需API密钥）
    """
    
    def __init__(self, region='cn-zh', safesearch='moderate', max_results=50):
        """
        初始化DuckDuckGo搜索器
        
        Args:
            region: 搜索区域（cn-zh=中国中文, us-en=美国英文, wt-wt=无区域）
            safesearch: 安全搜索级别（on/moderate/off）
            max_results: 最大返回结果数（默认50）
        """
        self.region = region
        self.safesearch = safesearch
        self.max_results = max_results
    
    def search(self, query, num_results=None):
        """
        使用DuckDuckGo搜索
        
        Args:
            query: 搜索查询字符串
            num_results: 返回结果数量（如果为None，使用初始化时的max_results）
            
        Returns:
            list[dict]: 搜索结果列表，每个结果包含title、href、body等字段
        """
        from ddgs import DDGS
        
        num_results = num_results or self.max_results
        
        try:
            # 创建DDGS实例并执行搜索
            results = DDGS().text(
                query,  # 第一个位置参数
                region=self.region,
                safesearch=self.safesearch,
                max_results=num_results
            )
            
            # 转换为统一格式（与BrightData保持一致）
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'snippet': result.get('body', ''),
                    'description': result.get('body', ''),
                })
            
            return formatted_results
        
        except Exception as e:
            raise RuntimeError(f"DuckDuckGo search failed: {str(e)}")


class BingSearcher(WebSearcher):
    """
    使用Bing搜索（通过duckduckgo_search库的备用接口）
    注：实际上DuckDuckGo聚合了多个搜索引擎的结果
    """
    
    def __init__(self, max_results=50):
        """
        初始化Bing搜索器
        
        Args:
            max_results: 最大返回结果数（默认50）
        """
        self.max_results = max_results
    
    def search(self, query, num_results=None):
        """
        使用DuckDuckGo执行搜索（聚合结果包含Bing）
        
        Args:
            query: 搜索查询字符串
            num_results: 返回结果数量
            
        Returns:
            list[dict]: 搜索结果列表
        """
        from ddgs import DDGS
        
        num_results = num_results or self.max_results
        
        try:
            # DuckDuckGo会聚合多个搜索引擎的结果
            results = DDGS().text(
                query,  # 第一个位置参数
                max_results=num_results
            )
            
            # 转换为统一格式
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'snippet': result.get('body', ''),
                    'description': result.get('body', ''),
                })
            
            return formatted_results
        
        except Exception as e:
            raise RuntimeError(f"Bing search (via DuckDuckGo) failed: {str(e)}")