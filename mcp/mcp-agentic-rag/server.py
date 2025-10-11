# server.py
import os
from mcp.server.fastmcp import FastMCP
from rag_retriever import EmbedData, QdrantVDB, RagRetriever, new_faq_text
from web_searcher import WebSearcher, BrightDataSearcher, DuckDuckGoSearcher, BingSearcher

# Create an MCP server
mcp = FastMCP("MCP-RAG-app",
              host="127.0.0.1",
              port=8080,
              timeout=30)

# 配置搜索引擎策略（可通过环境变量切换）
# 支持的搜索引擎: 'brightdata', 'duckduckgo', 'bing'
SEARCH_ENGINE = os.getenv("WEB_SEARCH_ENGINE", "duckduckgo").lower()

@mcp.tool()
def machine_learning_faq_retrieval_tool(query: str) -> str:
    """Retrieve the most relevant documents from the machine learning
       FAQ collection. Use this tool when the user asks about ML.

    Input:
        query: str -> The user query to retrieve the most relevant documents

    Output:
        context: str -> most relevant documents retrieved from a vector DB
    """

    # check type of text
    if not isinstance(query, str):
        raise ValueError("query must be a string")
    
    retriever = RagRetriever(QdrantVDB("ml_faq_collection"), EmbedData())
    response = retriever.search(query)

    return response


def _get_web_searcher():
    """
    根据配置获取web搜索器实例（策略模式）
    
    Returns:
        WebSearcher: 配置的搜索器实例
    """
    if SEARCH_ENGINE == "brightdata":
        return BrightDataSearcher()
    elif SEARCH_ENGINE == "duckduckgo":
        return DuckDuckGoSearcher(region='cn-zh')
    elif SEARCH_ENGINE == "bing":
        return BingSearcher()
    else:
        # 默认使用DuckDuckGo（免费、无需配置）
        return DuckDuckGoSearcher()


@mcp.tool()
def bright_data_web_search_tool(query: str) -> list[str]:
    """
    在网络上搜索信息。
    支持多种搜索引擎：DuckDuckGo（默认，免费）、Bright Data、Bing。
    可通过环境变量WEB_SEARCH_ENGINE配置搜索引擎。
    
    Use this tool when the user asks about a specific topic or question 
    that is not related to general machine learning.

    Input:
        query: str -> The user query to search for information

    Output:
        context: list[dict] -> list of most relevant web search results
        
    Supported search engines:
        - duckduckgo (default, free, no API key required)
        - brightdata (requires credentials)
        - bing (via duckduckgo)
    """
    # check type of text
    if not isinstance(query, str):
        raise ValueError("query must be a string")
    
    # 使用策略模式获取搜索器
    web_searcher = _get_web_searcher()
    response = web_searcher.search(query)
    
    return response

if __name__ == "__main__":
    print("Starting MCP server at http://127.0.0.1:8080 on port 8080")
    mcp.run()

