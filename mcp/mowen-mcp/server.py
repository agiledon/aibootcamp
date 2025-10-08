"""
墨问笔记 MCP 服务器
提供创建、编辑和设置笔记的工具
"""
import os
import json
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# 加载环境变量
load_dotenv()

# 创建 FastMCP 实例
mcp = FastMCP("mowen-notes")

# 墨问 API 配置
MOWEN_API_BASE = "https://open.mowen.cn"
MOWEN_API_KEY = os.getenv("MOWEN_API_KEY")

def get_headers():
    """获取API请求头"""
    return {
        "Authorization": f"Bearer {MOWEN_API_KEY}",
        "Content-Type": "application/json"
    }

def create_note_body(title: str, content: str, use_formatting: bool = True) -> dict:
    """
    创建笔记的body数据结构
    
    Args:
        title: 笔记标题
        content: 笔记内容（支持格式化）
        use_formatting: 是否使用格式化
    
    Returns:
        符合墨问API规范的body字典
    """
    # 解析内容，支持简单的markdown格式
    paragraphs = []
    
    for line in content.split('\n'):
        if not line.strip():
            # 空行
            paragraphs.append({"type": "paragraph"})
            continue
            
        # 创建段落内容
        text_parts = []
        
        # 简单解析：查找**加粗**和==高亮==
        parts = line.split('**')
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # 普通文本，再检查高亮
                highlight_parts = part.split('==')
                for j, h_part in enumerate(highlight_parts):
                    if h_part:
                        if j % 2 == 0:
                            text_parts.append({"type": "text", "text": h_part})
                        else:
                            text_parts.append({"type": "text", "marks": [{"type": "highlight"}], "text": h_part})
            else:
                # 加粗文本
                if part:
                    text_parts.append({"type": "text", "marks": [{"type": "bold"}], "text": part})
        
        if text_parts:
            paragraphs.append({"type": "paragraph", "content": text_parts})
    
    # 构建最终body
    body = {
        "type": "doc",
        "content": paragraphs
    }
    
    return {
        "title": title,
        "body": json.dumps(body, ensure_ascii=False, separators=(',', ':'))
    }

@mcp.tool()
def create_note(title: str, content: str, is_private: bool = True) -> str:
    """
    创建墨问笔记
    
    Args:
        title: 笔记标题
        content: 笔记内容，支持简单格式：
                 - 使用 **文本** 表示加粗
                 - 使用 ==文本== 表示高亮
                 - 空行表示段落分隔
        is_private: 是否设置为隐私笔记，默认为True
    
    Returns:
        创建结果的JSON字符串
    
    Example:
        >>> create_note(
        ...     "我的第一个笔记", 
        ...     "这是**加粗文本**和==高亮文本==\\n\\n这是第二段"
        ... )
    """
    if not MOWEN_API_KEY:
        return json.dumps({"error": "MOWEN_API_KEY not set in environment"}, ensure_ascii=False)
    
    try:
        # 创建笔记body
        note_data = create_note_body(title, content)
        
        # 添加隐私设置
        if is_private:
            note_data["settings"] = json.dumps({
                "privacy": {"type": "private"}
            }, ensure_ascii=False, separators=(',', ':'))
        
        # 调用墨问API创建笔记
        response = requests.post(
            f"{MOWEN_API_BASE}/open-api/note",
            headers=get_headers(),
            json=note_data,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        return json.dumps({
            "success": True,
            "note_id": result.get("data", {}).get("id"),
            "message": f"笔记 '{title}' 创建成功"
        }, ensure_ascii=False)
        
    except requests.RequestException as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)

