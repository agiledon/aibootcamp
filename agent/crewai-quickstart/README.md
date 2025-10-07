# CrewAI Quickstart

A simple and practical example of CrewAI multi-agent collaboration for AI research and reporting. This project demonstrates how to create intelligent agents that work together to research topics and generate comprehensive reports.

## Features

- **Multi-Agent Collaboration**: Two specialized agents working in sequence
- **Web Research**: Automated web search using SerperDevTool
- **Local LLM**: Uses Ollama with Qwen 3 8B model for cost-effective processing
- **Report Generation**: Automated markdown report creation
- **YAML Configuration**: Easy-to-modify agent and task configurations
- **CrewAI Framework**: Built on the latest CrewAI framework with decorators

## Architecture

The system consists of two specialized AI agents working in sequence:

```
┌─────────────────┐    Sequential     ┌─────────────────┐
│  Researcher     │ ───────────────► │ Reporting       │
│  Agent          │                  │ Analyst Agent   │
└─────────────────┘                  └─────────────────┘
         │                                     │
         ▼                                     ▼
   Web Search                           Report Generation
  (SerperDevTool)                      (Markdown Output)
```

### 1. Researcher Agent
- **Role**: Senior Data Researcher specializing in the given topic
- **Goal**: Uncover cutting-edge developments in the research topic
- **Tools**: SerperDevTool for web search capabilities
- **Output**: 10 bullet points of relevant information

### 2. Reporting Analyst Agent
- **Role**: Reporting Analyst
- **Goal**: Create detailed reports based on research findings
- **Input**: Research results from the Researcher Agent
- **Output**: Comprehensive markdown report

## Prerequisites

- Python >= 3.12
- [Ollama](https://ollama.com/) installed and running
- Qwen 3 8B model downloaded
- SerperDev API key (for web search)

## Installation

1. **Install Ollama and Qwen Model**:

   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull the Qwen 3 8B model
   ollama pull qwen3:8b
   ```

2. **Install Project Dependencies**:

   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

3. **Set up SerperDev API Key**:

   Create a `.env` file in the project root:
   ```bash
   SERPER_API_KEY=your_serper_api_key_here
   ```

   Get your API key from [SerperDev](https://serper.dev/)

## Usage

### Running the Crew

Execute the main crew workflow:

```bash
uv run run_crew
```

Or run directly:

```bash
uv run src/crewai_quickstart/main.py
```

Or using CrewAI CLI (if you have CrewAI installed as a tool):

```bash
# First install CrewAI as a tool (if not already installed)
uv tool install crewai

# Then run the crew
crewai run
```

### Customizing the Research Topic

Edit the `main.py` file to change the research topic:

```python
def run():
    inputs = {
        'topic': 'Your Research Topic Here'  # Change this
    }
    LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)
