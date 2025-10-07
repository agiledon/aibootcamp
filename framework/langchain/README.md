# LangChain Framework Examples

A collection of practical LangChain framework examples demonstrating chain architectures and prompt templates using the latest API.

## Modules

### 1. chain_demo - Multi-Step Chain Architecture

Demonstrates LangChain's chaining capabilities with sequential story generation pipelines.

**Features:**
- Multi-step sequential chaining
- Modern `RunnablePassthrough.assign()` API
- Template-based prompt management
- Two implementation styles (standard and simplified)

**Files:**
- `chain-demo-standard.py` - Detailed implementation with extensive comments
- `chain-demo-simplified.py` - Modern, concise implementation

**Example:**
```python
# Creates a three-step chain: summary → title → character → story
story_pipeline = (
    RunnablePassthrough.assign(title=create_chain(templates["title"]))
    .assign(character=create_chain(templates["character"]))
    .assign(story=create_chain(templates["story"]))
)
```

### 2. prompt_template - Prompt Template Examples

Demonstrates various types of prompt templates in LangChain.

**Features:**
- ChatPromptTemplate - Multi-message conversation templates
- FewShotPromptTemplate - Few-shot learning examples
- Custom StringPromptTemplate - User-defined template classes

**Files:**
- `chat_prompt_template.py` - System and human message templates
- `frew_shot_prompt_template.py` - Few-shot learning examples
- `person_info_prompt_template.py` - Custom template with validation

**Example:**
```python
# ChatPromptTemplate with system and human messages
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a {role}"),
    HumanMessagePromptTemplate.from_template("{input}")
])
```

## Prerequisites

- Python >= 3.12
- [Ollama](https://ollama.com/) installed and running (for chain_demo)
- Qwen 7B model downloaded (for chain_demo)

## Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## Usage

### Running Chain Demo

```bash
# Standard version
python chain_demo/chain-demo-standard.py

# Simplified version
python chain_demo/chain-demo-simplified.py
```

### Running Prompt Template Examples

```bash
# Chat prompt template
python prompt_template/chat_prompt_template.py

# Few-shot prompt template
python prompt_template/frew_shot_prompt_template.py

# Custom prompt template
python prompt_template/person_info_prompt_template.py
```

## Project Structure

```
langchain/
├── chain_demo/                    # Chain architecture demonstrations
│   ├── __init__.py               # Module initialization
│   ├── chain-demo-standard.py   # Standard implementation
│   ├── chain-demo-simplified.py # Simplified implementation
│   └── README.md                # Detailed documentation
├── prompt_template/              # Prompt template examples
│   ├── __init__.py              # Module initialization
│   ├── chat_prompt_template.py  # Chat prompt examples
│   ├── frew_shot_prompt_template.py  # Few-shot examples
│   └── person_info_prompt_template.py  # Custom template
├── pyproject.toml               # Project configuration
├── uv.lock                      # UV lock file
└── README.md                    # This file
```

## Key Concepts

### Chain Architecture
- Sequential processing pipelines
- RunnablePassthrough for data flow
- Template-based prompt composition

### Prompt Templates
- Message-based templates for chat models
- Few-shot learning templates
- Custom template classes with validation

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

This project is based on examples from "Hands-On Large Language Models", specifically:
- Chapter 7: Multi-Prompt Chain Architecture (chain_demo)
- Various prompt template patterns (prompt_template)

The code has been updated to work with the latest version of LangChain and incorporates modern API patterns.

**Key References:**
- "Hands-On Large Language Models" - Chapters on LangChain
- [LangChain Documentation](https://python.langchain.com/)
- [LangChain Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/)

We extend our gratitude to the authors of "Hands-On Large Language Models" for providing the foundational concepts and implementation patterns.

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# LangChain 框架示例

使用最新API演示链式架构和提示模板的实用LangChain框架示例集合。

## 模块

### 1. chain_demo - 多步骤链式架构

演示LangChain的链式功能和顺序故事生成管道。

**功能特性：**
- 多步骤顺序链式
- 现代`RunnablePassthrough.assign()` API
- 基于模板的提示管理
- 两种实现风格（标准和简化）

**文件：**
- `chain-demo-standard.py` - 带有详细注释的实现
- `chain-demo-simplified.py` - 现代、简洁的实现

**示例：**
```python
# 创建三步链式：摘要 → 标题 → 角色 → 故事
story_pipeline = (
    RunnablePassthrough.assign(title=create_chain(templates["title"]))
    .assign(character=create_chain(templates["character"]))
    .assign(story=create_chain(templates["story"]))
)
```

### 2. prompt_template - 提示模板示例

演示LangChain中的各种提示模板类型。

**功能特性：**
- ChatPromptTemplate - 多消息对话模板
- FewShotPromptTemplate - Few-shot学习示例
- 自定义StringPromptTemplate - 用户定义的模板类

**文件：**
- `chat_prompt_template.py` - 系统和人类消息模板
- `frew_shot_prompt_template.py` - Few-shot学习示例
- `person_info_prompt_template.py` - 带验证的自定义模板

**示例：**
```python
# 带有系统和人类消息的ChatPromptTemplate
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("你是一个{role}"),
    HumanMessagePromptTemplate.from_template("{input}")
])
```

## 环境要求

- Python >= 3.12
- [Ollama](https://ollama.com/) 已安装并运行（用于chain_demo）
- 已下载Qwen 7B模型（用于chain_demo）

## 安装步骤

```bash
# 使用uv（推荐）
uv sync

# 或使用pip
pip install -e .
```

## 使用方法

### 运行链式演示

```bash
# 标准版本
python chain_demo/chain-demo-standard.py

# 简化版本
python chain_demo/chain-demo-simplified.py
```

### 运行提示模板示例

```bash
# 聊天提示模板
python prompt_template/chat_prompt_template.py

# Few-shot提示模板
python prompt_template/frew_shot_prompt_template.py

# 自定义提示模板
python prompt_template/person_info_prompt_template.py
```

## 项目结构

```
langchain/
├── chain_demo/                    # 链式架构演示
│   ├── __init__.py               # 模块初始化
│   ├── chain-demo-standard.py   # 标准实现
│   ├── chain-demo-simplified.py # 简化实现
│   └── README.md                # 详细文档
├── prompt_template/              # 提示模板示例
│   ├── __init__.py              # 模块初始化
│   ├── chat_prompt_template.py  # 聊天提示示例
│   ├── frew_shot_prompt_template.py  # Few-shot示例
│   └── person_info_prompt_template.py  # 自定义模板
├── pyproject.toml               # 项目配置
├── uv.lock                      # UV锁文件
└── README.md                    # 本文件
```

## 关键概念

### 链式架构
- 顺序处理管道
- RunnablePassthrough用于数据流
- 基于模板的提示组合

### 提示模板
- 用于聊天模型的基于消息的模板
- Few-shot学习模板
- 带验证的自定义模板类

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

本项目基于《图解大模型》（Hands-On Large Language Models）的示例，特别是：
- 第7章：多提示链式架构（chain_demo）
- 各种提示模板模式（prompt_template）

代码已更新以与LangChain的最新版本兼容，并融入了现代API模式。

**主要参考资料：**
- 《图解大模型》- 关于LangChain的章节
- [LangChain文档](https://python.langchain.com/)
- [LangChain提示模板](https://python.langchain.com/docs/modules/model_io/prompts/)

我们向《图解大模型》的作者表示感谢，感谢他们提供了基础概念和实现模式。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。