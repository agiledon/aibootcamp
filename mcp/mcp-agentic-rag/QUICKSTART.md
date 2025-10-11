# 快速开始 - MCP Agentic RAG

## 🚀 5分钟快速开始

### 步骤1: 安装依赖

```bash
cd /path/to/mcp-agentic-rag
uv sync
```

### 步骤2: 配置搜索引擎（可选）

**推荐：使用DuckDuckGo（免费，无需配置）**

.env文件已自动创建，默认配置：
```bash
WEB_SEARCH_ENGINE=duckduckgo
```

**如需使用BrightData：**
```bash
# 编辑.env文件
WEB_SEARCH_ENGINE=brightdata
BRIGHT_DATA_USERNAME=your_actual_username
BRIGHT_DATA_PASSWORD=your_actual_password
```

### 步骤3: 启动Qdrant数据库

```bash
# 使用Docker
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant
```

### 步骤4: 初始化知识库

```bash
uv run rag_code.py
```

### 步骤5: 启动MCP服务器

```bash
uv run server.py
```

### 步骤6: 测试功能

```bash
# 测试搜索引擎
uv run test_simple_ddgs.py

# 预期输出：
# ✅ 所有基本功能测试通过！
```

## 🎯 支持的搜索引擎

### 1. DuckDuckGo（默认，推荐）

**优点：**
- ✅ 完全免费
- ✅ 无需API密钥
- ✅ 零配置即用
- ✅ 隐私保护

**配置：**
```bash
WEB_SEARCH_ENGINE=duckduckgo
```

**代码示例：**
```python
from rag_code import DuckDuckGoSearcher

searcher = DuckDuckGoSearcher(region='cn-zh')
results = searcher.search("人工智能", num_results=5)
```

---

### 2. Bright Data（高级）

**优点：**
- ✅ 高质量结果
- ✅ 稳定可靠
- ✅ 支持代理

**缺点：**
- ❌ 需要付费
- ❌ 需要配置

**配置：**
```bash
WEB_SEARCH_ENGINE=brightdata
BRIGHT_DATA_USERNAME=your_username
BRIGHT_DATA_PASSWORD=your_password
```

---

### 3. Bing（通过DuckDuckGo）

**配置：**
```bash
WEB_SEARCH_ENGINE=bing
```

## 📝 MCP工具使用

### 在Cursor中配置

编辑 `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "mcp-rag-app": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-agentic-rag",
        "run",
        "server.py"
      ]
    }
  }
}
```

### 使用工具

在Cursor中，AI会自动使用两个工具：

1. **machine_learning_faq_retrieval_tool** - 搜索本地ML知识库
2. **bright_data_web_search_tool** - 搜索网络信息

**示例对话：**
```
你: "什么是过拟合？"
  → 使用 machine_learning_faq_retrieval_tool（本地知识库）

你: "2025年最新的AI技术趋势是什么？"
  → 使用 bright_data_web_search_tool（网络搜索）
```

## 🔍 快速测试

### 测试1: 搜索引擎功能

```bash
uv run test_simple_ddgs.py
```

### 测试2: MCP工具集成

```python
from server import bright_data_web_search_tool

results = bright_data_web_search_tool("machine learning")
print(f"找到 {len(results)} 条结果")
```

### 测试3: 策略切换

```bash
# 测试DuckDuckGo
export WEB_SEARCH_ENGINE=duckduckgo
uv run server.py

# 测试Bing
export WEB_SEARCH_ENGINE=bing
uv run server.py
```

## 💡 常见问题

### Q1: 使用哪个搜索引擎？

**推荐：DuckDuckGo**
- 免费、无需配置
- 适合开发和测试
- 结果质量良好

**如果需要更高质量 → BrightData**

### Q2: 搜索失败怎么办？

```bash
# 检查网络连接
ping duckduckgo.com

# 切换搜索引擎
# 在.env中修改 WEB_SEARCH_ENGINE

# 查看详细错误
uv run server.py
```

### Q3: 如何添加新的搜索引擎？

1. 创建新的子类继承`WebSearcher`
2. 实现`search`方法
3. 在`server.py`的`_get_web_searcher()`中添加选项

```python
class MySearcher(WebSearcher):
    def search(self, query, num_results=50):
        # 实现搜索逻辑
        return results
```

## 🎊 完成！

现在您可以：
- ✅ 使用免费的DuckDuckGo进行网络搜索
- ✅ 通过配置轻松切换搜索引擎
- ✅ 在MCP客户端（如Cursor）中使用
- ✅ 结合本地知识库和网络搜索

**祝使用愉快！** 🚀

