# Advanced RAG with LlamaIndex and Milvus

An advanced RAG (Retrieval-Augmented Generation) implementation using LlamaIndex framework and Milvus vector database. This project demonstrates sentence window retrieval with reranking for improved answer quality.

## Features

- **Milvus Vector Database**: High-performance vector storage and retrieval
- **Sentence Window Node Parser**: Context-aware text chunking with surrounding sentences
- **Reranking**: Cross-encoder reranking for better result relevance
- **DeepSeek LLM**: Powerful language model for answer generation
- **Ollama Embeddings**: Local nomic-embed-text embedding model
- **Metadata Post-Processing**: Enhanced context through metadata replacement
- **Embedded Milvus Server**: Automatic Milvus server management

## Architecture

```
┌──────────────┐
│  Documents   │
│ (Milvus Docs)│
└──────┬───────┘
       │
       ▼
┌────────────────────┐
│ Sentence Window    │
│   Node Parser      │
│ (window_size=3)    │
└──────┬─────────────┘
       │
       ▼
┌────────────────────┐
│  Milvus Vector     │
│      Store         │
│ (768 dimensions)   │
└──────┬─────────────┘
       │
       ▼
┌────────────────────┐    ┌──────────────┐
│  Query Engine      │───►│  Reranker    │
│  (Top-K=3)         │    │ (BGE Model)  │
└────────────────────┘    └──────────────┘
```

## Prerequisites

