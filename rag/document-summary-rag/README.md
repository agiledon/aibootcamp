# Document Summary RAG

A document summarization and retrieval system using LlamaIndex's DocumentSummaryIndex. This project demonstrates how to build an intelligent Q&A system that generates summaries for each document and uses them for efficient retrieval and question answering.

## Features

- **Document Summary Index**: Creates summaries for each document for better retrieval
- **Tree Summarize**: Hierarchical summarization for comprehensive answers
- **LLM Retrieval**: Uses LLM to select relevant documents based on summaries
- **Embedding Retrieval**: Retrieves relevant chunks using semantic search
- **Ollama Integration**: Local DeepSeek LLM and nomic-embed-text embedding model
- **Persistent Storage**: Saves index to disk for cross-session usage
- **Chinese City Knowledge Base**: Pre-configured with information about 5 major Chinese cities

## Architecture

```
┌──────────────┐
│   Documents  │
│ (City Info)  │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Document Summarizer  │
│ (Tree Summarize)     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐    ┌────────────────┐
│ Document Summary     │───►│  Query Engine  │
│      Index           │    │ (LLM/Embedding)│
└──────────────────────┘    └────────────────┘
```

### Workflow

1. **Document Loading**: Load city information from text files or predefined data
2. **Summary Generation**: Generate comprehensive summaries for each document
3. **Index Creation**: Build DocumentSummaryIndex with embeddings
4. **Index Persistence**: Save index to `city_index` directory
5. **Query Processing**: Answer questions using LLM or embedding-based retrieval

## Prerequisites

