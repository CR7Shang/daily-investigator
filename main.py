#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
每日侦察兵 V2 — Daily Investigator
每日自动搜集接单市场情报 + 新物种发现 + 英文趋势

使用方法：
    cd C:\dev\projects\daily-investigator
    PYTHONUTF8=1 python main.py

输出：
    output/YYYY-MM-DD.md
"""

import os
import sys
import time
from datetime import date
from ddgs import DDGS


# ============================================================
#  配置区 —— 你可以自由修改这里
# ============================================================

# 每个关键词取多少条结果
RESULTS_PER_QUERY = 5

# 输出目录
OUTPUT_DIR = "output"

# ============================================================
#  搜索分类 —— V2 新增：按类别组织搜索
# ============================================================

SEARCH_CATEGORIES = {
    "known_platforms": ("🔍 已知平台监控", [
        "一品威客 Python脚本 自动化 接单",
        "一品威客 简单编程 外包 新手",
        "程聚宝 Python 爬虫 自动化 任务",
        "python脚本 接单 兼职 入门 2026",
        "一品威客 小程序 开发 外包 2026",
    ]),
    "new_discovery_cn": ("🆕 新物种发现 · 中文", [
        "全球首个 AI 交易平台 上线",
        "AI Agent 接单 新平台 2026",
        "AI 自由职业 新平台 上线",
        "AI 能力交易平台 发布",
        "AI 副业 赚钱 新方式 2026",
    ]),
    "new_discovery_en": ("🌐 新物种发现 · 英文", [
        "AI marketplace platform launch 2026",
        "AI agent freelance platform",
        "best AI freelancer platforms 2026",
        "AI agent earn money platform",
        "new AI gig economy platform",
    ]),
    "industry_news": ("📡 行业情报", [
        "AI Agent 融资 2026",
        "Product Hunt AI tools trending",
        "AI 创业 新平台 投资 2026",
        "自由职业 平台 新趋势 2026",
        "AI 自动化 接单 工具 2026",
    ]),
}


# ============================================================
#  搜索模块
# ============================================================

def search_web(query: str, max_results: int = 5) -> list[dict]:
    """对单个关键词执行搜索，返回结果列表"""
    results = []
    try:
        with DDGS() as ddgs:
            for i, r in enumerate(ddgs.text(query, max_results=max_results)):
                results.append({
                    "title": r.get("title", ""),
                    "url":   r.get("href", ""),
                    "body":  r.get("body", ""),
                })
    except Exception as e:
        print(f"    [错误] 搜索失败: {e}", file=sys.stderr)
    return results


# ============================================================
#  报告生成 —— V2 全新版式
# ============================================================

def generate_report(categorized_results: dict, today: str) -> str:
    """把搜索结果组装成 Markdown 简报，按类别组织"""
    lines = []
    lines.append(f"# 每日侦察简报 V2 · {today}")
    lines.append("")
    lines.append("> 自动搜集 | 新物种发现 | 英文趋势")
    lines.append("")

    total_queries = 0
    total_results = 0
    for cat_name, queries_data in categorized_results.values():
        for query, results in queries_data:
            total_queries += 1
            total_results += len(results)

    lines.append(f"**扫描概况：** {total_queries} 个关键词 · {total_results} 条结果")
    lines.append("")
    lines.append("---")
    lines.append("")

    for category_key, (category_name, queries_data) in categorized_results.items():
        lines.append(f"## {category_name}")
        lines.append("")

        has_any_results = any(results for _, results in queries_data)
        if not has_any_results:
            lines.append("_本轮无结果_")
            lines.append("")
            continue

        for query, results in queries_data:
            if not results:
                continue

            lines.append(f"### 📡 {query}")
            lines.append("")

            for i, r in enumerate(results, 1):
                title = r.get("title", "无标题") or "无标题"
                url   = r.get("url", "") or ""
                body  = r.get("body", "无摘要") or "无摘要"

                lines.append(f"{i}. **[{title}]({url})**")
                lines.append(f"   {body[:200]}")
                lines.append("")

        lines.append("---")
        lines.append("")

    # 尾部信息
    lines.append(f"> 自动生成于 {today} | 每日侦察兵 V2")
    lines.append("> 三层情报体系：同行雷达 → 主动扫描 → 跨圈搜索")

    return "\n".join(lines)


# ============================================================
#  主流程
# ============================================================

def main():
    today = date.today().isoformat()

    print("=" * 55)
    print(f"  🔍 每日侦察兵 V2 · {today}")
    print(f"  三层情报 | 新物种发现 | 英文趋势")
    print("=" * 55)

    # 1. 逐类别搜索
    categorized_results = {}
    total_failed = 0
    total_queries = 0

    for cat_index, (cat_key, (cat_name, queries)) in enumerate(SEARCH_CATEGORIES.items()):
        print(f"\n  📂 [{cat_name}]")
        cat_results = []

        for q_index, query in enumerate(queries):
            print(f"\n    📡 搜索: {query}")
            results = search_web(query, RESULTS_PER_QUERY)
            count = len(results)
            print(f"        → {count} 条结果")
            cat_results.append((query, results))
            if count == 0:
                total_failed += 1
            total_queries += 1
            # 搜索之间等3秒，避免被限流
            time.sleep(3)

        categorized_results[cat_key] = (cat_name, cat_results)

    # 2. 打印统计
    print(f"\n{'=' * 55}")
    print(f"  📊 扫描完成")
    print(f"     关键词: {total_queries}")
    print(f"     失败:   {total_failed}")
    if total_failed == total_queries:
        print("  ⚠️ 所有搜索均失败，请检查网络连接")

    # 3. 生成报告
    report = generate_report(categorized_results, today)

    # 4. 保存到文件
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{today}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n  ✅ 简报已保存: {output_path(filepath)}")
    print("=" * 55)


def output_path(filepath: str) -> str:
    """返回相对路径显示"""
    cwd = os.getcwd()
    if filepath.startswith(cwd):
        return os.path.relpath(filepath, cwd)
    return filepath


if __name__ == "__main__":
    main()
