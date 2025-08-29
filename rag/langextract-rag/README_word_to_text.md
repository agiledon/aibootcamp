# Word文档转文本工具

这个工具提供了将Word文档（.docx格式）转换为文本字符串的功能，支持处理单个文件或整个文件夹中的Word文档。

## 功能特性

- ✅ 支持处理单个Word文档
- ✅ 支持批量处理文件夹中的所有Word文档
- ✅ 多种文本提取方法（python-docx, mammoth, textract）
- ✅ 自动选择最佳提取方法
- ✅ 支持表格内容提取
- ✅ 可自定义文档分隔符
- ✅ 支持保存为文本文件
- ✅ 详细的日志记录

## 安装依赖

```bash
# 进入项目目录
cd rag/langextract-rag

# 安装依赖（使用uv）
uv add python-docx mammoth textract

# 或者使用pip
pip install python-docx mammoth textract
```

## 主要函数

### 1. `extract_text_from_word_document(file_path, method="auto")`

从单个Word文档中提取文本。

**参数：**
- `file_path`: Word文档的路径
- `method`: 提取方法，可选值：
  - `"auto"`: 自动选择最佳方法（默认）
  - `"python-docx"`: 使用python-docx库
  - `"mammoth"`: 使用mammoth库
  - `"textract"`: 使用textract库

**返回值：**
- 提取的文本字符串

**示例：**
```python
from word_to_text import extract_text_from_word_document

# 提取单个文档的文本
text = extract_text_from_word_document("document/bounded_context.docx")
print(f"提取的文本长度: {len(text)} 字符")
```

### 2. `convert_documents_to_text(folder_path, file_pattern="*.docx", method="auto", combine_all=True, separator="...")`

将指定文件夹下的Word文档转换为文本。

**参数：**
- `folder_path`: 文档文件夹路径
- `file_pattern`: 文件匹配模式，默认为"*.docx"
- `method`: 提取方法
- `combine_all`: 是否将所有文档合并为一个字符串
- `separator`: 文档之间的分隔符（仅在combine_all=True时使用）

**返回值：**
- 如果`combine_all=True`，返回合并的文本字符串
- 如果`combine_all=False`，返回文本字符串列表

**示例：**
```python
from word_to_text import convert_documents_to_text

# 合并所有文档为一个字符串
combined_text = convert_documents_to_text(
    folder_path="document",
    file_pattern="*.docx",
    combine_all=True
)

# 分别处理每个文档
texts = convert_documents_to_text(
    folder_path="document",
    file_pattern="*.docx",
    combine_all=False
)
```

### 3. `save_text_to_file(text, output_path)`

将文本保存到文件。

**参数：**
- `text`: 要保存的文本
- `output_path`: 输出文件路径

**返回值：**
- 是否保存成功

## 使用示例

### 基本用法

```python
from word_to_text import convert_documents_to_text, save_text_to_file

# 处理document文件夹下的所有Word文档
text = convert_documents_to_text("document")

# 保存到文件
save_text_to_file(text, "output/extracted_text.txt")
```

### 高级用法

```python
from word_to_text import convert_documents_to_text

# 自定义分隔符和处理选项
text = convert_documents_to_text(
    folder_path="document",
    file_pattern="*.docx",
    method="python-docx",
    combine_all=True,
    separator="\n\n" + "="*80 + "\n\n"
)

# 分别处理每个文档
documents = convert_documents_to_text(
    folder_path="document",
    combine_all=False
)

for i, doc_text in enumerate(documents):
    print(f"文档 {i+1}: {len(doc_text)} 字符")
```

### 运行示例

```bash
# 运行完整示例
python example_usage.py

# 运行主程序
python word_to_text.py
```

## 输出格式

提取的文本包含以下格式：

1. **文档标题**: 每个文档以 `# 文件名` 开头
2. **段落文本**: 保持原有的段落结构
3. **表格文本**: 表格内容以 `|` 分隔符连接
4. **文档分隔**: 多个文档之间用自定义分隔符分隔

## 支持的库

工具支持以下三个主要的Word文档处理库：

1. **python-docx**: 最稳定，支持表格提取
2. **mammoth**: 轻量级，处理速度快
3. **textract**: 功能全面，支持多种格式

工具会自动选择可用的最佳方法，如果某个方法失败，会尝试其他方法。

## 注意事项

1. 确保Word文档是`.docx`格式（不支持旧的`.doc`格式）
2. 某些复杂的文档格式可能无法完全保留
3. 图片和图表内容无法提取
4. 建议在处理大量文档前先测试单个文档

## 错误处理

工具包含完善的错误处理机制：

- 文件不存在时会记录错误并返回空字符串
- 提取失败时会尝试其他方法
- 所有错误都会记录到日志中
- 不会因为单个文件失败而中断整个处理过程

## 性能优化

- 对于大文件，建议使用`mammoth`方法
- 对于包含表格的文档，建议使用`python-docx`方法
- 批量处理时，工具会按文件名排序处理
