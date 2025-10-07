# LangExtract RAG - Structured Information Extraction

A collection of examples demonstrating LangExtract's powerful structured information extraction capabilities from unstructured text. This project shows how to extract entities, relationships, and attributes from various types of documents using local LLMs instead of cloud-based models.

## Features

- **Precise Source Grounding**: Maps every extraction to its exact location in source text
- **Structured Outputs**: Enforces consistent output schema based on few-shot examples
- **Long Document Processing**: Handles large documents with optimized text chunking
- **Interactive Visualization**: Generates HTML visualizations for extracted entities
- **Local LLM Support**: Uses Ollama models (Llama3, Gemma2) instead of Gemini
- **Medical Entity Extraction**: Specialized examples for healthcare documents
- **Literature Analysis**: Character and emotion extraction from literary texts
- **Word Document Processing**: Extract text from DOCX files for analysis

## Prerequisites

- Python >= 3.12
- [Ollama](https://ollama.com/) installed and running
- Llama3 or Gemma2 models downloaded

## Installation

1. **Install Ollama and Required Models**:

   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull required models
   ollama pull llama3:latest
   ollama pull gemma2:9b
   ```

2. **Install Project Dependencies**:

   ```bash
   # Using uv (recommended)
   uv sync
   ```

## Usage

### 1. Medical Entity Extraction

Extract medication information from clinical notes:

```bash
uv run extract_medician_entity.py
```

This will extract:
- Medication names
- Dosages
- Routes of administration
- Frequency
- Duration

**Example Input:**
```
Patient took 400 mg PO Ibuprofen q4h for two days.
```

**Example Output:**
```
• Dosage: 400 mg (pos: 13-19)
• Route: PO (pos: 20-22)
• Medication: Ibuprofen (pos: 23-32)
• Frequency: q4h (pos: 33-36)
• Duration: for two days (pos: 37-49)
```

### 2. Literature Analysis

Extract characters, emotions, and relationships from Romeo and Juliet:

```bash
# Using Gemma2 model
uv run long_text_extract.py
```

This will:
- Download Romeo and Juliet from Project Gutenberg
- Extract characters, emotions, and relationships
- Generate interactive HTML visualization
- Save results to `romeo_juliet_extractions.jsonl`

### 3. Local Text Extraction

Enhanced extraction with local models:

```bash
uv run long_local_text_extract.py
```

Features:
- Parallel processing for speed
- Multiple extraction passes for higher recall
- Detailed progress tracking

### 4. Word Document Processing

Extract text from Word documents:

```bash
uv run word_to_text.py
```

Converts DOCX files to plain text while preserving formatting.

## Project Structure

```
langextract-rag/
├── extract_medician_entity.py    # Medical entity extraction
├── long_text_extract.py          # Literature analysis (Romeo & Juliet)
├── long_local_text_extract.py    # Enhanced local extraction
├── word_to_text.py               # Word document text extraction
├── example_usage.py              # General usage examples
├── document/                     # Input documents
│   ├── bounded_context.docx     # Example Word document
│   └── extracted_text.txt       # Extracted text output
├── pyproject.toml                # Project configuration
├── README.md                     # This file
└── README_word_to_text.md        # Word processing documentation
```

## Technical Details

### Extraction Configuration

```python
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="llama3:latest",  # Using Ollama provider
    model_url="http://localhost:11434",
    fence_output=False,
    use_schema_constraints=False
)
```

### Example Definition

```python
examples = [
    lx.data.ExampleData(
        text="Patient was given 250 mg IV Cefazolin TID for one week.",
        extractions=[
            lx.data.Extraction(
                extraction_class="dosage", 
                extraction_text="250 mg"
            ),
            # ... more extractions
        ]
    )
]
```

### Visualization Generation

```python
# Save results
lx.io.save_annotated_documents(
    [result], 
    output_name="results.jsonl"
)

# Generate interactive HTML
html_content = lx.visualize("results.jsonl")
with open("visualization.html", "w") as f:
    f.write(html_content)
