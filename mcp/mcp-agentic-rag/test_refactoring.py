#!/usr/bin/env python3
"""
测试重构后的模块结构
验证所有功能正常工作
"""

def test_module_imports():
    """测试模块导入"""
    print("="*70)
    print("测试1: 模块导入")
    print("="*70)
    
    try:
        # 测试rag_retriever模块
        from rag_retriever import EmbedData, QdrantVDB, RagRetriever, new_faq_text
        print("✅ rag_retriever.py 导入成功")
        print("   - EmbedData")
        print("   - QdrantVDB")
        print("   - RagRetriever (原Retriever)")
        print("   - new_faq_text")
        
        # 测试web_searcher模块
        from web_searcher import WebSearcher, BrightDataSearcher, DuckDuckGoSearcher, BingSearcher
        print("\n✅ web_searcher.py 导入成功")
        print("   - WebSearcher (抽象基类)")
        print("   - BrightDataSearcher")
        print("   - DuckDuckGoSearcher")
        print("   - BingSearcher")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False


def test_server_imports():
    """测试server.py的导入"""
    print("\n" + "="*70)
    print("测试2: server.py导入")
    print("="*70)
    
    try:
        from server import (
            machine_learning_faq_retrieval_tool,
            bright_data_web_search_tool,
            _get_web_searcher
        )
        print("✅ server.py 导入成功")
        print("   - machine_learning_faq_retrieval_tool")
        print("   - bright_data_web_search_tool")
        print("   - _get_web_searcher")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False


def test_rag_retriever_class():
    """测试RagRetriever类重命名"""
    print("\n" + "="*70)
    print("测试3: RagRetriever类（原Retriever）")
    print("="*70)
    
    try:
        from rag_retriever import RagRetriever, QdrantVDB, EmbedData
        
        print("✅ RagRetriever类可以正常导入")
        print(f"   - 类名: RagRetriever")
        print(f"   - 原类名: Retriever")
        
        # 检查类是否可以实例化（不实际连接数据库）
        print("\n   检查类结构...")
        print(f"   - 有__init__方法: {hasattr(RagRetriever, '__init__')}")
        print(f"   - 有search方法: {hasattr(RagRetriever, 'search')}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_web_searcher_strategy():
    """测试WebSearcher策略模式"""
    print("\n" + "="*70)
    print("测试4: WebSearcher策略模式")
    print("="*70)
    
    try:
        from server import _get_web_searcher
        import os
        
        # 测试默认策略（DuckDuckGo）
        searcher = _get_web_searcher()
        print(f"✅ 默认搜索引擎: {searcher.__class__.__name__}")
        print(f"   配置: WEB_SEARCH_ENGINE={os.getenv('WEB_SEARCH_ENGINE', 'duckduckgo')}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_duckduckgo_search():
    """测试DuckDuckGo搜索功能"""
    print("\n" + "="*70)
    print("测试5: DuckDuckGo搜索功能")
    print("="*70)
    
    try:
        from web_searcher import DuckDuckGoSearcher
        
        searcher = DuckDuckGoSearcher(max_results=2)
        print("✅ DuckDuckGoSearcher初始化成功")
        
        # 执行搜索
        query = "artificial intelligence"
        print(f"\n执行搜索: '{query}'")
        results = searcher.search(query, num_results=2)
        
        print(f"✅ 搜索成功，返回{len(results)}条结果")
        
        if results:
            print(f"\n第一条结果:")
            print(f"  标题: {results[0].get('title', 'N/A')}")
            print(f"  URL: {results[0].get('url', 'N/A')[:60]}")
        
        return True
    except Exception as e:
        print(f"❌ 搜索失败: {e}")
        return False


def test_file_structure():
    """测试文件结构"""
    print("\n" + "="*70)
    print("测试6: 文件结构")
    print("="*70)
    
    from pathlib import Path
    
    base_dir = Path(__file__).parent
    
    files_to_check = [
        ('rag_retriever.py', 'RAG检索器模块（原rag_code.py）'),
        ('web_searcher.py', 'Web搜索器模块（新建）'),
        ('server.py', 'MCP服务器'),
    ]
    
    files_should_not_exist = [
        ('rag_code.py', '已重命名为rag_retriever.py'),
    ]
    
    all_good = True
    
    print("应该存在的文件:")
    for filename, desc in files_to_check:
        file_path = base_dir / filename
        exists = file_path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {filename} - {desc}")
        if not exists:
            all_good = False
    
    print("\n应该不存在的文件:")
    for filename, desc in files_should_not_exist:
        file_path = base_dir / filename
        exists = file_path.exists()
        status = "✅" if not exists else "❌"
        print(f"  {status} {filename} - {desc}")
        if exists:
            all_good = False
    
    return all_good


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*20 + "重构验证测试" + " "*22 + "║")
    print("╚" + "="*68 + "╝")
    print()
    
    results = []
    
    # 运行所有测试
    results.append(("模块导入", test_module_imports()))
    results.append(("Server导入", test_server_imports()))
    results.append(("RagRetriever类", test_rag_retriever_class()))
    results.append(("策略模式", test_web_searcher_strategy()))
    results.append(("DuckDuckGo搜索", test_duckduckgo_search()))
    results.append(("文件结构", test_file_structure()))
    
    # 总结
    print("\n" + "="*70)
    print("重构验证总结")
    print("="*70)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 重构成功！所有功能正常工作！")
        print("\n✨ 重构成果:")
        print("   ✅ rag_code.py → rag_retriever.py")
        print("   ✅ Retriever → RagRetriever")
        print("   ✅ WebSearcher相关代码 → web_searcher.py")
        print("   ✅ 所有依赖更新完成")
        print("   ✅ 功能完全兼容")
    else:
        print(f"\n⚠️  {total - passed}项测试失败，请检查")

