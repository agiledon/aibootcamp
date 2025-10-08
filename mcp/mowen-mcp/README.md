# Mowen Notes MCP - 墨问笔记模型上下文协议

An MCP (Model Context Protocol) server for interacting with Mowen Notes (墨问笔记) API, enabling AI assistants to create, edit, and manage notes programmatically.

## Features

- **Create Notes**: Create rich-text notes with formatting (bold, highlight, paragraphs)
- **Edit Notes**: Update existing notes with new content and formatting
- **Privacy Settings**: Set notes as public or private
- **MCP Integration**: Standard MCP protocol for Cursor and other AI IDEs
- **Rich Text Support**: Supports markdown-like syntax for formatting
- **Stdio Transport**: Communication via standard input/output

## Prerequisites

- Python >= 3.11
- Mowen Notes Pro account
- Mowen API Key

## Installation

1. **Get Mowen API Key**:

   - Log in to [Mowen Notes](https://mowen.cn)
   - Subscribe to Mowen Pro membership
   - Get your API key from account settings

2. **Set up Environment**:

   Create a `.env` file:
   ```bash
   MOWEN_API_KEY=your_mowen_api_key_here
   ```

3. **Install Project Dependencies**:

   ```bash
   # Using uv (recommended)
   uv sync
   ```

## MCP Tools

### 1. create_note
Creates a new note in Mowen.

**Parameters:**
- `title` (str): Note title
- `content` (str): Note content with formatting support
- `is_private` (bool, optional): Whether to set note as private (default: True)

**Formatting Syntax:**
- `**text**` - Bold text
- `==text==` - Highlighted text
- Empty line - Paragraph separator

**Example:**
```python
create_note(
    "My First Note",
    "This is **bold text** and ==highlighted text==\n\nSecond paragraph"
)
```

### 2. edit_note
Edits an existing note.

**Parameters:**
- `note_id` (str): Note ID to edit
- `new_content` (str): New content with formatting support

**Example:**
```python
edit_note("note_123", "Updated **content** with ==highlights==")
```

### 3. set_note_privacy
Sets note privacy status.

**Parameters:**
- `note_id` (str): Note ID
- `privacy_type` (str): Privacy type - "public", "private", or "rule"

**Example:**
```python
set_note_privacy("note_123", "public")
```

## Usage

### Running as MCP Server

Start the MCP server for Cursor or other MCP clients:

```bash
uv run server.py
```

### Configure in Cursor

Add to your Cursor MCP configuration (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "mowen-notes": {
      "command": "uv",
      "args": ["run", "server.py"],
      "cwd": "/absolute/path/to/mowen-mcp"
    }
  }
}
```

### Testing Tools

Test individual tools:

```bash
uv run test_tools.py
```

This will test:
1. Create a test note
2. Edit the created note
3. Change privacy settings

## Project Structure

```
mowen-mcp/
├── server.py           # MCP server with Mowen API tools
├── test_tools.py       # Tool testing script
├── .env                # API key configuration (not tracked)
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

## Technical Details

### Note Body Structure

Notes are created using Mowen's NoteAtom structure:

```json
{
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Normal text"},
        {"type": "text", "marks": [{"type": "bold"}], "text": "Bold text"},
        {"type": "text", "marks": [{"type": "highlight"}], "text": "Highlighted"}
      ]
    }
  ]
}
```

### API Endpoints

- **Create Note**: `POST https://open.mowen.cn/open-api/note`
- **Edit Note**: `POST https://open.mowen.cn/open-api/note/edit`
- **Settings**: `POST https://open.mowen.cn/open-api/note/settings`

### Authentication

```python
headers = {
    "Authorization": f"Bearer {MOWEN_API_KEY}",
    "Content-Type": "application/json"
}
```

## Formatting Examples

### Basic Formatting
```
This is normal text
This is **bold text**
This is ==highlighted text==
This has **bold** and ==highlight== together
```

### Paragraphs
```
First paragraph

Second paragraph

Third paragraph
```

### Combined Formatting
```
Title: **Important Update**

Content: We have ==critical information== to share

Details: Visit **our website** for ==more details==
```

## Troubleshooting

### Common Issues

1. **API Key Not Set**:
   ```bash
   # Check .env file
   cat .env
   
   # Ensure MOWEN_API_KEY is set
   echo $MOWEN_API_KEY
   ```

2. **503 Service Unavailable**:
   - Mowen API service may be temporarily down
   - Check Mowen status page
   - Retry after a few moments

3. **401 Unauthorized**:
   - Verify API key is correct
   - Ensure Pro membership is active
   - Check API key hasn't expired

4. **Note Not Found (Edit/Settings)**:
   - Verify note_id is correct
   - Ensure note exists in your account

## API Reference

