# SQLite MCP - 100% Local MCP Client

A fully local implementation of the Model Context Protocol (MCP) using SQLite database, LlamaIndex agents, and DeepSeek LLM. This project demonstrates how to build an MCP-powered agent that can interact with a SQLite database through natural language.

## Features

- **100% Local MCP Server**: FastMCP-based SQLite server with standardized tools
- **LlamaIndex Agent**: Function-calling agent with MCP tool integration
- **DeepSeek LLM**: Powerful language model for natural language understanding
- **Database Operations**: Add and query data using natural language
- **Interactive CLI**: Command-line interface for agent interaction

## Architecture

```
┌─────────────────┐    MCP Protocol    ┌─────────────────┐
│  LlamaIndex     │ ◄─────────────────► │  FastMCP        │
│  Agent Client   │                     │  SQLite Server  │
│  (Port: Client) │                     │  (Port: 8000)   │
└─────────────────┘                     └─────────────────┘
         │                                       │
         ▼                                       ▼
   DeepSeek LLM                           SQLite Database
   (Tool Calling)                         (demo.db)
```

### Workflow

1. User submits a natural language query
2. Agent connects to MCP server and discovers available tools
3. Agent invokes appropriate tools (add_data or read_data)
4. MCP server executes SQL operations on SQLite database
5. Agent returns context-aware response to user

## MCP Tools

### 1. add_data
- **Function**: Add new records to the people table
- **Input**: SQL INSERT query
- **Schema**: name (TEXT), age (INTEGER), profession (TEXT)
- **Example**: `INSERT INTO people (name, age, profession) VALUES ('John Doe', 30, 'Engineer')`

### 2. read_data
- **Function**: Query data from the people table
- **Input**: SQL SELECT query (optional, defaults to SELECT *)
- **Returns**: List of tuples containing query results
- **Example**: `SELECT * FROM people WHERE age > 25`

## Prerequisites

- Python >= 3.10
- DeepSeek API key

## Installation

1. **Set up DeepSeek API Key**:

   Create a `.env` file or export the environment variable:
   ```bash
   export DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

   Get your API key from [DeepSeek Platform](https://platform.deepseek.com/)

2. **Install Project Dependencies**:

   ```bash
   # Using uv (recommended)
   uv sync
   ```

## Usage

### Step 1: Start the MCP Server

In Terminal 1, start the SQLite MCP server:

```bash
# Production mode (SSE)
uv run server.py --server_type=sse

# Or debug mode
uv run mcp dev server.py
```

The server will start on `http://127.0.0.1:8000/sse`

### Step 2: Run the MCP Client

In Terminal 2, run the agent client:

```bash
uv run client.py
```

### Step 3: Interact with the Agent

The agent will display available tools and wait for your input:

```
Available tools:
add_data: Add new data to the people table using a SQL INSERT query.
read_data: Read data from the people table using a SQL SELECT query.

Enter 'exit' to quit

Enter your message: Add Rafael Nadal, age 38, profession Tennis Player
```

The agent will:
1. Understand your intent
2. Generate appropriate SQL INSERT command
3. Execute the command via the MCP tool
4. Confirm the operation

## Example Interactions

### Adding Data

```
User: Add Rafael Nadal, age 38, profession Tennis Player
Agent: I've successfully added Rafael Nadal to the database.
```

### Querying Data

```
User: Show me all people in the database
Agent: Here are all the people in the database:
1. Rafael Nadal, 38, Tennis Player
2. John Doe, 30, Engineer
```

### Filtered Queries

```
User: Find all people older than 35
Agent: Found 1 person older than 35:
- Rafael Nadal, 38, Tennis Player
```

## Project Structure

```
sqlite-mcp/
├── server.py              # FastMCP SQLite server implementation
├── client.py              # LlamaIndex agent client
├── demo.db                # SQLite database file
├── pyproject.toml         # Project configuration
├── uv.lock                # UV lock file
├── pyrightconfig.json     # Python type checking config
└── README.md              # This file
```

## Technical Details

### MCP Server Configuration

