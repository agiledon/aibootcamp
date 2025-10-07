# KFlow RAG - Intelligent Document Q&A System with ChromaDB

## Overview

KFlow RAG is an intelligent document question-answering system based on ChromaDB vector database, supporting multiple document formats for upload, processing, and intelligent Q&A. The system adopts the MVP architecture pattern, integrating LlamaIndex framework, DeepSeek LLM, and Ollama embedding models, providing persistent document storage and cross-session retrieval capabilities.

## Features

### 🎯 Core Features
- **Persistent Storage**: Document embeddings stored in ChromaDB database
- **Collection Management**: Uses "kflow" as the default collection name
- **File Replacement**: Same-name files automatically replace old versions
- **Global Retrieval**: Retrieve relevant documents from the entire collection
- **Intelligent Q&A**: Supports full knowledge base and specific document retrieval
- **Streaming Response**: Real-time answer generation for better user experience

### 📁 File Structure
- `chroma_repository.py`: ChromaDB database operations class
- `custom_query_engine.py`: Custom query engine with document filtering
- `model.py`: Core business logic integrating ChromaDB storage and retrieval
- `controller.py`: Controller coordinating View and Model interactions
- `view.py`: View layer with Streamlit user interface
- `app.py`: Main application entry point

## Installation and Configuration

### 1. Install Dependencies

#### Using uv (Recommended)
```bash
# Install project dependencies
uv sync

# Or using pip
pip install -e .
```

### 2. Start Ollama Service

```bash
# Start Ollama service
ollama serve

# Install embedding model
ollama pull nomic-embed-text
```

### 3. Configure DeepSeek API

```bash
# Set DeepSeek API Key
export DEEPSEEK_API_KEY="your_api_key_here"
```

### 4. Verify Installation
```bash
# Check Ollama service status
curl http://localhost:11434/api/tags

# Check installed models
ollama list
```

## Usage

### Starting the Application

#### Method 1: Direct Start (Recommended)
```bash
# Ensure Ollama service is running
ollama serve

# Start the application
uv run streamlit run app.py
```

#### Method 2: Using Ollama Startup Script
```bash
# Start Ollama service
python start_ollama.py

# Start the application in another terminal
uv run streamlit run app.py
```

### Document Operation Workflow

1. **Upload Documents**: Supports PDF, Word, Markdown, CSV, TXT files
2. **Automatic Storage**: Documents automatically stored in ChromaDB collection "kflow"
3. **Select Retrieval Scope**: Supports full knowledge base or specific document retrieval
4. **Intelligent Q&A**: RAG-based Q&A with streaming responses

## Technical Architecture

### ChromaRepository Class
```python
class ChromaRepository:
    def __init__(self, collection_name="kflow")
    def store_documents(self, documents, file_name, embed_model, progress_callback=None)
    def get_query_engine(self, file_names=None, llm=None, streaming=True)
    def get_collection_info(self)
    def clear_collection(self)
    def update_vector_store_with_new_documents(self, embed_model)
```

### FilteredQueryEngine Class
```python
class FilteredQueryEngine(BaseQueryEngine):
    def __init__(self, index, target_files=None, similarity_top_k=5, streaming=True, llm=None)
    def query(self, query_str)
    def set_target_files(self, target_files)
    def get_target_files(self)
```

### Storage Strategy
- **Collection Name**: kflow
- **Vector Dimension**: 768 (nomic-embed-text model)
- **Document Splitting**: 1024 character chunks, 200 character overlap
- **Metadata**: Includes filename and source information

### Retrieval Strategy
- **Similarity Search**: Retrieve top 5 most relevant document chunks
- **Global Search**: Retrieve from entire collection, not limited to single files
- **Document Filtering**: Support filtering by filename
- **Streaming Response**: Real-time answer generation

## Troubleshooting

### Common Issues

#### 1. Ollama Service Connection Failed
```
Error: HTTP Request: POST http://localhost:11434/api/embed "HTTP/1.1 502 Bad Gateway"
Solution: Ensure Ollama service is running with nomic-embed-text model installed
Check:
  - curl http://localhost:11434/api/tags
  - ollama list
  - ollama pull nomic-embed-text
Note: Embedding model is required for document vector generation
```