For detailed API documentation, visit:
- [Mowen API Documentation](https://mowen.apifox.cn/)

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

---

# 墨问笔记 MCP - Mowen Notes Model Context Protocol

用于与墨问笔记（Mowen Notes）API交互的MCP（模型上下文协议）服务器，使AI助手能够以编程方式创建、编辑和管理笔记。

## 功能特性

- **创建笔记**：创建支持格式化的富文本笔记（加粗、高亮、段落）
- **编辑笔记**：使用新内容和格式更新现有笔记
- **隐私设置**：将笔记设置为公开或隐私
- **MCP集成**：适用于Cursor和其他AI IDE的标准MCP协议
- **富文本支持**：支持类似markdown的格式化语法
- **Stdio传输**：通过标准输入/输出通信

## 环境要求

- Python >= 3.11
- 墨问笔记Pro账户
- 墨问API密钥

## 安装步骤

1. **获取墨问API密钥**：

   - 登录[墨问笔记](https://mowen.cn)
   - 订阅墨问Pro会员
   - 从账户设置中获取API密钥

2. **设置环境**：

   创建`.env`文件：
   ```bash
   MOWEN_API_KEY=your_mowen_api_key_here
   ```

3. **安装项目依赖**：

   ```bash
   # 使用uv（推荐）
   uv sync
   ```

## MCP工具

### 1. create_note
在墨问中创建新笔记。

**参数：**
- `title` (str)：笔记标题
- `content` (str)：支持格式化的笔记内容
- `is_private` (bool, 可选)：是否设置为隐私笔记（默认：True）

**格式化语法：**
- `**文本**` - 加粗文本
- `==文本==` - 高亮文本
- 空行 - 段落分隔符

**示例：**
```python
create_note(
    "我的第一个笔记",
    "这是**加粗文本**和==高亮文本==\n\n第二段"
)
```

### 2. edit_note
编辑现有笔记。

**参数：**
- `note_id` (str)：要编辑的笔记ID
- `new_content` (str)：支持格式化的新内容

**示例：**
```python
edit_note("note_123", "更新的**内容**包含==高亮==")
```

### 3. set_note_privacy
设置笔记隐私状态。

**参数：**
- `note_id` (str)：笔记ID
- `privacy_type` (str)：隐私类型 - "public"、"private" 或 "rule"

**示例：**
```python
set_note_privacy("note_123", "public")
```

## 使用方法

### 作为MCP服务器运行

为Cursor或其他MCP客户端启动MCP服务器：

```bash
uv run server.py
```

### 在Cursor中配置

添加到Cursor MCP配置（`~/.cursor/mcp.json`）：

```json
{
  "mcpServers": {
    "mowen-notes": {
      "command": "uv",
      "args": ["run", "server.py"],
      "cwd": "/absolute/path/to/mowen-mcp"
    }
  }
}
```

### 测试工具

测试单个工具：

```bash
uv run test_tools.py
```

这将测试：
1. 创建测试笔记
2. 编辑创建的笔记
3. 更改隐私设置

## 项目结构

```
mowen-mcp/
├── server.py           # 带有墨问API工具的MCP服务器
├── test_tools.py       # 工具测试脚本
├── .env                # API密钥配置（不跟踪）
├── pyproject.toml      # 项目配置
└── README.md           # 本文件
```

## 技术细节

### 笔记Body结构

笔记使用墨问的NoteAtom结构创建：

```json
{
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "普通文本"},
        {"type": "text", "marks": [{"type": "bold"}], "text": "加粗文本"},
        {"type": "text", "marks": [{"type": "highlight"}], "text": "高亮"}
      ]
    }
  ]
}
```

### API端点

- **创建笔记**：`POST https://open.mowen.cn/open-api/note`
- **编辑笔记**：`POST https://open.mowen.cn/open-api/note/edit`
- **设置**：`POST https://open.mowen.cn/open-api/note/settings`

### 认证

```python
headers = {
    "Authorization": f"Bearer {MOWEN_API_KEY}",
    "Content-Type": "application/json"
}
```

## 格式化示例

### 基本格式化
```
这是普通文本
这是**加粗文本**
这是==高亮文本==
这同时有**加粗**和==高亮==
```

### 段落
```
第一段

第二段

第三段
```

### 组合格式化
```
标题：**重要更新**

内容：我们有==关键信息==要分享

详情：访问**我们的网站**获取==更多详情==
```

## 故障排除

### 常见问题

1. **API密钥未设置**：
   ```bash
   # 检查.env文件
   cat .env
   
   # 确保MOWEN_API_KEY已设置
   echo $MOWEN_API_KEY
   ```

2. **503服务不可用**：
   - 墨问API服务可能暂时宕机
   - 检查墨问状态页面
   - 稍后重试

3. **401未授权**：
   - 验证API密钥是否正确
   - 确保Pro会员处于活跃状态
   - 检查API密钥是否过期

4. **笔记未找到（编辑/设置）**：
   - 验证note_id是否正确
   - 确保笔记存在于您的账户中

## API参考

详细API文档，请访问：
- [墨问API文档](https://mowen.apifox.cn/)

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

