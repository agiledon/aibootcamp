# Core LLM Knowledge and Implementations

A collection of fundamental Large Language Model (LLM) implementations and core concepts, demonstrating key techniques from tokenization to full GPT model training.

## Modules

### 1. basic_concept - LLM Fundamentals

Core LLM concepts and basic implementations.

**Files:**
- `dataloader.py` - GPT dataset creation and data loading with sliding window
- `input_embeddings.py` - Token and positional embedding implementations
- `tiktoken_tokenizer.py` - Tokenization using TikToken (GPT-2 encoding)
- `generate_text.py` - Text generation with temperature and top-k sampling
- `use_sliding_window.py` - Sliding window attention mechanism
- `music_recommendation.py` - LLM-based music recommendation system

**Key Concepts:**
- Tokenization and encoding
- Input embeddings (token + positional)
- Data loading with sliding windows
- Text generation strategies
- Sampling techniques (temperature, top-k)

### 2. easy-gpt - Complete GPT Implementation

A from-scratch GPT model implementation following the GPT-2 architecture.

**Files:**
- `gpt_model.py` - Complete GPT model architecture
- `gpt_config.py` - Model configuration (124M parameters)
- `multi_head_attention.py` - Multi-head self-attention mechanism
- `feed_forward.py` - Feed-forward neural network
- `layer_norm.py` - Layer normalization
- `transformer_block.py` - Transformer block implementation
- `train_gpt.py` - Model training script
- `load_model.py` - Model loading and inference

**Key Components:**
- Multi-head self-attention
- Feed-forward networks
- Layer normalization
- Transformer blocks
- Text generation with trained model

### 3. qlora-example - Parameter-Efficient Fine-Tuning

QLoRA (Quantized Low-Rank Adaptation) fine-tuning examples.

**Files:**
- `qlora.py` - QLoRA fine-tuning implementation with TinyLlama

**Key Features:**
- 4-bit quantization for memory efficiency
- LoRA adapters for parameter-efficient training
- Local model and dataset caching
- HuggingFace integration

## Prerequisites

- Python >= 3.10
- PyTorch >= 2.8.0
- Sufficient GPU memory (recommended for training)

## Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## Usage

### Running Basic Concepts

```bash
# Tokenization example
python basic_concept/tiktoken_tokenizer.py

# Data loading example
python basic_concept/dataloader.py

# Text generation example
python basic_concept/generate_text.py

# Input embeddings example
python basic_concept/input_embeddings.py

# Sliding window example
python basic_concept/use_sliding_window.py

# Music recommendation example
python basic_concept/music_recommendation.py
```

### Training GPT Model

```bash
# Navigate to easy-gpt directory
cd easy-gpt

# Run training
python train_gpt.py
```

The trained model will be saved as `model.pth`.

### Running QLoRA Fine-Tuning

```bash
# Navigate to qlora-example directory
cd qlora-example

# Run QLoRA fine-tuning
python qlora.py
```

## Project Structure

```
llm/
├── basic_concept/              # Fundamental LLM concepts
│   ├── __init__.py
│   ├── dataloader.py          # Data loading with sliding window
│   ├── input_embeddings.py    # Token and positional embeddings
│   ├── tiktoken_tokenizer.py  # Tokenization
│   ├── generate_text.py       # Text generation
│   ├── use_sliding_window.py  # Sliding window attention
│   └── music_recommendation.py # Recommendation system
├── easy-gpt/                   # Complete GPT implementation
│   ├── gpt_model.py           # GPT model architecture
│   ├── gpt_config.py          # Model configuration
│   ├── multi_head_attention.py # Self-attention
│   ├── feed_forward.py        # Feed-forward network
│   ├── layer_norm.py          # Layer normalization
│   ├── transformer_block.py   # Transformer block
│   ├── train_gpt.py           # Training script
│   └── load_model.py          # Model loading
├── qlora-example/              # QLoRA fine-tuning
│   ├── qlora.py               # QLoRA implementation
│   └── cache/                 # Model and dataset cache
├── data/                       # Training data
│   ├── the-verdict.txt        # Sample text data
│   ├── train.txt              # Training data
│   └── song_hash.txt          # Music data
├── main.py                     # Main entry point
└── README.md                   # This file
```

