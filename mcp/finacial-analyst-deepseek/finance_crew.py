import re
import json
import os
import akshare as ak
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import CodeInterpreterTool, FileReadTool

from dotenv import load_dotenv

load_dotenv()

class QueryAnalysisOutput(BaseModel):
    """Structured output for the query analysis task."""
    stock_codes: list[str] = Field(..., description="股票代码列表 (例如: ['600519', '601398'])，600开头为沪市，000/002/300开头为深市")
    stock_names: list[str] = Field(..., description="股票名称列表 (例如: ['贵州茅台', '工商银行'])")
    timeframe: str = Field(..., description="时间周期 (例如: '日K', '周K', '月K'，或具体天数如 '30', '90', '365').")
    action: str = Field(..., description="执行的操作 (例如: '获取数据', '绘图', '分析').")

llm = LLM(
    model="ollama/deepseek-r1:7b",
    base_url="http://localhost:11434",
    # temperature=0.7
)

# llm = LLM(
#     model="openai/gpt-4o",
#     # temperature=0.7
# )

# 1) Query parser agent - 专注中国A股市场
query_parser_agent = Agent(
    role="中国A股数据分析师",
    goal="从用户查询中提取中国A股股票详细信息: {query}. 识别股票代码（如600519代表贵州茅台）和时间周期。",
    backstory="""你是专门研究中国A股市场的金融分析师，熟悉沪深股市的股票代码规则：
    - 沪市主板：600开头（如600519贵州茅台、601398工商银行）
    - 深市主板：000开头（如000001平安银行）
    - 中小板：002开头
    - 创业板：300开头
    你能够准确识别股票名称并转换为对应的股票代码。""",
    llm=llm,
    verbose=True,
    memory=True,
)

query_parsing_task = Task(
    description="""分析用户查询并提取中国A股股票详细信息。
    需要识别：
    1. 股票代码（6位数字）
    2. 股票名称（如贵州茅台、工商银行）
    3. 时间周期（天数或K线类型）
    4. 要执行的操作
    
    常见股票示例：
    - 贵州茅台: 600519
    - 工商银行: 601398
    - 平安银行: 000001
    - 招商银行: 600036
    - 比亚迪: 002594
    """,
    expected_output="包含stock_codes, stock_names, timeframe, action的字典",
    output_pydantic=QueryAnalysisOutput,
    agent=query_parser_agent,
)


# 2) Code writer agent - 专注中国A股
code_writer_agent = Agent(
    role="高级Python开发工程师",
    goal="编写Python代码以可视化中国A股股票数据",
    backstory="""你是专门从事中国股市数据可视化的高级Python开发者。
                 你精通 akshare、Pandas、Matplotlib 库。
                 你知道如何使用akshare获取中国股市数据：
                 - 使用 ak.stock_zh_a_hist() 获取A股历史数据
                 - 股票代码格式：6位数字（如600519）
                 - 数据包含：日期、开盘、收盘、最高、最低、成交量等
                 - 生成的代码需要包含中文标签和清晰的可视化
                 你擅长编写生产级Python代码，包含完善的错误处理和中文注释。""",
    llm=llm,
    verbose=True,
)

code_writer_task = Task(
    description="""基于股票分析师提供的信息编写Python代码以可视化中国A股股票数据。
    
    必须使用 akshare 库获取数据：
    - 函数：ak.stock_zh_a_hist(symbol=股票代码, period="daily", adjust="qfq")
    - 参数说明：
      * symbol: 股票代码（6位数字，如"600519"）
      * period: "daily"（日线）、"weekly"（周线）、"monthly"（月线）
      * adjust: "qfq"（前复权）、"hfq"（后复权）、""（不复权）
    
    代码要求：
    1. 使用 akshare 获取股票历史数据
    2. 计算关键指标（价格变化、收益率、波动率）
    3. 创建至少4个图表（价格走势、成交量、收益率分布、累计收益）
    4. 所有图表标签使用中文
    5. 设置中文字体支持
    6. 包含完善的数据统计输出
    7. 添加详细的中文注释
    
    重要：生成的代码必须将所有输出文件（Python脚本和图表）保存到output目录：
    - 使用 output/ 作为输出路径前缀
    - 如果output目录不存在，代码中需要创建它
    - 图表文件保存格式：output/{股票代码}_{股票名称}_analysis_{时间戳}.png
    """,
    expected_output="一个干净、可执行的Python脚本文件(.py)，用于中国A股股票可视化分析。所有生成的文件都保存在output目录中。",
    agent=code_writer_agent,
)


# 3) Code interpreter agent (uses code interpreter tool from crewai)
code_interpreter_tool = CodeInterpreterTool()

code_execution_agent = Agent(
    role="Senior Code Execution Expert",
    goal="Review and execute the generated Python code by code writer agent to visualize stock data and fix any errors encountered. It can delegate tasks to code writer agent if needed.",
    backstory="You are a code execution expert. You are skilled at executing Python code.",
    # tools=[code_interpreter_tool],
    allow_code_execution=True,   # This automatically adds the CodeInterpreterTool
    allow_delegation=True,
    llm=llm,
    verbose=True,
)

code_execution_task = Task(
    description="""Review and execute the generated Python code by code writer agent to visualize stock data and fix any errors encountered.""",
    expected_output="A clean, working and executable Python script file (.py) for stock visualization.",
    agent=code_execution_agent,
)

# Create the crew
crew = Crew(
    agents=[query_parser_agent, code_writer_agent, code_execution_agent],
    tasks=[query_parsing_task, code_writer_task, code_execution_task],
    process=Process.sequential
)

# Function to be wrapped inside MCP tool
def run_financial_analysis(query):
    result = crew.kickoff(inputs={"query": query})
    return result.raw

if __name__ == "__main__":
    # Run the crew with a query
    # query = input("请输入要分析的股票（名称或代码）：")
    result = crew.kickoff(inputs={"query": "分析贵州茅台过去一年的股票表现"})
    print(result.raw)