- Python >= 3.12
- [Ollama](https://ollama.com/) installed and running
- DeepSeek API key
- Sufficient disk space for Milvus data

## Installation

1. **Install Ollama and Embedding Model**:

   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull embedding model
   ollama pull nomic-embed-text
   ```

2. **Set up DeepSeek API**:

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

### Running the Advanced RAG System

Execute the main script:

```bash
uv run advanced_rag_llamaindex_milvus.py
```

The script will:
1. Start embedded Milvus server
2. Load Milvus documentation
3. Parse documents with sentence window strategy
4. Create Milvus vector store and index
5. Set up query engine with reranking
6. Process example query
7. Shut down Milvus server gracefully

### Example Query

```python
query = "Can user delete milvus entities through non-primary key filtering?"
response = query_engine.query(query)
print(response)
```

## Technical Details

### Sentence Window Node Parser

Creates nodes with surrounding context for better retrieval:

```python
node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,
    window_metadata_key="window",
    original_text_metadata_key="original_text",
)
```

- `window_size=3`: Includes 3 sentences before and after
- Stores original text and window context in metadata

### Milvus Vector Store Configuration

```python
vector_store = MilvusVectorStore(
    dim=768,  # nomic-embed-text dimension
    uri="http://localhost:19530",
    collection_name='advance_rag',
    overwrite=True
)
```

### Post-Processing Pipeline

**1. Metadata Replacement:**
```python
postproc = MetadataReplacementPostProcessor(
    target_metadata_key="window"
)
```
Replaces node content with window context for richer information.

**2. Reranking:**
```python
rerank = SentenceTransformerRerank(
    top_n=3,
    model="BAAI/bge-reranker-base"
)
```
Uses cross-encoder model to rerank retrieved results.

### Query Engine

```python
query_engine = index.as_query_engine(
    similarity_top_k=3,
    node_postprocessors=[postproc, rerank],
)
```

## Advanced RAG Techniques

### 1. Sentence Window Retrieval
- Retrieves sentences with surrounding context
- Improves answer quality by providing more information
- Reduces loss of context from aggressive chunking

### 2. Metadata Replacement
- Replaces retrieved chunks with window metadata
- Provides richer context to the LLM
- Maintains sentence-level granularity

### 3. Reranking
- Uses BAAI/bge-reranker-base cross-encoder
- Reorders results based on query relevance
- Improves final answer quality

## Project Structure

```
rag-on-milvus/
├── advanced_rag_llamaindex_milvus.py  # Main implementation
├── main.py                            # Entry point
├── data/                              # Input documents
│   └── milvus_doc.md                 # Milvus documentation
├── pyproject.toml                     # Project configuration
└── README.md                          # This file
```

## Performance Optimization

- **Embedding Model**: Local Ollama for fast, cost-free embeddings
- **Milvus**: High-performance vector database with efficient indexing
- **Reranking**: Improves precision without sacrificing recall
- **Sentence Windows**: Balances chunk size and context

## Troubleshooting

### Common Issues

1. **Milvus Server Start Failed**:
   ```bash
   # Check if port 19530 is available
   lsof -i :19530
   
   # Kill existing Milvus process if needed
   pkill -f milvus
   ```

2. **Ollama Connection Failed**:
   ```bash
   # Ensure Ollama is running
   ollama serve
   
   # Check embedding model
   ollama pull nomic-embed-text
   ```

3. **DeepSeek API Issues**:
   - Verify API key in `.env` file
   - Check API quota and billing
   - Ensure network connectivity

4. **Reranker Model Download**:
   - First run will download BAAI/bge-reranker-base from HuggingFace
   - Requires stable internet connection
   - Model cached locally after first download

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

This project's source code is primarily based on the article ["基于 Milvus + LlamaIndex 实现高级 RAG"](https://xie.infoq.cn/article/a08897bedfcea40840d42c301?utm_campaign=geektime_search&utm_content=geektime_search&utm_medium=geektime_search&utm_source=geektime_search&utm_term=geektime_search) with minor adjustments based on specific requirements.

**Original Article:** https://xie.infoq.cn/article/a08897bedfcea40840d42c301

**Key Adjustments:**
- Updated dependencies to latest versions
- Enhanced error handling and logging
- Added graceful server shutdown

**Key References:**
- [Advanced RAG with Milvus + LlamaIndex (InfoQ Article)](https://xie.infoq.cn/article/a08897bedfcea40840d42c301)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Milvus Documentation](https://milvus.io/docs)
- [BAAI/bge-reranker-base Model](https://huggingface.co/BAAI/bge-reranker-base)

We extend our gratitude to the article author for providing this excellent advanced RAG implementation guide.

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# 基于 Milvus + LlamaIndex 的高级 RAG

使用LlamaIndex框架和Milvus向量数据库的高级RAG（检索增强生成）实现。本项目展示了带重排序的句子窗口检索，以提高答案质量。

## 功能特性

- **Milvus向量数据库**：高性能向量存储和检索
- **句子窗口节点解析器**：带上下文句子的上下文感知文本分块
- **重排序**：使用交叉编码器重排序以提高结果相关性
- **DeepSeek LLM**：用于答案生成的强大语言模型
- **Ollama嵌入**：本地nomic-embed-text嵌入模型
- **元数据后处理**：通过元数据替换增强上下文
- **嵌入式Milvus服务器**：自动Milvus服务器管理

## 架构

```
┌──────────────┐
│  文档        │
│ (Milvus文档) │
└──────┬───────┘
       │
       ▼
┌────────────────────┐
│ 句子窗口           │
│   节点解析器       │
│ (window_size=3)    │
└──────┬─────────────┘
       │
       ▼
┌────────────────────┐
│  Milvus向量        │
│     存储           │
│ (768维度)          │
└──────┬─────────────┘
       │
       ▼