## Key Concepts Covered

### Tokenization
- BPE (Byte Pair Encoding) tokenization
- TikToken encoding (GPT-2 compatible)
- Vocabulary management

### Embeddings
- Token embeddings
- Positional embeddings
- Combined embedding layers

### Model Architecture
- Multi-head self-attention
- Feed-forward networks
- Layer normalization
- Residual connections
- Transformer blocks

### Training Techniques
- Cross-entropy loss
- Adam optimizer
- Learning rate scheduling
- Gradient clipping

### Text Generation
- Greedy decoding
- Temperature sampling
- Top-k sampling
- Beam search (advanced)

### Fine-Tuning
- QLoRA (Quantized LoRA)
- 4-bit quantization
- Parameter-efficient training
- LoRA adapters

## Dependencies

```
torch>=2.8.0          # Deep learning framework
transformers>=4.56.1  # HuggingFace transformers
datasets>=4.0.0       # Dataset loading
tiktoken>=0.11.0      # Tokenization
matplotlib>=3.10.6    # Visualization
pandas>=2.3.2         # Data manipulation
gensim>=4.3.3         # NLP utilities
accelerate>=1.10.1    # Training acceleration
```

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

This project's code is primarily based on:
- **"Hands-On Large Language Models"** - Fundamental concepts and implementations
- **"Build a Large Language Model from Scratch"** - Complete GPT implementation from scratch

The code has been adapted and updated to work with the latest versions of PyTorch, Transformers, and related libraries.

**Key References:**
- "Hands-On Large Language Models" (《图解大模型》)
- "Build a Large Language Model from Scratch" (《从零构建大模型》)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)

We extend our gratitude to the authors of these books for providing comprehensive guides and implementation examples that made this learning project possible.

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# 大模型核心知识与实现

大语言模型（LLM）的基础实现和核心概念集合，展示从分词到完整GPT模型训练的关键技术。

## 模块

### 1. basic_concept - LLM基础知识

LLM的核心概念和基础实现。

**文件：**
- `dataloader.py` - GPT数据集创建和滑动窗口数据加载
- `input_embeddings.py` - 词元和位置嵌入实现
- `tiktoken_tokenizer.py` - 使用TikToken进行分词（GPT-2编码）
- `generate_text.py` - 带温度和top-k采样的文本生成
- `use_sliding_window.py` - 滑动窗口注意力机制
- `music_recommendation.py` - 基于LLM的音乐推荐系统

**关键概念：**
- 分词和编码
- 输入嵌入（词元 + 位置）
- 滑动窗口数据加载
- 文本生成策略
- 采样技术（温度、top-k）

### 2. easy-gpt - 完整GPT实现

遵循GPT-2架构的从零开始GPT模型实现。

**文件：**
- `gpt_model.py` - 完整的GPT模型架构
- `gpt_config.py` - 模型配置（1.24亿参数）
- `multi_head_attention.py` - 多头自注意力机制
- `feed_forward.py` - 前馈神经网络
- `layer_norm.py` - 层归一化
- `transformer_block.py` - Transformer块实现
- `train_gpt.py` - 模型训练脚本
- `load_model.py` - 模型加载和推理

**关键组件：**
- 多头自注意力
- 前馈网络
- 层归一化
- Transformer块
- 使用训练模型生成文本

### 3. qlora-example - 参数高效微调

QLoRA（量化低秩适应）微调示例。

**文件：**
- `qlora.py` - 使用TinyLlama的QLoRA微调实现

**关键特性：**
- 4位量化以提高内存效率
- 用于参数高效训练的LoRA适配器
- 本地模型和数据集缓存
- HuggingFace集成

## 环境要求

- Python >= 3.10
- PyTorch >= 2.8.0
- 足够的GPU内存（训练时推荐）

