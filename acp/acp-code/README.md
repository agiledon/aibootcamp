# Multi-Agent Research Workflow with ACP

A demonstration of the Agent Communication Protocol (ACP) showcasing how two agents built with different frameworks (CrewAI and Smolagents) can collaborate seamlessly to generate and verify research summaries.

## Features

- **Research Drafter Agent**: Uses CrewAI to create initial research summaries
- **Research Verifier Agent**: Uses Smolagents with web search to fact-check and enhance summaries
- **ACP Protocol**: Enables seamless communication between different agent frameworks
- **Ollama Integration**: Uses local Qwen 7B model for cost-effective processing

## Architecture

```
┌─────────────────┐    ACP     ┌─────────────────┐
│  CrewAI Server  │ ◄─────────► │ Smolagents      │
│  (Port 8000)    │            │ Server (8001)   │
└─────────────────┘            └─────────────────┘
         ▲                              ▲
         │                              │
         └──────────────┬───────────────┘
                        │
                ┌───────▼────────┐
                │  ACP Client    │
                │  (Workflow)    │
                └────────────────┘
```

## Prerequisites

- Python 3.12+
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
   pip install -e .
   ```

## Usage

1. **Start the CrewAI ACP Server** (Terminal 1):
   ```bash
   uv run crew_acp_server.py
   ```

2. **Start the Smolagents ACP Server** (Terminal 2):
   ```bash
   uv run smolagents_acp_server.py
   ```

3. **Run the Client Workflow** (Terminal 3):
   ```bash
   uv run acp_client.py
   ```

## Expected Output

The workflow will:
1. Generate an initial research summary using CrewAI
2. Fact-check and enhance the summary using Smolagents with web search
3. Display both the draft and final verified summary

## Project Structure

```
acp-code/
├── crew_acp_server.py      # CrewAI ACP server (port 8000)
├── smolagents_acp_server.py # Smolagents ACP server (port 8001)
├── acp_client.py           # Client workflow orchestrator
├── pyproject.toml          # Project dependencies
└── README.md              # This file
```

## Configuration

The project uses the following default configuration:
- **Model**: Qwen 7B via Ollama
- **Ollama Base URL**: http://localhost:11434
- **CrewAI Server Port**: 8000
- **Smolagents Server Port**: 8001
- **Max Tokens**: 8192

## Original Project Credits

This project is based on the original implementation from the [AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub) repository, specifically the `acp-code` directory. The original work demonstrates the Agent Communication Protocol (ACP) for multi-agent collaboration.

**Original Repository**: https://github.com/patchy631/ai-engineering-hub/tree/main/acp-code

---

---

# 基于ACP的多智能体研究工作流

Agent Communication Protocol (ACP) 的演示，展示了使用不同框架（CrewAI和Smolagents）构建的两个智能体如何无缝协作生成和验证研究摘要。

## 功能特性

- **研究起草智能体**：使用CrewAI创建初始研究摘要
- **研究验证智能体**：使用Smolagents结合网络搜索进行事实检查和摘要增强
- **ACP协议**：实现不同智能体框架间的无缝通信
- **Ollama集成**：使用本地Qwen 7B模型进行经济高效的处理

## 架构设计

```
┌─────────────────┐    ACP     ┌─────────────────┐
│  CrewAI 服务器   │ ◄─────────► │ Smolagents      │
│  (端口 8000)    │            │ 服务器 (8001)   │
└─────────────────┘            └─────────────────┘
         ▲                              ▲
         │                              │
         └──────────────┬───────────────┘
                        │
                ┌───────▼────────┐
                │  ACP 客户端    │
                │  (工作流编排)  │
                └────────────────┘
```

## 环境要求

- Python 3.12+
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
   pip install -e .
   ```

## 使用方法

1. **启动CrewAI ACP服务器**（终端1）：
   ```bash
   uv run crew_acp_server.py
   ```

2. **启动Smolagents ACP服务器**（终端2）：
   ```bash
   uv run smolagents_acp_server.py
   ```

3. **运行客户端工作流**（终端3）：
   ```bash
   uv run acp_client.py
   ```

## 预期输出

工作流将执行以下步骤：
1. 使用CrewAI生成初始研究摘要
2. 使用Smolagents结合网络搜索进行事实检查和摘要增强
3. 显示草稿摘要和最终验证摘要

## 项目结构

```
acp-code/
├── crew_acp_server.py      # CrewAI ACP服务器 (端口 8000)
├── smolagents_acp_server.py # Smolagents ACP服务器 (端口 8001)
├── acp_client.py           # 客户端工作流编排器
├── pyproject.toml          # 项目依赖
└── README.md              # 本文件
```

## 配置说明

项目使用以下默认配置：
- **模型**：通过Ollama的Qwen 7B
- **Ollama基础URL**：http://localhost:11434
- **CrewAI服务器端口**：8000
- **Smolagents服务器端口**：8001
- **最大令牌数**：8192

## 原始项目致谢

本项目基于 [AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub) 仓库的原始实现，特别是 `acp-code` 目录。原始工作展示了Agent Communication Protocol (ACP) 在多智能体协作中的应用。

**原始仓库**：https://github.com/patchy631/ai-engineering-hub/tree/main/acp-code