# LangChain Chain Demo

A practical demonstration of LangChain's chaining capabilities using the latest API. This project showcases how to create multi-step chains for story generation, implementing a sequential pipeline that generates titles, character descriptions, and complete stories from simple summaries.

## Features

- **Multi-Step Chaining**: Sequential story generation pipeline
- **Modern LangChain API**: Uses the latest `RunnablePassthrough.assign()` syntax
- **Ollama Integration**: Local Qwen 7B model for cost-effective processing
- **Two Implementation Styles**: Standard and simplified versions
- **Template-Based Prompts**: Reusable prompt templates for different tasks

## Architecture

The system implements a three-step chaining process:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Summary   │───►│    Title    │───►│ Character   │
│   Input     │    │ Generation  │    │ Description │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
                                              ▼
                                    ┌─────────────┐
                                    │   Story     │
                                    │ Generation  │
                                    └─────────────┘
```

### Chain Flow

1. **Title Generation**: Creates a title based on the story summary
2. **Character Description**: Generates character description using summary and title
3. **Story Generation**: Creates the complete story using all previous outputs

## Prerequisites

- Python >= 3.12
- [Ollama](https://ollama.com/) installed and running
- Qwen 7B model downloaded

## Installation

1. **Install Ollama and Qwen Model**:

   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull the Qwen 7B model
   ollama pull qwen:7b
   ```

2. **Install Project Dependencies**:

   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install langchain langchain-core langchain-ollama
   ```

## Usage

### Running the Standard Version

Execute the standard implementation:

```bash
python chain-demo-standard.py
```

### Running the Simplified Version

Execute the simplified implementation:

```bash
python chain-demo-simplified.py
```

### Example Input

Both scripts use the same input:

```python
summary = "一个小女孩失去了她的妈妈，她很伤心。"
```

### Expected Output

The system will generate:
- A creative title for the story
- A detailed character description
- A complete story incorporating all elements

## Project Structure

```
chain-demo/
├── chain-demo-standard.py     # Standard implementation with detailed comments
├── chain-demo-simplified.py   # Simplified implementation with modern syntax
└── README.md                  # This file
```

## Technical Details

### Modern LangChain API

The project uses the latest LangChain API features:

```python
# Modern chain creation
story_pipeline = (
    RunnablePassthrough.assign(title=create_chain(templates["title"]))
    .assign(character=create_chain(templates["character"]))
    .assign(story=create_chain(templates["story"]))
)
```

### Template-Based Architecture

```python
def create_chain(template: str):
    """Create standardized chains"""
    return PromptTemplate.from_template(template) | llm | parser
```

### LLM Configuration

```python
llm = OllamaLLM(model="qwen:7b")
```

## Implementation Differences

### Standard Version (`chain-demo-standard.py`)
- **Detailed Comments**: Extensive documentation for learning
- **Step-by-Step**: Clear separation of each chain component
- **Traditional Approach**: Uses individual PromptTemplate definitions

### Simplified Version (`chain-demo-simplified.py`)
- **Modern Syntax**: Uses latest LangChain API features
- **Concise Code**: More compact and readable implementation
- **Template Dictionary**: Centralized template management

## Example Output

```
📖 故事生成结果:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️  标题: 失去妈妈的悲伤

👤 角色: 一个8岁的小女孩，名叫小雨，有着长长的黑发和大大的眼睛...

📚 故事: 小雨失去了她最爱的妈妈，每天都感到无比的孤独和悲伤...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Key Concepts Demonstrated

1. **RunnablePassthrough**: Passes input through while adding new fields
2. **Chain Composition**: Combining multiple chains into a pipeline
3. **Template Management**: Organizing and reusing prompt templates
4. **Output Parsing**: Using StrOutputParser for clean text output
5. **Modern LangChain API**: Latest syntax and best practices

## Troubleshooting

### Common Issues

1. **Ollama Model Not Found**:
   ```bash
   # Ensure Ollama is running
   ollama serve
   
   # Pull the required model
   ollama pull qwen:7b
   ```

2. **Import Errors**:
   - Ensure all LangChain packages are installed
   - Check Python version compatibility (>= 3.12)

3. **Chain Execution Issues**:
   - Verify all required input variables are provided
   - Check prompt template syntax

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

This project is based on the multi-prompt chain architecture case study from "Hands-On Large Language Models", specifically Chapter 7. The code has been updated to work with the latest version of LangChain and incorporates modern API patterns.

