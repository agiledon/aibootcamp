# KFlow RAG - 基于Milvus的智能文档问答系统

## 概述

KFlow RAG是一个基于Milvus向量数据库的智能文档问答系统，支持多种文档格式的上传、处理和智能问答。系统采用MVP架构模式，集成了LlamaIndex框架和Ollama嵌入模型，提供持久化的文档存储和跨会话的检索功能。

## 功能特性

### 🎯 核心功能
- **持久化存储**: 文档嵌入向量存储在Milvus数据库中
- **集合管理**: 使用"kflow"作为默认集合名称
- **文件替换**: 同名文件会自动替换旧版本
- **全局检索**: 从整个集合中检索相关文档
- **优雅降级**: Milvus不可用时自动使用内存存储

### 📁 文件结构
- `milvus_repository.py`: Milvus数据库操作类
- `start_milvus.py`: Milvus服务器启动脚本
- `model.py`: 已集成Milvus存储和检索功能

## 安装和配置

### 1. 安装Milvus

#### 使用Docker（推荐）
```bash
# 下载Milvus docker-compose文件
wget https://github.com/milvus-io/milvus/releases/download/v2.4.0/milvus-standalone-docker-compose.yml -O docker-compose.yml

# 启动Milvus
docker-compose up -d
```

#### 使用二进制文件
```bash
# 下载Milvus二进制文件
wget https://github.com/milvus-io/milvus/releases/download/v2.4.0/milvus-2.4.0-linux-amd64.tar.gz

# 解压并安装
tar -xzf milvus-2.4.0-linux-amd64.tar.gz
cd milvus-2.4.0-linux-amd64
./milvus run standalone
```

### 2. 验证安装
```bash
# 检查Milvus服务状态（健康检查端点）
curl http://localhost:9091/healthz

# 检查Docker容器状态
docker-compose ps

# 检查Milvus连接（如果使用Docker Compose）
curl http://localhost:19530/health
```

## 使用方法

### 启动应用

#### 方法1: 使用启动脚本
```bash
# 启动Milvus服务器
python start_milvus.py

# 启动Ollama服务（用于嵌入模型）
python start_ollama.py

# 在另一个终端启动应用
uv run streamlit run app.py
```

#### 方法2: 手动启动
```bash
# 启动Milvus服务器
milvus run standalone

# 启动Ollama服务
ollama serve

# 安装嵌入模型（如果未安装）
ollama pull nomic-embed-text

# 启动应用
uv run streamlit run app.py
```

### 文档操作流程

1. **上传文档**: 支持PDF、Word、Markdown、CSV、TXT文件
2. **自动存储**: 文档自动存储到Milvus集合"kflow"
3. **向量检索**: 从整个集合中检索相关文档片段
4. **智能问答**: 基于检索结果进行RAG问答

## 技术架构

### MilvusRepository类
```python
class MilvusRepository:
    def __init__(self, collection_name="kflow", uri="http://localhost:19530")
    def store_documents(self, documents, file_name, progress_callback=None)
    def get_query_engine(self, streaming=True)
    def get_collection_info(self)
    def clear_collection(self)
```

### 存储策略
- **集合名称**: kflow
- **向量维度**: 768（nomic-embed-text模型）
- **文档分割**: 1024字符块，200字符重叠
- **元数据**: 包含文件名和来源信息

### 检索策略
- **相似度检索**: 检索前5个最相关文档片段
- **全局搜索**: 从整个集合中检索，不限于单个文件
- **流式响应**: 支持实时流式回答生成

## 故障排除

### 常见问题

#### 1. Milvus连接失败
```
错误: Fail connecting to server on localhost:19530
解决: 确保Milvus服务器正在运行
检查方法: curl http://localhost:9091/healthz
```

#### 1.1. 健康检查404错误
```
错误: 404 page not found (curl http://localhost:19530/health)
解决: 使用正确的健康检查端点
正确命令: curl http://localhost:9091/healthz
说明: Milvus的健康检查端点是/healthz，不是/health
```

#### 1.2. Streamlit环境中的异步事件循环问题
```
错误: There is no current event loop in thread 'ScriptRunner.scriptThread'
解决: 已实现完全同步的存储和查询解决方案
说明: 使用pymilvus的同步连接 + 直接嵌入存储，避免异步事件循环冲突
技术细节: 
  - 同步连接: connections.connect()
  - 同步存储: collection.insert() + collection.flush()
  - 嵌入模型: OllamaEmbedding.get_text_embedding_batch()
```

#### 1.3. Ollama嵌入模型502错误
```
错误: HTTP Request: POST http://localhost:11434/api/embed "HTTP/1.1 502 Bad Gateway"
解决: 确保Ollama服务正常运行并安装nomic-embed-text模型
检查方法: 
  - curl http://localhost:11434/api/tags
  - ollama list
  - ollama pull nomic-embed-text
说明: 嵌入模型用于生成文档向量，必须正常运行
```

#### 1.4. LlamaIndex向量存储创建失败
```
错误: Failed to create new connection using: async-http://localhost:19530
解决: 已实现延迟创建机制，避免初始化时的异步连接问题
技术细节:
  - 初始化时只建立同步连接
  - LlamaIndex向量存储在需要时才创建
  - 添加了llama-index-embeddings-openai依赖
说明: 这种设计避免了Streamlit环境中的异步事件循环冲突
```

#### 2. 端口冲突
```
错误: Address already in use
解决: 检查19530端口是否被占用，或修改配置
```

#### 3. 内存不足
```
错误: Out of memory
解决: 增加系统内存或调整Milvus配置
```

### 降级模式
当Milvus服务器不可用时，系统会自动切换到内存存储模式：
- 文档存储在内存中
- 功能正常，但重启后数据丢失
- 控制台会显示相应提示信息

## 配置选项

### 环境变量
```bash
# Milvus服务器地址
export MILVUS_URI="http://localhost:19530"

# 集合名称
export MILVUS_COLLECTION="kflow"
```

### 代码配置
```python
# 自定义Milvus配置
milvus_repo = MilvusRepository(
    collection_name="my_collection",
    uri="http://my-milvus-server:19530"
)
```

## 性能优化

### 推荐配置
- **内存**: 至少8GB RAM
- **存储**: SSD硬盘，至少50GB可用空间
- **CPU**: 4核心以上
- **网络**: 低延迟网络连接

### 调优参数
```python
# 文档分割参数
text_splitter = SentenceSplitter(
    chunk_size=1024,      # 块大小
    chunk_overlap=200,    # 重叠大小
    separator=" "         # 分隔符
)

# 检索参数
query_engine = index.as_query_engine(
    similarity_top_k=5,   # 检索数量
    streaming=True        # 流式响应
)
```

## 监控和维护

### 健康检查
```python
# 获取集合信息
info = model.get_milvus_info()
print(f"状态: {info['status']}")
print(f"存储类型: {info['storage_type']}")
```

### 数据清理
```python
# 清空整个集合
model.clear_milvus_collection()
```

## 更新日志

### v1.0.0
- ✅ 集成Milvus向量数据库
- ✅ 实现文档持久化存储
- ✅ 支持文件替换功能
- ✅ 添加优雅降级机制
- ✅ 优化检索性能

## 支持

如有问题，请检查：
1. Milvus服务器是否正常运行
2. 网络连接是否正常
3. 系统资源是否充足
4. 依赖包是否正确安装