#### 2. DeepSeek API Connection Failed
```
Error: HTTP Request: POST https://api.deepseek.com/chat/completions "HTTP/1.1 401 Unauthorized"
Solution: Ensure correct DeepSeek API Key is set
Check:
  - echo $DEEPSEEK_API_KEY
  - Verify API Key is valid with sufficient quota
```

#### 3. ChromaDB Initialization Failed
```
Error: Failed to create ChromaDB collection
Solution: Check ChromaDB dependencies are correctly installed
Check:
  - pip list | grep chromadb
  - Ensure chromadb>=1.1.0 is installed
```

#### 4. Callback Manager Error
```
Error: IndexError: pop from empty list
Solution: System has automatic recovery mechanism, will reset callback manager and retry
Note: This is caused by llama_index callback manager state inconsistency, handled automatically
```

#### 5. Out of Memory
```
Error: Out of memory
Solution: Increase system memory or adjust document splitting parameters
```

### System Status Check
```python
# Check service status
chroma_status, ollama_status = model.check_services_status()
print(f"ChromaDB Status: {chroma_status}")
print(f"Ollama Status: {ollama_status}")

# Get ChromaDB collection info
info = model.get_chroma_info()
print(f"Collection Status: {info['status']}")
print(f"Document Count: {info['total_documents']}")
```

## Configuration Options

### Environment Variables
```bash
# DeepSeek API Key
export DEEPSEEK_API_KEY="your_api_key_here"

# ChromaDB Collection Name (optional, defaults to kflow)
export CHROMA_COLLECTION="kflow"

# Ollama Service URL (optional, defaults to localhost:11434)
export OLLAMA_BASE_URL="http://localhost:11434"
```

### Code Configuration
```python
# Custom ChromaDB configuration
chroma_repo = ChromaRepository(
    collection_name="my_collection"
)

# Custom query engine configuration
query_engine = FilteredQueryEngine(
    index=index,
    target_files=["specific_file.pdf"],  # Specific file retrieval
    similarity_top_k=10,  # Retrieve more results
    streaming=True
)
```

## Performance Optimization

### Recommended Configuration
- **Memory**: At least 8GB RAM
- **Storage**: SSD drive, at least 10GB available space
- **CPU**: 4+ cores
- **Network**: Stable network connection (for DeepSeek API)

### Tuning Parameters
```python
# Document splitting parameters
text_splitter = SentenceSplitter(
    chunk_size=1024,      # Chunk size
    chunk_overlap=200,    # Overlap size
    separator=" "         # Separator
)

# Retrieval parameters
query_engine = FilteredQueryEngine(
    index=index,
    similarity_top_k=5,   # Number of results
    streaming=True        # Streaming response
)
```

## Monitoring and Maintenance

### Health Check
```python
# Get ChromaDB collection info
info = model.get_chroma_info()
print(f"Status: {info['status']}")
print(f"Storage Type: {info['storage_type']}")
print(f"Document Count: {info['total_documents']}")
```

### Data Cleanup
```python
# Clear entire collection
model.clear_chroma_collection()
```

## Changelog

### v2.0.0
- ✅ Migrated to ChromaDB vector database
- ✅ Integrated DeepSeek LLM and Ollama embedding models
- ✅ Implemented custom filtered query engine
- ✅ Support for document filtering and full knowledge base retrieval
- ✅ Fixed callback manager error handling
- ✅ Optimized error recovery mechanism

### v1.0.0
- ✅ Integrated Milvus vector database
- ✅ Implemented persistent document storage
- ✅ Added file replacement functionality
- ✅ Added graceful degradation mechanism
- ✅ Optimized retrieval performance

## Support

If you encounter issues, please check:
1. Ollama service is running properly
2. DeepSeek API Key is valid
3. Network connection is stable
4. System resources are sufficient
5. Dependencies are correctly installed

---

# KFlow RAG - 基于ChromaDB的智能文档问答系统

