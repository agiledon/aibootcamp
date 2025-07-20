#!/usr/bin/env python3
"""
Tesla Stock Analysis - Last 3 Months
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def analyze_tesla_performance():
    """分析Tesla股票表现"""
    print("正在获取Tesla (TSLA) 的股票数据 (3个月)...")
    
    # 获取股票数据
    stock = yf.Ticker('TSLA')
    hist = stock.history(period='3mo')
    
    if hist.empty:
        print("无法获取Tesla的数据")
        return
    
    # 基本信息
    print(f"\n=== TSLA 股票分析报告 ===")
    print(f"分析期间: 3个月")
    print(f"数据点数量: {len(hist)}")
    print(f"开始日期: {hist.index[0].strftime('%Y-%m-%d')}")
    print(f"结束日期: {hist.index[-1].strftime('%Y-%m-%d')}")
    
    # 价格统计
    current_price = hist['Close'].iloc[-1]
    start_price = hist['Close'].iloc[0]
    price_change = current_price - start_price
    price_change_pct = (price_change / start_price) * 100
    
    print(f"\n=== 价格表现 ===")
    print(f"起始价格: ${start_price:.2f}")
    print(f"当前价格: ${current_price:.2f}")
    print(f"价格变化: ${price_change:.2f} ({price_change_pct:+.2f}%)")
    
    # 交易量统计
    avg_volume = hist['Volume'].mean()
    max_volume = hist['Volume'].max()
    min_volume = hist['Volume'].min()
    
    print(f"\n=== 交易量统计 ===")
    print(f"平均交易量: {avg_volume:,.0f}")
    print(f"最大交易量: {max_volume:,.0f}")
    print(f"最小交易量: {min_volume:,.0f}")
    
    # 波动性分析
    daily_returns = hist['Close'].pct_change().dropna()
    volatility = daily_returns.std() * (252 ** 0.5)  # 年化波动率
    
    print(f"\n=== 波动性分析 ===")
    print(f"日收益率标准差: {daily_returns.std():.4f}")
    print(f"年化波动率: {volatility:.2%}")
    
    # 最高价和最低价
    max_price = hist['High'].max()
    min_price = hist['Low'].min()
    print(f"\n=== 价格区间 ===")
    print(f"期间最高价: ${max_price:.2f}")
    print(f"期间最低价: ${min_price:.2f}")
    print(f"价格区间: ${max_price - min_price:.2f}")
    
    # 创建可视化图表
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Tesla (TSLA) 股票分析 - 过去3个月', fontsize=16, fontweight='bold')
    
    # 1. 价格走势图
    axes[0, 0].plot(hist.index, hist['Close'], linewidth=2, color='#1f77b4')
    axes[0, 0].set_title('股票价格走势', fontweight='bold')
    axes[0, 0].set_ylabel('价格 ($)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. 交易量图
    axes[0, 1].bar(hist.index, hist['Volume'], alpha=0.7, color='#ff7f0e')
    axes[0, 1].set_title('交易量', fontweight='bold')
    axes[0, 1].set_ylabel('交易量')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. 日收益率分布
    axes[1, 0].hist(daily_returns, bins=30, alpha=0.7, color='#2ca02c', edgecolor='black')
    axes[1, 0].set_title('日收益率分布', fontweight='bold')
    axes[1, 0].set_xlabel('日收益率')
    axes[1, 0].set_ylabel('频次')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. 价格变化百分比
    price_pct_change = ((hist['Close'] - start_price) / start_price) * 100
    axes[1, 1].plot(hist.index, price_pct_change, linewidth=2, color='#d62728')
    axes[1, 1].set_title('累计价格变化 (%)', fontweight='bold')
    axes[1, 1].set_ylabel('变化百分比 (%)')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show()
    
    # 返回关键指标
    return {
        'symbol': 'TSLA',
        'period': '3mo',
        'current_price': current_price,
        'price_change': price_change,
        'price_change_pct': price_change_pct,
        'volatility': volatility,
        'avg_volume': avg_volume,
        'max_price': max_price,
        'min_price': min_price
    }

if __name__ == "__main__":
    # 执行分析
    result = analyze_tesla_performance()
    print(f"\n分析完成！") 