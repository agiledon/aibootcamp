"""
测试墨问笔记MCP工具
"""
import json
from server import create_note, edit_note, set_note_privacy

def test_create_note():
    """测试创建笔记"""
    print("=== 测试创建笔记 ===")
    
    title = "MCP测试笔记"
    content = """这是一个测试笔记

第一段：普通文本

第二段：包含**加粗文本**和==高亮文本==

第三段：更多**加粗**的内容"""
    
    result = create_note(title, content, is_private=True)
    result_dict = json.loads(result)
    
    print(f"结果: {json.dumps(result_dict, ensure_ascii=False, indent=2)}")
    
    if result_dict.get("success"):
        print("✅ 创建笔记成功")
        return result_dict.get("note_id")
    else:
        print("❌ 创建笔记失败")
        return None

def test_edit_note(note_id: str):
    """测试编辑笔记"""
    print("\n=== 测试编辑笔记 ===")
    
    if not note_id:
        print("❌ 没有note_id，跳过编辑测试")
        return False
    
    new_content = """这是编辑后的内容

已更新：==这是新增的高亮内容==

**重要更新**：笔记已编辑"""
    
    result = edit_note(note_id, new_content)
    result_dict = json.loads(result)
    
    print(f"结果: {json.dumps(result_dict, ensure_ascii=False, indent=2)}")
    
    if result_dict.get("success"):
        print("✅ 编辑笔记成功")
        return True
    else:
        print("❌ 编辑笔记失败")
        return False

def test_set_privacy(note_id: str):
    """测试设置笔记隐私"""
    print("\n=== 测试设置笔记隐私 ===")
    
    if not note_id:
        print("❌ 没有note_id，跳过隐私设置测试")
        return False
    
    # 测试设置为公开
    result = set_note_privacy(note_id, "public")
    result_dict = json.loads(result)
    
    print(f"设置为公开: {json.dumps(result_dict, ensure_ascii=False, indent=2)}")
    
    if result_dict.get("success"):
        print("✅ 设置隐私成功")
        
        # 再设置回隐私
        result2 = set_note_privacy(note_id, "private")
        result2_dict = json.loads(result2)
        print(f"设置为隐私: {json.dumps(result2_dict, ensure_ascii=False, indent=2)}")
        
        return True
    else:
        print("❌ 设置隐私失败")
        return False

if __name__ == "__main__":
    print("开始测试墨问笔记MCP工具\n")
    
    # 测试创建
    note_id = test_create_note()
    
    # 如果创建成功，测试编辑和设置
    if note_id:
        test_edit_note(note_id)
        test_set_privacy(note_id)
        
        print(f"\n✅ 所有测试完成！笔记ID: {note_id}")
    else:
        print("\n❌ 测试失败：无法创建笔记")