@mcp.tool()
def edit_note(note_id: str, new_content: str) -> str:
    """
    编辑已存在的墨问笔记
    
    Args:
        note_id: 笔记ID
        new_content: 新的笔记内容，支持格式化：
                     - 使用 **文本** 表示加粗
                     - 使用 ==文本== 表示高亮
                     - 空行表示段落分隔
    
    Returns:
        编辑结果的JSON字符串
    
    Example:
        >>> edit_note("note_123", "更新的**内容**")
    """
    if not MOWEN_API_KEY:
        return json.dumps({"error": "MOWEN_API_KEY not set in environment"}, ensure_ascii=False)
    
    try:
        # 解析新内容
        paragraphs = []
        for line in new_content.split('\n'):
            if not line.strip():
                paragraphs.append({"type": "paragraph"})
                continue
                
            text_parts = []
            parts = line.split('**')
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    highlight_parts = part.split('==')
                    for j, h_part in enumerate(highlight_parts):
                        if h_part:
                            if j % 2 == 0:
                                text_parts.append({"type": "text", "text": h_part})
                            else:
                                text_parts.append({"type": "text", "marks": [{"type": "highlight"}], "text": h_part})
                else:
                    if part:
                        text_parts.append({"type": "text", "marks": [{"type": "bold"}], "text": part})
            
            if text_parts:
                paragraphs.append({"type": "paragraph", "content": text_parts})
        
        body = {
            "type": "doc",
            "content": paragraphs
        }
        
        # 调用编辑API
        edit_data = {
            "note_id": note_id,
            "body": json.dumps(body, ensure_ascii=False, separators=(',', ':'))
        }
        
        response = requests.post(
            f"{MOWEN_API_BASE}/open-api/note/edit",
            headers=get_headers(),
            json=edit_data,
            timeout=30
        )
        
        response.raise_for_status()
        
        return json.dumps({
            "success": True,
            "note_id": note_id,
            "message": f"笔记 {note_id} 编辑成功"
        }, ensure_ascii=False)
        
    except requests.RequestException as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "message": "笔记编辑失败，请检查note_id是否正确"
        }, ensure_ascii=False)

@mcp.tool()
def set_note_privacy(note_id: str, privacy_type: str = "private") -> str:
    """
    设置笔记的隐私状态
    
    Args:
        note_id: 笔记ID
        privacy_type: 隐私类型，可选值：
                     - "public": 完全公开
                     - "private": 完全隐私
                     - "rule": 基于规则的公开（暂不支持）
    
    Returns:
        设置结果的JSON字符串
    
    Example:
        >>> set_note_privacy("note_123", "public")
    """
    if not MOWEN_API_KEY:
        return json.dumps({"error": "MOWEN_API_KEY not set in environment"}, ensure_ascii=False)
    
    if privacy_type not in ["public", "private", "rule"]:
        return json.dumps({
            "success": False,
            "error": f"无效的privacy_type: {privacy_type}，必须是 'public', 'private' 或 'rule'"
        }, ensure_ascii=False)
    
    try:
        # 构建设置数据
        settings_data = {
            "note_id": note_id,
            "section": 1,  # 隐私规则分类
            "settings": json.dumps({
                "privacy": {"type": privacy_type}
            }, ensure_ascii=False, separators=(',', ':'))
        }
        
        # 调用设置API
        response = requests.post(
            f"{MOWEN_API_BASE}/open-api/note/settings",
            headers=get_headers(),
            json=settings_data,
            timeout=30
        )
        
        response.raise_for_status()
        
        privacy_desc = {
            "public": "公开",
            "private": "隐私",
            "rule": "基于规则"
        }
        
        return json.dumps({
            "success": True,
            "note_id": note_id,
            "privacy": privacy_type,
            "message": f"笔记 {note_id} 已设置为{privacy_desc.get(privacy_type, privacy_type)}"
        }, ensure_ascii=False)
        
    except requests.RequestException as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "message": "笔记设置失败，请检查note_id是否正确"
        }, ensure_ascii=False)

# 运行服务器
if __name__ == "__main__":
    print("Starting Mowen Notes MCP Server...")
    print(f"API Base: {MOWEN_API_BASE}")
    print(f"API Key configured: {'Yes' if MOWEN_API_KEY else 'No'}")
    print("\nAvailable tools:")
    print("1. create_note - 创建笔记")
    print("2. edit_note - 编辑笔记")
    print("3. set_note_privacy - 设置笔记隐私")
    mcp.run(transport='stdio')

