# MCP-Powered Agentic RAG

An agentic RAG (Retrieval-Augmented Generation) system powered by Model Context Protocol (MCP), combining vector database retrieval with web search capabilities. This project demonstrates how to build an intelligent agent that can search both a local knowledge base and the web using MCP tools.

## Features

- **Dual Search Capabilities**: Vector database retrieval + web search fallback
- **MCP Integration**: Standardized tool interface via Model Context Protocol
- **Qdrant Vector Database**: High-performance vector storage and retrieval
- **HuggingFace Embeddings**: Local embedding model for semantic search
- **Web Search Fallback**: Bright Data integration for real-time web information
- **Machine Learning FAQ**: Pre-indexed ML knowledge base

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

### 2. bright_data_web_search_tool
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

   Create a `.env` file:
   ```bash
   BRIGHT_DATA_USERNAME=your_brightdata_username
   BRIGHT_DATA_PASSWORD=your_brightdata_password
   ```

   Get credentials from [Bright Data](https://brightdata.com/)

3. **Install Project Dependencies**:

   ```bash
   # Using uv (recommended)
   uv sync
   ```

## Usage

### Step 1: Initialize the Knowledge Base

First, run the RAG code to create and populate the Qdrant collection:

```bash
uv run rag_code.py
```

This will:
- Create a Qdrant collection named `ml_faq_collection`
- Generate embeddings for ML FAQ documents
- Index the data in the vector database

### Step 2: Start the MCP Server

Start the MCP server to expose the tools:

```bash
uv run server.py
```

The server will start on `http://127.0.0.1:8080`

### Step 3: Configure MCP Client

In your MCP client (e.g., Cursor IDE), add the server configuration:

```json
{
  "mcpServers": {
    "mcp-rag-app": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "host": "127.0.0.1",
      "port": 8080,
      "timeout": 30000
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
├── server.py              # MCP server with RAG tools
├── rag_code.py            # RAG implementation (embeddings, Qdrant)
├── pyproject.toml         # Project configuration
├── uv.lock                # UV lock file
└── README.md              # This file
```

## Technical Details

### RAG Components

**EmbedData Class:**
- Generates embeddings using HuggingFace models
- Batch processing for efficiency
- Supports custom embedding models

**QdrantVDB Class:**
- Manages Qdrant vector database operations
- Creates collections with optimized settings
- Handles data ingestion and search

**Retriever Class:**
- Combines embeddings and vector database
- Performs semantic search
- Returns formatted search results

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
- Minor code adjustments for compatibility
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

### 2. bright_data_web_search_tool
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

   创建`.env`文件：
   ```bash
   BRIGHT_DATA_USERNAME=your_brightdata_username
   BRIGHT_DATA_PASSWORD=your_brightdata_password
   ```

   从 [Bright Data](https://brightdata.com/) 获取凭据

3. **安装项目依赖**：

   ```bash
   # 使用uv（推荐）
   uv sync
   ```

## 使用方法

### 步骤1：初始化知识库

首先，运行RAG代码创建并填充Qdrant集合：

```bash
uv run rag_code.py
```

这将：
- 创建名为`ml_faq_collection`的Qdrant集合
- 为ML FAQ文档生成嵌入
- 在向量数据库中索引数据

### 步骤2：启动MCP服务器

启动MCP服务器以公开工具：

```bash
uv run server.py
```

服务器将在 `http://127.0.0.1:8080` 上启动

### 步骤3：配置MCP客户端

在您的MCP客户端（如Cursor IDE）中，添加服务器配置：

```json
{
  "mcpServers": {
    "mcp-rag-app": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "host": "127.0.0.1",
      "port": 8080,
      "timeout": 30000
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
├── server.py              # 带有RAG工具的MCP服务器
├── rag_code.py            # RAG实现（嵌入、Qdrant）
├── pyproject.toml         # 项目配置
├── uv.lock                # UV锁文件
└── README.md              # 本文件
```

## 技术细节

### RAG组件

**EmbedData类：**
- 使用HuggingFace模型生成嵌入
- 批处理以提高效率
- 支持自定义嵌入模型

**QdrantVDB类：**
- 管理Qdrant向量数据库操作
- 使用优化设置创建集合
- 处理数据摄取和搜索

**Retriever类：**
- 结合嵌入和向量数据库
- 执行语义搜索
- 返回格式化的搜索结果

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
- 轻微代码调整以提高兼容性
- 增强文档

**主要参考资料：**
- [AI Engineering Hub - MCP Agentic RAG](https://github.com/patchy631/ai-engineering-hub/tree/main/mcp-agentic-rag)
- [MCP文档](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Qdrant文档](https://qdrant.tech/documentation/)

我们向AI Engineering Hub贡献者表示感谢，感谢他们提供了这个优秀的实现。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。