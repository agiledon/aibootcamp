#!/usr/bin/env python3
"""
简单的akshare测试脚本
用于验证akshare库是否正常工作
"""

import akshare as ak
from datetime import datetime

def test_akshare():
    """测试akshare基本功能"""
    print("="*60)
    print("测试 akshare 库功能")
    print("="*60)
    
    # 测试股票列表
    test_stocks = [
        ('600519', '贵州茅台'),
        ('601398', '工商银行'),
        ('600036', '招商银行'),
        ('002594', '比亚迪'),
        ('300750', '宁德时代'),
    ]
    
    for code, name in test_stocks:
        print(f"\n测试股票: {name}({code})")
        try:
            # 获取最近5天的数据
            df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
            if not df.empty:
                df = df.tail(5)
                latest_price = float(df['收盘'].iloc[-1])
                print(f"  ✅ 成功获取数据")
                print(f"  📈 最新收盘价: ¥{latest_price:.2f}")
                print(f"  📅 最新日期: {df['日期'].iloc[-1]}")
            else:
                print(f"  ⚠️ 数据为空")
        except Exception as e:
            print(f"  ❌ 错误: {str(e)}")
    
    print("\n" + "="*60)
    print("测试完成！")
    print("="*60)
    
    # 测试总结
    print("\n如果所有股票都显示 ✅，说明 akshare 工作正常！")
    print("现在可以运行:")
    print("  - uv run maotai_analysis_example.py  (完整分析)")
    print("  - uv run finance_crew.py             (使用CrewAI)")

if __name__ == "__main__":
    test_akshare()

