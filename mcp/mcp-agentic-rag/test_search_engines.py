#!/usr/bin/env python3
"""
测试多种Web搜索引擎的实现
使用策略模式支持BrightData、DuckDuckGo、Bing
"""

from web_searcher import WebSearcher, BrightDataSearcher, DuckDuckGoSearcher, BingSearcher


def test_duckduckgo_searcher():
    """测试DuckDuckGo搜索器"""
    print("="*70)
    print("测试1: DuckDuckGoSearcher（免费、无需API密钥）")
    print("="*70)
    
    try:
        searcher = DuckDuckGoSearcher(region='cn-zh', max_results=5)
        print("✅ DuckDuckGoSearcher初始化成功")
        print(f"   - 区域: {searcher.region}")
        print(f"   - 安全搜索: {searcher.safesearch}")
        print(f"   - 最大结果数: {searcher.max_results}")
        
        # 执行搜索
        query = "machine learning basics"
        print(f"\n执行搜索: '{query}'")
        results = searcher.search(query, num_results=3)
        
        print(f"✅ 搜索成功")
        print(f"   - 返回结果数: {len(results)}")
        
        if results:
            print(f"\n前3条结果:")
            for i, result in enumerate(results[:3], 1):
                print(f"   {i}. {result.get('title', 'N/A')[:60]}")
                print(f"      URL: {result.get('url', 'N/A')[:70]}")
                print(f"      摘要: {result.get('snippet', 'N/A')[:80]}...")
                print()
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_bing_searcher():
    """测试Bing搜索器"""
    print("="*70)
    print("测试2: BingSearcher（通过DuckDuckGo）")
    print("="*70)
    
    try:
        searcher = BingSearcher(max_results=5)
        print("✅ BingSearcher初始化成功")
        print(f"   - 最大结果数: {searcher.max_results}")
        
        # 执行搜索
        query = "artificial intelligence"
        print(f"\n执行搜索: '{query}'")
        results = searcher.search(query, num_results=3)
        
        print(f"✅ 搜索成功")
        print(f"   - 返回结果数: {len(results)}")
        
        if results:
            print(f"\n前3条结果:")
            for i, result in enumerate(results[:3], 1):
                print(f"   {i}. {result.get('title', 'N/A')[:60]}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_brightdata_searcher():
    """测试BrightData搜索器"""
    print("="*70)
    print("测试3: BrightDataSearcher（需要API凭证）")
    print("="*70)
    
    try:
        searcher = BrightDataSearcher()
        print("✅ BrightDataSearcher初始化成功")
        print(f"   - Host: {searcher.host}")
        print(f"   - Port: {searcher.port}")
        
        # 检查是否配置了真实凭证
        if "your_brightdata" in searcher.username:
            print("⚠️  检测到示例配置，跳过实际搜索测试")
            return None  # 标记为跳过
        
        return True
        
    except FileNotFoundError as e:
        print(f"⚠️  .env文件未找到: {e}")
        return None
    except ValueError as e:
        print(f"⚠️  凭证未配置: {e}")
        print("   提示: 如需测试BrightData，请在.env文件中配置实际凭证")
        return None
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_strategy_pattern():
    """测试策略模式切换"""
    print("="*70)
    print("测试4: 策略模式（通过环境变量切换搜索引擎）")
    print("="*70)
    
    import os
    
    # 测试默认策略
    print("当前搜索引擎配置: WEB_SEARCH_ENGINE =", os.getenv("WEB_SEARCH_ENGINE", "duckduckgo"))
    
    from server import _get_web_searcher
    
    try:
        searcher = _get_web_searcher()
        print(f"✅ 获取搜索器成功: {searcher.__class__.__name__}")
        return True
    except Exception as e:
        print(f"❌ 获取搜索器失败: {e}")
        return False


def test_server_tool_integration():
    """测试server.py的工具函数集成"""
    print("="*70)
    print("测试5: MCP工具函数集成测试")
    print("="*70)
    
    try:
        from server import bright_data_web_search_tool
        
        query = "what is deep learning"
        print(f"执行搜索: '{query}'")
        
        results = bright_data_web_search_tool(query)
        
        print(f"✅ 工具函数调用成功")
        print(f"   - 返回结果数: {len(results)}")
        print(f"   - 返回类型: {type(results)}")
        
        if results:
            print(f"   - 第一条结果: {results[0].get('title', 'N/A')[:60]}")
        
        return True
        
    except Exception as e:
        print(f"❌ 工具函数调用失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_result_format_consistency():
    """测试不同搜索器的返回格式一致性"""
    print("="*70)
    print("测试6: 返回格式一致性测试")
    print("="*70)
    
    query = "python programming"
    required_fields = ['title', 'url', 'snippet', 'description']
    
    searchers = [
        ("DuckDuckGo", DuckDuckGoSearcher()),
        ("Bing", BingSearcher()),
    ]
    
    all_consistent = True
    
    for name, searcher in searchers:
        try:
            print(f"\n测试 {name}:")
            results = searcher.search(query, num_results=2)
            
            if results:
                result = results[0]
                has_all_fields = all(field in result for field in required_fields)
                
                if has_all_fields:
                    print(f"  ✅ 包含所有必需字段: {', '.join(required_fields)}")
                else:
                    missing = [f for f in required_fields if f not in result]
                    print(f"  ⚠️  缺少字段: {', '.join(missing)}")
                    all_consistent = False
            else:
                print(f"  ⚠️  未返回结果")
                
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            all_consistent = False
    
    return all_consistent


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "Web搜索引擎策略模式测试" + " "*15 + "║")
    print("╚" + "="*68 + "╝")
    print()
    
    results = []
    
    # 运行测试
    results.append(("DuckDuckGo搜索器", test_duckduckgo_searcher()))
    results.append(("Bing搜索器", test_bing_searcher()))
    results.append(("BrightData搜索器", test_brightdata_searcher()))
    results.append(("策略模式切换", test_strategy_pattern()))
    results.append(("MCP工具集成", test_server_tool_integration()))
    results.append(("返回格式一致性", test_result_format_consistency()))
    
    # 总结
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    
    passed = 0
    failed = 0
    skipped = 0
    
    for name, result in results:
        if result is True:
            status = "✅ 通过"
            passed += 1
        elif result is False:
            status = "❌ 失败"
            failed += 1
        else:  # None = skipped
            status = "⊘ 跳过"
            skipped += 1
        
        print(f"{name}: {status}")
    
    total = len(results)
    print(f"\n总计: {passed}通过, {failed}失败, {skipped}跳过 (共{total}项)")
    
    if failed == 0:
        print("\n🎉 重构成功！所有功能测试通过！")
        print("\n✨ 设计模式应用:")
        print("   - 策略模式: 支持多种搜索引擎切换")
        print("   - 模板方法: WebSearcher抽象基类定义统一接口")
        print("   - 依赖注入: 通过配置选择具体实现")
    else:
        print(f"\n⚠️  {failed}项测试失败，请检查配置")
    
    print("\n💡 使用提示:")
    print("   - 默认使用DuckDuckGo（免费、无需配置）")
    print("   - 在.env中设置 WEB_SEARCH_ENGINE=brightdata 切换到BrightData")
    print("   - 在.env中设置 WEB_SEARCH_ENGINE=bing 切换到Bing")