## 概述

KFlow RAG是一个基于ChromaDB向量数据库的智能文档问答系统，支持多种文档格式的上传、处理和智能问答。系统采用MVP架构模式，集成了LlamaIndex框架、DeepSeek LLM和Ollama嵌入模型，提供持久化的文档存储和跨会话的检索功能。

## 功能特性

### 🎯 核心功能
- **持久化存储**: 文档嵌入向量存储在ChromaDB数据库中
- **集合管理**: 使用"kflow"作为默认集合名称
- **文件替换**: 同名文件会自动替换旧版本
- **全局检索**: 从整个集合中检索相关文档
- **智能问答**: 支持全知识库检索和特定文档检索
- **流式响应**: 实时生成回答，提供更好的用户体验

### 📁 文件结构
- `chroma_repository.py`: ChromaDB数据库操作类
- `custom_query_engine.py`: 自定义查询引擎，支持文档过滤
- `model.py`: 核心业务逻辑，集成ChromaDB存储和检索功能
- `controller.py`: 控制器，协调View和Model之间的交互
- `view.py`: 视图层，Streamlit用户界面
- `app.py`: 主应用入口

## 安装和配置

### 1. 安装依赖

#### 使用 uv（推荐）
```bash
# 安装项目依赖
uv sync

# 或者使用 pip
pip install -e .
```

### 2. 启动 Ollama 服务

```bash
# 启动 Ollama 服务
ollama serve

# 安装嵌入模型
ollama pull nomic-embed-text
```

### 3. 配置 DeepSeek API

```bash
# 设置 DeepSeek API Key
export DEEPSEEK_API_KEY="your_api_key_here"
```

### 4. 验证安装
```bash
# 检查 Ollama 服务状态
curl http://localhost:11434/api/tags

# 检查已安装的模型
ollama list
```

## 使用方法

### 启动应用

#### 方法1: 直接启动（推荐）
```bash
# 确保 Ollama 服务正在运行
ollama serve

# 启动应用
uv run streamlit run app.py
```

#### 方法2: 使用 Ollama 启动脚本
```bash
# 启动 Ollama 服务
python start_ollama.py

# 在另一个终端启动应用
uv run streamlit run app.py
```

### 文档操作流程

1. **上传文档**: 支持PDF、Word、Markdown、CSV、TXT文件
2. **自动存储**: 文档自动存储到ChromaDB集合"kflow"
3. **选择检索范围**: 支持全知识库检索或特定文档检索
4. **智能问答**: 基于检索结果进行RAG问答，支持流式响应

## 技术架构

### ChromaRepository类
```python
class ChromaRepository:
    def __init__(self, collection_name="kflow")
    def store_documents(self, documents, file_name, embed_model, progress_callback=None)
    def get_query_engine(self, file_names=None, llm=None, streaming=True)
    def get_collection_info(self)
    def clear_collection(self)
    def update_vector_store_with_new_documents(self, embed_model)
```

### FilteredQueryEngine类
```python
class FilteredQueryEngine(BaseQueryEngine):
    def __init__(self, index, target_files=None, similarity_top_k=5, streaming=True, llm=None)
    def query(self, query_str)
    def set_target_files(self, target_files)
    def get_target_files(self)
```

### 存储策略
- **集合名称**: kflow
- **向量维度**: 768（nomic-embed-text模型）
- **文档分割**: 1024字符块，200字符重叠
- **元数据**: 包含文件名和来源信息

### 检索策略
- **相似度检索**: 检索前5个最相关文档片段
- **全局搜索**: 从整个集合中检索，不限于单个文件
- **文档过滤**: 支持按文件名过滤检索结果
- **流式响应**: 支持实时流式回答生成

## 故障排除

### 常见问题

#### 1. Ollama 服务连接失败
```
错误: HTTP Request: POST http://localhost:11434/api/embed "HTTP/1.1 502 Bad Gateway"
解决: 确保 Ollama 服务正常运行并安装 nomic-embed-text 模型
检查方法: 
  - curl http://localhost:11434/api/tags
  - ollama list
  - ollama pull nomic-embed-text
说明: 嵌入模型用于生成文档向量，必须正常运行
```

