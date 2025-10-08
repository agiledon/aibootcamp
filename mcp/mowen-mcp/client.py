"""
墨问笔记 MCP 客户端
使用 LlamaIndex FunctionAgent 与 MCP 服务器交互
"""
import asyncio
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context
from llama_index.llms.ollama import Ollama

# 配置 LLM
llm = Ollama(
    model="qwen:7b",
    base_url="http://localhost:11434",
    request_timeout=120.0
)

# 系统提示词
SYSTEM_PROMPT = """你是墨问笔记的AI助手。

你可以帮助用户：
1. 创建笔记 - 使用create_note工具
2. 编辑笔记 - 使用edit_note工具
3. 设置笔记隐私 - 使用set_note_privacy工具

格式化语法：
- 使用 **文本** 表示加粗
- 使用 ==文本== 表示高亮
- 空行表示段落分隔

在创建或编辑笔记时，请合理使用格式化以提高可读性。
"""

async def get_agent(tools: McpToolSpec):
    """创建并返回配置好的 FunctionAgent"""
    tools = await tools.to_tool_list_async()
    agent = FunctionAgent(
        name="MowenNotesAgent",
        description="An agent that can create, edit and manage Mowen notes.",
        tools=tools,
        llm=llm,
        system_prompt=SYSTEM_PROMPT,
    )
    return agent

async def handle_user_message(
    message_content: str,
    agent: FunctionAgent,
    agent_context: Context,
    verbose: bool = True,
):
    """处理用户消息"""
    from llama_index.core.agent.workflow import ToolCall, ToolCallResult
    
    handler = agent.run(message_content, ctx=agent_context)
    async for event in handler.stream_events():
        if verbose and isinstance(event, ToolCall):
            print(f"🔧 调用工具: {event.tool_name}")
            print(f"   参数: {event.tool_kwargs}")
        elif verbose and isinstance(event, ToolCallResult):
            print(f"✅ 工具 {event.tool_name} 返回结果")

    response = await handler
    return str(response)

async def main():
    print("=" * 60)
    print("墨问笔记 MCP 客户端")
    print("=" * 60)
    
    # 初始化 MCP 客户端和工具
    # 注意：服务器需要先启动
    try:
        # 使用stdio连接到MCP服务器
        # 在实际使用中，需要先启动server.py
        print("\n⚠️  注意：此客户端需要先启动 server.py")
        print("   启动方式：uv run server.py")
        print("\n由于使用stdio传输，建议直接在Cursor中使用MCP服务器。")
        print("参考 USAGE.md 了解如何在Cursor中配置。\n")
        
        # 演示客户端代码结构
        print("客户端代码已准备好，主要功能：")
        print("1. 连接到MCP服务器")
        print("2. 创建FunctionAgent")
        print("3. 处理用户输入并调用工具")
        print("4. 返回格式化的响应")
        
        print("\n💡 推荐使用方式：")
        print("   在Cursor中配置MCP服务器后，直接使用AI助手交互")
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())

