from mcp.server.fastmcp import FastMCP
from finance_crew import run_financial_analysis

# create FastMCP instance
mcp = FastMCP("financial-analyst")

@mcp.tool()
def analyze_stock(query: str) -> str:
    """
    分析中国A股市场数据并生成可执行的Python代码用于分析和可视化。
    返回格式化的、可直接执行的Python脚本。
    
    查询字符串必须包含股票名称或代码（如贵州茅台、600519、工商银行等），
    时间周期（如30天、3个月、1年），以及要执行的操作（如绘图、分析、对比）。
    
    示例查询：
    - "分析贵州茅台过去一年的股票表现"
    - "显示工商银行最近3个月的股价走势"
    - "分析比亚迪过去半年的交易量变化"
    - "对比招商银行和平安银行过去一年的表现"
    
    支持的股票示例：
    - 贵州茅台 (600519)
    - 工商银行 (601398)
    - 平安银行 (000001)
    - 招商银行 (600036)
    - 比亚迪 (002594)

    Args:
        query (str): 用于分析中国A股市场数据的查询
    
    Returns:
        str: 格式化的Python代码字符串
    """
    try:
        result = run_financial_analysis(query)
        return result
    except Exception as e:
        return f"Error: {e}"
    

@mcp.tool()
def save_code(code: str) -> str:
    """
    Expects a nicely formatted, working and executable python code as input in form of a string. 
    Save the given code to a file stock_analysis.py, make sure the code is a valid python file, nicely formatted and ready to execute.

    Args:
        code (str): The nicely formatted, working and executable python code as string.
    
    Returns:
        str: A message indicating the code was saved successfully.
    """
    try:
        with open('stock_analysis.py', 'w') as f:
            f.write(code)
        return "Code saved to stock_analysis.py"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def run_code_and_show_plot() -> str:
    """
    Run the code in stock_analysis.py and generate the plot
    """
    with open('stock_analysis.py', 'r') as f:
        exec(f.read())

# Run the server locally
if __name__ == "__main__":
    mcp.run(transport='stdio')