```

### Configuration

The system uses YAML configuration files for agents and tasks:

- `src/crewai_quickstart/config/agents.yaml`: Agent configurations
- `src/crewai_quickstart/config/tasks.yaml`: Task definitions

You can modify these files to customize agent roles, goals, backstories, and task descriptions.

## Expected Output

The system will:

1. **Research Phase**: The Researcher Agent searches the web for current information about the topic
2. **Analysis Phase**: The Reporting Analyst Agent creates a comprehensive report
3. **Output**: A detailed markdown report saved to `output/report.md`

Example topics that work well:
- AI Agents
- Machine Learning
- Climate Change
- Renewable Energy
- Space Exploration

## Project Structure

```
crewai-quickstart/
├── src/crewai_quickstart/          # Main source code
│   ├── main.py                    # Entry point
│   ├── crew.py                    # Crew definition with agents and tasks
│   ├── config/                    # Configuration files
│   │   ├── agents.yaml           # Agent configurations
│   │   └── tasks.yaml            # Task definitions
│   └── tools/                     # Custom tools (empty in this example)
├── output/                        # Generated reports
│   └── report.md                 # Final report output
├── pyproject.toml                # Project configuration
├── uv.lock                       # UV lock file
└── README.md                     # This file
```

## Technical Details

### CrewAI Framework Features

- **Decorator-based Configuration**: Uses `@CrewBase`, `@agent`, `@task`, and `@crew` decorators
- **Lifecycle Hooks**: `@before_kickoff` and `@after_kickoff` for custom processing
- **YAML Configuration**: External configuration for easy customization
- **Sequential Process**: Agents work in sequence for structured workflows

### LLM Configuration

```python
llm = LLM(
    model="ollama/qwen3:8b",
    base_url="http://localhost:11434",
    temperature=0.1,
    max_tokens=4096
)
```

### Tools Integration

- **SerperDevTool**: Provides web search capabilities
- **Extensible**: Easy to add custom tools in the `tools/` directory

## Troubleshooting

### Common Issues

1. **Ollama Model Not Found**:
   ```bash
   # Ensure Ollama is running
   ollama serve
   
   # Pull the required model
   ollama pull qwen3:8b
   ```

2. **SerperDev API Issues**:
   - Verify your API key is correct in `.env`
   - Check your SerperDev account quota
   - Ensure network connectivity

3. **Output File Not Created**:
   - Check that the `output/` directory exists
   - Verify write permissions in the project directory

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

This project is based on the CrewAI official documentation and examples. The core concepts, agent configurations, and workflow patterns follow the official CrewAI framework guidelines and best practices.

**Key References:**
- [CrewAI Official Documentation](https://docs.crewai.com/)
- [CrewAI GitHub Repository](https://github.com/joaomdmoura/crewAI)
- [CrewAI Framework Examples](https://github.com/joaomdmoura/crewAI/tree/main/examples)

We extend our gratitude to the CrewAI team for providing the excellent framework and comprehensive documentation that made this quickstart project possible.

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# CrewAI 快速入门

一个简单实用的CrewAI多智能体协作示例，用于AI研究和报告生成。本项目展示了如何创建智能体协同工作来研究主题并生成综合报告。

## 功能特性

- **多智能体协作**：两个专门的智能体按顺序工作
- **网络研究**：使用SerperDevTool进行自动化网络搜索
- **本地LLM**：使用Ollama和Qwen 3 8B模型进行经济高效的处理
- **报告生成**：自动化markdown报告创建
- **YAML配置**：易于修改的智能体和任务配置
- **CrewAI框架**：基于最新CrewAI框架和装饰器构建

## 架构

系统由两个专门的AI智能体按顺序工作：

```
┌─────────────────┐    顺序执行    ┌─────────────────┐
│  研究智能体      │ ──────────────► │  报告分析师     │
│                 │                │  智能体         │
└─────────────────┘                └─────────────────┘
         │                                    │
         ▼                                    ▼
   网络搜索                             报告生成
  (SerperDevTool)                     (Markdown输出)
```

### 1. 研究智能体
- **角色**：专门研究给定主题的高级数据研究员
- **目标**：发现研究主题的前沿发展
- **工具**：SerperDevTool用于网络搜索功能
- **输出**：10个相关信息的要点

### 2. 报告分析师智能体
- **角色**：报告分析师
- **目标**：基于研究发现创建详细报告
- **输入**：来自研究智能体的研究结果
- **输出**：综合markdown报告

## 环境要求

- Python >= 3.12
- [Ollama](https://ollama.com/) 已安装并运行
- 已下载Qwen 3 8B模型
- SerperDev API密钥（用于网络搜索）

## 安装步骤

1. **安装Ollama和Qwen模型**：

   ```bash
   # 安装Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # 下载Qwen 3 8B模型
   ollama pull qwen3:8b
   ```

2. **安装项目依赖**：

   ```bash
   # 使用uv（推荐）
   uv sync
   
   # 或使用pip
   pip install -e .
   ```

3. **设置SerperDev API密钥**：

   在项目根目录创建`.env`文件：
   ```bash
   SERPER_API_KEY=your_serper_api_key_here
   ```

   从 [SerperDev](https://serper.dev/) 获取您的API密钥

## 使用方法

### 运行智能体团队

执行主要的智能体团队工作流：

```bash
uv run run_crew
```

或直接运行：

```bash
uv run src/crewai_quickstart/main.py
```

或使用CrewAI CLI（如果您已将CrewAI安装为工具）：

```bash
# 首先安装CrewAI作为工具（如果尚未安装）
uv tool install crewai

