# CrewAI Flow Multimodal

A multimodal RAG (Retrieval-Augmented Generation) system based on CrewAI that supports processing and querying documents and audio files.

## Features

- **Multimodal Support**: Supports PDF documents and audio files (MP3, WAV, M4A, FLAC)
- **Intelligent Processing**: Uses CrewAI multi-agent collaboration for document processing
- **Vector Retrieval**: Semantic search based on Milvus vector database
- **Speech-to-Text**: Audio transcription using AssemblyAI
- **Unified LLM**: All components (CrewAI, direct LLM calls) use DeepSeek models
- **Intelligent Q&A**: Intelligent question-answering system based on DeepSeek models

## Architecture

The system consists of several key components organized in a modular architecture:

- **Client Layer**: Specialized clients for external service integration
  - **DeepSeek LLM**: Unified language model for all text generation tasks
  - **Ollama Embeddings**: Local embedding model for vector generation
  - **Milvus Vector Database**: High-performance vector storage and retrieval
  - **AssemblyAI Integration**: Real-time audio transcription services

- **Workflow Layer**: CrewAI-based intelligent workflows
  - **CrewAI Agents**: Multi-agent collaboration for document processing and analysis
  - **Data Ingestion Flow**: Automated document and audio processing
  - **Multimodal RAG Flow**: Intelligent query processing and response generation

- **Command Layer**: Command pattern implementation for operation management
  - **Command Handler**: Centralized command execution and management
  - **Command Pattern**: Extensible command structure for future operations

## Environment Setup

### 1. Create .env File

Create a `.env` file in the project root directory with the following configuration:

```bash
# DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here
LLM_MODEL=deepseek-chat
LLM_API_BASE=https://api.deepseek.com

# AssemblyAI API Configuration
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here

# Milvus Vector Database Configuration
MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_COLLECTION_NAME=multimodal_rag

# Embedding Model Configuration (Ollama Local Model)
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_DIMENSION=768
OLLAMA_BASE_URL=http://localhost:11434
```

### 2. API Key Setup

#### DeepSeek API
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Register an account and obtain API key
3. Add the key to `DEEPSEEK_API_KEY`

#### Ollama (Embedding Model)
1. Install Ollama: https://ollama.ai/
2. Download embedding model: `ollama pull nomic-embed-text:latest`
3. Ensure Ollama service is running: `ollama serve`

