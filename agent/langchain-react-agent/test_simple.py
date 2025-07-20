#!/usr/bin/env python3
"""
简单测试脚本
"""

import re

# 测试数学计算器
def test_calculator():
    """测试数学计算器"""
    def math_calculator(expression: str) -> str:
        try:
            clean_expr = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            clean_expr = clean_expr.strip()
            
            if not clean_expr:
                return "Error: No valid expression found"
            
            result = eval(clean_expr)
            return f"The result is: {result}"
            
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    print("=== 测试数学计算器 ===")
    test_cases = [
        "100 * 0.85",
        "2 + 2",
        "10 / 2",
        "invalid expression"
    ]
    
    for test in test_cases:
        result = math_calculator(test)
        print(f"Input: {test} -> {result}")

# 测试搜索工具
def test_search():
    """测试搜索工具"""
    def web_search(query: str) -> str:
        try:
            from ddgs import DDGS
            
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if results:
                    search_text = " ".join([result.get('body', '') for result in results])
                    return f"Search results: {search_text[:200]}..."
                else:
                    return "No search results found"
        except Exception as e:
            return f"Search error: {str(e)}"
    
    print("\n=== 测试搜索工具 ===")
    test_query = "MacBook Pro price"
    result = web_search(test_query)
    print(f"Query: {test_query}")
    print(f"Result: {result}")

if __name__ == "__main__":
    test_calculator()
    test_search() 