#### 2. DeepSeek API 连接失败
```
错误: HTTP Request: POST https://api.deepseek.com/chat/completions "HTTP/1.1 401 Unauthorized"
解决: 确保设置了正确的 DeepSeek API Key
检查方法: 
  - echo $DEEPSEEK_API_KEY
  - 确认 API Key 有效且有足够的配额
```

#### 3. ChromaDB 初始化失败
```
错误: Failed to create ChromaDB collection
解决: 检查 ChromaDB 依赖是否正确安装
检查方法:
  - pip list | grep chromadb
  - 确认 chromadb>=1.1.0 已安装
```

#### 4. 回调管理器错误
```
错误: IndexError: pop from empty list
解决: 系统已实现自动恢复机制，会自动重置回调管理器并重试
说明: 这是由于 llama_index 回调管理器状态不一致导致的，系统会自动处理
```

#### 5. 内存不足
```
错误: Out of memory
解决: 增加系统内存或调整文档分割参数
```

### 系统状态检查
```python
# 检查服务状态
chroma_status, ollama_status = model.check_services_status()
print(f"ChromaDB状态: {chroma_status}")
print(f"Ollama状态: {ollama_status}")

# 获取 ChromaDB 集合信息
info = model.get_chroma_info()
print(f"集合状态: {info['status']}")
print(f"文档数量: {info['total_documents']}")
```

## 配置选项

### 环境变量
```bash
# DeepSeek API Key
export DEEPSEEK_API_KEY="your_api_key_here"

# ChromaDB 集合名称（可选，默认为 kflow）
export CHROMA_COLLECTION="kflow"

# Ollama 服务地址（可选，默认为 localhost:11434）
export OLLAMA_BASE_URL="http://localhost:11434"
```

### 代码配置
```python
# 自定义 ChromaDB 配置
chroma_repo = ChromaRepository(
    collection_name="my_collection"
)

# 自定义查询引擎配置
query_engine = FilteredQueryEngine(
    index=index,
    target_files=["specific_file.pdf"],  # 特定文件检索
    similarity_top_k=10,  # 检索更多结果
    streaming=True
)
```

## 性能优化

### 推荐配置
- **内存**: 至少8GB RAM
- **存储**: SSD硬盘，至少10GB可用空间
- **CPU**: 4核心以上
- **网络**: 稳定的网络连接（用于 DeepSeek API）

### 调优参数
```python
# 文档分割参数
text_splitter = SentenceSplitter(
    chunk_size=1024,      # 块大小
    chunk_overlap=200,    # 重叠大小
    separator=" "         # 分隔符
)

# 检索参数
query_engine = FilteredQueryEngine(
    index=index,
    similarity_top_k=5,   # 检索数量
    streaming=True        # 流式响应
)
```

## 监控和维护

### 健康检查
```python
# 获取 ChromaDB 集合信息
info = model.get_chroma_info()
print(f"状态: {info['status']}")
print(f"存储类型: {info['storage_type']}")
print(f"文档数量: {info['total_documents']}")
```

### 数据清理
```python
# 清空整个集合
model.clear_chroma_collection()
```

## 更新日志

### v2.0.0
- ✅ 迁移到 ChromaDB 向量数据库
- ✅ 集成 DeepSeek LLM 和 Ollama 嵌入模型
- ✅ 实现自定义过滤查询引擎
- ✅ 支持文档过滤和全知识库检索
- ✅ 修复回调管理器错误处理
- ✅ 优化错误恢复机制

### v1.0.0
- ✅ 集成 Milvus 向量数据库
- ✅ 实现文档持久化存储
- ✅ 支持文件替换功能
- ✅ 添加优雅降级机制
- ✅ 优化检索性能

## 支持

如有问题，请检查：
1. Ollama 服务是否正常运行
2. DeepSeek API Key 是否有效
3. 网络连接是否正常
4. 系统资源是否充足
5. 依赖包是否正确安装
