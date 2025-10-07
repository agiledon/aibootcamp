# CrewAI DDD Expert

A CrewAI-powered system that implements Domain-Driven Design (DDD) methodologies and processes to perform domain modeling from requirements, generating both domain layer product code and test code.

## Overview

This project leverages CrewAI to create an intelligent crew of AI agents that work collaboratively to transform business requirements into well-structured domain models following DDD principles. The system consists of three specialized agents working in sequence to deliver complete domain modeling solutions.

## Features

- **Domain Modeling**: Automatically analyzes business requirements and creates domain models using DDD principles
- **Code Generation**: Generates Java code implementing the domain model with proper DDD patterns
- **Unit Testing**: Creates comprehensive unit tests for the generated domain layer code
- **PlantUML Integration**: Generates UML class diagrams using PlantUML syntax
- **Multi-Agent Collaboration**: Uses specialized agents for different aspects of the development process

## Architecture

The system consists of three specialized AI agents:

### 1. Domain Expert Agent
- **Role**: DDD domain modeling expert
- **Responsibility**: Analyzes business requirements and creates domain models following DDD principles
- **Output**: Markdown domain model documentation with PlantUML diagrams
- **LLM**: `ollama/deepseek-r1:7b`

### 2. Developer Agent
- **Role**: Java development engineer specialized in DDD
- **Responsibility**: Converts domain model documentation into Java code implementation
- **Output**: Java classes following DDD patterns (AggregateRoot, Entity, ValueObject)
- **LLM**: `ollama/qwen2.5-coder:7b`

### 3. Tester Agent
- **Role**: Unit testing specialist
- **Responsibility**: Creates comprehensive unit tests for the generated domain code
- **Output**: JUnit5 test classes with Mockito and AssertJ
- **LLM**: `ollama/qwen2.5-coder:7b`

## Installation

### Prerequisites

