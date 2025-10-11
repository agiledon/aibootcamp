# MCP-Powered Agentic RAG

An agentic RAG (Retrieval-Augmented Generation) system powered by Model Context Protocol (MCP), combining vector database retrieval with web search capabilities. This project demonstrates how to build an intelligent agent that can search both a local knowledge base and the web using MCP tools.

## Features

- **Dual Search Capabilities**: Vector database retrieval + web search fallback
- **MCP Integration**: Standardized tool interface via Model Context Protocol
- **Qdrant Vector Database**: High-performance vector storage and retrieval
- **HuggingFace Embeddings**: Local embedding model for semantic search
- **Multiple Search Engines**: DuckDuckGo (default, free), Bright Data, Bing
- **Strategy Pattern**: Easily switch between search engines via configuration
- **Machine Learning FAQ**: Pre-indexed ML knowledge base
- **Standard Python Structure**: Clean src/tests/docs organization

## Architecture

```
┌─────────────────┐    MCP Tools     ┌─────────────────┐
│   MCP Client    │ ◄───────────────► │   MCP Server    │
│   (Cursor/IDE)  │                  │   (Port: 8080)  │
└─────────────────┘                  └─────────────────┘
                                              │
                         ┌────────────────────┴────────────────────┐
                         ▼                                         ▼
                  ┌──────────────┐                        ┌────────────┐
                  │   Qdrant     │                        │ Bright Data│
                  │   Vector DB  │                        │ Web Search │
                  │ (ML FAQ Data)│                        └────────────┘
                  └──────────────┘
```

### Workflow

1. User asks a question through MCP client (e.g., Cursor IDE)
2. MCP server provides two tools:
   - `machine_learning_faq_retrieval_tool` - Search local ML knowledge base
   - `bright_data_web_search_tool` - Search the web for current information
3. Agent selects appropriate tool based on query context
4. Tool executes and returns relevant information
5. Agent synthesizes response using retrieved context

## MCP Tools

### 1. machine_learning_faq_retrieval_tool
- **Function**: Retrieve relevant documents from ML FAQ knowledge base
- **Input**: User query string
- **Output**: Most relevant documents from Qdrant vector database
- **Use Case**: Questions about general machine learning concepts

### 2. web_search_tool
- **Function**: Search the web for current information
- **Input**: Search query string
- **Output**: List of relevant web search results
- **Use Case**: Specific topics or current events not in knowledge base

## Prerequisites

- Python >= 3.10
- Qdrant database running (Docker recommended)
- Bright Data account (for web search)

## Installation

1. **Start Qdrant Database**:

   ```bash
   # Using Docker
   docker run -p 6333:6333 -p 6334:6334 \
     -v $(pwd)/qdrant_storage:/qdrant/storage:z \
     qdrant/qdrant
   ```

