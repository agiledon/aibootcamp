#!/usr/bin/env python3
"""
简单测试ddgs库的基本功能
"""


def test_ddgs_import():
    """测试ddgs导入"""
    print("测试1: ddgs包导入")
    try:
        from ddgs import DDGS
        print("✅ ddgs包导入成功")
        return True
    except ImportError as e:
        print(f"❌ ddgs包导入失败: {e}")
        return False


def test_ddgs_basic_search():
    """测试基本搜索功能"""
    print("\n测试2: 基本搜索功能")
    try:
        from ddgs import DDGS
        
        # 尝试简单搜索
        query = "python"
        print(f"搜索查询: '{query}'")
        
        ddgs = DDGS()
        results = ddgs.text(query, max_results=2)
        
        result_list = list(results)
        
        if result_list:
            print(f"✅ 搜索成功，返回{len(result_list)}条结果")
            print(f"\n第一条结果:")
            print(f"  标题: {result_list[0].get('title', 'N/A')}")
            print(f"  URL: {result_list[0].get('href', 'N/A')[:60]}")
            return True
        else:
            print("⚠️  搜索返回空结果")
            return False
            
    except Exception as e:
        print(f"❌ 搜索失败: {e}")
        return False


def test_classes_import():
    """测试搜索器类导入"""
    print("\n测试3: 搜索器类导入")
    try:
        from mcp_agentic_rag import WebSearcher, BrightDataSearcher, DuckDuckGoSearcher, BingSearcher
        print("✅ 所有搜索器类导入成功")
        print("  - WebSearcher (抽象基类)")
        print("  - BrightDataSearcher")
        print("  - DuckDuckGoSearcher")
        print("  - BingSearcher")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False


def test_duckduckgo_searcher_instance():
    """测试DuckDuckGoSearcher实例化"""
    print("\n测试4: DuckDuckGoSearcher实例化")
    try:
        from mcp_agentic_rag import DuckDuckGoSearcher
        
        searcher = DuckDuckGoSearcher(region='wt-wt', max_results=3)
        print("✅ DuckDuckGoSearcher实例化成功")
        print(f"   - 类型: {type(searcher).__name__}")
        print(f"   - 区域: {searcher.region}")
        print(f"   - 最大结果: {searcher.max_results}")
        return True
    except Exception as e:
        print(f"❌ 实例化失败: {e}")
        return False


if __name__ == "__main__":
    print("="*70)
    print("DDGS库基本功能测试")
    print("="*70)
    print()
    
    results = []
    results.append(test_ddgs_import())
    results.append(test_ddgs_basic_search())
    results.append(test_classes_import())
    results.append(test_duckduckgo_searcher_instance())
    
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("✅ 所有基本功能测试通过！")
    else:
        print(f"⚠️  {total - passed}项测试失败")

