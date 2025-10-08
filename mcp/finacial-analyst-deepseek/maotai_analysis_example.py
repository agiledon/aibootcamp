#!/usr/bin/env python3
"""
贵州茅台股票分析示例
使用 akshare 库获取中国A股数据
"""

import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STHeiti', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def analyze_cn_stock(stock_code='600519', stock_name='贵州茅台', days=365):
    """
    分析中国A股股票表现
    
    Args:
        stock_code: 股票代码（6位数字）
        stock_name: 股票名称
        days: 分析天数
    """
    print(f"正在获取 {stock_name}({stock_code}) 的股票数据...")
    print(f"时间范围: 最近{days}天\n")
    
    try:
        # 使用 akshare 获取股票历史数据
        # period="daily" 表示日K线数据
        # adjust="qfq" 表示前复权
        df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", adjust="qfq")
        
        if df.empty:
            print(f"无法获取 {stock_name} 的数据")
            return
        
        # 只保留最近N天的数据
        df = df.tail(days)
        
        # 转换日期列为datetime格式
        df['日期'] = pd.to_datetime(df['日期'])
        df = df.set_index('日期')
        
        print(f"=== {stock_name}({stock_code}) 股票分析报告 ===")
        print(f"数据点数量: {len(df)}")
        print(f"开始日期: {df.index[0].strftime('%Y-%m-%d')}")
        print(f"结束日期: {df.index[-1].strftime('%Y-%m-%d')}")
        
        # 价格统计
        current_price = float(df['收盘'].iloc[-1])
        start_price = float(df['收盘'].iloc[0])
        highest_price = float(df['最高'].max())
        lowest_price = float(df['最低'].min())
        price_change = current_price - start_price
        price_change_pct = (price_change / start_price) * 100
        
        print(f"\n=== 价格表现 ===")
        print(f"起始价格: ¥{start_price:.2f}")
        print(f"当前价格: ¥{current_price:.2f}")
        print(f"最高价格: ¥{highest_price:.2f}")
        print(f"最低价格: ¥{lowest_price:.2f}")
        print(f"价格变化: ¥{price_change:.2f} ({price_change_pct:+.2f}%)")
        
        # 成交量和成交额统计
        avg_volume = df['成交量'].mean()
        max_volume = df['成交量'].max()
        total_amount = df['成交额'].sum()
        
        print(f"\n=== 交易统计 ===")
        print(f"平均成交量: {avg_volume:,.0f} 手")
        print(f"最大成交量: {max_volume:,.0f} 手")
        print(f"累计成交额: ¥{total_amount/100000000:.2f} 亿元")
        
        # 计算日收益率
        df['日收益率'] = df['收盘'].pct_change()
        daily_returns = df['日收益率'].dropna()
        
        # 波动性分析
        volatility_daily = daily_returns.std()
        volatility_annual = volatility_daily * np.sqrt(252)  # 年化波动率
        
        print(f"\n=== 波动性分析 ===")
        print(f"日收益率标准差: {volatility_daily:.4f}")
        print(f"年化波动率: {volatility_annual:.2%}")
        print(f"最大单日涨幅: {daily_returns.max():.2%}")
        print(f"最大单日跌幅: {daily_returns.min():.2%}")
        
        # 计算累计收益率
        df['累计收益率'] = (1 + df['日收益率']).cumprod() - 1
        total_return = df['累计收益率'].iloc[-1] * 100
        
        print(f"累计收益率: {total_return:+.2f}%")
        
        # 创建可视化图表
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'{stock_name}({stock_code}) 股票分析 - 最近{days}天', 
                     fontsize=18, fontweight='bold')
        
        # 1. 价格走势图
        axes[0, 0].plot(df.index, df['收盘'], linewidth=2.5, color='#1f77b4', label='收盘价')
        axes[0, 0].fill_between(df.index, df['最低'], df['最高'], 
                                alpha=0.2, color='#1f77b4', label='日内波动范围')
        axes[0, 0].set_title('股票价格走势', fontweight='bold', fontsize=14)
        axes[0, 0].set_ylabel('价格 (¥)', fontsize=12)
        axes[0, 0].legend(loc='best')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. 成交量图
        colors = ['#2ca02c' if x > avg_volume else '#d62728' for x in df['成交量']]
        axes[0, 1].bar(df.index, df['成交量'], alpha=0.7, color=colors, width=1)
        axes[0, 1].axhline(y=avg_volume, color='black', linestyle='--', 
                          linewidth=2, label=f'平均成交量: {avg_volume:,.0f}')
        axes[0, 1].set_title('成交量', fontweight='bold', fontsize=14)
        axes[0, 1].set_ylabel('成交量 (手)', fontsize=12)
        axes[0, 1].legend(loc='best')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. 日收益率分布
        axes[1, 0].hist(daily_returns * 100, bins=40, alpha=0.7, 
                       color='#ff7f0e', edgecolor='black')
        axes[1, 0].axvline(x=0, color='red', linestyle='--', linewidth=2)
        axes[1, 0].axvline(x=daily_returns.mean() * 100, color='green', 
                          linestyle='--', linewidth=2, label=f'均值: {daily_returns.mean()*100:.2f}%')
        axes[1, 0].set_title('日收益率分布', fontweight='bold', fontsize=14)
        axes[1, 0].set_xlabel('日收益率 (%)', fontsize=12)
        axes[1, 0].set_ylabel('频次', fontsize=12)
        axes[1, 0].legend(loc='best')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. 累计收益率
        axes[1, 1].plot(df.index, df['累计收益率'] * 100, linewidth=2.5, color='#9467bd')
        axes[1, 1].fill_between(df.index, 0, df['累计收益率'] * 100, 
                               alpha=0.3, color='#9467bd')
        axes[1, 1].set_title('累计收益率', fontweight='bold', fontsize=14)
        axes[1, 1].set_ylabel('累计收益率 (%)', fontsize=12)
        axes[1, 1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # 保存图表
        filename = f'{stock_code}_{stock_name}_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n📊 图表已保存至: {filename}")
        
        plt.show()
        
        print(f"\n" + "="*70)
        print("关键指标总结")
        print("="*70)
        print(f"股票名称: {stock_name}")
        print(f"股票代码: {stock_code}")
        print(f"分析周期: {days}天")
        print(f"起始价格: ¥{start_price:.2f}")
        print(f"当前价格: ¥{current_price:.2f}")
        print(f"价格变化: {price_change_pct:+.2f}%")
        print(f"最高价: ¥{highest_price:.2f}")
        print(f"最低价: ¥{lowest_price:.2f}")
        print(f"年化波动率: {volatility_annual:.2%}")
        print(f"总收益率: {total_return:+.2f}%")
        print(f"平均成交量: {avg_volume:,.0f} 手")
        print("="*70)
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        print("请检查：")
        print("1. 网络连接是否正常")
        print("2. 股票代码是否正确")
        print("3. akshare库是否正确安装")

if __name__ == "__main__":
    # 分析贵州茅台过去一年的表现
    analyze_cn_stock(stock_code='600519', stock_name='贵州茅台', days=365)