2. **Set up Environment Variables**:

   Configure `src/mcp_agentic_rag/.env` file:
   ```bash
   # Copy from example
   cp src/mcp_agentic_rag/.env.example src/mcp_agentic_rag/.env
   
   # Edit the .env file:
   WEB_SEARCH_ENGINE=duckduckgo  # duckduckgo (default, free), brightdata, or bing
   
   # Only if using BrightData:
   BRIGHT_DATA_USERNAME=your_brightdata_username
   BRIGHT_DATA_PASSWORD=your_brightdata_password
   ```

   Get Bright Data credentials from [Bright Data](https://brightdata.com/) (optional)

3. **Install Project Dependencies**:

   ```bash
   # Using uv (recommended)
   uv sync
   ```

## Usage

### Step 1: Configure Search Engine (Optional)

The project defaults to DuckDuckGo (free, no API key required). To use a different search engine:

```bash
# Edit src/mcp_agentic_rag/.env
WEB_SEARCH_ENGINE=duckduckgo  # or: brightdata, bing

# For BrightData only:
BRIGHT_DATA_USERNAME=your_username
BRIGHT_DATA_PASSWORD=your_password
```

### Step 2: Start the MCP Server

The knowledge base will be automatically initialized on first use. Simply start the MCP server:

```bash
uv run src/mcp_agentic_rag/server.py
```

The server will start on `http://127.0.0.1:8080`

**Note:** When you first use `machine_learning_faq_retrieval_tool`, the system will automatically:
- Create the Qdrant collection `ml_faq_collection`
- Generate embeddings for ML FAQ documents
- Index the data in the vector database

### Step 3: Configure MCP Client

In your MCP client (e.g., Cursor IDE), add the server configuration:

```json
{
  "mcpServers": {
    "mcp-rag-app": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-agentic-rag",
        "run",
        "src/mcp_agentic_rag/server.py"
      ]
    }
  }
}
```

### Step 4: Interact with the Agent

In your MCP client, you can now ask questions:

**Example 1 - ML FAQ Query:**
```
User: What is the first step before building a machine learning model?
Agent: [Retrieves from vector database] The first step is to understand the problem, 
       define the objective, and identify the right metrics for evaluation.
```

**Example 2 - Web Search Query:**
```
User: What are the latest developments in quantum computing?
Agent: [Searches web via Bright Data] According to recent sources...
```

## Project Structure

```
mcp-agentic-rag/
├── src/                          # Source code
│   └── mcp_agentic_rag/         # Main package
│       ├── __init__.py          # Package initialization
│       ├── rag_retriever.py     # RAG retriever (Qdrant, embeddings)
│       ├── web_searcher.py      # Web searchers (strategy pattern)
│       ├── server.py            # MCP server with tools
│       ├── .env                 # Environment configuration
│       └── .env.example         # Configuration template
│
├── tests/                       # Test files
│   └── mcp_agentic_rag/        # Test package (mirrors src structure)
│       ├── __init__.py
│       ├── test_refactoring.py     # Refactoring validation tests
│       ├── test_simple_ddgs.py     # Basic DDGS tests
│       ├── test_search_engines.py  # Search engine tests
│       └── test_web_searcher.py    # Web searcher tests
│
├── docs/                        # Documentation
│   └── QUICKSTART.md           # Quick start guide
│
├── pyproject.toml              # Project configuration
├── uv.lock                     # UV lock file
└── README.md                   # This file
```

## Technical Details

### Module Architecture

The project uses a clean separation of concerns with three main modules:

#### 1. `rag_retriever.py` - RAG Components

**EmbedData Class:**
- Generates embeddings using HuggingFace models
- Batch processing for efficiency
- Supports custom embedding models

**QdrantVDB Class:**
- Manages Qdrant vector database operations
- Creates collections with optimized settings
- Handles data ingestion and search

**RagRetriever Class** (formerly `Retriever`):
- Combines embeddings and vector database
- Performs semantic search on local knowledge base
- Returns formatted search results

#### 2. `web_searcher.py` - Web Search Components (Strategy Pattern)

**WebSearcher (Abstract Base Class):**
- Defines common interface for all web searchers
- Ensures consistent return format

**BrightDataSearcher:**
- Uses Bright Data proxy service
- Requires API credentials
- High-quality Google search results

**DuckDuckGoSearcher** (Default, Recommended):
- Free, open-source, no API key required
- Privacy-focused search
- Good quality results

**BingSearcher:**
- Via DuckDuckGo aggregation
- Free, no configuration needed

#### 3. `server.py` - MCP Server

**Strategy Selector:**
- `_get_web_searcher()` - Selects search engine based on config
- Supports switching via `WEB_SEARCH_ENGINE` environment variable

**MCP Tools:**
- `machine_learning_faq_retrieval_tool` - Local knowledge base
- `bright_data_web_search_tool` - Web search (configurable engine)

### MCP Server Configuration

```python
mcp = FastMCP("MCP-RAG-app",
              host="127.0.0.1",
              port=8080,
              timeout=30)
```

### Knowledge Base

Pre-indexed with 30+ machine learning FAQ items covering:
- Data preprocessing and cleaning
- Feature engineering
- Model selection and training
- Overfitting and underfitting
- Hyperparameter tuning
- Model evaluation

## Troubleshooting

### Common Issues

1. **Qdrant Connection Failed**:
   ```bash
   # Ensure Qdrant is running
   docker ps | grep qdrant
   
   # Restart Qdrant if needed
   docker restart <qdrant-container-id>
   ```

2. **Bright Data Issues**:
   - Verify credentials in `.env` file
   - Check Bright Data account status
   - Ensure proxy configuration is correct

3. **Embedding Generation Errors**:
   - Check HuggingFace model availability
   - Verify network connectivity for model download
   - Ensure sufficient disk space for model cache

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

This project's code is copied from the [AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub) repository, specifically the [mcp-agentic-rag](https://github.com/patchy631/ai-engineering-hub/tree/main/mcp-agentic-rag) project, with minor modifications.

**Original Repository:** https://github.com/patchy631/ai-engineering-hub/tree/main/mcp-agentic-rag

**Key Modifications:**
- Updated dependencies to latest versions
- Introduced DuckDuckGo for web search with configurable multi-engine support
- Optimized code structure for improved readability and extensibility
- Enhanced documentation

**Key References:**
- [AI Engineering Hub - MCP Agentic RAG](https://github.com/patchy631/ai-engineering-hub/tree/main/mcp-agentic-rag)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Qdrant Documentation](https://qdrant.tech/documentation/)

We extend our gratitude to the AI Engineering Hub contributors for providing this excellent implementation.

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# MCP驱动的智能体RAG

由Model Context Protocol (MCP) 驱动的智能体RAG（检索增强生成）系统，结合向量数据库检索和网络搜索功能。本项目展示了如何构建一个可以使用MCP工具搜索本地知识库和网络的智能智能体。

## 功能特性

- **双重搜索能力**：向量数据库检索 + 网络搜索回退
- **MCP集成**：通过Model Context Protocol的标准化工具接口
- **Qdrant向量数据库**：高性能向量存储和检索
- **HuggingFace嵌入**：用于语义搜索的本地嵌入模型
- **网络搜索回退**：Bright Data集成用于实时网络信息
- **机器学习FAQ**：预索引的ML知识库

## 架构

```
┌─────────────────┐    MCP工具      ┌─────────────────┐
│   MCP客户端     │ ◄──────────────► │   MCP服务器     │
│   (Cursor/IDE)  │                  │   (端口: 8080)  │
└─────────────────┘                  └─────────────────┘
                                              │
                         ┌────────────────────┴────────────────────┐
                         ▼                                         ▼
                  ┌──────────────┐                        ┌────────────┐
                  │   Qdrant     │                        │ Bright Data│
                  │   向量数据库  │                        │  网络搜索   │
                  │ (ML FAQ数据) │                        └────────────┘
                  └──────────────┘
```

### 工作流程

1. 用户通过MCP客户端（如Cursor IDE）提问
2. MCP服务器提供两个工具：
   - `machine_learning_faq_retrieval_tool` - 搜索本地ML知识库
   - `bright_data_web_search_tool` - 在网络上搜索当前信息
3. 智能体根据查询上下文选择适当的工具
4. 工具执行并返回相关信息
5. 智能体使用检索到的上下文合成响应

## MCP工具

### 1. machine_learning_faq_retrieval_tool
- **功能**：从ML FAQ知识库检索相关文档
- **输入**：用户查询字符串
- **输出**：来自Qdrant向量数据库的最相关文档
- **使用场景**：关于一般机器学习概念的问题

### 2. web_search_tool
- **功能**：在网络上搜索当前信息
- **输入**：搜索查询字符串
- **输出**：相关网络搜索结果列表
- **使用场景**：知识库中没有的特定主题或当前事件

## 环境要求

- Python >= 3.10
- Qdrant数据库运行（推荐使用Docker）
- Bright Data账户（用于网络搜索）

## 安装步骤

1. **启动Qdrant数据库**：

```bash
   # 使用Docker
docker run -p 6333:6333 -p 6334:6334 \
-v $(pwd)/qdrant_storage:/qdrant/storage:z \
qdrant/qdrant
```

2. **设置环境变量**：

   配置`src/mcp_agentic_rag/.env`文件：
   ```bash
   # 从示例复制
   cp src/mcp_agentic_rag/.env.example src/mcp_agentic_rag/.env
   
   # 编辑.env文件：
   WEB_SEARCH_ENGINE=duckduckgo  # duckduckgo（默认，免费）、brightdata或bing
   
   # 仅在使用BrightData时需要：
   BRIGHT_DATA_USERNAME=your_brightdata_username
   BRIGHT_DATA_PASSWORD=your_brightdata_password
   ```

   从 [Bright Data](https://brightdata.com/) 获取凭据（可选）

3. **安装项目依赖**：

   ```bash
   # 使用uv（推荐）
   uv sync
   ```

## 使用方法

### 步骤1：配置搜索引擎（可选）

项目默认使用DuckDuckGo（免费、无需API密钥）。如需使用其他搜索引擎：

```bash
# 编辑 src/mcp_agentic_rag/.env
WEB_SEARCH_ENGINE=duckduckgo  # 可选：duckduckgo, brightdata, bing

# 仅在使用BrightData时需要：
BRIGHT_DATA_USERNAME=your_username
BRIGHT_DATA_PASSWORD=your_password
```

### 步骤2：启动MCP服务器

知识库将在首次使用时自动初始化。直接启动MCP服务器：

```bash
uv run src/mcp_agentic_rag/server.py
```

服务器将在 `http://127.0.0.1:8080` 上启动

**注意：** 首次使用`machine_learning_faq_retrieval_tool`时，系统将自动：
- 创建Qdrant集合`ml_faq_collection`
- 为ML FAQ文档生成嵌入
- 在向量数据库中索引数据

### 步骤3：配置MCP客户端

在您的MCP客户端（如Cursor IDE）中，添加服务器配置：

```json
{
  "mcpServers": {
    "mcp-rag-app": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-agentic-rag",
        "run",
        "src/mcp_agentic_rag/server.py"
      ]
    }
  }
}
```

### 步骤4：与智能体交互

在您的MCP客户端中，现在可以提问：

**示例1 - ML FAQ查询：**
```
用户：构建机器学习模型之前的第一步是什么？
智能体：[从向量数据库检索] 第一步是理解问题，定义目标，
       并确定评估的正确指标。
```

**示例2 - 网络搜索查询：**
```
用户：量子计算的最新发展是什么？
智能体：[通过Bright Data搜索网络] 根据最近的资料...
```

## 项目结构

```
mcp-agentic-rag/
├── src/                          # 源代码
│   └── mcp_agentic_rag/         # 主包
│       ├── __init__.py          # 包初始化
│       ├── rag_retriever.py     # RAG检索器（Qdrant、嵌入）
│       ├── web_searcher.py      # Web搜索器（策略模式）
│       ├── server.py            # MCP服务器
│       ├── .env                 # 环境配置
│       └── .env.example         # 配置模板
│
├── tests/                       # 测试文件
│   └── mcp_agentic_rag/        # 测试包（镜像src结构）
│       ├── __init__.py
│       ├── test_refactoring.py     # 重构验证测试
│       ├── test_simple_ddgs.py     # 基本DDGS测试
│       ├── test_search_engines.py  # 搜索引擎测试
│       └── test_web_searcher.py    # Web搜索器测试
│
├── docs/                        # 文档
│   └── QUICKSTART.md           # 快速开始指南
│
├── pyproject.toml              # 项目配置
├── uv.lock                     # UV锁文件
└── README.md                   # 本文件
```

## 技术细节

### 模块架构

项目采用清晰的职责分离，包含三个主要模块：

#### 1. `rag_retriever.py` - RAG组件

**EmbedData类：**
- 使用HuggingFace模型生成嵌入
- 批处理以提高效率
- 支持自定义嵌入模型

**QdrantVDB类：**
- 管理Qdrant向量数据库操作
- 使用优化设置创建集合
- 处理数据摄取和搜索

**RagRetriever类**（原`Retriever`）：
- 结合嵌入和向量数据库
- 对本地知识库执行语义搜索
- 返回格式化的搜索结果

#### 2. `web_searcher.py` - Web搜索组件（策略模式）

**WebSearcher（抽象基类）：**
- 定义所有web搜索器的通用接口
- 确保返回格式一致

**BrightDataSearcher：**
- 使用Bright Data代理服务
- 需要API凭证
- 高质量Google搜索结果

**DuckDuckGoSearcher**（默认，推荐）：
- 免费、开源、无需API密钥
- 注重隐私的搜索
- 良好的结果质量

**BingSearcher：**
- 通过DuckDuckGo聚合
- 免费、无需配置

#### 3. `server.py` - MCP服务器

**策略选择器：**
- `_get_web_searcher()` - 根据配置选择搜索引擎
- 支持通过`WEB_SEARCH_ENGINE`环境变量切换

**MCP工具：**
- `machine_learning_faq_retrieval_tool` - 本地知识库
- `bright_data_web_search_tool` - Web搜索（可配置引擎）

### MCP服务器配置

```python
mcp = FastMCP("MCP-RAG-app",
              host="127.0.0.1",
              port=8080,
              timeout=30)
```

### 知识库

预索引了30+机器学习FAQ项目，涵盖：
- 数据预处理和清理
- 特征工程
- 模型选择和训练
- 过拟合和欠拟合
- 超参数调优
- 模型评估

## 故障排除

### 常见问题

1. **Qdrant连接失败**：
   ```bash
   # 确保Qdrant正在运行
   docker ps | grep qdrant
   
   # 如需重启Qdrant
   docker restart <qdrant-container-id>
   ```

2. **Bright Data问题**：
   - 验证`.env`文件中的凭据
   - 检查Bright Data账户状态
   - 确保代理配置正确

3. **嵌入生成错误**：
   - 检查HuggingFace模型可用性
   - 验证模型下载的网络连接
   - 确保模型缓存有足够的磁盘空间

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

本项目的代码复制自[AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub)仓库，特别是[mcp-agentic-rag](https://github.com/patchy631/ai-engineering-hub/tree/main/mcp-agentic-rag)项目，并进行了少量修改。

**原始仓库：** https://github.com/patchy631/ai-engineering-hub/tree/main/mcp-agentic-rag

**主要修改：**
- 更新依赖到最新版本
- 引入DuckDuckGo完成Web搜索，并支持多种Web搜索的可配置
- 优化了代码结构，提升了代码可读性和可扩展性
- 增强文档

**主要参考资料：**
- [AI Engineering Hub - MCP Agentic RAG](https://github.com/patchy631/ai-engineering-hub/tree/main/mcp-agentic-rag)
- [MCP文档](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Qdrant文档](https://qdrant.tech/documentation/)

我们向AI Engineering Hub贡献者表示感谢，感谢他们提供了这个优秀的实现。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。