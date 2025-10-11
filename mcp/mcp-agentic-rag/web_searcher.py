"""
Web搜索器模块
提供多种web搜索引擎的实现，使用策略模式支持灵活切换
"""

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