## 安装步骤

```bash
# 使用uv（推荐）
uv sync

# 或使用pip
pip install -e .
```

## 使用方法

### 运行基础概念

```bash
# 分词示例
python basic_concept/tiktoken_tokenizer.py

# 数据加载示例
python basic_concept/dataloader.py

# 文本生成示例
python basic_concept/generate_text.py

# 输入嵌入示例
python basic_concept/input_embeddings.py

# 滑动窗口示例
python basic_concept/use_sliding_window.py

# 音乐推荐示例
python basic_concept/music_recommendation.py
```

### 训练GPT模型

```bash
# 进入easy-gpt目录
cd easy-gpt

# 运行训练
python train_gpt.py
```

训练后的模型将保存为 `model.pth`。

### 运行QLoRA微调

```bash
# 进入qlora-example目录
cd qlora-example

# 运行QLoRA微调
python qlora.py
```

## 项目结构

```
llm/
├── basic_concept/              # LLM基础概念
│   ├── __init__.py
│   ├── dataloader.py          # 滑动窗口数据加载
│   ├── input_embeddings.py    # 词元和位置嵌入
│   ├── tiktoken_tokenizer.py  # 分词
│   ├── generate_text.py       # 文本生成
│   ├── use_sliding_window.py  # 滑动窗口注意力
│   └── music_recommendation.py # 推荐系统
├── easy-gpt/                   # 完整GPT实现
│   ├── gpt_model.py           # GPT模型架构
│   ├── gpt_config.py          # 模型配置
│   ├── multi_head_attention.py # 自注意力
│   ├── feed_forward.py        # 前馈网络
│   ├── layer_norm.py          # 层归一化
│   ├── transformer_block.py   # Transformer块
│   ├── train_gpt.py           # 训练脚本
│   └── load_model.py          # 模型加载
├── qlora-example/              # QLoRA微调
│   ├── qlora.py               # QLoRA实现
│   └── cache/                 # 模型和数据集缓存
├── data/                       # 训练数据
│   ├── the-verdict.txt        # 示例文本数据
│   ├── train.txt              # 训练数据
│   └── song_hash.txt          # 音乐数据
├── main.py                     # 主入口点
└── README.md                   # 本文件
```

## 涵盖的关键概念

### 分词
- BPE（字节对编码）分词
- TikToken编码（与GPT-2兼容）
- 词汇表管理

### 嵌入
- 词元嵌入
- 位置嵌入
- 组合嵌入层

### 模型架构
- 多头自注意力
- 前馈网络
- 层归一化
- 残差连接
- Transformer块

### 训练技术
- 交叉熵损失
- Adam优化器
- 学习率调度
- 梯度裁剪

### 文本生成
- 贪婪解码
- 温度采样
- Top-k采样
- 束搜索（高级）

### 微调
- QLoRA（量化LoRA）
- 4位量化
- 参数高效训练
- LoRA适配器

## 依赖项

```
torch>=2.8.0          # 深度学习框架
transformers>=4.56.1  # HuggingFace transformers
datasets>=4.0.0       # 数据集加载
tiktoken>=0.11.0      # 分词
matplotlib>=3.10.6    # 可视化
pandas>=2.3.2         # 数据处理
gensim>=4.3.3         # NLP工具
accelerate>=1.10.1    # 训练加速
```

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

本项目的代码主要基于：
- **《图解大模型》（Hands-On Large Language Models）** - 基础概念和实现
- **《从零构建大模型》（Build a Large Language Model from Scratch）** - 从零开始的完整GPT实现

代码已经过调整和更新，以与PyTorch、Transformers和相关库的最新版本兼容。

**主要参考资料：**
- 《图解大模型》（Hands-On Large Language Models）
- 《从零构建大模型》（Build a Large Language Model from Scratch）
- [PyTorch文档](https://pytorch.org/docs/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)

我们向这些书籍的作者表示感谢，感谢他们提供了全面的指南和实现示例，使这个学习项目成为可能。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。