#### AssemblyAI API
1. Visit [AssemblyAI](https://www.assemblyai.com/)
2. Register an account and obtain API key
3. Add the key to `ASSEMBLYAI_API_KEY`

### 3. Install Dependencies

```bash
# Recommended: Install dependencies using uv (faster and more reliable)
uv sync

# Alternative: Install using pip
pip install -r requirements.txt

# Note: The project uses Python 3.12 as specified in .python-version
```

### 4. Start Services

#### Option 1: Use Existing Milvus Service
If you already have Milvus service running on your system:

```bash
# Check Milvus service status
docker ps | grep milvus

# If Milvus is running, start the main program directly
python main.py
```

#### Option 2: Start New Milvus Service
If you need to start a new Milvus service:

```bash
# Start Milvus database (using Docker)
docker-compose up -d

# Run the main program
python main.py
```

### 5. System Testing

Before first run, it's recommended to run the system test script:

```bash
# Run system tests
python test_system.py
```

The test script will check:
- ✅ All dependency packages are correctly installed
- ✅ Configuration files are correct
- ✅ API keys are configured
- ✅ Milvus connection is normal
- ✅ Ollama embedding model connection is normal
- ✅ Embedding dimension consistency (768 dimensions)

## Usage

### Basic Usage

1. **Start the system**:
   ```bash
   python main.py
   ```

2. **Upload documents**: Place your PDF files in the `data/` directory

3. **Upload audio files**: Place your audio files (MP3, WAV, etc.) in the `data/` directory

4. **Query the system**: Use the interactive interface to ask questions about your documents

### Advanced Usage

The system supports various query types:

- **Document-based queries**: Ask questions about PDF content
- **Audio-based queries**: Ask questions about transcribed audio content
- **Cross-modal queries**: Ask questions that span multiple document types
- **Temporal queries**: Ask about content changes over time

## File Structure

```
├── main.py                    # Main program file
├── config.py                  # Configuration file
├── pyproject.toml             # Project configuration and dependencies
├── requirements.txt           # Python dependencies (legacy)
├── uv.lock                    # UV lock file for dependency management
├── uv.toml                    # UV configuration
├── .python-version            # Python version specification (3.12)
├── docker-compose.yml         # Docker service configuration
├── client/                    # Client modules directory
│   ├── __init__.py           # Client package initialization
│   ├── llm_client.py         # LLM client wrapper
│   ├── embedding_client.py   # Embedding model client
│   ├── milvus_client.py      # Milvus vector database client
│   └── assemblyai_client.py  # AssemblyAI transcription client
├── crewai_workflows/          # CrewAI workflow modules
│   ├── __init__.py           # Workflow package initialization
│   ├── crewai_client.py      # CrewAI integration client
│   ├── data_ingestion_flow.py # Data ingestion workflow
│   └── multimodal_rag_flow.py # Multimodal RAG workflow
├── command/                   # Command pattern modules
│   ├── __init__.py           # Command package initialization
│   ├── command_handler.py    # Command pattern handler
│   └── command_pattern.py    # Command pattern implementation
├── data/                      # Data files directory
│   ├── annualreport-2024.pdf # Sample PDF document
│   └── finance_audio.mp3     # Sample audio file
├── __pycache__/               # Python cache directory
└── .env                       # Environment variables configuration (not tracked)
```

## Technical Details

### Modular Architecture

The system is built with a modular architecture for better maintainability and scalability:

- **Client Layer** (`client/`): Contains specialized clients for different services
  - `llm_client.py`: DeepSeek LLM integration
  - `embedding_client.py`: Ollama embedding model integration
  - `milvus_client.py`: Milvus vector database operations
  - `assemblyai_client.py`: Audio transcription services

- **Workflow Layer** (`crewai_workflows/`): Contains CrewAI-based workflows
  - `crewai_client.py`: CrewAI agent orchestration
  - `data_ingestion_flow.py`: Document and audio processing workflows
  - `multimodal_rag_flow.py`: RAG query processing workflows

- **Command Layer** (`command/`): Implements command pattern for operation handling
  - `command_pattern.py`: Base command pattern implementation
  - `command_handler.py`: Command execution and management

### Multimodal Processing Pipeline

1. **Document Processing**: PDFs are parsed and chunked for optimal retrieval
2. **Audio Processing**: Audio files are transcribed using AssemblyAI
3. **Embedding Generation**: Text chunks are converted to vectors using Ollama
4. **Vector Storage**: Embeddings are stored in Milvus with metadata
5. **Query Processing**: User queries are processed through the same pipeline
6. **Retrieval**: Relevant chunks are retrieved based on semantic similarity
7. **Generation**: Final answers are generated using DeepSeek LLM

### Performance Optimizations

- **Batch Processing**: Multiple documents processed in parallel
- **Caching**: Embedding results cached to avoid recomputation
- **Indexing**: Optimized Milvus indexes for fast retrieval
- **Memory Management**: Efficient memory usage for large document sets

## Troubleshooting

### Common Issues

1. **Milvus Connection Failed**:
   - Ensure Milvus service is running
   - Check connection parameters in `.env`
   - Verify network connectivity

2. **Ollama Embedding Model Not Found**:
   - Run `ollama pull nomic-embed-text:latest`
   - Check Ollama service status
   - Verify model name in configuration

3. **API Key Issues**:
   - Verify API keys are correctly set in `.env`
   - Check API quotas and billing
   - Ensure network access to API endpoints

### Performance Tuning

- **Embedding Dimension**: Adjust `EMBEDDING_DIMENSION` based on your needs
- **Chunk Size**: Modify chunk size for optimal retrieval performance
- **Batch Size**: Adjust batch processing size based on available memory

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

### Original Project Credits
This repository is based on and significantly refactored from the [multimodal-rag-assemblyai](https://github.com/patchy631/ai-engineering-hub) project in the [AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub). 

**Key Improvements and Enhancements:**
- **Code Refactoring**: Complete architectural redesign with improved modularity and maintainability
- **DeepSeek Integration**: Full support for DeepSeek LLM models as the primary language model
- **Ollama Local Deployment**: Integration with Ollama for local deployment of nomic-embed-text embedding models

We extend our gratitude to the original contributors of the AI Engineering Hub for providing the foundational multimodal RAG implementation.

## Notes

1. **Embedding Model Limitation**: DeepSeek API currently doesn't support embedding models, so OpenAI's text-embedding-3-small model is used
2. **Network Requirements**: Requires access to DeepSeek, OpenAI, and AssemblyAI API services
3. **Milvus Database**: Milvus database service must be running for vector retrieval functionality to work properly
4. **Resource Requirements**: Ensure sufficient memory and CPU resources for optimal performance

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# CrewAI Flow 多模态

基于CrewAI的多模态RAG（检索增强生成）系统，支持处理和查询文档和音频文件。

## 功能特性

- **多模态支持**：支持PDF文档和音频文件（MP3、WAV、M4A、FLAC）
- **智能处理**：使用CrewAI多智能体协作进行文档处理
- **向量检索**：基于Milvus向量数据库的语义搜索
- **语音转文字**：使用AssemblyAI进行音频转录
- **统一LLM**：所有组件（CrewAI、直接LLM调用）使用DeepSeek模型
- **智能问答**：基于DeepSeek模型的智能问答系统

## 架构

系统由几个关键组件组成，采用模块化架构组织：

- **客户端层**：专门用于外部服务集成的客户端
  - **DeepSeek LLM**：所有文本生成任务的统一语言模型
  - **Ollama嵌入**：用于向量生成的本地嵌入模型
  - **Milvus向量数据库**：高性能向量存储和检索
  - **AssemblyAI集成**：实时音频转录服务

- **工作流层**：基于CrewAI的智能工作流
  - **CrewAI智能体**：文档处理和分析的多智能体协作
  - **数据摄取流程**：自动化文档和音频处理
  - **多模态RAG流程**：智能查询处理和响应生成

- **命令层**：用于操作管理的命令模式实现
  - **命令处理器**：集中式命令执行和管理
  - **命令模式**：可扩展的命令结构，用于未来操作

## 环境设置

### 1. 创建.env文件

在项目根目录创建`.env`文件，包含以下配置：

```bash
# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
LLM_MODEL=deepseek-chat
LLM_API_BASE=https://api.deepseek.com

# AssemblyAI API配置
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here

# Milvus向量数据库配置
MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_COLLECTION_NAME=multimodal_rag

# 嵌入模型配置（Ollama本地模型）
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_DIMENSION=768
OLLAMA_BASE_URL=http://localhost:11434
```

### 2. API密钥设置

#### DeepSeek API
1. 访问 [DeepSeek Platform](https://platform.deepseek.com/)
2. 注册账户并获取API密钥
3. 将密钥添加到`DEEPSEEK_API_KEY`

#### Ollama（嵌入模型）
1. 安装Ollama：https://ollama.ai/
2. 下载嵌入模型：`ollama pull nomic-embed-text:latest`
3. 确保Ollama服务运行：`ollama serve`

#### AssemblyAI API
1. 访问 [AssemblyAI](https://www.assemblyai.com/)
2. 注册账户并获取API密钥
3. 将密钥添加到`ASSEMBLYAI_API_KEY`

### 3. 安装依赖

```bash
# 推荐：使用uv安装依赖（更快更可靠）
uv sync

# 备选：使用pip安装
pip install -r requirements.txt

# 注意：项目使用.python-version中指定的Python 3.12
```

### 4. 启动服务

#### 选项1：使用现有Milvus服务
如果您的系统上已有Milvus服务运行：

```bash
# 检查Milvus服务状态
docker ps | grep milvus

# 如果Milvus正在运行，直接启动主程序
python main.py
```

#### 选项2：启动新的Milvus服务
如果需要启动新的Milvus服务：

```bash
# 启动Milvus数据库（使用Docker）
docker-compose up -d

# 运行主程序
python main.py
```

### 5. 系统测试

首次运行前，建议运行系统测试脚本：

```bash
# 运行系统测试
python test_system.py
```

测试脚本将检查：
- ✅ 所有依赖包正确安装
- ✅ 配置文件正确
- ✅ API密钥已配置
- ✅ Milvus连接正常
- ✅ Ollama嵌入模型连接正常
- ✅ 嵌入维度一致性（768维度）

## 使用方法

### 基本使用

1. **启动系统**：
   ```bash
   python main.py
   ```

2. **上传文档**：将PDF文件放在`data/`目录中

3. **上传音频文件**：将音频文件（MP3、WAV等）放在`data/`目录中

4. **查询系统**：使用交互界面询问关于文档的问题

### 高级使用

系统支持各种查询类型：

- **基于文档的查询**：询问PDF内容相关问题
- **基于音频的查询**：询问转录音频内容相关问题
- **跨模态查询**：询问跨越多种文档类型的问题
- **时间查询**：询问内容随时间变化的问题

## 文件结构

```
├── main.py                    # 主程序文件
├── config.py                  # 配置文件
├── pyproject.toml             # 项目配置和依赖
├── requirements.txt           # Python依赖（遗留）
├── uv.lock                    # UV锁文件，用于依赖管理
├── uv.toml                    # UV配置
├── .python-version            # Python版本规范（3.12）
├── docker-compose.yml         # Docker服务配置
├── client/                    # 客户端模块目录
│   ├── __init__.py           # 客户端包初始化
│   ├── llm_client.py         # LLM客户端包装器
│   ├── embedding_client.py   # 嵌入模型客户端
│   ├── milvus_client.py      # Milvus向量数据库客户端
│   └── assemblyai_client.py  # AssemblyAI转录客户端
├── crewai_workflows/          # CrewAI工作流模块
│   ├── __init__.py           # 工作流包初始化
│   ├── crewai_client.py      # CrewAI集成客户端
│   ├── data_ingestion_flow.py # 数据摄取工作流
│   └── multimodal_rag_flow.py # 多模态RAG工作流
├── command/                   # 命令模式模块
│   ├── __init__.py           # 命令包初始化
│   ├── command_handler.py    # 命令模式处理器
│   └── command_pattern.py    # 命令模式实现
├── data/                      # 数据文件目录
│   ├── annualreport-2024.pdf # 示例PDF文档
│   └── finance_audio.mp3     # 示例音频文件
├── __pycache__/               # Python缓存目录
└── .env                       # 环境变量配置（不跟踪）
```

## 技术细节

### 模块化架构

系统采用模块化架构构建，以便更好地维护和扩展：

- **客户端层**（`client/`）：包含不同服务的专门客户端
  - `llm_client.py`：DeepSeek LLM集成
  - `embedding_client.py`：Ollama嵌入模型集成
  - `milvus_client.py`：Milvus向量数据库操作
  - `assemblyai_client.py`：音频转录服务

- **工作流层**（`crewai_workflows/`）：包含基于CrewAI的工作流
  - `crewai_client.py`：CrewAI智能体编排
  - `data_ingestion_flow.py`：文档和音频处理工作流
  - `multimodal_rag_flow.py`：RAG查询处理工作流

- **命令层**（`command/`）：实现用于操作处理的命令模式
  - `command_pattern.py`：基础命令模式实现
  - `command_handler.py`：命令执行和管理

### 多模态处理管道

1. **文档处理**：PDF被解析和分块以优化检索
2. **音频处理**：使用AssemblyAI转录音频文件
3. **嵌入生成**：使用Ollama将文本块转换为向量
4. **向量存储**：嵌入存储在Milvus中，带有元数据
5. **查询处理**：用户查询通过相同管道处理
6. **检索**：基于语义相似性检索相关块
7. **生成**：使用DeepSeek LLM生成最终答案

### 性能优化

- **批处理**：并行处理多个文档
- **缓存**：缓存嵌入结果以避免重新计算
- **索引**：优化的Milvus索引以实现快速检索
- **内存管理**：对大型文档集的高效内存使用

## 故障排除

### 常见问题

1. **Milvus连接失败**：
   - 确保Milvus服务正在运行
   - 检查`.env`中的连接参数
   - 验证网络连接

2. **找不到Ollama嵌入模型**：
   - 运行`ollama pull nomic-embed-text:latest`
   - 检查Ollama服务状态
   - 验证配置中的模型名称

3. **API密钥问题**：
   - 验证API密钥在`.env`中正确设置
   - 检查API配额和计费
   - 确保对API端点的网络访问

### 性能调优

- **嵌入维度**：根据需求调整`EMBEDDING_DIMENSION`
- **块大小**：修改块大小以优化检索性能
- **批处理大小**：根据可用内存调整批处理大小

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

### 原始项目致谢
本仓库基于并大幅重构了[AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub)中的[multimodal-rag-assemblyai](https://github.com/patchy631/ai-engineering-hub)项目。

**关键改进和增强：**
- **代码重构**：完整的架构重新设计，提高了模块化和可维护性
- **DeepSeek集成**：完全支持DeepSeek LLM模型作为主要语言模型
- **Ollama本地部署**：与Ollama集成，用于nomic-embed-text嵌入模型的本地部署

我们向AI Engineering Hub的原始贡献者表示感谢，感谢他们提供了基础的多模态RAG实现。

## 注意事项

1. **嵌入模型限制**：DeepSeek API目前不支持嵌入模型，因此使用OpenAI的text-embedding-3-small模型
2. **网络要求**：需要访问DeepSeek、OpenAI和AssemblyAI API服务
3. **Milvus数据库**：Milvus数据库服务必须运行，向量检索功能才能正常工作
4. **资源要求**：确保有足够的内存和CPU资源以获得最佳性能

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。