```python
mcp = FastMCP('sqlite-demo')

@mcp.tool()
def add_data(query: str) -> bool:
    # SQL INSERT execution
    
@mcp.tool()
def read_data(query: str = "SELECT * FROM people") -> list:
    # SQL SELECT execution
```

### LlamaIndex Agent Setup

```python
llm = DeepSeek(model="deepseek-chat", request_timeout=120.0)

agent = FunctionAgent(
    name="Agent",
    description="An agent that can work with Our Database software.",
    tools=mcp_tools,
    llm=llm,
    system_prompt=SYSTEM_PROMPT,
)
```

### MCP Client Connection

```python
mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
mcp_tool = McpToolSpec(client=mcp_client)
```

## Troubleshooting

### Common Issues

1. **MCP Server Connection Failed**:
   - Ensure the server is running on port 8000
   - Check if another process is using the port
   - Verify server type matches client connection (SSE)

2. **DeepSeek API Issues**:
   - Verify your API key is correctly set
   - Check API quotas and billing
   - Ensure network connectivity to DeepSeek API

3. **Database Errors**:
   - Check SQL query syntax
   - Verify database file permissions
   - Ensure table schema matches your queries

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

This project is based on the implementation described in the Daily Dose of Data Science article: ["Building a 100% local MCP Client"](https://www.dailydoseofds.com/p/building-a-100-local-mcp-client/).

The original article demonstrates:
- Building MCP servers with FastMCP
- Creating LlamaIndex agents with MCP tool integration
- Local development with Ollama (we use DeepSeek instead)
- Practical MCP client-server architecture

**Key References:**
- [Daily Dose of DS: Building a 100% local MCP Client](https://www.dailydoseofds.com/p/building-a-100-local-mcp-client/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [LlamaIndex MCP Integration](https://docs.llamaindex.ai/en/stable/examples/tools/mcp/)

We extend our gratitude to the Daily Dose of Data Science team for providing the foundational implementation and comprehensive tutorial.

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# SQLite MCP - 100% 本地MCP客户端

使用SQLite数据库、LlamaIndex智能体和DeepSeek LLM的完全本地化Model Context Protocol (MCP) 实现。本项目展示了如何构建一个可以通过自然语言与SQLite数据库交互的MCP驱动智能体。

## 功能特性

- **100% 本地MCP服务器**：基于FastMCP的SQLite服务器，提供标准化工具
- **LlamaIndex智能体**：集成MCP工具的函数调用智能体
- **DeepSeek LLM**：用于自然语言理解的强大语言模型
- **数据库操作**：使用自然语言添加和查询数据
- **交互式CLI**：用于智能体交互的命令行界面

## 架构

```
┌─────────────────┐    MCP协议      ┌─────────────────┐
│  LlamaIndex     │ ◄─────────────► │  FastMCP        │
│  智能体客户端    │                 │  SQLite服务器   │
│  (客户端端口)    │                 │  (端口: 8000)   │
└─────────────────┘                 └─────────────────┘
         │                                   │
         ▼                                   ▼
   DeepSeek LLM                        SQLite数据库
   (工具调用)                          (demo.db)
```

### 工作流程

1. 用户提交自然语言查询
2. 智能体连接到MCP服务器并发现可用工具
3. 智能体调用适当的工具（add_data或read_data）
4. MCP服务器在SQLite数据库上执行SQL操作
5. 智能体向用户返回上下文感知响应

## MCP工具

### 1. add_data
- **功能**：向people表添加新记录
- **输入**：SQL INSERT查询
- **架构**：name（TEXT）、age（INTEGER）、profession（TEXT）
- **示例**：`INSERT INTO people (name, age, profession) VALUES ('John Doe', 30, 'Engineer')`

### 2. read_data
- **功能**：从people表查询数据
- **输入**：SQL SELECT查询（可选，默认为SELECT *）
- **返回**：包含查询结果的元组列表
- **示例**：`SELECT * FROM people WHERE age > 25`

## 环境要求

- Python >= 3.10
- DeepSeek API密钥

## 安装步骤

1. **设置DeepSeek API密钥**：

   创建`.env`文件或导出环境变量：
   ```bash
   export DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

   从 [DeepSeek Platform](https://platform.deepseek.com/) 获取您的API密钥

2. **安装项目依赖**：

   ```bash
   # 使用uv（推荐）
   uv sync
   ```

## 使用方法

### 步骤1：启动MCP服务器

在终端1中启动SQLite MCP服务器：

```bash
# 生产模式（SSE）
uv run server.py --server_type=sse

# 或调试模式
uv run mcp dev server.py
```

服务器将在 `http://127.0.0.1:8000/sse` 上启动

### 步骤2：运行MCP客户端

在终端2中运行智能体客户端：

```bash
uv run client.py
```

### 步骤3：与智能体交互

智能体将显示可用工具并等待您的输入：

```
可用工具：
add_data: 使用SQL INSERT查询向people表添加新数据。
read_data: 使用SQL SELECT查询从people表读取数据。

输入'exit'退出

输入您的消息：添加Rafael Nadal，年龄38，职业网球运动员
```

智能体将：
1. 理解您的意图
2. 生成适当的SQL INSERT命令
3. 通过MCP工具执行命令
4. 确认操作

## 示例交互

### 添加数据

```
用户：添加Rafael Nadal，年龄38，职业网球运动员
智能体：我已成功将Rafael Nadal添加到数据库中。
```

### 查询数据

```
用户：显示数据库中的所有人
智能体：数据库中的所有人：
1. Rafael Nadal，38岁，网球运动员
2. John Doe，30岁，工程师
```

### 过滤查询

```
用户：查找所有年龄超过35岁的人
智能体：找到1位年龄超过35岁的人：
- Rafael Nadal，38岁，网球运动员
```

## 项目结构

```
sqlite-mcp/
├── server.py              # FastMCP SQLite服务器实现
├── client.py              # LlamaIndex智能体客户端
├── demo.db                # SQLite数据库文件
├── pyproject.toml         # 项目配置
├── uv.lock                # UV锁文件
├── pyrightconfig.json     # Python类型检查配置
└── README.md              # 本文件
```

## 技术细节

### MCP服务器配置

```python
mcp = FastMCP('sqlite-demo')

@mcp.tool()
def add_data(query: str) -> bool:
    # SQL INSERT执行
    
@mcp.tool()
def read_data(query: str = "SELECT * FROM people") -> list:
    # SQL SELECT执行
```

### LlamaIndex智能体设置

```python
llm = DeepSeek(model="deepseek-chat", request_timeout=120.0)

agent = FunctionAgent(
    name="Agent",
    description="An agent that can work with Our Database software.",
    tools=mcp_tools,
    llm=llm,
    system_prompt=SYSTEM_PROMPT,
)
```

### MCP客户端连接

```python
mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
mcp_tool = McpToolSpec(client=mcp_client)
```

## 故障排除

### 常见问题

1. **MCP服务器连接失败**：
   - 确保服务器在端口8000上运行
   - 检查是否有其他进程占用该端口
   - 验证服务器类型与客户端连接匹配（SSE）

2. **DeepSeek API问题**：
   - 验证您的API密钥是否正确设置
   - 检查API配额和计费
   - 确保对DeepSeek API的网络连接

3. **数据库错误**：
   - 检查SQL查询语法
   - 验证数据库文件权限
   - 确保表架构与您的查询匹配

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

本项目基于Daily Dose of Data Science的文章实现：["Building a 100% local MCP Client"](https://www.dailydoseofds.com/p/building-a-100-local-mcp-client/)。

原始文章演示了：
- 使用FastMCP构建MCP服务器
- 创建集成MCP工具的LlamaIndex智能体
- 使用Ollama进行本地开发（我们使用DeepSeek代替）
- 实用的MCP客户端-服务器架构

**主要参考资料：**
- [Daily Dose of DS: Building a 100% local MCP Client](https://www.dailydoseofds.com/p/building-a-100-local-mcp-client/)
- [MCP文档](https://modelcontextprotocol.io/)
- [FastMCP文档](https://github.com/jlowin/fastmcp)
- [LlamaIndex MCP集成](https://docs.llamaindex.ai/en/stable/examples/tools/mcp/)

我们向Daily Dose of Data Science团队表示感谢，感谢他们提供了基础实现和全面的教程。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。