**Key References:**
- "Hands-On Large Language Models"  - Chapter 7: Multi-Prompt Chain Architecture
- [LangChain Documentation](https://python.langchain.com/docs/modules/chains/)
- [LangChain Runnable Interface](https://python.langchain.com/docs/modules/chains/)

We extend our gratitude to the authors of "Hands-On Large Language Models" for providing the foundational concepts and implementation patterns that inspired this chain demonstration project.

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# LangChain 链式演示

使用最新API的LangChain链式功能实践演示。本项目展示了如何创建多步骤链式架构进行故事生成，实现从简单摘要生成标题、角色描述和完整故事的顺序管道。

## 功能特性

- **多步骤链式**：顺序故事生成管道
- **现代LangChain API**：使用最新的`RunnablePassthrough.assign()`语法
- **Ollama集成**：本地Qwen 7B模型进行经济高效的处理
- **两种实现风格**：标准版本和简化版本
- **基于模板的提示**：用于不同任务的可重用提示模板

## 架构

系统实现三步链式流程：

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   摘要      │───►│   标题      │───►│   角色      │
│   输入      │    │   生成      │    │   描述      │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
                                              ▼
                                    ┌─────────────┐
                                    │   故事      │
                                    │   生成      │
                                    └─────────────┘
```

### 链式流程

1. **标题生成**：基于故事摘要创建标题
2. **角色描述**：使用摘要和标题生成角色描述
3. **故事生成**：使用所有先前输出创建完整故事

## 环境要求

- Python >= 3.12
- [Ollama](https://ollama.com/) 已安装并运行
- 已下载Qwen 7B模型

## 安装步骤

1. **安装Ollama和Qwen模型**：

   ```bash
   # 安装Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # 下载Qwen 7B模型
   ollama pull qwen:7b
   ```

2. **安装项目依赖**：

   ```bash
   # 使用uv（推荐）
   uv sync
   
   # 或使用pip
   pip install langchain langchain-core langchain-ollama
   ```

## 使用方法

### 运行标准版本

执行标准实现：

```bash
python chain-demo-standard.py
```

### 运行简化版本

执行简化实现：

```bash
python chain-demo-simplified.py
```

### 示例输入

两个脚本使用相同的输入：

```python
summary = "一个小女孩失去了她的妈妈，她很伤心。"
```

### 预期输出

系统将生成：
- 故事的创意标题
- 详细角色描述
- 包含所有元素的完整故事

## 项目结构

```
chain-demo/
├── chain-demo-standard.py     # 带有详细注释的标准实现
├── chain-demo-simplified.py   # 使用现代语法的简化实现
└── README.md                  # 本文件
```

## 技术细节

### 现代LangChain API

项目使用最新的LangChain API特性：

```python
# 现代链式创建
story_pipeline = (
    RunnablePassthrough.assign(title=create_chain(templates["title"]))
    .assign(character=create_chain(templates["character"]))
    .assign(story=create_chain(templates["story"]))
)
```

### 基于模板的架构

```python
def create_chain(template: str):
    """创建标准化链"""
    return PromptTemplate.from_template(template) | llm | parser
```

### LLM配置

```python
llm = OllamaLLM(model="qwen:7b")
```

## 实现差异

### 标准版本（`chain-demo-standard.py`）
- **详细注释**：用于学习的广泛文档
- **逐步说明**：每个链式组件的清晰分离
- **传统方法**：使用单独的PromptTemplate定义

### 简化版本（`chain-demo-simplified.py`）
- **现代语法**：使用最新的LangChain API特性
- **简洁代码**：更紧凑和可读的实现
- **模板字典**：集中式模板管理

## 示例输出

```
📖 故事生成结果:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️  标题: 失去妈妈的悲伤

👤 角色: 一个8岁的小女孩，名叫小雨，有着长长的黑发和大大的眼睛...

📚 故事: 小雨失去了她最爱的妈妈，每天都感到无比的孤独和悲伤...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 演示的关键概念

1. **RunnablePassthrough**：在传递输入的同时添加新字段
2. **链式组合**：将多个链组合成管道
3. **模板管理**：组织和重用提示模板
4. **输出解析**：使用StrOutputParser进行清洁文本输出
5. **现代LangChain API**：最新语法和最佳实践

## 故障排除

### 常见问题

1. **找不到Ollama模型**：
   ```bash
   # 确保Ollama正在运行
   ollama serve
   
   # 下载所需模型
   ollama pull qwen:7b
   ```

2. **导入错误**：
   - 确保所有LangChain包已安装
   - 检查Python版本兼容性（>= 3.12）

3. **链式执行问题**：
   - 验证所有必需的输入变量已提供
   - 检查提示模板语法

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

本项目基于《图解大模型》（Hands-On Large Language Models）第7章的多提示链式架构案例研究。代码已更新以与LangChain的最新版本兼容，并融入了现代API模式。

**主要参考资料：**
- 《图解大模型》- 第7章：多提示链式架构
- [LangChain文档](https://python.langchain.com/docs/modules/chains/)
- [LangChain Runnable接口](https://python.langchain.com/docs/modules/chains/)

我们向《图解大模型》的作者表示感谢，感谢他们提供了基础概念和实现模式，启发了这个链式演示项目。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。
