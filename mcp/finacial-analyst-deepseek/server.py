import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from finance_crew import run_financial_analysis

# create FastMCP instance
mcp = FastMCP("financial-analyst")

# 确保output目录存在
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

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
def save_code(code: str, filename: str = "stock_analysis.py") -> str:
    """
    接受格式化、可工作和可执行的Python代码作为字符串输入。
    将代码保存到output目录下的指定文件，确保代码是有效的Python文件，格式良好并可执行。

    Args:
        code (str): 格式化、可工作和可执行的Python代码字符串
        filename (str): 保存的文件名（默认：stock_analysis.py）
    
    Returns:
        str: 指示代码保存成功的消息
    """
    try:
        output_file = OUTPUT_DIR / filename
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)
        return f"代码已保存到 output/{filename}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def run_code_and_show_plot(filename: str = "stock_analysis.py") -> str:
    """
    运行output目录下指定的Python代码文件并生成图表
    
    Args:
        filename (str): 要执行的文件名（默认：stock_analysis.py）
    
    Returns:
        str: 执行结果消息
    """
    try:
        output_file = OUTPUT_DIR / filename
        if not output_file.exists():
            return f"错误: 文件 output/{filename} 不存在"
        
        # 切换到output目录执行，以便图表也保存在output目录
        original_dir = os.getcwd()
        try:
            os.chdir(OUTPUT_DIR)
            with open(filename, 'r', encoding='utf-8') as f:
                exec(f.read())
            return f"代码执行成功，图表已保存到 output/ 目录"
        finally:
            os.chdir(original_dir)
    except Exception as e:
        return f"执行错误: {str(e)}"

# Run the server locally
if __name__ == "__main__":
    mcp.run(transport='stdio')