# LangChain ReAct Agent

A practical implementation of the ReAct (Reasoning and Acting) pattern using LangChain framework. This project demonstrates how to create an intelligent agent that can reason about problems and take actions using available tools.

## Features

- **ReAct Pattern Implementation**: Combines reasoning and acting in an iterative loop
- **Tool Integration**: Mathematical calculator and web search capabilities
- **Ollama LLM**: Uses local Llama3 model for cost-effective processing
- **Error Handling**: Robust error handling for parsing and execution
- **Interactive Agent**: Can handle complex queries requiring multiple steps

## Architecture

The system implements the ReAct pattern with the following components:

```
┌─────────────────┐    ReAct Loop     ┌─────────────────┐
│   Reasoning     │ ◄──────────────► │     Acting      │
│   (Thought)     │                  │   (Action)      │
└─────────────────┘                  └─────────────────┘
         │                                     │
         ▼                                     ▼
   Analyze Problem                        Execute Tools
   Plan Next Step                         Get Results
```

### ReAct Pattern Flow

1. **Thought**: Agent reasons about the current situation
2. **Action**: Agent decides which tool to use
3. **Action Input**: Agent provides input to the tool
4. **Observation**: Agent receives tool output
5. **Repeat**: Continue until problem is solved

## Tools Available

### 1. Calculator Tool
- **Function**: Performs mathematical calculations
- **Input**: Mathematical expressions (e.g., "2 + 2", "100 * 0.85")
- **Output**: Calculated results with error handling

### 2. Search Tool
- **Function**: Searches the web for current information
- **Input**: Search queries (e.g., "MacBook Pro price")
- **Output**: Relevant search results (simplified for demo)

## Prerequisites