┌────────────────────┐    ┌──────────────┐
│  查询引擎          │───►│  重排序器     │
│  (Top-K=3)         │    │ (BGE模型)    │
└────────────────────┘    └──────────────┘
```

## 环境要求

- Python >= 3.12
- [Ollama](https://ollama.com/) 已安装并运行
- DeepSeek API密钥
- 足够的磁盘空间用于Milvus数据

## 安装步骤

1. **安装Ollama和嵌入模型**：

   ```bash
   # 安装Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # 下载嵌入模型
   ollama pull nomic-embed-text
   ```

2. **设置DeepSeek API**：

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

### 运行高级RAG系统

执行主脚本：

```bash
uv run advanced_rag_llamaindex_milvus.py
```

脚本将：
1. 启动嵌入式Milvus服务器
2. 加载Milvus文档
3. 使用句子窗口策略解析文档
4. 创建Milvus向量存储和索引
5. 设置带重排序的查询引擎
6. 处理示例查询
7. 优雅关闭Milvus服务器

### 示例查询

```python
query = "用户可以通过非主键过滤删除Milvus实体吗？"
response = query_engine.query(query)
print(response)
```

## 技术细节

### 句子窗口节点解析器

创建带周围上下文的节点以实现更好的检索：

```python
node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,
    window_metadata_key="window",
    original_text_metadata_key="original_text",
)
```

- `window_size=3`：包含前后3个句子
- 在元数据中存储原始文本和窗口上下文

### Milvus向量存储配置

```python
vector_store = MilvusVectorStore(
    dim=768,  # nomic-embed-text维度
    uri="http://localhost:19530",
    collection_name='advance_rag',
    overwrite=True
)
```

### 后处理管道

**1. 元数据替换：**
```python
postproc = MetadataReplacementPostProcessor(
    target_metadata_key="window"
)
```
用窗口上下文替换节点内容以获得更丰富的信息。

**2. 重排序：**
```python
rerank = SentenceTransformerRerank(
    top_n=3,
    model="BAAI/bge-reranker-base"
)
```
使用交叉编码器模型重排序检索结果。

### 查询引擎

```python
query_engine = index.as_query_engine(
    similarity_top_k=3,
    node_postprocessors=[postproc, rerank],
)
```

## 高级RAG技术

### 1. 句子窗口检索
- 检索带周围上下文的句子
- 通过提供更多信息提高答案质量
- 减少激进分块导致的上下文丢失

### 2. 元数据替换
- 用窗口元数据替换检索的块
- 为LLM提供更丰富的上下文
- 保持句子级粒度

### 3. 重排序
- 使用BAAI/bge-reranker-base交叉编码器
- 根据查询相关性重新排序结果
- 提高最终答案质量

## 项目结构

```
rag-on-milvus/
├── advanced_rag_llamaindex_milvus.py  # 主实现
├── main.py                            # 入口点
├── data/                              # 输入文档
│   └── milvus_doc.md                 # Milvus文档
├── pyproject.toml                     # 项目配置
└── README.md                          # 本文件
```

## 性能优化

- **嵌入模型**：本地Ollama实现快速、免费的嵌入
- **Milvus**：具有高效索引的高性能向量数据库
- **重排序**：在不牺牲召回率的情况下提高精确度
- **句子窗口**：平衡块大小和上下文

## 故障排除

### 常见问题

1. **Milvus服务器启动失败**：
   ```bash
   # 检查端口19530是否可用
   lsof -i :19530
   
   # 如需要，杀死现有Milvus进程
   pkill -f milvus
   ```

2. **Ollama连接失败**：
   ```bash
   # 确保Ollama正在运行
   ollama serve
   
   # 检查嵌入模型
   ollama pull nomic-embed-text
   ```

3. **DeepSeek API问题**：
   - 验证`.env`文件中的API密钥
   - 检查API配额和计费
   - 确保网络连接

4. **重排序模型下载**：
   - 首次运行将从HuggingFace下载BAAI/bge-reranker-base
   - 需要稳定的网络连接
   - 首次下载后模型会缓存在本地

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

本项目的源代码主要来自文章["基于 Milvus + LlamaIndex 实现高级 RAG"](https://xie.infoq.cn/article/a08897bedfcea40840d42c301?utm_campaign=geektime_search&utm_content=geektime_search&utm_medium=geektime_search&utm_source=geektime_search&utm_term=geektime_search)，然后根据需要做了少量调整。

**原始文章：** https://xie.infoq.cn/article/a08897bedfcea40840d42c301

**主要调整：**
- 更新依赖到最新版本
- 增强错误处理和日志记录
- 添加优雅的服务器关闭

**主要参考资料：**
- [基于 Milvus + LlamaIndex 实现高级 RAG（InfoQ文章）](https://xie.infoq.cn/article/a08897bedfcea40840d42c301)
- [LlamaIndex文档](https://docs.llamaindex.ai/)
- [Milvus文档](https://milvus.io/docs)
- [BAAI/bge-reranker-base模型](https://huggingface.co/BAAI/bge-reranker-base)

我们向文章作者表示感谢，感谢他们提供了这个优秀的高级RAG实现指南。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。

