# 🕵️ 每日侦察兵 · Daily Investigator

> 每日自动搜集接单市场情报 + 新物种发现 + 英文趋势
> Auto-collect freelance market intelligence, discover new platforms, and track global trends.

## 这是什么

一个轻量级的情报搜集工具，每天自动扫描 20 个关键词（中英文混合），输出一份结构化 Markdown 简报。帮你**打破信息茧房**，及时发现新的接单平台、技术趋势和市场机会。

Built for freelancers and solo developers who need to stay ahead of the market — without spending hours on research.

## 三层情报体系

| 层级 | 覆盖 | 关键词数量 | 目标 |
|------|------|:----------:|------|
| 📡 同行雷达 | 一品威客、程聚宝等已知平台 | 5 | 监控已有渠道的活跃度 |
| 🆕 新物种·中文 | AI 交易平台、Agent 接单等中文新词 | 5 | 发现国内新平台 |
| 🌐 新物种·英文 | AI marketplace, freelance platform 等英文趋势 | 5 | 发现全球新机会 |
| 📊 行业情报 | AI 融资、Product Hunt、自由职业趋势 | 5 | 把握行业方向 |

## 快速开始

```bash
# 安装依赖
pip install ddgs

# 运行（Windows）
PYTHONUTF8=1 python main.py

# 运行（macOS / Linux）
python main.py
```

输出文件：`output/YYYY-MM-DD.md`

## 配置

编辑 `main.py` 中的配置区：

```python
RESULTS_PER_QUERY = 5     # 每个关键词取多少条结果
OUTPUT_DIR = "output"      # 输出目录
```

关键词分类在 `SEARCH_CATEGORIES` 字典中，可按需增删。

## 输出示例

```
# 每日侦察简报 V2 · 2026-06-16

**扫描概况：** 20 个关键词 · 100 条结果

## 🔍 已知平台监控

### 📡 一品威客 Python脚本 自动化 接单
1. **[标题](链接)**
   摘要内容...

## 🆕 新物种发现 · 英文

### 📡 AI marketplace platform launch 2026
...
```

## 技术栈

- Python 3.8+
- [ddgs](https://pypi.org/project/ddgs/) (DuckDuckGo Search)
- 纯本地运行，无需 API Key

## 项目结构

```
daily-investigator/
├── main.py           # 主程序
├── requirements.txt  # 依赖
├── .gitignore
└── output/           # 报告输出目录（git ignored）
```

## License

MIT
