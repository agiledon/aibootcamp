# LlamaIndex RAG Examples

A comprehensive collection of LlamaIndex RAG (Retrieval-Augmented Generation) examples, including basic concepts and practical implementations. This project demonstrates core LlamaIndex features and real-world RAG applications.

## Modules

### 1. basic-concepts - LlamaIndex Fundamentals

Core LlamaIndex concepts and basic implementations based on official documentation.

**Files:**
- `documents.py` - Document creation and metadata handling
- `common_file_parser.py` - File parsing utilities
- `common_text_splitter.py` - Text splitting strategies
- `use_sentence_splitter.py` - Sentence-based text splitting
- `setting_with_sentence_splitter.py` - Configuration with sentence splitter
- `full_query_engine.py` - Complete query engine implementation
- `retriever_router_query_engine.py` - Router-based query engine
- `use_ingestion_pipeline.py` - Data ingestion pipeline

**Key Concepts:**
- Document creation and metadata management
- Text parsing and splitting
- Query engines and retrievers
- Ingestion pipelines
- Router patterns

### 2. rag-demo - Practical RAG Implementation

Real-world RAG application built by Zhang Yi, demonstrating production-ready implementations.

**Files:**
- `rag_main.py` - Main RAG system implementation with ChromaDB
- `memory_rag.py` - RAG with conversation memory
- `documents/` - Sample documents (DOCX files)
- `chroma_db/` - ChromaDB persistent storage

**Features:**
- DeepSeek LLM integration
- Ollama embedding model (nomic-embed-text)
- ChromaDB vector store
- Multi-format document support (PDF, DOCX, Excel, Markdown)
- Persistent storage and retrieval
- Conversation memory

## Prerequisites

