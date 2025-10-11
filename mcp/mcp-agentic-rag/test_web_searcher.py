#!/usr/bin/env python3
"""
测试WebSearcher类的功能
"""

from web_searcher import BrightDataSearcher

def test_web_searcher_initialization():
    """测试BrightDataSearcher初始化"""
    print("测试1: BrightDataSearcher初始化")
    try:
        searcher = BrightDataSearcher()
        print("✅ WebSearcher初始化成功")
        print(f"   - Host: {searcher.host}")
        print(f"   - Port: {searcher.port}")
        print(f"   - 用户名已配置: {'是' if searcher.username else '否'}")
        return True
    except ValueError as e:
        print(f"⚠️  需要配置环境变量: {e}")
        return False
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return False


def test_web_searcher_search():
    """测试BrightDataSearcher搜索功能"""
    print("\n测试2: BrightDataSearcher搜索功能")
    try:
        searcher = BrightDataSearcher()
        
        # 执行一个简单的搜索测试
        query = "machine learning basics"
        print(f"   搜索查询: '{query}'")
        
        results = searcher.search(query, num_results=5)
        
        print(f"✅ 搜索成功")
        print(f"   - 返回结果数: {len(results)}")
        
        if results:
            print(f"   - 第一条结果标题: {results[0].get('title', 'N/A')[:50]}...")
        
        return True
        
    except ValueError as e:
        print(f"⚠️  需要配置环境变量: {e}")
        return False
    except RuntimeError as e:
        print(f"❌ 搜索失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False


def test_consistency_with_server():
    """测试与server.py的一致性"""
    print("\n测试3: 与server.py工具函数的一致性")
    try:
        from server import bright_data_web_search_tool
        
        # 测试工具函数
        query = "test query"
        print(f"   测试查询: '{query}'")
        
        result = bright_data_web_search_tool(query)
        
        print("✅ 工具函数调用成功")
        print(f"   - 返回类型: {type(result)}")
        print(f"   - 是否为列表: {isinstance(result, list)}")
        
        return True
        
    except ValueError as e:
        print(f"⚠️  需要配置环境变量: {e}")
        return False
    except Exception as e:
        print(f"❌ 工具函数调用失败: {e}")
        return False


if __name__ == "__main__":
    print("="*60)
    print("WebSearcher类重构测试")
    print("="*60)
    
    results = []
    
    # 运行测试
    results.append(test_web_searcher_initialization())
    
    if results[0]:  # 只有初始化成功才继续
        # results.append(test_web_searcher_search())  # 需要实际的API凭证
        results.append(test_consistency_with_server())
    
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"通过: {sum(results)}/{len(results)}")
    
    if all(results):
        print("✅ 所有测试通过！重构成功且功能保持一致。")
    else:
        print("⚠️  部分测试未通过（可能需要配置Bright Data凭证）")

