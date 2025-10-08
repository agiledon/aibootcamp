# 快速开始指南 - 中国A股分析

## 1. 环境准备

### 前置条件
- Python 3.12+
- uv 包管理工具
- Ollama (用于运行DeepSeek模型)

### 安装Ollama和模型
```bash
# 安装Ollama
# macOS
brew install ollama

# 启动Ollama服务
ollama serve

# 安装DeepSeek-R1模型
ollama pull deepseek-r1:7b
```

## 2. 项目设置

### 克隆并进入项目
```bash
cd /path/to/aibootcamp/mcp/finacial-analyst-deepseek
```

### 安装依赖
```bash
# uv会自动创建虚拟环境并安装所有依赖
uv sync
```

## 3. 快速测试

### 方式1: 运行示例代码（推荐首次使用）
```bash
# 分析贵州茅台
uv run maotai_analysis_example.py
```

**预期输出：**
- 控制台显示详细的股票分析数据
- 自动生成并保存可视化图表（PNG文件）
- 4个图表：价格走势、成交量、收益率分布、累计收益

### 方式2: 使用CrewAI进行分析
```bash
# 编辑 finance_crew.py 中的查询
# 将第142行的查询改为你想分析的股票
uv run finance_crew.py
```

### 方式3: 通过MCP服务（高级用法）
```bash
# 启动MCP服务器
uv run server.py

# 在另一个终端使用MCP客户端连接
# 或在Cursor中配置MCP工具
```

## 4. 常用股票代码

| 股票名称 | 代码 | 行业 |
|---------|------|------|
| 贵州茅台 | 600519 | 白酒 |
| 工商银行 | 601398 | 银行 |
| 招商银行 | 600036 | 银行 |
| 中国平安 | 601318 | 保险 |
| 五粮液   | 000858 | 白酒 |
| 平安银行 | 000001 | 银行 |
| 比亚迪   | 002594 | 新能源 |
| 宁德时代 | 300750 | 电池 |

## 5. 自定义分析

### 修改示例代码
编辑 `maotai_analysis_example.py` 最后一行：

```python
# 分析不同的股票
analyze_cn_stock(stock_code='601398', stock_name='工商银行', days=365)

# 分析不同的时间范围
analyze_cn_stock(stock_code='600519', stock_name='贵州茅台', days=180)  # 半年
analyze_cn_stock(stock_code='002594', stock_name='比亚迪', days=90)      # 3个月
```

### 使用CrewAI进行自定义查询
编辑 `finance_crew.py` 第142行：

```python
# 示例查询
result = crew.kickoff(inputs={"query": "分析比亚迪过去半年的股票表现"})
result = crew.kickoff(inputs={"query": "对比招商银行和工商银行过去一年的表现"})
result = crew.kickoff(inputs={"query": "显示宁德时代过去3个月的交易量变化"})
```

## 6. 生成的输出

### 控制台输出
```
=== 贵州茅台(600519) 股票分析报告 ===
数据点数量: 365
开始日期: 2024-04-03
结束日期: 2025-09-30

=== 价格表现 ===
起始价格: ¥1632.75
当前价格: ¥1443.99
价格变化: ¥-188.76 (-11.56%)
最高价格: ¥1858.52
最低价格: ¥1194.35

=== 交易统计 ===
平均成交量: 34,152 手
最大成交量: 194,709 手
累计成交额: ¥18887.69 亿元

=== 波动性分析 ===
日收益率标准差: 0.0161
年化波动率: 25.50%
最大单日涨幅: 9.65%
最大单日跌幅: -7.65%
累计收益率: -11.56%
```

### 图表文件
- 文件名格式：`{股票代码}_{股票名称}_analysis_{时间戳}.png`
- 示例：`600519_贵州茅台_analysis_20251008_222219.png`
- 包含4个子图：
  1. 股票价格走势（含日内波动范围）
  2. 成交量柱状图
  3. 日收益率分布
  4. 累计收益率曲线

## 7. 故障排查

### 问题1: 无法获取股票数据
```bash
# 检查网络连接
ping baidu.com

# 检查股票代码是否正确（必须是6位数字）
# 600519 ✓
# SH600519 ✗ (不要加前缀)
```

### 问题2: 中文字体显示问题
代码已包含多种中文字体设置：
```python
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STHeiti', 'Microsoft YaHei']
```
如果仍有问题，安装对应字体或使用系统已有字体。

### 问题3: DeepSeek模型未运行
```bash
# 检查Ollama是否运行
ollama list

# 如果没有deepseek-r1:7b模型
ollama pull deepseek-r1:7b

# 重启Ollama服务
ollama serve
```

### 问题4: uv命令不存在
```bash
# macOS安装
brew install uv

# 或使用pip
pip install uv
```

## 8. 进阶使用

### 在Cursor中配置MCP
1. 编辑 `~/.cursor/mcp.json`
2. 添加配置：
```json
{
  "mcpServers": {
    "financial-analyst": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/aibootcamp/mcp/finacial-analyst-deepseek",
        "run",
        "server.py"
      ]
    }
  }
}
```
3. 重启Cursor
4. 在对话中使用工具分析股票

### 批量分析多个股票
创建脚本 `batch_analysis.py`：
```python
from maotai_analysis_example import analyze_cn_stock

stocks = [
    ('600519', '贵州茅台'),
    ('601398', '工商银行'),
    ('600036', '招商银行'),
    ('002594', '比亚迪'),
]

for code, name in stocks:
    print(f"\n{'='*50}")
    print(f"正在分析 {name}({code})")
    print(f"{'='*50}\n")
    analyze_cn_stock(code, name, days=365)
```

运行：
```bash
uv run batch_analysis.py
```

## 9. 更多资源

- **完整文档**: [README.md](./README.md)
- **股票代码指南**: [CN_STOCK_GUIDE.md](./CN_STOCK_GUIDE.md)
- **更新日志**: [CHANGELOG_CN.md](./CHANGELOG_CN.md)
- **akshare文档**: https://akshare.akfamily.xyz/

## 10. 获取帮助

如遇问题：
1. 查看 [CN_STOCK_GUIDE.md](./CN_STOCK_GUIDE.md) 常见问题部分
2. 检查股票代码是否正确
3. 确认网络连接正常
4. 查看控制台错误信息

---

**祝您使用愉快！**

