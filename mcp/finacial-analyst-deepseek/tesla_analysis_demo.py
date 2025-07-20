#!/usr/bin/env python3
"""
Tesla Stock Analysis Demo - Last 3 Months
Using simulated data for demonstration
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_simulated_tesla_data():
    """创建模拟的Tesla股票数据"""
    # 生成过去3个月的日期
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 模拟Tesla股票价格数据（基于真实趋势）
    np.random.seed(42)  # 确保结果可重现
    
    # 起始价格（模拟Tesla当前价格范围）
    start_price = 180.0
    
    # 生成价格序列（包含趋势和波动）
    returns = np.random.normal(0.001, 0.03, len(dates))  # 日收益率
    prices = [start_price]
    
    for i in range(1, len(dates)):
        # 添加一些趋势（模拟Tesla的波动性）
        trend = 0.0005 if i < len(dates)//2 else -0.0003
        new_price = prices[-1] * (1 + returns[i] + trend)
        prices.append(max(new_price, 50))  # 确保价格不会太低
    
    # 生成交易量数据
    base_volume = 50000000  # 基础交易量
    volumes = np.random.lognormal(17, 0.5, len(dates)) * base_volume
    
    # 创建DataFrame
    df = pd.DataFrame({
        'Open': prices,
        'High': [p * (1 + abs(np.random.normal(0, 0.02))) for p in prices],
        'Low': [p * (1 - abs(np.random.normal(0, 0.02))) for p in prices],
        'Close': prices,
        'Volume': volumes
    }, index=dates)
    
    # 调整High和Low确保逻辑正确
    df['High'] = df[['Open', 'Close']].max(axis=1) * (1 + abs(np.random.normal(0, 0.01)))
    df['Low'] = df[['Open', 'Close']].min(axis=1) * (1 - abs(np.random.normal(0, 0.01)))
    
    return df

def analyze_tesla_performance_demo():
    """分析Tesla股票表现（演示版本）"""
    print("正在获取Tesla (TSLA) 的股票数据 (3个月)...")
    print("注意：这是演示数据，用于展示分析功能")
    
    # 获取模拟数据
    hist = create_simulated_tesla_data()
    
    # 基本信息
    print(f"\n=== TSLA 股票分析报告（演示数据）===")
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
    fig.suptitle('Tesla (TSLA) 股票分析 - 过去3个月（演示数据）', fontsize=16, fontweight='bold')
    
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
    result = analyze_tesla_performance_demo()
    print(f"\n分析完成！")
    print(f"\n=== 总结 ===")
    print(f"Tesla在过去3个月中表现{'积极' if result['price_change_pct'] > 0 else '消极'}")
    print(f"价格变化: {result['price_change_pct']:+.2f}%")
    print(f"年化波动率: {result['volatility']:.2%}")
    print(f"当前价格: ${result['current_price']:.2f}") 