# 然后运行智能体团队
crewai run
```

### 自定义研究主题

编辑`main.py`文件来更改研究主题：

```python
def run():
    inputs = {
        'topic': '您的研究主题'  # 更改这里
    }
    LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)
```

### 配置

系统使用YAML配置文件进行智能体和任务配置：

- `src/crewai_quickstart/config/agents.yaml`：智能体配置
- `src/crewai_quickstart/config/tasks.yaml`：任务定义

您可以修改这些文件来自定义智能体角色、目标、背景故事和任务描述。

## 预期输出

系统将执行以下步骤：

1. **研究阶段**：研究智能体在网络上搜索有关主题的当前信息
2. **分析阶段**：报告分析师智能体创建综合报告
3. **输出**：详细的markdown报告保存到`output/report.md`

适合的研究主题示例：
- AI智能体
- 机器学习
- 气候变化
- 可再生能源
- 太空探索

## 项目结构

```
crewai-quickstart/
├── src/crewai_quickstart/          # 主要源代码
│   ├── main.py                    # 入口点
│   ├── crew.py                    # 智能体团队定义和任务
│   ├── config/                    # 配置文件
│   │   ├── agents.yaml           # 智能体配置
│   │   └── tasks.yaml            # 任务定义
│   └── tools/                     # 自定义工具（此示例中为空）
├── output/                        # 生成的报告
│   └── report.md                 # 最终报告输出
├── pyproject.toml                # 项目配置
├── uv.lock                       # UV锁文件
└── README.md                     # 本文件
```

## 技术细节

### CrewAI框架特性

- **基于装饰器的配置**：使用`@CrewBase`、`@agent`、`@task`和`@crew`装饰器
- **生命周期钩子**：`@before_kickoff`和`@after_kickoff`用于自定义处理
- **YAML配置**：外部配置便于自定义
- **顺序流程**：智能体按顺序工作以实现结构化工作流

### LLM配置

```python
llm = LLM(
    model="ollama/qwen3:8b",
    base_url="http://localhost:11434",
    temperature=0.1,
    max_tokens=4096
)
```

### 工具集成

- **SerperDevTool**：提供网络搜索功能
- **可扩展**：易于在`tools/`目录中添加自定义工具

## 故障排除

### 常见问题

1. **找不到Ollama模型**：
   ```bash
   # 确保Ollama正在运行
   ollama serve
   
   # 下载所需模型
   ollama pull qwen3:8b
   ```

2. **SerperDev API问题**：
   - 验证您的API密钥在`.env`中是否正确
   - 检查您的SerperDev账户配额
   - 确保网络连接

3. **输出文件未创建**：
   - 检查`output/`目录是否存在
   - 验证项目目录的写入权限

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

本项目基于CrewAI官方文档和示例。核心概念、智能体配置和工作流模式遵循官方CrewAI框架指南和最佳实践。

**主要参考资料：**
- [CrewAI官方文档](https://docs.crewai.com/)
- [CrewAI GitHub仓库](https://github.com/joaomdmoura/crewAI)
- [CrewAI框架示例](https://github.com/joaomdmoura/crewAI/tree/main/examples)

我们向CrewAI团队表示感谢，感谢他们提供了优秀的框架和全面的文档，使这个快速入门项目成为可能。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。
