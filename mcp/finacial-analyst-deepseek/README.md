# Financial Analyst with DeepSeek and MCP

An MCP-powered financial analysis system using CrewAI multi-agent collaboration and DeepSeek LLM. This project demonstrates how to build an intelligent stock analysis tool that generates executable Python code for data visualization and analysis.

**🇨🇳 中国A股支持**: 本项目已更新为支持中国A股市场（沪深股市），使用 `akshare` 库替代 `yfinance`，无需API密钥，访问稳定。

## Features

- **Multi-Agent Collaboration**: Three specialized agents working in sequence
- **MCP Integration**: Standardized tool interface via Model Context Protocol
- **Chinese A-Share Support**: Automated Chinese stock market data retrieval using akshare
- **Code Generation**: Generates executable Python scripts for visualization
- **DeepSeek LLM**: Uses Ollama-served DeepSeek-R1 7B model
- **Automatic Code Execution**: Reviews and executes generated code
- **Interactive Tools**: Stock analysis, code saving, and plot generation
- **No API Key Required**: akshare provides free access to Chinese stock data

## Architecture

```
┌─────────────────┐    MCP Tools     ┌─────────────────┐
│   MCP Client    │ ◄───────────────► │   MCP Server    │
│   (Cursor/IDE)  │                  │   (Port: 8080)  │
└─────────────────┘                  └─────────────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │  CrewAI Agents   │
                                    │  (3 Agents)      │
                                    └──────────────────┘
                                              │
                  ┌───────────────────────────┼───────────────────────────┐
                  ▼                           ▼                           ▼
          ┌───────────────┐          ┌───────────────┐          ┌───────────────┐
          │ Query Parser  │─────────►│ Code Writer   │─────────►│Code Executor  │
          │    Agent      │          │    Agent      │          │    Agent      │
          └───────────────┘          └───────────────┘          └───────────────┘
```

### Agent Workflow

1. **Query Parser Agent**: Extracts stock symbol, timeframe, and action from user query
2. **Code Writer Agent**: Generates Python code for stock data visualization
3. **Code Executor Agent**: Reviews and executes the code, fixes errors if needed

## MCP Tools

### 1. analyze_stock
- **Function**: Analyze stock market data and generate visualization code
- **Input**: Natural language query with stock symbol, timeframe, and action
- **Output**: Executable Python code as a string
- **Example**: "Show me Tesla's stock performance over the last 3 months"

### 2. save_code
- **Function**: Save generated Python code to a file
- **Input**: Python code string
- **Output**: Confirmation message
- **File**: Saves to `stock_analysis.py`

### 3. run_code_and_show_plot
- **Function**: Execute saved code and generate plots
- **Input**: None (reads from stock_analysis.py)
- **Output**: Executes code and displays visualization

## Prerequisites

