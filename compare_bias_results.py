#!/usr/bin/env python3
"""
对比传统推荐任务和解释生成任务的偏见评估结果
"""

import json
import os
from collections import defaultdict

TRADITIONAL_RESULTS = "/ai/tcy/tcy-exp/traditional_bias_evaluation_results.json"
EXPLANATION_RESULTS = "/ai/tcy/tcy-exp/explanation_bias_evaluation_results.json"


def load_results(file_path):
    """加载评估结果"""
    if not os.path.exists(file_path):
        print(f"⚠️  文件不存在: {file_path}")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_bias_severity(gaps, threshold=0.05):
    """分析偏见严重程度"""
    severe = []  # 统计显著
    moderate = []  # 差异较大但不显著
    mild = []  # 差异较小
    
    for gap in gaps:
        if gap['statistically_significant']:
            severe.append(gap)
        elif gap['abs_delta'] > threshold:
            moderate.append(gap)
        else:
            mild.append(gap)
    
    return severe, moderate, mild


def compare_tasks():
    """对比两个任务的偏见情况"""
    print("=" * 80)
    print("传统推荐 vs 解释生成：偏见对比分析")
    print("=" * 80)
    
    trad_results = load_results(TRADITIONAL_RESULTS)
    expl_results = load_results(EXPLANATION_RESULTS)
    
    if not trad_results:
        print("\n❌ 传统推荐结果文件不存在，请先运行评估")
        return
    
    if not expl_results:
        print("\n❌ 解释生成结果文件不存在，请先运行评估")
        return
    
    print("\n" + "=" * 80)
    print("【任务概览】")
    print("=" * 80)
    
    # 传统推荐任务概览
    print("\n传统推荐任务:")
    trad_attrs = trad_results.get('attributes', {})
    for attr, data in trad_attrs.items():
        print(f"  {attr}: {len(data)} 个类别")
    
    # 解释生成任务概览
    print("\n解释生成任务:")
    expl_attrs = expl_results.get('attributes', {})
    for attr, data in expl_attrs.items():
        print(f"  {attr}: {len(data)} 个类别")
    
    # 分析偏见严重程度
    print("\n" + "=" * 80)
    print("【偏见严重程度分析】")
    print("=" * 80)
    
    trad_gaps = trad_results.get('performance_gaps', [])
    expl_gaps = expl_results.get('performance_gaps', [])
    
    trad_severe, trad_moderate, trad_mild = analyze_bias_severity(trad_gaps)
    expl_severe, expl_moderate, expl_mild = analyze_bias_severity(expl_gaps)
    
    print("\n传统推荐任务:")
    print(f"  严重偏见（统计显著）: {len(trad_severe)} 项")
    print(f"  中等偏见（差异>0.05）: {len(trad_moderate)} 项")
    print(f"  轻微偏见（差异≤0.05）: {len(trad_mild)} 项")
    print(f"  总计: {len(trad_gaps)} 项对比")
    
    print("\n解释生成任务:")
    print(f"  严重偏见（统计显著）: {len(expl_severe)} 项")
    print(f"  中等偏见（差异>0.05）: {len(expl_moderate)} 项")
    print(f"  轻微偏见（差异≤0.05）: {len(expl_mild)} 项")
    print(f"  总计: {len(expl_gaps)} 项对比")
    
    # 按属性分析
    print("\n" + "=" * 80)
    print("【按属性分析最大偏见】")
    print("=" * 80)
    
    def get_max_bias_by_attr(gaps):
        """获取每个属性的最大偏见"""
        by_attr = defaultdict(list)
        for gap in gaps:
            by_attr[gap['attribute']].append(gap)
        
        max_biases = {}
        for attr, attr_gaps in by_attr.items():
            if attr_gaps:
                max_gap = max(attr_gaps, key=lambda x: x['abs_delta'])
                max_biases[attr] = max_gap
        return max_biases
    
    trad_max = get_max_bias_by_attr(trad_gaps)
    expl_max = get_max_bias_by_attr(expl_gaps)
    
    all_attrs = set(trad_max.keys()) | set(expl_max.keys())
    
    for attr in sorted(all_attrs):
        print(f"\n【{attr.upper()}】")
        
        if attr in trad_max:
            tg = trad_max[attr]
            print(f"  传统推荐:")
            print(f"    最大差异: {tg['abs_delta']:.4f} ({tg['metric']})")
            print(f"    对比组: {tg['group1']} vs {tg['group2']}")
            print(f"    显著性: {'是' if tg['statistically_significant'] else '否'}")
        
        if attr in expl_max:
            eg = expl_max[attr]
            print(f"  解释生成:")
            print(f"    最大差异: {eg['abs_delta']:.4f} ({eg['metric']})")
            print(f"    对比组: {eg['group1']} vs {eg['group2']}")
            print(f"    显著性: {'是' if eg['statistically_significant'] else '否'}")
    
    # 识别共同的高风险属性
    print("\n" + "=" * 80)
    print("【共同高风险属性】")
    print("=" * 80)
    
    trad_high_risk = {attr for attr, gap in trad_max.items() 
                      if gap['abs_delta'] > 0.05 or gap['statistically_significant']}
    expl_high_risk = {attr for attr, gap in expl_max.items() 
                      if gap['abs_delta'] > 0.05 or gap['statistically_significant']}
    
    common_risk = trad_high_risk & expl_high_risk
    
    if common_risk:
        print("\n两个任务都存在较大偏见的属性:")
        for attr in sorted(common_risk):
            print(f"  - {attr.upper()}")
    else:
        print("\n✓ 没有共同的高风险属性")
    
    # 任务特有的风险
    trad_only = trad_high_risk - expl_high_risk
    expl_only = expl_high_risk - trad_high_risk
    
    if trad_only:
        print("\n仅传统推荐任务存在的高风险属性:")
        for attr in sorted(trad_only):
            print(f"  - {attr.upper()}")
    
    if expl_only:
        print("\n仅解释生成任务存在的高风险属性:")
        for attr in sorted(expl_only):
            print(f"  - {attr.upper()}")
    
    # 总结建议
    print("\n" + "=" * 80)
    print("【总结与建议】")
    print("=" * 80)
    
    total_severe = len(trad_severe) + len(expl_severe)
    total_moderate = len(trad_moderate) + len(expl_moderate)
    
    print(f"\n1. 偏见总体情况:")
    print(f"   - 统计显著的偏见: {total_severe} 项")
    print(f"   - 需要关注的偏见: {total_moderate} 项")
    
    if common_risk:
        print(f"\n2. 优先处理属性: {', '.join(sorted(common_risk))}")
        print(f"   这些属性在两个任务中都表现出偏见，需要优先改进")
    
    if total_severe > 0:
        print(f"\n3. 严重偏见需要立即处理")
    elif total_moderate > 0:
        print(f"\n3. 存在中等程度偏见，建议进行优化")
    else:
        print(f"\n3. ✓ 整体公平性表现良好")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    compare_tasks()