- Python >= 3.12
- UV package manager (recommended)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd agent/crewai_ddd_expert
```

2. Install dependencies:
```bash
uv sync
```

3. Ensure Ollama is running with the required models:
```bash
# Install required models
ollama pull deepseek-r1:7b
ollama pull qwen2.5-coder:7b
```

## Usage

### Running the Crew

Execute the main crew workflow:

```bash
uv run run_crew
```

Or run directly:

```bash
uv run src/crewai_ddd_expert/main.py
```

### Configuration

The system uses YAML configuration files for agents and tasks:

- `src/crewai_ddd_expert/config/agents.yaml`: Agent configurations
- `src/crewai_ddd_expert/config/tasks.yaml`: Task definitions

### Example Output

The system generates the following outputs in the `output/` directory:

1. **`domain_model.md`**: Domain model documentation with PlantUML diagrams
2. **`domain_model.java`**: Java implementation of the domain model
3. **`domain_model_test.java`**: Unit tests for the domain classes

## Example Domain Model

The system can handle complex business domains. For example, it can model an online meeting lifecycle management system with:

- **Meeting Lifecycle**: Pre-meeting, during-meeting, and post-meeting phases
- **Calendar Integration**: Google Calendar and Outlook integration
- **Workspace Management**: User workspaces with member management and permissions
- **Real-time Translation**: Meeting assistant bots for multilingual support
- **Resource Management**: Meeting recordings, transcripts, and documents

## DDD Patterns Implemented

The generated code follows key DDD patterns:

- **AggregateRoot**: Root entities that maintain consistency boundaries
- **Entity**: Objects with distinct identity
- **ValueObject**: Immutable objects defined by their attributes
- **Repository Pattern**: Data access abstraction
- **Domain Services**: Business logic that doesn't belong to entities

## Code Quality Standards

The generated code follows these standards:

- **Naming Conventions**: CamelCase for classes, snake_case for test methods
- **Package Structure**: Organized by domain concepts
- **Documentation**: Markdown-formatted class comments
- **Testing**: Given-When-Then pattern for test methods
- **Mocking**: Mockito for external dependencies
- **Assertions**: AssertJ for fluent assertions

## Workflow Process

1. **Requirement Analysis**: The domain expert analyzes business requirements
2. **Domain Modeling**: Creates domain model with PlantUML diagrams
3. **Code Generation**: Developer converts model to Java implementation
4. **Test Creation**: Tester generates comprehensive unit tests
5. **Output Generation**: All artifacts saved to output directory

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

## Support

For issues and questions, please open an issue in the repository or contact the development team.

## Future Enhancements

- Support for additional programming languages
- Integration with more LLM providers
- Enhanced PlantUML diagram generation
- Real-time collaboration features
- API endpoints for remote execution

---

# CrewAI DDD专家

一个基于CrewAI的系统，实现了领域驱动设计（DDD）方法论和流程，从需求执行领域建模，生成领域层产品代码和测试代码。

## 概述

本项目利用CrewAI创建一个智能AI智能体团队，协作将业务需求转换为遵循DDD原则的结构化领域模型。系统由三个专门的智能体按顺序工作，提供完整的领域建模解决方案。

## 功能特性

- **领域建模**：自动分析业务需求并使用DDD原则创建领域模型
- **代码生成**：生成实现领域模型的Java代码，采用正确的DDD模式
- **单元测试**：为生成的领域层代码创建全面的单元测试
- **PlantUML集成**：使用PlantUML语法生成UML类图
- **多智能体协作**：使用专门的智能体处理开发过程的不同方面

## 架构

系统由三个专门的AI智能体组成：

### 1. 领域专家智能体
- **角色**：DDD领域建模专家
- **职责**：分析业务需求并创建遵循DDD原则的领域模型
- **输出**：包含PlantUML图表的Markdown领域模型文档
- **LLM**：`ollama/deepseek-r1:7b`

### 2. 开发者智能体
- **角色**：专门从事DDD的Java开发工程师
- **职责**：将领域模型文档转换为Java代码实现
- **输出**：遵循DDD模式的Java类（AggregateRoot、Entity、ValueObject）
- **LLM**：`ollama/qwen2.5-coder:7b`

### 3. 测试者智能体
- **角色**：单元测试专家
- **职责**：为生成的领域代码创建全面的单元测试
- **输出**：使用Mockito和AssertJ的JUnit5测试类
- **LLM**：`ollama/qwen2.5-coder:7b`

## 安装

### 环境要求

- Python >= 3.12
- UV包管理器（推荐）

### 设置

1. 克隆仓库：
```bash
git clone <repository-url>
cd agent/crewai_ddd_expert
```

2. 安装依赖：
```bash
uv sync
```

3. 确保Ollama运行并具有所需模型：
```bash
# 安装所需模型
ollama pull deepseek-r1:7b
ollama pull qwen2.5-coder:7b
```

## 使用方法

### 运行智能体团队

执行主要的智能体团队工作流：

```bash
uv run run_crew
```

或直接运行：

```bash
uv run src/crewai_ddd_expert/main.py
```

### 配置

系统使用YAML配置文件进行智能体和任务配置：

- `src/crewai_ddd_expert/config/agents.yaml`：智能体配置
- `src/crewai_ddd_expert/config/tasks.yaml`：任务定义

### 示例输出

系统在 `output/` 目录中生成以下输出：

1. **`domain_model.md`**：包含PlantUML图表的领域模型文档
2. **`domain_model.java`**：领域模型的Java实现
3. **`domain_model_test.java`**：领域类的单元测试

## 示例领域模型

系统可以处理复杂的业务领域。例如，它可以建模一个在线会议生命周期管理系统，包括：

- **会议生命周期**：会前、会中、会后阶段
- **日历集成**：Google日历和Outlook集成
- **工作空间管理**：具有成员管理和权限的用户工作空间
- **实时翻译**：用于多语言支持的会议助手机器人
- **资源管理**：会议录音、转录和文档

## 实现的DDD模式

生成的代码遵循关键的DDD模式：

- **AggregateRoot**：维护一致性边界的根实体
- **Entity**：具有独特身份的对象
- **ValueObject**：由其属性定义的不可变对象
- **Repository模式**：数据访问抽象
- **领域服务**：不属于实体的业务逻辑

## 代码质量标准

生成的代码遵循以下标准：

- **命名约定**：类使用CamelCase，测试方法使用snake_case
- **包结构**：按领域概念组织
- **文档**：Markdown格式的类注释
- **测试**：测试方法的Given-When-Then模式
- **Mocking**：使用Mockito进行外部依赖
- **断言**：使用AssertJ进行流畅断言

## 工作流程

1. **需求分析**：领域专家分析业务需求
2. **领域建模**：使用PlantUML图表创建领域模型
3. **代码生成**：开发者将模型转换为Java实现
4. **测试创建**：测试者生成全面的单元测试
5. **输出生成**：所有工件保存到output目录

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

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。

## 未来增强

- 支持更多编程语言
- 集成更多LLM提供商
- 增强PlantUML图表生成
- 实时协作功能
- 远程执行的API端点