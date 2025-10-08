# Mowen MCP Usage Guide / 墨问MCP使用指南

## English

### Setup in Cursor IDE

1. **Configure MCP Server**:

   Open your Cursor MCP configuration file:
   ```bash
   ~/.cursor/mcp.json
   ```

   Add the Mowen Notes server:
   ```json
   {
     "mcpServers": {
       "mowen-notes": {
         "command": "uv",
         "args": ["run", "server.py"],
         "cwd": "/Users/zhangyi/workspace/learning/llm/aibootcamp/mcp/mowen-mcp"
       }
     }
   }
   ```

2. **Restart Cursor**:
   - Restart Cursor IDE to load the new MCP server
   - The Mowen Notes tools will be available in Cursor's AI assistant

### Using in Cursor

Once configured, you can ask Cursor AI to interact with Mowen Notes:

**Example 1 - Create a Note:**
```
Create a new Mowen note titled "Meeting Notes" with the following content:
- Discussed **quarterly goals**
- Next steps are ==highlighted==
- Follow-up meeting scheduled
```

**Example 2 - Edit a Note:**
```
Edit Mowen note [note_id] and update it with:
**Project Update**: We have completed ==Phase 1== successfully
```

**Example 3 - Change Privacy:**
```
Set Mowen note [note_id] to public
```

---

## 中文

### 在Cursor IDE中设置

1. **配置MCP服务器**：

   打开Cursor MCP配置文件：
   ```bash
   ~/.cursor/mcp.json
   ```

   添加墨问笔记服务器：
   ```json
   {
     "mcpServers": {
       "mowen-notes": {
         "command": "uv",
         "args": ["run", "server.py"],
         "cwd": "/Users/zhangyi/workspace/learning/llm/aibootcamp/mcp/mowen-mcp"
       }
     }
   }
   ```

2. **重启Cursor**：
   - 重启Cursor IDE以加载新的MCP服务器
   - 墨问笔记工具将在Cursor的AI助手中可用

### 在Cursor中使用

配置完成后，您可以要求Cursor AI与墨问笔记交互：

**示例1 - 创建笔记：**
```
创建一个标题为"会议笔记"的墨问笔记，内容如下：
- 讨论了**季度目标**
- 下一步是==高亮的==
- 已安排后续会议
```

**示例2 - 编辑笔记：**
```
编辑墨问笔记[note_id]，更新为：
**项目更新**：我们已成功完成==第一阶段==
```

**示例3 - 更改隐私：**
```
将墨问笔记[note_id]设置为公开
```