- Python >= 3.12
- [Ollama](https://ollama.com/) installed and running
- DeepSeek-R1 7B model downloaded

## Installation

1. **Install Ollama and DeepSeek Model**:

```bash
   # Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

   # Pull the DeepSeek-R1 7B model
   ollama pull deepseek-r1:7b
   ```

2. **Install Project Dependencies**:

```bash
   # Using uv (recommended)
 uv sync
```

## Usage

### Option 1: Run as MCP Server

**Step 1: Start the MCP Server**

```bash
uv run server.py
```

The server will start with stdio transport for MCP communication.

**Step 2: Configure MCP Client**

Add to your MCP client configuration (e.g., Cursor IDE):

```json
{
  "mcpServers": {
    "financial-analyst": {
      "command": "uv",
      "args": ["run", "server.py"],
      "cwd": "/absolute/path/to/finacial-analyst-deepseek"
    }
  }
}
```

**Step 3: Interact via MCP Client**

In your MCP client, you can now use the financial analysis tools:

```
User: Analyze Tesla stock performance over the last year
Agent: [Generates Python code using CrewAI agents]
```

### Option 2: Run Standalone

Run the financial analysis crew directly:

```bash
# Run the main crew
uv run finance_crew.py
```

Or test with example scripts:

```bash
# Tesla analysis demo
uv run tesla_analysis_demo.py

# Tesla analysis final version
uv run tesla_analysis_final.py

# Stock analysis
uv run stock_analysis.py
```

## Example Queries

### Chinese A-Share Examples (中国A股示例)

**Query 1: 基本股票分析**
```
"分析贵州茅台(600519)过去一年的股票表现"
```

**Query 2: 股票对比**
```
"对比招商银行和工商银行过去一年的表现"
```

**Query 3: 交易量分析**
```
"分析比亚迪过去3个月的交易量变化"
```

**Query 4: 价格趋势**
```
"显示宁德时代过去半年的股价走势"
```

### Quick Reference (快速参考)
- 贵州茅台: 600519
- 工商银行: 601398  
- 招商银行: 600036
- 比亚迪: 002594
- 宁德时代: 300750

See `doc/CN_STOCK_GUIDE.md` for more stock codes and examples.

## Project Structure

```
finacial-analyst-deepseek/
├── server.py                    # MCP server with financial tools
├── finance_crew.py              # CrewAI multi-agent workflow
├── doc/                         # Documentation directory
│   ├── ARCHITECTURE_COMPARISON.md  # Architecture comparison guide
│   ├── CHANGELOG_CN.md            # Change log (Chinese)
│   ├── CN_STOCK_GUIDE.md          # Chinese stock guide
│   ├── EXECUTION_FLOW.md          # Execution flow explanation
│   ├── MIGRATION_SUMMARY.md       # Migration summary
│   └── QUICKSTART_CN.md           # Quick start guide (Chinese)
├── output/                      # Generated files directory (git-ignored)
├── pyproject.toml               # Project configuration
├── uv.lock                      # UV lock file
└── README.md                    # This file
```

## Technical Details

### CrewAI Agents

**1. Query Parser Agent:**
- **Role**: Stock Data Analyst
- **Goal**: Extract stock symbols, timeframe, and actions from queries
- **Output**: Structured data (Pydantic model)

**2. Code Writer Agent:**
- **Role**: Senior Python Developer
- **Goal**: Generate Python code for stock visualization
- **Skills**: Pandas, Matplotlib, yfinance expertise

**3. Code Executor Agent:**
- **Role**: Code Execution Expert
- **Goal**: Execute and validate generated code
- **Features**: Error fixing, code delegation

### MCP Server Configuration

```python
mcp = FastMCP("financial-analyst")

@mcp.tool()
def analyze_stock(query: str) -> str:
    # Run CrewAI workflow
    
@mcp.tool()
def save_code(code: str) -> str:
    # Save generated code
    
@mcp.tool()
def run_code_and_show_plot() -> str:
    # Execute code and display plots
```

### LLM Configuration

```python
llm = LLM(
    model="ollama/deepseek-r1:7b",
    base_url="http://localhost:11434",
)
```

## Generated Code Example

The agents will generate code like:

```python
import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False

# 获取贵州茅台股票数据（过去一年）
df = ak.stock_zh_a_hist(symbol="600519", period="daily", adjust="qfq")
df = df.tail(365)  # 最近365天
df['日期'] = pd.to_datetime(df['日期'])
df = df.set_index('日期')

# 绘制收盘价走势
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['收盘'], linewidth=2)
plt.title('贵州茅台股票表现 - 过去一年', fontsize=16, fontweight='bold')
plt.xlabel('日期', fontsize=12)
plt.ylabel('价格 (¥)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.show()
```

## Troubleshooting

### Common Issues

1. **Ollama Model Not Found**:
   ```bash
   # Ensure Ollama is running
   ollama serve
   
   # Pull the required model
   ollama pull deepseek-r1:7b
   ```

2. **yfinance Data Errors**:
   - Check internet connectivity
   - Verify stock symbol is valid
   - Try different timeframe if data is missing

3. **Code Execution Errors**:
   - Ensure matplotlib backend is properly configured
   - Check that all required libraries are installed
   - Review generated code for syntax errors

4. **MCP Server Connection**:
   - Verify server is running
   - Check MCP client configuration
   - Ensure correct transport type (stdio)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Contributors

### Zhang Yi

AI Strategy Consultant and AI-Native Application Developer, DDD Evangelist, Enterprise Mentor at Nanjing University DevOps+ Research Lab.

- GitHub: [@agiledon](https://github.com/agiledon)

## Original Project Credits

This project's code is copied from the [AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub) repository, specifically the [financial-analyst-deepseek](https://github.com/patchy631/ai-engineering-hub/tree/main/financial-analyst-deepseek) project, with minor modifications based on specific objectives.

**Original Repository:** https://github.com/patchy631/ai-engineering-hub/tree/main/financial-analyst-deepseek

**Key Modifications:**
- Updated dependencies to latest versions
- Minor code adjustments for specific use cases
- Enhanced documentation and examples

**Key References:**
- [AI Engineering Hub - Financial Analyst DeepSeek](https://github.com/patchy631/ai-engineering-hub/tree/main/financial-analyst-deepseek)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [akshare Documentation](https://akshare.akfamily.xyz/)

We extend our gratitude to the AI Engineering Hub contributors for providing this excellent financial analysis implementation.

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# 基于DeepSeek和MCP的金融分析师

使用CrewAI多智能体协作和DeepSeek LLM的MCP驱动金融分析系统。本项目展示了如何构建一个智能股票分析工具，可以生成用于数据可视化和分析的可执行Python代码。

**🇨🇳 中国A股支持**: 本项目已更新为支持中国A股市场（沪深股市），使用 `akshare` 库替代 `yfinance`，无需API密钥，访问稳定。

## 功能特性

- **多智能体协作**：三个专门的智能体按顺序工作
- **MCP集成**：通过Model Context Protocol的标准化工具接口
- **中国A股支持**：使用akshare自动检索中国股票市场数据
- **代码生成**：生成用于可视化的可执行Python脚本
- **DeepSeek LLM**：使用Ollama提供的DeepSeek-R1 7B模型
- **自动代码执行**：审查和执行生成的代码
- **交互式工具**：股票分析、代码保存和图表生成
- **无需API密钥**：akshare提供免费的中国股市数据访问

## 架构

```
┌─────────────────┐    MCP工具      ┌─────────────────┐
│   MCP客户端     │ ◄──────────────► │   MCP服务器     │
│   (Cursor/IDE)  │                  │   (端口: 8080)  │
└─────────────────┘                  └─────────────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │  CrewAI智能体    │
                                    │  (3个智能体)     │
                                    └──────────────────┘
                                              │
                  ┌───────────────────────────┼───────────────────────────┐
                  ▼                           ▼                           ▼
          ┌───────────────┐          ┌───────────────┐          ┌───────────────┐
          │ 查询解析器     │─────────►│ 代码编写器     │─────────►│代码执行器     │
          │   智能体       │          │   智能体       │          │   智能体      │
          └───────────────┘          └───────────────┘          └───────────────┘
```

### 智能体工作流

1. **查询解析器智能体**：从用户查询中提取股票代码、时间范围和操作
2. **代码编写器智能体**：生成用于股票数据可视化的Python代码
3. **代码执行器智能体**：审查和执行代码，如需要则修复错误

## MCP工具

### 1. analyze_stock
- **功能**：分析股票市场数据并生成可视化代码
- **输入**：包含股票代码、时间范围和操作的自然语言查询
- **输出**：可执行的Python代码字符串
- **示例**："显示特斯拉过去3个月的股票表现"

### 2. save_code
- **功能**：将生成的Python代码保存到文件
- **输入**：Python代码字符串
- **输出**：确认消息
- **文件**：保存到 `stock_analysis.py`

### 3. run_code_and_show_plot
- **功能**：执行保存的代码并生成图表
- **输入**：无（从stock_analysis.py读取）
- **输出**：执行代码并显示可视化

## 环境要求

- Python >= 3.12
- [Ollama](https://ollama.com/) 已安装并运行
- 已下载DeepSeek-R1 7B模型

## 安装步骤

1. **安装Ollama和DeepSeek模型**：

   ```bash
   # 安装Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # 下载DeepSeek-R1 7B模型
   ollama pull deepseek-r1:7b
   ```

2. **安装项目依赖**：

   ```bash
   # 使用uv（推荐）
   uv sync
   ```

## 使用方法

### 选项1：作为MCP服务器运行

**步骤1：启动MCP服务器**

```bash
uv run server.py
```

服务器将使用stdio传输启动MCP通信。

**步骤2：配置MCP客户端**

添加到您的MCP客户端配置（如Cursor IDE）：

```json
{
  "mcpServers": {
    "financial-analyst": {
      "command": "uv",
      "args": ["run", "server.py"],
      "cwd": "/absolute/path/to/finacial-analyst-deepseek"
    }
  }
}
```

**步骤3：通过MCP客户端交互**

在您的MCP客户端中，现在可以使用金融分析工具：

```
用户：分析特斯拉过去一年的股票表现
智能体：[使用CrewAI智能体生成Python代码]
```

### 选项2：独立运行

直接运行金融分析智能体团队：

```bash
# 运行主智能体团队
uv run finance_crew.py
```

或使用示例脚本测试：

```bash
# 特斯拉分析演示
uv run tesla_analysis_demo.py

# 特斯拉分析最终版本
uv run tesla_analysis_final.py

# 股票分析
uv run stock_analysis.py
```

## 示例查询

### 中国A股示例

**查询1：基本股票分析**
```
"分析贵州茅台(600519)过去一年的股票表现"
```

**查询2：股票对比**
```
"对比招商银行和工商银行过去一年的表现"
```

**查询3：交易量分析**
```
"分析比亚迪过去3个月的交易量变化"
```

**查询4：价格趋势**
```
"显示宁德时代过去半年的股价走势"
```

### 常用股票代码
- 贵州茅台: 600519
- 工商银行: 601398  
- 招商银行: 600036
- 比亚迪: 002594
- 宁德时代: 300750

详细股票代码和使用说明请参考 `doc/CN_STOCK_GUIDE.md`。

## 项目结构

```
finacial-analyst-deepseek/
├── server.py                    # 带有金融工具的MCP服务器
├── finance_crew.py              # CrewAI多智能体工作流
├── doc/                         # 文档目录
│   ├── ARCHITECTURE_COMPARISON.md  # 架构对比指南
│   ├── CHANGELOG_CN.md            # 更新日志（中文）
│   ├── CN_STOCK_GUIDE.md          # 中国股市指南
│   ├── EXECUTION_FLOW.md          # 执行流程说明
│   ├── MIGRATION_SUMMARY.md       # 迁移总结
│   └── QUICKSTART_CN.md           # 快速开始指南（中文）
├── output/                      # 生成文件目录（被git忽略）
├── pyproject.toml               # 项目配置
├── uv.lock                      # UV锁文件
└── README.md                    # 本文件
```

## 技术细节

### CrewAI智能体

**1. 查询解析器智能体：**
- **角色**：股票数据分析师
- **目标**：从查询中提取股票代码、时间范围和操作
- **输出**：结构化数据（Pydantic模型）

**2. 代码编写器智能体：**
- **角色**：高级Python开发者
- **目标**：生成用于股票可视化的Python代码
- **技能**：Pandas、Matplotlib、yfinance专家

**3. 代码执行器智能体：**
- **角色**：代码执行专家
- **目标**：执行和验证生成的代码
- **特性**：错误修复、代码委托

### MCP服务器配置

```python
mcp = FastMCP("financial-analyst")

@mcp.tool()
def analyze_stock(query: str) -> str:
    # 运行CrewAI工作流
    
@mcp.tool()
def save_code(code: str) -> str:
    # 保存生成的代码
    
@mcp.tool()
def run_code_and_show_plot() -> str:
    # 执行代码并显示图表
```

### LLM配置

```python
llm = LLM(
    model="ollama/deepseek-r1:7b",
    base_url="http://localhost:11434",
)
```

## 生成代码示例

智能体将生成如下代码：

```python
import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False

# 获取贵州茅台股票数据（过去一年）
df = ak.stock_zh_a_hist(symbol="600519", period="daily", adjust="qfq")
df = df.tail(365)  # 最近365天
df['日期'] = pd.to_datetime(df['日期'])
df = df.set_index('日期')

# 绘制收盘价走势
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['收盘'], linewidth=2)
plt.title('贵州茅台股票表现 - 过去一年', fontsize=16, fontweight='bold')
plt.xlabel('日期', fontsize=12)
plt.ylabel('价格 (¥)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.show()
```

## 故障排除

### 常见问题

1. **找不到Ollama模型**：
   ```bash
   # 确保Ollama正在运行
   ollama serve
   
   # 下载所需模型
   ollama pull deepseek-r1:7b
   ```

2. **yfinance数据错误**：
   - 检查网络连接
   - 验证股票代码有效
   - 如果数据缺失，尝试不同的时间范围

3. **代码执行错误**：
   - 确保matplotlib后端正确配置
   - 检查所有必需的库已安装
   - 检查生成代码的语法错误

4. **MCP服务器连接**：
   - 验证服务器正在运行
   - 检查MCP客户端配置
   - 确保正确的传输类型（stdio）

## 贡献

1. Fork仓库
2. 创建功能分支
3. 进行更改
4. 如适用，添加测试
5. 提交拉取请求

## 贡献者

### 张逸

AI战略顾问和AI原生应用开发者，DDD布道者，南京大学DevOps+研究实验室企业导师。

- GitHub: [@agiledon](https://github.com/agiledon)

## 原始项目致谢

本项目的代码复制自[AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub)仓库，特别是[financial-analyst-deepseek](https://github.com/patchy631/ai-engineering-hub/tree/main/financial-analyst-deepseek)项目，并根据具体目标进行了少量修改。

**原始仓库：** https://github.com/patchy631/ai-engineering-hub/tree/main/financial-analyst-deepseek

**主要修改：**
- 更新依赖到最新版本
- **替换yfinance为akshare以支持中国A股市场**
- 针对特定用例的轻微代码调整
- 增强文档和示例

**主要参考资料：**
- [AI Engineering Hub - Financial Analyst DeepSeek](https://github.com/patchy631/ai-engineering-hub/tree/main/financial-analyst-deepseek)
- [MCP文档](https://modelcontextprotocol.io/)
- [CrewAI文档](https://docs.crewai.com/)
- [akshare文档](https://akshare.akfamily.xyz/)

我们向AI Engineering Hub贡献者表示感谢，感谢他们提供了这个优秀的金融分析实现。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。