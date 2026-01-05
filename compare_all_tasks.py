#!/usr/bin/env python3
"""
对比三个任务的偏见评估结果
- 传统推荐 (Traditional Recommendation)
- 解释生成 (Explanation Generation)
- 评论总结 (Review Summarization)
"""

import json
import os
from collections import defaultdict

# 结果文件路径
TRADITIONAL_RESULTS = "/ai/tcy/tcy-exp/traditional_bias_evaluation_results.json"
EXPLANATION_RESULTS = "/ai/tcy/tcy-exp/explanation_bias_evaluation_results.json"
REVIEW_RESULTS = "/ai/tcy/tcy-exp/review_bias_evaluation_results.json"

def load_results(file_path):
    """加载结果文件"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_section(title):
    """打印分隔线"""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

def compare_tasks():
    """对比三个任务"""
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 25 + "三任务偏见评估对比" + " " * 33 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # 加载结果
    traditional = load_results(TRADITIONAL_RESULTS)
    explanation = load_results(EXPLANATION_RESULTS)
    review = load_results(REVIEW_RESULTS)
    
    # 检查文件状态
    print_section("文件状态")
    print(f"传统推荐: {'✓ 已加载' if traditional else '✗ 未找到'}")
    print(f"解释生成: {'✓ 已加载' if explanation else '✗ 未找到'}")
    print(f"评论总结: {'✓ 已加载' if review else '✗ 未找到'}")
    
    if not any([traditional, explanation, review]):
        print("\n⚠ 没有找到任何结果文件，请先运行评估脚本")
        return
    
    # 对比各属性
    attributes = ['age', 'gender', 'nationality', 'ses', 'religion']
    
    for attribute in attributes:
        print_section(f"属性: {attribute.upper()}")
        
        # 传统推荐
        if traditional and attribute in traditional:
            print("\n【传统推荐任务】")
            data = traditional[attribute]
            print(f"  类别数: {len(data.get('categories', []))}")
            print(f"  类别: {', '.join(data.get('categories', []))}")
            
            if 'average_results' in data:
                print("  平均指标:")
                for cat, results in data['average_results'].items():
                    hr_10 = results.get('hr', {}).get(10, 0)
                    ndcg_10 = results.get('ndcg', {}).get(10, 0)
                    print(f"    {cat}: HR@10={hr_10:.4f}, NDCG@10={ndcg_10:.4f}")
            
            # 显示最大差距
            if 'performance_gaps' in data and data['performance_gaps']:
                max_gap = 0
                max_gap_info = None
                for gap_key, gap_data in data['performance_gaps'].items():
                    for metric, values in gap_data.items():
                        if abs(values['mean_difference']) > max_gap:
                            max_gap = abs(values['mean_difference'])
                            max_gap_info = (gap_key, metric, values['mean_difference'])
                
                if max_gap_info:
                    print(f"  最大差距: {max_gap_info[0]} - {max_gap_info[1]} = {max_gap_info[2]:.4f}")
        
        # 解释生成
        if explanation and attribute in explanation:
            print("\n【解释生成任务】")
            data = explanation[attribute]
            print(f"  类别数: {len(data.get('categories', []))}")
            print(f"  类别: {', '.join(data.get('categories', []))}")
            
            if 'average_results' in data:
                print("  平均指标:")
                for cat, results in data['average_results'].items():
                    bleu_1 = results.get('bleu', {}).get(1, 0)
                    rouge_l = results.get('rouge', {}).get('rougeL', 0)
                    print(f"    {cat}: BLEU-1={bleu_1:.4f}, ROUGE-L={rouge_l:.4f}")
            
            # 显示最大差距
            if 'performance_gaps' in data and data['performance_gaps']:
                max_gap = 0
                max_gap_info = None
                for gap_key, gap_data in data['performance_gaps'].items():
                    for metric, values in gap_data.items():
                        if abs(values['mean_difference']) > max_gap:
                            max_gap = abs(values['mean_difference'])
                            max_gap_info = (gap_key, metric, values['mean_difference'])
                
                if max_gap_info:
                    print(f"  最大差距: {max_gap_info[0]} - {max_gap_info[1]} = {max_gap_info[2]:.4f}")
        
        # 评论总结
        if review and attribute in review:
            print("\n【评论总结任务】")
            data = review[attribute]
            print(f"  类别数: {len(data.get('categories', []))}")
            print(f"  类别: {', '.join(data.get('categories', []))}")
            
            if 'average_results' in data:
                print("  平均指标:")
                for cat, results in data['average_results'].items():
                    bleu_1 = results.get('bleu', {}).get(1, 0)
                    rouge_l = results.get('rouge', {}).get('rougeL', 0)
                    print(f"    {cat}: BLEU-1={bleu_1:.4f}, ROUGE-L={rouge_l:.4f}")
            
            # 显示最大差距
            if 'performance_gaps' in data and data['performance_gaps']:
                max_gap = 0
                max_gap_info = None
                for gap_key, gap_data in data['performance_gaps'].items():
                    for metric, values in gap_data.items():
                        if abs(values['mean_difference']) > max_gap:
                            max_gap = abs(values['mean_difference'])
                            max_gap_info = (gap_key, metric, values['mean_difference'])
                
                if max_gap_info:
                    print(f"  最大差距: {max_gap_info[0]} - {max_gap_info[1]} = {max_gap_info[2]:.4f}")
    
    # 总结
    print_section("总体总结")
    
    print("\n任务对比:")
    print("┌─────────────┬──────────────┬──────────────┬──────────────┐")
    print("│ 维度        │ 传统推荐     │ 解释生成     │ 评论总结     │")
    print("├─────────────┼──────────────┼──────────────┼──────────────┤")
    print("│ 任务类型    │ 推荐商品     │ 生成解释     │ 总结评论     │")
    print("│ 评估指标    │ HR, NDCG     │ BLEU, ROUGE  │ BLEU, ROUGE  │")
    print("│ 输出类型    │ 商品列表     │ 短文本       │ 短文本       │")
    print("│ 结果文件    │ %-12s │ %-12s │ %-12s │" % (
        '✓' if traditional else '✗',
        '✓' if explanation else '✗',
        '✓' if review else '✗'
    ))
    print("└─────────────┴──────────────┴──────────────┴──────────────┘")
    
    print("\n偏见发现:")
    print("- 检查每个属性在三个任务中的表现")
    print("- 关注相对差距而非绝对分数")
    print("- 寻找跨任务的一致性偏见模式")
    
    print("\n建议:")
    print("1. 如果某个群体在所有任务中都表现较差 → 系统性偏见")
    print("2. 如果某个任务对特定属性更敏感 → 任务相关偏见")
    print("3. 对比不同任务的偏见缓解策略效果")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    compare_tasks()
