#!/usr/bin/env python3
"""
从已生成的组合数据集中提取基线数据集（不含用户画像的原始任务）
"""

import json
import os

def extract_baseline_from_combined():
    """
    从已生成的组合数据集中提取基线数据
    由于每个原始任务都与所有用户画像组合，我们可以从任意一个文件中提取
    """
    
    # 使用age文件，因为它是最大的，肯定包含所有任务
    combined_file = '/ai/tcy/tcy-exp/renwu/combined_datasets/by_attribute/rating_with_age_profiles.json'
    output_file = '/ai/tcy/tcy-exp/renwu/combined_datasets/rating_baseline.json'
    
    print("="*80)
    print("提取基线数据集（无用户画像）")
    print("="*80)
    
    print(f"\n输入文件: {combined_file}")
    print(f"输出文件: {output_file}")
    
    # 读取统计信息以获取用户画像数量
    stats_file = '/ai/tcy/tcy-exp/renwu/combined_datasets/by_attribute/_statistics.json'
    with open(stats_file, 'r') as f:
        stats = json.load(f)
    
    num_age_profiles = None
    for attr_info in stats['by_attribute']:
        if attr_info['attribute'] == 'age':
            num_age_profiles = 94  # 我们知道age有94个画像
            break
    
    print(f"\n策略: 每{num_age_profiles}条数据对应1个原始任务")
    print(f"预计提取: {stats['num_tasks']:,} 条基线数据")
    
    # 提取基线数据
    print("\n开始提取...")
    baseline_data = []
    seen_originals = set()
    
    with open(combined_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if line_num % 100000 == 0:
                print(f"  已处理 {line_num:,} 行...")
            
            data = json.loads(line.strip())
            original_instruction = data['original_instruction']
            
            # 只保留第一次出现的原始任务
            if original_instruction not in seen_originals:
                seen_originals.add(original_instruction)
                
                # 提取原始任务数据（不含用户画像）
                baseline_item = {
                    'instruction': original_instruction,
                    'input': data['input'],
                    'output': data['output'],
                    'task_type': data['task_type']
                }
                baseline_data.append(baseline_item)
    
    print(f"\n✓ 提取完成: {len(baseline_data):,} 条基线数据")
    
    # 保存基线数据集
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in baseline_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    # 获取文件大小
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
    print(f"✓ 文件大小: {file_size:.2f} MB")
    
    return baseline_data, output_file

def verify_baseline(baseline_data):
    """验证基线数据集"""
    print("\n" + "="*80)
    print("验证基线数据集")
    print("="*80)
    
    print(f"\n数据量: {len(baseline_data):,} 条")
    
    # 显示前5个样例
    print("\n前5个样例:")
    for i, item in enumerate(baseline_data[:5], 1):
        print(f"\n  样例 {i}:")
        print(f"    Instruction: {item['instruction'][:100]}...")
        print(f"    Output: {item['output']}")
    
    # 验证数据完整性
    print("\n数据完整性检查:")
    required_fields = ['instruction', 'input', 'output', 'task_type']
    all_valid = True
    
    for i, item in enumerate(baseline_data):
        for field in required_fields:
            if field not in item:
                print(f"  ✗ 第{i+1}条数据缺少字段: {field}")
                all_valid = False
                break
        if not all_valid:
            break
    
    if all_valid:
        print("  ✓ 所有数据包含必需字段")
    
    # 验证task_type
    task_types = set(item['task_type'] for item in baseline_data)
    print(f"\n任务类型: {task_types}")
    
    if len(task_types) == 1 and 'rating' in task_types:
        print("  ✓ 所有数据为评分预测任务")
    
    return all_valid

def compare_with_original():
    """与原始采样任务对比"""
    print("\n" + "="*80)
    print("与组合数据集对比")
    print("="*80)
    
    # 读取统计信息
    stats_file = '/ai/tcy/tcy-exp/renwu/combined_datasets/by_attribute/_statistics.json'
    with open(stats_file, 'r') as f:
        stats = json.load(f)
    
    baseline_file = '/ai/tcy/tcy-exp/renwu/combined_datasets/rating_baseline.json'
    
    with open(baseline_file, 'r') as f:
        baseline_count = sum(1 for _ in f)
    
    print(f"\n基线数据集:")
    print(f"  数据量: {baseline_count:,} 条")
    print(f"  特点: 原始任务，无用户画像")
    
    print(f"\n组合数据集:")
    print(f"  采样任务数: {stats['num_tasks']:,} 条")
    print(f"  用户画像数: {stats['num_profiles']:,} 条")
    print(f"  总数据量: {stats['total_count']:,} 条")
    
    print(f"\n数据量对比:")
    print(f"  基线数据集: {baseline_count:,} 条")
    print(f"  组合数据集: {stats['total_count']:,} 条")
    print(f"  倍数: {stats['total_count'] / baseline_count:.1f}x")

def main():
    print("╔" + "═"*78 + "╗")
    print("║" + " "*20 + "提取基线数据集（无用户画像）" + " "*28 + "║")
    print("╚" + "═"*78 + "╝\n")
    
    # 提取基线数据
    baseline_data, output_file = extract_baseline_from_combined()
    
    # 验证数据
    verify_baseline(baseline_data)
    
    # 对比分析
    compare_with_original()
    
    print("\n" + "="*80)
    print("✅ 基线数据集提取完成！")
    print("="*80)
    
    print(f"\n文件位置: {output_file}")
    print(f"数据量: {len(baseline_data):,} 条")
    
    print("\n用途:")
    print("  • 作为对照组，与包含用户画像的数据集对比")
    print("  • 分析用户画像对模型预测的影响")
    print("  • 评估基线模型性能")

if __name__ == "__main__":
    main()

