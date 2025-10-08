# 中国A股分析指南 / Chinese A-Share Stock Analysis Guide

## 支持的股票代码 / Supported Stock Codes

### 常见A股股票 / Common A-Share Stocks

| 股票名称 | 股票代码 | 市场 | 行业 |
|---------|---------|------|------|
| 贵州茅台 | 600519 | 沪市 | 白酒 |
| 工商银行 | 601398 | 沪市 | 银行 |
| 招商银行 | 600036 | 沪市 | 银行 |
| 中国平安 | 601318 | 沪市 | 保险 |
| 五粮液   | 000858 | 深市 | 白酒 |
| 平安银行 | 000001 | 深市 | 银行 |
| 比亚迪   | 002594 | 深市 | 新能源汽车 |
| 宁德时代 | 300750 | 深市创业板 | 新能源电池 |
| 中国石油 | 601857 | 沪市 | 能源 |
| 中国移动 | 600941 | 沪市 | 通信 |

### 市场代码规则 / Market Code Rules

- **沪市主板**: 600xxx, 601xxx, 603xxx, 605xxx
- **深市主板**: 000xxx
- **中小板**: 002xxx
- **创业板**: 300xxx
- **科创板**: 688xxx

## 使用 akshare 的示例查询 / Example Queries with akshare

### English Queries

```
Analyze Kweichow Moutai (600519) stock performance over the past year
Show Industrial and Commercial Bank of China (601398) stock trend for the last 6 months
Compare China Merchants Bank (600036) and Ping An Bank (000001) performance
Analyze BYD (002594) trading volume changes over the past 3 months
```

### 中文查询

```
分析贵州茅台过去一年的股票表现
显示工商银行最近6个月的股价走势
对比招商银行和平安银行的表现
分析比亚迪过去3个月的交易量变化
```

## akshare 关键函数 / Key akshare Functions

### 获取股票历史数据 / Get Stock Historical Data

```python
import akshare as ak

# 获取日K线数据
df = ak.stock_zh_a_hist(
    symbol="600519",      # 股票代码
    period="daily",       # daily/weekly/monthly
    start_date="20240101",  # 开始日期（可选）
    end_date="20241231",    # 结束日期（可选）
    adjust="qfq"          # 复权方式：qfq(前复权), hfq(后复权), ""(不复权)
)
```

### 数据字段说明 / Data Fields

| 字段名 | 说明 | English |
|--------|------|---------|
| 日期 | 交易日期 | Date |
| 开盘 | 开盘价 | Open |
| 收盘 | 收盘价 | Close |
| 最高 | 最高价 | High |
| 最低 | 最低价 | Low |
| 成交量 | 成交量（手） | Volume (lots) |
| 成交额 | 成交额（元） | Turnover (CNY) |
| 振幅 | 振幅（%） | Amplitude |
| 涨跌幅 | 涨跌幅（%） | Change % |
| 涨跌额 | 涨跌额（元） | Change Amount |
| 换手率 | 换手率（%） | Turnover Rate |

## 示例代码 / Example Code

### 简单分析 / Simple Analysis

```python
import akshare as ak
import pandas as pd

# 获取贵州茅台最近一年数据
df = ak.stock_zh_a_hist(symbol="600519", period="daily", adjust="qfq")
df = df.tail(365)

print(f"当前价格: {df['收盘'].iloc[-1]}")
print(f"一年涨跌幅: {((df['收盘'].iloc[-1] / df['收盘'].iloc[0]) - 1) * 100:.2f}%")
```

### 完整分析示例 / Complete Analysis

参考项目中的 `maotai_analysis_example.py` 文件。

## 运行示例 / Run Examples

```bash
# 分析贵州茅台
uv run maotai_analysis_example.py

# 使用 CrewAI 分析（修改查询内容）
uv run finance_crew.py
```

## 注意事项 / Notes

1. **网络要求**: akshare 需要网络连接获取数据
2. **数据延迟**: 数据可能有15-20分钟延迟
3. **交易日**: 只返回交易日数据，节假日无数据
4. **复权处理**: 推荐使用前复权(qfq)以获得真实收益率

## 常见问题 / FAQ

**Q: 如何查找股票代码？**
A: 可以使用 `ak.stock_zh_a_spot_em()` 获取所有A股实时数据，包含代码和名称。

**Q: 数据获取失败怎么办？**
A: 检查网络连接，确认股票代码正确，重试即可。

**Q: 支持哪些时间范围？**
A: akshare 支持获取全部历史数据，可以通过 `start_date` 和 `end_date` 参数指定，或使用 `.tail(n)` 获取最近n天。

## 参考资源 / References

- [akshare 官方文档](https://akshare.akfamily.xyz/)
- [akshare GitHub](https://github.com/akfamily/akshare)
- [沪深交易所](http://www.sse.com.cn/)