- Python >= 3.12
- [Ollama](https://ollama.com/) installed and running
- DeepSeek and nomic-embed-text models downloaded
- DeepSeek API key (optional, for enhanced features)

## Installation

1. **Install Ollama and Required Models**:

   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull required models
   ollama pull deepseek-r1:7b
   ollama pull nomic-embed-text
   ```

2. **Set up Environment (Optional)**:

   Create a `.env` file:
   ```bash
   DEEPSEEK_API_KEY=your_deepseek_api_key  # Optional
   ```

3. **Install Project Dependencies**:

   ```bash
   # Using uv (recommended)
   uv sync
   ```

## Usage

### Running the Document Summary System

Execute the main script:

```bash
uv run docuemnt_summanry.py
```

The script will:
1. Load city information for Beijing, Shanghai, Guangzhou, Shenzhen, and Hangzhou
2. Generate summaries for each city
3. Create a DocumentSummaryIndex
4. Persist the index to `city_index/`
5. Demonstrate query examples

### Example Queries

The system demonstrates two retrieval modes:

**1. LLM-based Retrieval (using document summaries):**
```python
retriever = DocumentSummaryIndexLLMRetriever(doc_summary_index)
response = retriever.retrieve("北京有哪些著名的旅游景点？")
```

**2. Embedding-based Retrieval (using vector similarity):**
```python
retriever = DocumentSummaryIndexEmbeddingRetriever(doc_summary_index)
response = retriever.retrieve("北京有哪些著名的旅游景点？")
```

## Project Structure

```
document-summary-rag/
├── docuemnt_summanry.py      # Main implementation
├── main.py                   # Entry point
├── data/                     # City information text files
│   ├── 北京.txt
│   ├── 上海.txt
│   ├── 广州.txt
│   ├── 深圳.txt
│   └── 杭州.txt
├── city_index/               # Persisted index storage
│   ├── docstore.json
│   ├── index_store.json
│   ├── default__vector_store.json
│   └── ...
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Technical Details

### DocumentSummaryIndex Creation

```python
# Create the index with tree summarization
response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize", 
    use_async=True, 
    llm=llm
)

doc_summary_index = DocumentSummaryIndex.from_documents(
    city_docs,
    llm=llm,
    embed_model=embed_model,
    transformations=[splitter],
    response_synthesizer=response_synthesizer,
    show_progress=True,
)
```

### LLM Configuration

```python
llm = Ollama(
    model="deepseek-r1:7b",
    base_url="http://localhost:11434",
    request_timeout=300.0,
    keep_alive="5m"
)
```

### Embedding Configuration

```python
embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    request_timeout=300,
    keep_alive="5m"
)
```

### Retrieval Modes

**1. LLM Retrieval:**
- Uses document summaries to select relevant documents
- LLM evaluates which summaries best match the query
- More intelligent but slower

**2. Embedding Retrieval:**
- Uses vector similarity to find relevant chunks
- Faster but may miss context from summaries
- Good for specific fact-finding

## City Knowledge Base

The system includes information about 5 major Chinese cities:

- **北京 (Beijing)**: Capital, political and cultural center, historical sites
- **上海 (Shanghai)**: Economic and financial center, international port city
- **广州 (Guangzhou)**: Commercial hub, "Flower City", trade center
- **深圳 (Shenzhen)**: Special Economic Zone, high-tech innovation center
- **杭州 (Hangzhou)**: E-commerce capital, "Paradise on Earth", home to Alibaba

## Example Output

**Query:** "北京有哪些著名的旅游景点？" (What are the famous tourist attractions in Beijing?)

**Response using Tree Summarize:**
```
北京拥有众多历史文化古迹，包括故宫、天坛、颐和园、长城等世界著名景点。
这些景点展示了中国悠久的历史和灿烂的文化。
```

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**:
   ```bash
   # Ensure Ollama is running
   ollama serve
   
   # Check models are installed
   ollama list
   ```

2. **Model Download Issues**:
   ```bash
   # Pull required models
   ollama pull deepseek-r1:7b
   ollama pull nomic-embed-text
   ```

3. **Index Persistence Issues**:
   - Ensure `city_index/` directory has write permissions
   - Check available disk space

4. **Query Timeout**:
   - Increase `request_timeout` parameter
   - Use embedding retrieval for faster responses

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

This project's code is primarily based on the Document Summary Index examples from the LlamaIndex official documentation, specifically the [RAG Workflow with Reranking](https://developers.llamaindex.ai/python/examples/workflow/rag) tutorial and Document Summary Index patterns.

**Key References:**
- [LlamaIndex RAG Workflow Examples](https://developers.llamaindex.ai/python/examples/workflow/rag)
- [LlamaIndex DocumentSummaryIndex](https://docs.llamaindex.ai/en/stable/examples/index_structs/doc_summary/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)

We extend our gratitude to the LlamaIndex team for providing comprehensive documentation and examples that made this project possible.

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# 文档摘要RAG

使用LlamaIndex的DocumentSummaryIndex的文档摘要和检索系统。本项目展示了如何构建一个智能问答系统，为每个文档生成摘要并使用它们进行高效检索和问答。

## 功能特性

- **文档摘要索引**：为每个文档创建摘要以实现更好的检索
- **树形摘要**：用于综合答案的层次化摘要
- **LLM检索**：使用LLM基于摘要选择相关文档
- **嵌入检索**：使用语义搜索检索相关块
- **Ollama集成**：本地DeepSeek LLM和nomic-embed-text嵌入模型
- **持久化存储**：将索引保存到磁盘以实现跨会话使用
- **中国城市知识库**：预配置了5个主要中国城市的信息

## 架构

```
┌──────────────┐
│   文档       │
│ (城市信息)   │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ 文档摘要生成器        │
│ (树形摘要)           │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐    ┌────────────────┐
│ 文档摘要索引          │───►│  查询引擎      │
│                      │    │ (LLM/嵌入)     │
└──────────────────────┘    └────────────────┘
```

### 工作流程

1. **文档加载**：从文本文件或预定义数据加载城市信息
2. **摘要生成**：为每个文档生成综合摘要
3. **索引创建**：使用嵌入构建DocumentSummaryIndex
4. **索引持久化**：将索引保存到`city_index`目录
5. **查询处理**：使用LLM或基于嵌入的检索回答问题

## 环境要求

- Python >= 3.12
- [Ollama](https://ollama.com/) 已安装并运行
- 已下载DeepSeek和nomic-embed-text模型
- DeepSeek API密钥（可选，用于增强功能）

## 安装步骤

1. **安装Ollama和所需模型**：

   ```bash
   # 安装Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # 下载所需模型
   ollama pull deepseek-r1:7b
   ollama pull nomic-embed-text
   ```

2. **设置环境（可选）**：

   创建`.env`文件：
   ```bash
   DEEPSEEK_API_KEY=your_deepseek_api_key  # 可选
   ```

3. **安装项目依赖**：

   ```bash
   # 使用uv（推荐）
   uv sync
   ```

## 使用方法

### 运行文档摘要系统

执行主脚本：

```bash
uv run docuemnt_summanry.py
```

脚本将：
1. 加载北京、上海、广州、深圳和杭州的城市信息
2. 为每个城市生成摘要
3. 创建DocumentSummaryIndex
4. 将索引持久化到`city_index/`
5. 演示查询示例

### 示例查询

系统演示了两种检索模式：

**1. 基于LLM的检索（使用文档摘要）：**
```python
retriever = DocumentSummaryIndexLLMRetriever(doc_summary_index)
response = retriever.retrieve("北京有哪些著名的旅游景点？")
```

**2. 基于嵌入的检索（使用向量相似度）：**
```python
retriever = DocumentSummaryIndexEmbeddingRetriever(doc_summary_index)
response = retriever.retrieve("北京有哪些著名的旅游景点？")
```

## 项目结构

```
document-summary-rag/
├── docuemnt_summanry.py      # 主实现
├── main.py                   # 入口点
├── data/                     # 城市信息文本文件
│   ├── 北京.txt
│   ├── 上海.txt
│   ├── 广州.txt
│   ├── 深圳.txt
│   └── 杭州.txt
├── city_index/               # 持久化索引存储
│   ├── docstore.json
│   ├── index_store.json
│   ├── default__vector_store.json
│   └── ...
├── pyproject.toml            # 项目配置
└── README.md                 # 本文件
```

## 技术细节

### DocumentSummaryIndex创建

```python
# 使用树形摘要创建索引
response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize", 
    use_async=True, 
    llm=llm
)

doc_summary_index = DocumentSummaryIndex.from_documents(
    city_docs,
    llm=llm,
    embed_model=embed_model,
    transformations=[splitter],
    response_synthesizer=response_synthesizer,
    show_progress=True,
)
```

### LLM配置

```python
llm = Ollama(
    model="deepseek-r1:7b",
    base_url="http://localhost:11434",
    request_timeout=300.0,
    keep_alive="5m"
)
```

### 嵌入配置

```python
embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    request_timeout=300,
    keep_alive="5m"
)
```

### 检索模式

**1. LLM检索：**
- 使用文档摘要选择相关文档
- LLM评估哪些摘要最匹配查询
- 更智能但速度较慢

**2. 嵌入检索：**
- 使用向量相似度查找相关块
- 更快但可能错过摘要中的上下文
- 适合特定事实查找

## 城市知识库

系统包含5个主要中国城市的信息：

- **北京**：首都，政治文化中心，历史名胜
- **上海**：经济金融中心，国际港口城市
- **广州**：商贸中心，"花城"，贸易中心
- **深圳**：经济特区，高科技创新中心
- **杭州**：电子商务之都，"人间天堂"，阿里巴巴总部所在地

## 示例输出

**查询：** "北京有哪些著名的旅游景点？"

**使用树形摘要的响应：**
```
北京拥有众多历史文化古迹，包括故宫、天坛、颐和园、长城等世界著名景点。
这些景点展示了中国悠久的历史和灿烂的文化。
```

## 故障排除

### 常见问题

1. **Ollama连接失败**：
   ```bash
   # 确保Ollama正在运行
   ollama serve
   
   # 检查模型已安装
   ollama list
   ```

2. **模型下载问题**：
   ```bash
   # 下载所需模型
   ollama pull deepseek-r1:7b
   ollama pull nomic-embed-text
   ```

3. **索引持久化问题**：
   - 确保`city_index/`目录有写入权限
   - 检查可用磁盘空间

4. **查询超时**：
   - 增加`request_timeout`参数
   - 使用嵌入检索以获得更快响应

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

本项目的代码主要参考了LlamaIndex官方文档，特别是[RAG Workflow with Reranking](https://developers.llamaindex.ai/python/examples/workflow/rag)教程中介绍的Document Summary Index示例。

**主要参考资料：**
- [LlamaIndex RAG工作流示例](https://developers.llamaindex.ai/python/examples/workflow/rag)
- [LlamaIndex DocumentSummaryIndex](https://docs.llamaindex.ai/en/stable/examples/index_structs/doc_summary/)
- [LlamaIndex文档](https://docs.llamaindex.ai/)

我们向LlamaIndex团队表示感谢，感谢他们提供了全面的文档和示例，使这个项目成为可能。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。