```

## Use Cases

### 1. Healthcare - Medical Records
- Extract medications, dosages, routes, frequencies
- Clinical note structuring
- HIPAA-compliant processing with local models

### 2. Literature - Text Analysis
- Character identification and tracking
- Emotion and sentiment extraction
- Relationship mapping

### 3. Research - Academic Papers
- Entity extraction from scholarly articles
- Structured data from unstructured research

### 4. Business - Document Processing
- Extract key information from reports
- Structure unorganized business documents

## Key Differences from Official Examples

This project modifies the official LangExtract examples:

**Original (Official):**
- Uses Gemini models (cloud-based)
- Requires Google API key
- Cloud processing

**Modified (This Project):**
- Uses Ollama local models (Llama3, Gemma2)
- No API key required
- 100% local processing
- Privacy-preserving

## Output Examples

### Medical Extraction Visualization
Interactive HTML showing extracted medications with highlighted source positions.

### Literature Extraction Visualization
Character and emotion extraction from Romeo and Juliet with relationship mapping.

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**:
   ```bash
   # Ensure Ollama is running
   ollama serve
   
   # Check models are installed
   ollama list
   ```

2. **Model Not Found**:
   ```bash
   # Pull required models
   ollama pull llama3:latest
   ollama pull gemma2:9b
   ```

3. **Extraction Quality Issues**:
   - Provide more detailed examples
   - Adjust `max_char_buffer` for context size
   - Increase `extraction_passes` for better recall

4. **Performance Issues**:
   - Adjust `max_workers` for parallel processing
   - Use smaller `max_char_buffer` for faster processing
   - Consider using smaller models for speed

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

This project's code is based on the official LangExtract examples from [LangExtract.com](https://langextract.com/). The code has been modified to use local Ollama models (Llama3, Gemma2) instead of Google's Gemini models for privacy and cost-effectiveness.

**Original Examples:** https://langextract.com/

**Key Modifications:**
- Replaced Gemini models with Ollama local models
- Removed Google API key requirements
- Adapted for 100% local processing
- Added Chinese use case examples

**Key References:**
- [LangExtract Official Website](https://langextract.com/)
- [LangExtract GitHub Repository](https://github.com/google/langextract)
- [LangExtract Documentation](https://langextract.com/documentation)
- [Ollama Documentation](https://ollama.com/)

We extend our gratitude to the Google LangExtract team for creating this powerful library and providing comprehensive examples.

## Support

For issues and questions, please open an issue in the repository or contact the development team.

---

# LangExtract RAG - 结构化信息提取

演示LangExtract从非结构化文本中强大的结构化信息提取能力的示例集合。本项目展示了如何使用本地LLM而不是基于云的模型从各种类型的文档中提取实体、关系和属性。

## 功能特性

- **精确源定位**：将每个提取映射到源文本中的确切位置
- **结构化输出**：基于少样本示例强制执行一致的输出架构
- **长文档处理**：使用优化的文本分块处理大型文档
- **交互式可视化**：为提取的实体生成HTML可视化
- **本地LLM支持**：使用Ollama模型（Llama3、Gemma2）而不是Gemini
- **医疗实体提取**：用于医疗保健文档的专门示例
- **文学分析**：从文学文本中提取角色和情感
- **Word文档处理**：从DOCX文件中提取文本进行分析

## 环境要求

- Python >= 3.12
- [Ollama](https://ollama.com/) 已安装并运行
- 已下载Llama3或Gemma2模型

## 安装步骤

1. **安装Ollama和所需模型**：

   ```bash
   # 安装Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # 下载所需模型
   ollama pull llama3:latest
   ollama pull gemma2:9b
   ```

2. **安装项目依赖**：

   ```bash
   # 使用uv（推荐）
   uv sync
   ```

## 使用方法

### 1. 医疗实体提取

从临床笔记中提取药物信息：

```bash
uv run extract_medician_entity.py
```

这将提取：
- 药物名称
- 剂量
- 给药途径
- 频率
- 持续时间

**示例输入：**
```
Patient took 400 mg PO Ibuprofen q4h for two days.
```

**示例输出：**
```
• 剂量: 400 mg (位置: 13-19)
• 途径: PO (位置: 20-22)
• 药物: Ibuprofen (位置: 23-32)
• 频率: q4h (位置: 33-36)
• 持续时间: for two days (位置: 37-49)
```

### 2. 文学分析

从《罗密欧与朱丽叶》中提取角色、情感和关系：

```bash
# 使用Gemma2模型
uv run long_text_extract.py
```

这将：
- 从Project Gutenberg下载《罗密欧与朱丽叶》
- 提取角色、情感和关系
- 生成交互式HTML可视化
- 将结果保存到`romeo_juliet_extractions.jsonl`

### 3. 本地文本提取

使用本地模型的增强提取：

```bash
uv run long_local_text_extract.py
```

功能：
- 并行处理以提高速度
- 多次提取以提高召回率
- 详细的进度跟踪

### 4. Word文档处理

从Word文档中提取文本：

```bash
uv run word_to_text.py
```

在保留格式的同时将DOCX文件转换为纯文本。

## 项目结构

```
langextract-rag/
├── extract_medician_entity.py    # 医疗实体提取
├── long_text_extract.py          # 文学分析（罗密欧与朱丽叶）
├── long_local_text_extract.py    # 增强本地提取
├── word_to_text.py               # Word文档文本提取
├── example_usage.py              # 通用使用示例
├── document/                     # 输入文档
│   ├── bounded_context.docx     # 示例Word文档
│   └── extracted_text.txt       # 提取的文本输出
├── pyproject.toml                # 项目配置
├── README.md                     # 本文件
└── README_word_to_text.md        # Word处理文档
```

## 技术细节

### 提取配置

```python
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="llama3:latest",  # 使用Ollama提供商
    model_url="http://localhost:11434",
    fence_output=False,
    use_schema_constraints=False
)
```

### 示例定义

```python
examples = [
    lx.data.ExampleData(
        text="Patient was given 250 mg IV Cefazolin TID for one week.",
        extractions=[
            lx.data.Extraction(
                extraction_class="dosage", 
                extraction_text="250 mg"
            ),
            # ... 更多提取
        ]
    )
]
```

### 可视化生成

```python
# 保存结果
lx.io.save_annotated_documents(
    [result], 
    output_name="results.jsonl"
)

