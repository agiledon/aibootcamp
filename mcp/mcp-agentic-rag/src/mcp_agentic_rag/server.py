# server.py
import os
from mcp.server.fastmcp import FastMCP
from mcp_agentic_rag.rag_retriever import EmbedData, QdrantVDB, RagRetriever
from mcp_agentic_rag.web_searcher import BrightDataSearcher, DuckDuckGoSearcher, BingSearcher

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
def web_search_tool(query: str) -> str:
    """
    Use this tool when the user asks about a specific topic or question 
    that is not related to general machine learning.

    Input:
        query: str -> The user query to search for information

    Output:
        context: str -> formatted web search results as text
        
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
    results = web_searcher.search(query)
    
    # 格式化结果为字符串（与machine_learning_faq_retrieval_tool保持一致）
    formatted_results = []
    for i, result in enumerate(results[:5], 1):  # 只返回前5条
        formatted_results.append(
            f"{i}. {result.get('title', 'N/A')}\n"
            f"   URL: {result.get('url', 'N/A')}\n"
            f"   {result.get('snippet', 'N/A')}"
        )
    
    return "\n\n---\n\n".join(formatted_results)

if __name__ == "__main__":
    print("Starting MCP server at http://127.0.0.1:8080 on port 8080")
    mcp.run()