- Python >= 3.12
- [Ollama](https://ollama.com/) installed and running
- Llama3 model downloaded

## Installation

1. **Install Ollama and Llama3 Model**:

   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull the Llama3 model
   ollama pull llama3:latest
   ```

2. **Install Project Dependencies**:

   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

## Usage

### Running the Agent

Execute the main agent:

```bash
python server.py
```

### Running Tests

Test individual tools:

```bash
python test_simple.py
```

### Example Queries

The agent can handle complex queries like:

```
"What is the current price of a MacBook Pro in USD? 
How much would it cost in EUR if the exchange rate is 0.85 EUR for 1 USD."
```

This query will:
1. Search for MacBook Pro prices
2. Calculate the EUR equivalent using the exchange rate
3. Provide a comprehensive answer

## Project Structure

```
langchain-react-agent/
├── server.py                    # Main agent implementation
├── test_simple.py              # Simple tool testing
├── pyproject.toml              # Project configuration
├── uv.lock                     # UV lock file
├── uv.toml                     # UV configuration
├── .python-version             # Python version specification
└── README.md                   # This file
```

## Technical Details

### ReAct Template

The agent uses a custom ReAct prompt template:

```
You are a helpful AI assistant with access to search and calculation tools.

Available tools:
{tools}

Use this exact format:
Question: the input question
Thought: think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input for the action
Observation: the result
... (repeat if needed)
Thought: I now know the answer
Final Answer: the final answer
```

### LLM Configuration

```python
llm = OllamaLLM(
    model="llama3:latest",
    temperature=0.0,
)
```

### Agent Configuration

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
)
```

## Example Output

When running the example query, the agent will:

1. **Thought**: "I need to find the current price of a MacBook Pro and then convert it to EUR"
2. **Action**: search
3. **Action Input**: "MacBook Pro price USD"
4. **Observation**: "Search results: MacBook Pro prices range from $1,299 to $2,499 USD..."
5. **Thought**: "Now I need to calculate the EUR equivalent using the exchange rate"
6. **Action**: calculator
7. **Action Input**: "2499 * 0.85"
8. **Observation**: "Result: 2124.15"
9. **Final Answer**: "The MacBook Pro costs between $1,299-$2,499 USD, which is approximately €1,104.15-€2,124.15 EUR at the current exchange rate."

## Troubleshooting

### Common Issues

1. **Ollama Model Not Found**:
   ```bash
   # Ensure Ollama is running
   ollama serve
   
   # Pull the required model
   ollama pull llama3:latest
   ```

2. **Tool Execution Errors**:
   - Check that all dependencies are installed
   - Verify network connectivity for search functionality
   - Review error messages in the verbose output

3. **Parsing Errors**:
   - The agent has built-in error handling for parsing issues
   - Check the agent's reasoning process in verbose mode

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

This project is based on the ReAct implementation described in "Hands-On Large Language Models", specifically Chapter 7, Section 7.4.2 "LangChain中的ReAct实现". The code has been updated to work with the latest versions of LangChain and related frameworks.

**Key References:**
- "Hands-On Large Language Models" (《图解大模型》) - Chapter 7.4.2
- [LangChain ReAct Documentation](https://python.langchain.com/docs/modules/agents/agent_types/react)
- [ReAct Paper](https://arxiv.org/abs/2210.03629) - "ReAct: Synergizing Reasoning and Acting in Language Models"

We extend our gratitude to the authors of "Hands-On Large Language Models" for providing the foundational concepts and implementation guidance that made this ReAct agent project possible.

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# LangChain ReAct 智能体

使用LangChain框架实现的ReAct（推理与行动）模式的实践项目。本项目展示了如何创建一个能够推理问题并使用可用工具采取行动的智能智能体。

## 功能特性

- **ReAct模式实现**：在迭代循环中结合推理和行动
- **工具集成**：数学计算器和网络搜索功能
- **Ollama LLM**：使用本地Llama3模型进行经济高效的处理
- **错误处理**：对解析和执行的强大错误处理
- **交互式智能体**：能够处理需要多个步骤的复杂查询

## 架构

系统使用以下组件实现ReAct模式：

```
┌─────────────────┐    ReAct循环     ┌─────────────────┐
│   推理          │ ◄──────────────► │   行动          │
│  (思考)         │                  │  (行动)         │
└─────────────────┘                  └─────────────────┘
         │                                     │
         ▼                                     ▼
   分析问题                              执行工具
   规划下一步                            获取结果
```

### ReAct模式流程

1. **思考**：智能体推理当前情况
2. **行动**：智能体决定使用哪个工具
3. **行动输入**：智能体为工具提供输入
4. **观察**：智能体接收工具输出
5. **重复**：继续直到问题解决

## 可用工具

### 1. 计算器工具
- **功能**：执行数学计算
- **输入**：数学表达式（例如："2 + 2", "100 * 0.85"）
- **输出**：计算结果和错误处理

### 2. 搜索工具
- **功能**：在网络上搜索当前信息
- **输入**：搜索查询（例如："MacBook Pro price"）
- **输出**：相关搜索结果（为演示简化）

## 环境要求

- Python >= 3.12
- [Ollama](https://ollama.com/) 已安装并运行
- 已下载Llama3模型

## 安装步骤

1. **安装Ollama和Llama3模型**：

   ```bash
   # 安装Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # 下载Llama3模型
   ollama pull llama3:latest
   ```

2. **安装项目依赖**：

   ```bash
   # 使用uv（推荐）
   uv sync
   
   # 或使用pip
   pip install -e .
   ```

## 使用方法

### 运行智能体

执行主智能体：

```bash
python server.py
```

### 运行测试

测试单个工具：

```bash
python test_simple.py
```

### 示例查询

智能体可以处理复杂的查询，如：

```
"MacBook Pro的当前价格是多少美元？
如果汇率是1美元兑换0.85欧元，那么用欧元计算需要多少钱？"
```

这个查询将：
1. 搜索MacBook Pro的价格
2. 使用汇率计算欧元等价物
3. 提供全面的答案

## 项目结构

```
langchain-react-agent/
├── server.py                    # 主智能体实现
├── test_simple.py              # 简单工具测试
├── pyproject.toml              # 项目配置
├── uv.lock                     # UV锁文件
├── uv.toml                     # UV配置
├── .python-version             # Python版本规范
└── README.md                   # 本文件
```

## 技术细节

### ReAct模板

智能体使用自定义的ReAct提示模板：

```
你是一个有用的AI助手，可以访问搜索和计算工具。

可用工具：
{tools}

使用这个确切格式：
问题：输入问题
思考：思考要做什么
行动：要采取的行动，应该是[{tool_names}]中的一个
行动输入：行动的输入
观察：结果
...（如果需要重复）
思考：我现在知道答案了
最终答案：最终答案
```

### LLM配置

```python
llm = OllamaLLM(
    model="llama3:latest",
    temperature=0.0,
)
```

### 智能体配置

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
)
```

## 示例输出

运行示例查询时，智能体将：

1. **思考**："我需要找到MacBook Pro的当前价格，然后将其转换为欧元"
2. **行动**：search
3. **行动输入**："MacBook Pro price USD"
4. **观察**："搜索结果：MacBook Pro价格范围从1,299美元到2,499美元..."
5. **思考**："现在我需要使用汇率计算欧元等价物"
6. **行动**：calculator
7. **行动输入**："2499 * 0.85"
8. **观察**："结果：2124.15"
9. **最终答案**："MacBook Pro的价格在1,299-2,499美元之间，按当前汇率计算约为1,104.15-2,124.15欧元。"

## 故障排除

### 常见问题

1. **找不到Ollama模型**：
   ```bash
   # 确保Ollama正在运行
   ollama serve
   
   # 下载所需模型
   ollama pull llama3:latest
   ```

2. **工具执行错误**：
   - 检查所有依赖是否已安装
   - 验证搜索功能的网络连接
   - 查看详细输出中的错误消息

3. **解析错误**：
   - 智能体具有内置的解析问题错误处理
   - 在详细模式下检查智能体的推理过程

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

本项目基于《图解大模型》（Hands-On Large Language Models）中描述的ReAct实现，特别是第7章第7.4.2节"LangChain中的ReAct实现"。代码已更新以与LangChain和相关框架的最新版本兼容。

**主要参考资料：**
- 《图解大模型》- 第7.4.2节
- [LangChain ReAct文档](https://python.langchain.com/docs/modules/agents/agent_types/react)
- [ReAct论文](https://arxiv.org/abs/2210.03629) - "ReAct: Synergizing Reasoning and Acting in Language Models"

我们向《图解大模型》的作者表示感谢，感谢他们提供了基础概念和实现指导，使这个ReAct智能体项目成为可能。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。