# 生成交互式HTML
html_content = lx.visualize("results.jsonl")
with open("visualization.html", "w") as f:
    f.write(html_content)
```

## 使用场景

### 1. 医疗保健 - 医疗记录
- 提取药物、剂量、途径、频率
- 临床笔记结构化
- 使用本地模型的HIPAA合规处理

### 2. 文学 - 文本分析
- 角色识别和跟踪
- 情感和情绪提取
- 关系映射

### 3. 研究 - 学术论文
- 从学术文章中提取实体
- 从非结构化研究中获取结构化数据

### 4. 商业 - 文档处理
- 从报告中提取关键信息
- 结构化无组织的商业文档

## 与官方示例的主要区别

本项目修改了官方LangExtract示例：

**原始（官方）：**
- 使用Gemini模型（基于云）
- 需要Google API密钥
- 云处理

**修改（本项目）：**
- 使用Ollama本地模型（Llama3、Gemma2）
- 不需要API密钥
- 100%本地处理
- 保护隐私

## 输出示例

### 医疗提取可视化
显示提取药物的交互式HTML，突出显示源位置。

### 文学提取可视化
从《罗密欧与朱丽叶》中提取的角色和情感，带有关系映射。

## 故障排除

### 常见问题

1. **Ollama连接失败**：
   ```bash
   # 确保Ollama正在运行
   ollama serve
   
   # 检查模型已安装
   ollama list
   ```

2. **找不到模型**：
   ```bash
   # 下载所需模型
   ollama pull llama3:latest
   ollama pull gemma2:9b
   ```

3. **提取质量问题**：
   - 提供更详细的示例
   - 调整`max_char_buffer`以设置上下文大小
   - 增加`extraction_passes`以提高召回率

4. **性能问题**：
   - 调整`max_workers`以进行并行处理
   - 使用较小的`max_char_buffer`以加快处理速度
   - 考虑使用较小的模型以提高速度

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

本项目的代码来自[LangExtract.com](https://langextract.com/)的官方示例。代码已修改为使用本地Ollama模型（Llama3、Gemma2）而不是Google的Gemini模型，以实现隐私保护和成本效益。

**原始示例：** https://langextract.com/

**主要修改：**
- 将Gemini模型替换为Ollama本地模型
- 移除Google API密钥要求
- 适配为100%本地处理
- 添加中文用例示例

**主要参考资料：**
- [LangExtract官方网站](https://langextract.com/)
- [LangExtract GitHub仓库](https://github.com/google/langextract)
- [LangExtract文档](https://langextract.com/documentation)
- [Ollama文档](https://ollama.com/)

我们向Google LangExtract团队表示感谢，感谢他们创建了这个强大的库并提供了全面的示例。

## 支持

如有问题和疑问，请在仓库中创建issue或联系开发团队。