- Python >= 3.12
- [Ollama](https://ollama.com/) installed and running
- DeepSeek and nomic-embed-text models
- DeepSeek API key (for rag-demo)

## Installation

1. **Install Ollama and Required Models**:

   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull required models
   ollama pull deepseek-chat
   ollama pull nomic-embed-text
   ```

2. **Set up DeepSeek API (for rag-demo)**:

   Create a `.env` file:
   ```bash
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

3. **Install Project Dependencies**:

   ```bash
   # Using uv (recommended)
   uv sync
   ```

## Usage

### Running Basic Concepts

Explore fundamental LlamaIndex concepts:

```bash
# Document handling
python basic-concepts/documents.py

# File parsing
python basic-concepts/common_file_parser.py

# Text splitting
python basic-concepts/use_sentence_splitter.py

# Query engine
python basic-concepts/full_query_engine.py

# Router query engine
python basic-concepts/retriever_router_query_engine.py

# Ingestion pipeline
python basic-concepts/use_ingestion_pipeline.py
```

### Running RAG Demo

Execute the practical RAG implementations:

```bash
# Main RAG system
cd rag-demo
python rag_main.py

# RAG with memory
python memory_rag.py
```

## Project Structure

```
llamaindex-rag/
├── basic-concepts/              # LlamaIndex fundamentals
│   ├── documents.py            # Document creation
│   ├── common_file_parser.py   # File parsing
│   ├── common_text_splitter.py # Text splitting
│   ├── use_sentence_splitter.py # Sentence splitter
│   ├── setting_with_sentence_splitter.py # Splitter config
│   ├── full_query_engine.py    # Query engine
│   ├── retriever_router_query_engine.py # Router query
│   ├── use_ingestion_pipeline.py # Ingestion pipeline
│   └── data/                   # Sample data files
├── rag-demo/                    # Practical RAG implementation
│   ├── rag_main.py             # Main RAG system
│   ├── memory_rag.py           # RAG with memory
│   ├── documents/              # Input documents
│   └── chroma_db/              # Vector database
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## Technical Details

### Basic Concepts Examples

**Document Creation:**
```python
document = Document(
    text="Custom document content",
    metadata={"category": "finance", "author": "LlamaIndex"},
    excluded_llm_metadata_keys=["file_name"]
)
```

**Query Engine:**
```python
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Your question here")
```

### RAG Demo Implementation

**DeepSeek RAG System:**
```python
class DeepSeekRAGSystem:
    def __init__(self, 
                 model_name="deepseek-chat",
                 embed_model="nomic-embed-text",
                 chroma_path="./chroma_db"):
        # Initialize LLM and embedding models
        Settings.llm = ChatDeepSeek(model=model_name)
        Settings.embed_model = OllamaEmbedding(model_name=embed_model)
```

**Features:**
- Multi-format document loading
- ChromaDB persistent storage
- Streaming responses
- Conversation memory

## Key Concepts Covered

### Basic Concepts
- Document abstraction and metadata
- File parsing (PDF, DOCX, Excel, Markdown)
- Text splitting strategies
- Query engines and retrievers
- Router patterns for multi-index queries
- Ingestion pipelines

### RAG Demo
- Production-ready RAG architecture
- Vector store integration (ChromaDB)
- LLM and embedding model configuration
- Document processing and indexing
- Query optimization
- Memory management

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**:
   ```bash
   # Ensure Ollama is running
   ollama serve
   
   # Check models
   ollama list
   ```

2. **DeepSeek API Issues** (rag-demo):
   - Verify API key in `.env` file
   - Check API quota and billing
   - Ensure network connectivity

3. **ChromaDB Issues**:
   - Check ChromaDB dependencies installed
   - Verify write permissions for `chroma_db/` directory

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

**basic-concepts:**
The Python code in the `basic-concepts` directory is primarily based on the LlamaIndex official documentation and examples.

**rag-demo:**
The `rag-demo` implementation is entirely from Zhang Yi's real-world project, demonstrating production-ready RAG applications with DeepSeek LLM and ChromaDB.

**Key References:**
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [LlamaIndex Examples](https://docs.llamaindex.ai/en/stable/examples/)
- [LlamaIndex RAG Tutorial](https://docs.llamaindex.ai/en/stable/understanding/putting_it_all_together/q_and_a/)

We extend our gratitude to the LlamaIndex team for providing comprehensive documentation and examples.

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# LlamaIndex RAG 示例

LlamaIndex RAG（检索增强生成）示例的综合集合，包括基础概念和实际实现。本项目展示了核心LlamaIndex特性和真实世界的RAG应用。

## 模块

### 1. basic-concepts - LlamaIndex基础

基于官方文档的核心LlamaIndex概念和基础实现。

**文件：**
- `documents.py` - 文档创建和元数据处理
- `common_file_parser.py` - 文件解析工具
- `common_text_splitter.py` - 文本分割策略
- `use_sentence_splitter.py` - 基于句子的文本分割
- `setting_with_sentence_splitter.py` - 句子分割器配置
- `full_query_engine.py` - 完整查询引擎实现
- `retriever_router_query_engine.py` - 基于路由器的查询引擎
- `use_ingestion_pipeline.py` - 数据摄取管道

**关键概念：**
- 文档创建和元数据管理
- 文本解析和分割
- 查询引擎和检索器
- 摄取管道
- 路由器模式

### 2. rag-demo - 实用RAG实现

由张逸构建的真实世界RAG应用，展示生产就绪的实现。

**文件：**
- `rag_main.py` - 使用ChromaDB的主RAG系统实现
- `memory_rag.py` - 带对话记忆的RAG
- `documents/` - 示例文档（DOCX文件）
- `chroma_db/` - ChromaDB持久化存储

**功能特性：**
- DeepSeek LLM集成
- Ollama嵌入模型（nomic-embed-text）
- ChromaDB向量存储
- 多格式文档支持（PDF、DOCX、Excel、Markdown）
- 持久化存储和检索
- 对话记忆

## 环境要求

- Python >= 3.12
- [Ollama](https://ollama.com/) 已安装并运行
- DeepSeek和nomic-embed-text模型
- DeepSeek API密钥（用于rag-demo）

## 安装步骤

1. **安装Ollama和所需模型**：

   ```bash
   # 安装Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # 下载所需模型
   ollama pull deepseek-chat
   ollama pull nomic-embed-text
   ```

2. **设置DeepSeek API（用于rag-demo）**：

   创建`.env`文件：
   ```bash
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

3. **安装项目依赖**：

   ```bash
   # 使用uv（推荐）
   uv sync
   ```

## 使用方法

### 运行基础概念

探索LlamaIndex基础概念：

```bash
# 文档处理
python basic-concepts/documents.py

# 文件解析
python basic-concepts/common_file_parser.py

# 文本分割
python basic-concepts/use_sentence_splitter.py

# 查询引擎
python basic-concepts/full_query_engine.py

# 路由器查询引擎
python basic-concepts/retriever_router_query_engine.py

# 摄取管道
python basic-concepts/use_ingestion_pipeline.py
```

### 运行RAG演示

执行实用RAG实现：

```bash
# 主RAG系统
cd rag-demo
python rag_main.py

# 带记忆的RAG
python memory_rag.py
```

## 项目结构

```
llamaindex-rag/
├── basic-concepts/              # LlamaIndex基础
│   ├── documents.py            # 文档创建
│   ├── common_file_parser.py   # 文件解析
│   ├── common_text_splitter.py # 文本分割
│   ├── use_sentence_splitter.py # 句子分割器
│   ├── setting_with_sentence_splitter.py # 分割器配置
│   ├── full_query_engine.py    # 查询引擎
│   ├── retriever_router_query_engine.py # 路由器查询
│   ├── use_ingestion_pipeline.py # 摄取管道
│   └── data/                   # 示例数据文件
├── rag-demo/                    # 实用RAG实现
│   ├── rag_main.py             # 主RAG系统
│   ├── memory_rag.py           # 带记忆的RAG
│   ├── documents/              # 输入文档
│   └── chroma_db/              # 向量数据库
├── pyproject.toml              # 项目配置
└── README.md                   # 本文件
```

## 技术细节

### 基础概念示例

**文档创建：**
```python
document = Document(
    text="自定义文档内容",
    metadata={"category": "finance", "author": "LlamaIndex"},
    excluded_llm_metadata_keys=["file_name"]
)
```

**查询引擎：**
```python
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("你的问题")
```

### RAG演示实现

**DeepSeek RAG系统：**
```python
class DeepSeekRAGSystem:
    def __init__(self, 
                 model_name="deepseek-chat",
                 embed_model="nomic-embed-text",
                 chroma_path="./chroma_db"):
        # 初始化LLM和嵌入模型
        Settings.llm = ChatDeepSeek(model=model_name)
        Settings.embed_model = OllamaEmbedding(model_name=embed_model)
```

**功能特性：**
- 多格式文档加载
- ChromaDB持久化存储
- 流式响应
- 对话记忆

## 涵盖的关键概念

### 基础概念
- 文档抽象和元数据
- 文件解析（PDF、DOCX、Excel、Markdown）
- 文本分割策略
- 查询引擎和检索器
- 多索引查询的路由器模式
- 摄取管道

### RAG演示
- 生产就绪的RAG架构
- 向量存储集成（ChromaDB）
- LLM和嵌入模型配置
- 文档处理和索引
- 查询优化
- 内存管理

## 故障排除

### 常见问题

1. **Ollama连接失败**：
   ```bash
   # 确保Ollama正在运行
   ollama serve
   
   # 检查模型
   ollama list
   ```

2. **DeepSeek API问题**（rag-demo）：
   - 验证`.env`文件中的API密钥
   - 检查API配额和计费
   - 确保网络连接

3. **ChromaDB问题**：
   - 检查ChromaDB依赖已安装
   - 验证`chroma_db/`目录的写入权限

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

**basic-concepts：**
`basic-concepts`目录中的Python代码主要基于LlamaIndex官方文档和示例。

**rag-demo：**
`rag-demo`实现完全来自张逸的真实项目，展示了使用DeepSeek LLM和ChromaDB的生产就绪RAG应用。

**主要参考资料：**
- [LlamaIndex文档](https://docs.llamaindex.ai/)
- [LlamaIndex示例](https://docs.llamaindex.ai/en/stable/examples/)
- [LlamaIndex RAG教程](https://docs.llamaindex.ai/en/stable/understanding/putting_it_all_together/q_and_a/)

我们向LlamaIndex团队表示感谢，感谢他们提供了全面的文档和示例。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。

