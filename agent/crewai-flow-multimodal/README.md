# CrewAI Flow Multimodal

这是一个基于CrewAI的多模态RAG系统，支持文档和音频文件的处理和查询。

## 环境配置

### 1. 创建.env文件

在项目根目录创建`.env`文件，包含以下配置：

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

# 嵌入模型配置（Ollama本地模型）
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_DIMENSION=768
OLLAMA_BASE_URL=http://localhost:11434
```

### 2. API密钥获取

#### DeepSeek API
1. 访问 [DeepSeek官网](https://platform.deepseek.com/)
2. 注册账号并获取API密钥
3. 将密钥填入`DEEPSEEK_API_KEY`

#### Ollama (嵌入模型)
1. 安装Ollama: https://ollama.ai/
2. 下载嵌入模型: `ollama pull nomic-embed-text:latest`
3. 确保Ollama服务运行: `ollama serve`

#### AssemblyAI API
1. 访问 [AssemblyAI官网](https://www.assemblyai.com/)
2. 注册账号并获取API密钥
3. 将密钥填入`ASSEMBLYAI_API_KEY`

### 3. 安装依赖

```bash
# 使用uv安装依赖
uv sync

# 或使用pip安装
pip install -r requirements.txt
```

### 4. 启动服务

#### 选项1：使用现有的Milvus服务
如果您的系统中已经有Milvus服务在运行，可以直接使用：

```bash
# 检查Milvus服务状态
docker ps | grep milvus

# 如果Milvus已运行，直接启动主程序
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

在首次运行前，建议先运行系统测试脚本：

```bash
# 运行系统测试
python test_system.py
```

测试脚本会检查：
- ✅ 所有依赖包是否正确安装
- ✅ 配置文件是否正确
- ✅ API密钥是否已配置
- ✅ Milvus连接是否正常
- ✅ Ollama嵌入模型连接是否正常
- ✅ 嵌入维度一致性（768维）

## 功能特性

- **多模态支持**: 支持PDF文档和音频文件（MP3、WAV、M4A、FLAC）
- **智能处理**: 使用CrewAI多智能体协作进行文档处理
- **向量检索**: 基于Milvus向量数据库的语义搜索
- **语音转文本**: 使用AssemblyAI进行音频转录
- **统一LLM**: 所有组件（CrewAI、直接LLM调用）都使用DeepSeek模型
- **智能问答**: 基于DeepSeek模型的智能问答系统

## 文件结构

```
├── main.py              # 主程序文件
├── config.py            # 配置文件
├── requirements.txt     # Python依赖
├── docker-compose.yml   # Docker服务配置
├── data/               # 数据文件目录
└── .env                # 环境变量配置
```

## 注意事项

1. **嵌入模型限制**: 目前DeepSeek API不支持嵌入模型，因此使用OpenAI的text-embedding-3-small模型
2. **网络要求**: 需要能够访问DeepSeek、OpenAI和AssemblyAI的API服务
3. **Milvus数据库**: 需要启动Milvus数据库服务才能正常使用向量检索功能

