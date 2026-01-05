#!/usr/bin/env python3
"""
将各种推荐任务与用户画像结合（按属性分组，任务随机抽取50%）

支持的任务类型：
- rating: 评分预测任务
- sequential: 序列推荐任务
- explanation: 解释生成任务
- traditional: 直接推荐任务
- review: 评论总结任务

使用方法：
  python generate_rating_combined.py              # 处理评分预测任务
  python generate_rating_combined.py sequential    # 处理序列推荐任务
  python generate_rating_combined.py explanation   # 处理解释生成任务
  python generate_rating_combined.py traditional   # 处理直接推荐任务
  python generate_rating_combined.py review       # 处理评论总结任务
"""

import json
import random
import os
from collections import defaultdict

def load_rating_tasks(file_path, sample_ratio=0.5):
    """加载评分预测任务数据，并随机采样"""
    print(f"\n加载任务数据（采样比例: {sample_ratio*100}%）...")
    tasks = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            tasks.append(json.loads(line.strip()))
    
    print(f"  原始任务数: {len(tasks):,} 条")
    
    # 随机采样
    random.seed(42)  # 设置随机种子保证可重复
    sampled_tasks = random.sample(tasks, int(len(tasks) * sample_ratio))
    
    print(f"  采样后任务数: {len(sampled_tasks):,} 条")
    
    return sampled_tasks

def load_sequential_tasks(file_path, sample_ratio=0.5):
    """加载序列推荐任务数据，并随机采样"""
    print(f"\n加载序列推荐任务数据（采样比例: {sample_ratio*100}%）...")
    tasks = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            tasks.append(json.loads(line.strip()))
    
    print(f"  原始任务数: {len(tasks):,} 条")
    
    # 随机采样
    random.seed(42)  # 设置随机种子保证可重复
    sampled_tasks = random.sample(tasks, int(len(tasks) * sample_ratio))
    
    print(f"  采样后任务数: {len(sampled_tasks):,} 条")
    
    return sampled_tasks

def load_explanation_tasks(file_path, sample_ratio=0.5):
    """加载解释生成任务数据，并随机采样"""
    print(f"\n加载解释生成任务数据（采样比例: {sample_ratio*100}%）...")
    tasks = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            tasks.append(json.loads(line.strip()))
    
    print(f"  原始任务数: {len(tasks):,} 条")
    
    # 随机采样
    random.seed(42)  # 设置随机种子保证可重复
    sampled_tasks = random.sample(tasks, int(len(tasks) * sample_ratio))
    
    print(f"  采样后任务数: {len(sampled_tasks):,} 条")
    
    return sampled_tasks

def load_traditional_tasks(file_path, sample_ratio=0.5):
    """加载直接推荐任务数据，并随机采样"""
    print(f"\n加载直接推荐任务数据（采样比例: {sample_ratio*100}%）...")
    tasks = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            tasks.append(json.loads(line.strip()))
    
    print(f"  原始任务数: {len(tasks):,} 条")
    
    # 随机采样
    random.seed(42)  # 设置随机种子保证可重复
    sampled_tasks = random.sample(tasks, int(len(tasks) * sample_ratio))
    
    print(f"  采样后任务数: {len(sampled_tasks):,} 条")
    
    return sampled_tasks

def load_review_tasks(file_path, sample_ratio=0.5):
    """加载评论总结任务数据，并随机采样"""
    print(f"\n加载评论总结任务数据（采样比例: {sample_ratio*100}%）...")
    tasks = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            tasks.append(json.loads(line.strip()))
    
    print(f"  原始任务数: {len(tasks):,} 条")
    
    # 随机采样
    random.seed(42)  # 设置随机种子保证可重复
    sampled_tasks = random.sample(tasks, int(len(tasks) * sample_ratio))
    
    print(f"  采样后任务数: {len(sampled_tasks):,} 条")
    
    return sampled_tasks

def load_user_profiles(file_path):
    """加载用户画像数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def combine_task_with_profile(task, profile):
    """
    将任务和用户画像结合
    将原始指令中的用户名替换为用户画像描述
    """
    original_instruction = task['instruction']
    
    # 提取原始指令中的用户名
    # 格式: "What star rating do you think [用户名] will give item_XXX ..."
    if "will give" in original_instruction:
        parts = original_instruction.split("will give")
        after_give = parts[1]
        
        # 替换用户描述
        new_instruction = f"{profile['profile']} What star rating do you think this learner will give{after_give}"
    else:
        # 如果格式不符，直接在前面加上用户画像
        new_instruction = f"{profile['profile']} {original_instruction}"
    
    # 创建新的任务对象
    combined_task = {
        "instruction": new_instruction,
        "input": task['input'],
        "output": task['output'],
        "task_type": task['task_type'],
        "original_instruction": original_instruction,  # 保留原始指令
        "user_profile": profile  # 保留完整的用户画像信息
    }
    
    return combined_task

def combine_sequential_task_with_profile(task, profile):
    """
    将序列推荐任务和用户画像结合
    在指令前面添加用户画像描述
    """
    original_instruction = task['instruction']
    
    # 格式: "Here is the purchase history list of user_X : \n ... \n try to recommend next item to the user"
    # 在指令前面添加用户画像信息
    new_instruction = f"{profile['profile']} {original_instruction}"
    
    # 创建新的任务对象
    combined_task = {
        "instruction": new_instruction,
        "input": task['input'],
        "output": task['output'],
        "task_type": task['task_type'],
        "original_instruction": original_instruction,  # 保留原始指令
        "user_profile": profile  # 保留完整的用户画像信息
    }
    
    return combined_task

def combine_explanation_task_with_profile(task, profile):
    """
    将解释生成任务和用户画像结合
    替换指令中的用户名
    """
    original_instruction = task['instruction']
    
    # 格式: "Help user_XXX generate a X-star explanation about this product : \n [产品名]"
    # 替换用户名或添加用户画像
    if "Help user_" in original_instruction:
        # 找到 "Help user_" 之后到 "generate" 之间的部分
        parts = original_instruction.split("generate", 1)
        if len(parts) == 2:
            new_instruction = f"{profile['profile']} Help this learner generate{parts[1]}"
        else:
            new_instruction = f"{profile['profile']} {original_instruction}"
    else:
        new_instruction = f"{profile['profile']} {original_instruction}"
    
    # 创建新的任务对象
    combined_task = {
        "instruction": new_instruction,
        "input": task['input'],
        "output": task['output'],
        "task_type": task['task_type'],
        "original_instruction": original_instruction,  # 保留原始指令
        "user_profile": profile  # 保留完整的用户画像信息
    }
    
    return combined_task

def combine_traditional_task_with_profile(task, profile):
    """
    将直接推荐任务和用户画像结合
    替换指令中的用户名
    """
    original_instruction = task['instruction']
    
    # 格式: "Which item of the following to recommend for [用户名] ? \n [物品列表]"
    # 替换用户名
    if "to recommend for" in original_instruction:
        parts = original_instruction.split("to recommend for", 1)
        if len(parts) == 2:
            # 找到问号之前的部分
            after_for = parts[1].split("?", 1)
            if len(after_for) == 2:
                new_instruction = f"{profile['profile']} Which item of the following to recommend for this learner?{after_for[1]}"
            else:
                new_instruction = f"{profile['profile']} {original_instruction}"
        else:
            new_instruction = f"{profile['profile']} {original_instruction}"
    else:
        new_instruction = f"{profile['profile']} {original_instruction}"
    
    # 创建新的任务对象
    combined_task = {
        "instruction": new_instruction,
        "input": task['input'],
        "output": task['output'],
        "task_type": task['task_type'],
        "original_instruction": original_instruction,  # 保留原始指令
        "user_profile": profile  # 保留完整的用户画像信息
    }
    
    return combined_task

def combine_review_task_with_profile(task, profile):
    """
    将评论总结任务和用户画像结合
    替换指令中的用户名
    """
    original_instruction = task['instruction']
    
    # 格式: "Write a short sentence to summarize the following product review from user_XXX : \n [评论内容]"
    # 替换用户名
    if "from user_" in original_instruction:
        parts = original_instruction.split("from user_", 1)
        if len(parts) == 2:
            # 找到冒号之前的部分
            after_user = parts[1].split(":", 1)
            if len(after_user) == 2:
                new_instruction = f"{profile['profile']} Write a short sentence to summarize the following product review from this learner:{after_user[1]}"
            else:
                new_instruction = f"{profile['profile']} {original_instruction}"
        else:
            new_instruction = f"{profile['profile']} {original_instruction}"
    else:
        new_instruction = f"{profile['profile']} {original_instruction}"
    
    # 创建新的任务对象
    combined_task = {
        "instruction": new_instruction,
        "input": task['input'],
        "output": task['output'],
        "task_type": task['task_type'],
        "original_instruction": original_instruction,  # 保留原始指令
        "user_profile": profile  # 保留完整的用户画像信息
    }
    
    return combined_task

def generate_by_attribute(rating_tasks, user_profiles, output_dir):
    """
    按属性分组生成数据集
    为每个敏感属性生成独立的数据集文件
    """
    print("\n" + "="*80)
    print("策略3: 按属性分组（50%任务采样）")
    print("="*80)
    
    # 按属性分组用户画像
    profiles_by_attr = defaultdict(list)
    for profile in user_profiles:
        profiles_by_attr[profile['attribute']].append(profile)
    
    print(f"\n共有 {len(profiles_by_attr)} 个敏感属性:")
    for attr, profiles in sorted(profiles_by_attr.items()):
        expected_count = len(rating_tasks) * len(profiles)
        print(f"  • {attr:12s}: {len(profiles):2d} 个画像 → 预计生成 {expected_count:,} 条数据")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 按属性生成数据
    total_count = 0
    file_info = []
    
    for attr in sorted(profiles_by_attr.keys()):
        profiles = profiles_by_attr[attr]
        output_file = os.path.join(output_dir, f'rating_with_{attr}_profiles.json')
        
        print(f"\n{'='*80}")
        print(f"生成【{attr.upper()}】属性数据集")
        print(f"{'='*80}")
        print(f"  输出文件: {output_file}")
        print(f"  任务数: {len(rating_tasks):,}")
        print(f"  画像数: {len(profiles)}")
        print(f"  预计生成: {len(rating_tasks) * len(profiles):,} 条")
        
        count = 0
        with open(output_file, 'w', encoding='utf-8') as f:
            for task_idx, task in enumerate(rating_tasks):
                if (task_idx + 1) % 2000 == 0:
                    print(f"    进度: {task_idx + 1:,}/{len(rating_tasks):,} ({(task_idx+1)/len(rating_tasks)*100:.1f}%)")
                
                for profile in profiles:
                    combined = combine_task_with_profile(task, profile)
                    f.write(json.dumps(combined, ensure_ascii=False) + '\n')
                    count += 1
        
        # 获取文件大小
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        
        print(f"  ✓ 完成: {count:,} 条数据")
        print(f"  ✓ 文件大小: {file_size:.2f} MB")
        
        file_info.append({
            'attribute': attr,
            'file': os.path.basename(output_file),
            'count': count,
            'size_mb': file_size
        })
        
        total_count += count
    
    # 生成统计报告
    print("\n" + "="*80)
    print("生成完成统计")
    print("="*80)
    
    for info in file_info:
        print(f"\n【{info['attribute'].upper()}】")
        print(f"  文件: {info['file']}")
        print(f"  数据量: {info['count']:,} 条")
        print(f"  大小: {info['size_mb']:.2f} MB")
    
    print(f"\n{'='*80}")
    print(f"总计: {total_count:,} 条数据")
    print(f"输出目录: {output_dir}")
    print("="*80)
    
    # 保存统计信息
    stats_file = os.path.join(output_dir, '_statistics.json')
    stats = {
        'total_count': total_count,
        'num_tasks': len(rating_tasks),
        'num_profiles': len(user_profiles),
        'sample_ratio': 0.5,
        'by_attribute': file_info
    }
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n统计信息已保存到: {stats_file}")
    
    return total_count, file_info

def show_samples(output_dir):
    """展示生成数据的样例"""
    print("\n" + "="*80)
    print("数据样例展示")
    print("="*80)
    
    # 读取每个属性的第一条数据作为样例
    for attr in ['age', 'gender', 'nationality', 'ses', 'religion']:
        file_path = os.path.join(output_dir, f'rating_with_{attr}_profiles.json')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                sample = json.loads(f.readline().strip())
            
            print(f"\n【{attr.upper()}属性样例】")
            print(f"  用户画像: {sample['user_profile']['profile']}")
            print(f"  提示语: {sample['instruction'][:120]}...")
            print(f"  输出: {sample['output']}")

def generate_sequential_by_attribute(sequential_tasks, user_profiles, output_dir):
    """
    按属性分组生成序列推荐数据集
    为每个敏感属性生成独立的数据集文件
    """
    print("\n" + "="*80)
    print("序列推荐任务: 按属性分组（50%任务采样）")
    print("="*80)
    
    # 按属性分组用户画像
    profiles_by_attr = defaultdict(list)
    for profile in user_profiles:
        profiles_by_attr[profile['attribute']].append(profile)
    
    print(f"\n共有 {len(profiles_by_attr)} 个敏感属性:")
    for attr, profiles in sorted(profiles_by_attr.items()):
        expected_count = len(sequential_tasks) * len(profiles)
        print(f"  • {attr:12s}: {len(profiles):2d} 个画像 → 预计生成 {expected_count:,} 条数据")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 按属性生成数据
    total_count = 0
    file_info = []
    
    for attr in sorted(profiles_by_attr.keys()):
        profiles = profiles_by_attr[attr]
        output_file = os.path.join(output_dir, f'sequential_with_{attr}_profiles.json')
        
        print(f"\n{'='*80}")
        print(f"生成【{attr.upper()}】属性数据集")
        print(f"{'='*80}")
        print(f"  输出文件: {output_file}")
        print(f"  任务数: {len(sequential_tasks):,}")
        print(f"  画像数: {len(profiles)}")
        print(f"  预计生成: {len(sequential_tasks) * len(profiles):,} 条")
        
        count = 0
        with open(output_file, 'w', encoding='utf-8') as f:
            for task_idx, task in enumerate(sequential_tasks):
                if (task_idx + 1) % 2000 == 0:
                    print(f"    进度: {task_idx + 1:,}/{len(sequential_tasks):,} ({(task_idx+1)/len(sequential_tasks)*100:.1f}%)")
                
                for profile in profiles:
                    combined = combine_sequential_task_with_profile(task, profile)
                    f.write(json.dumps(combined, ensure_ascii=False) + '\n')
                    count += 1
        
        # 获取文件大小
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        
        print(f"  ✓ 完成: {count:,} 条数据")
        print(f"  ✓ 文件大小: {file_size:.2f} MB")
        
        file_info.append({
            'attribute': attr,
            'file': os.path.basename(output_file),
            'count': count,
            'size_mb': file_size
        })
        
        total_count += count
    
    # 生成统计报告
    print("\n" + "="*80)
    print("生成完成统计")
    print("="*80)
    
    for info in file_info:
        print(f"\n【{info['attribute'].upper()}】")
        print(f"  文件: {info['file']}")
        print(f"  数据量: {info['count']:,} 条")
        print(f"  大小: {info['size_mb']:.2f} MB")
    
    print(f"\n{'='*80}")
    print(f"总计: {total_count:,} 条数据")
    print(f"输出目录: {output_dir}")
    print("="*80)
    
    # 保存统计信息
    stats_file = os.path.join(output_dir, '_sequential_statistics.json')
    stats = {
        'total_count': total_count,
        'num_tasks': len(sequential_tasks),
        'num_profiles': len(user_profiles),
        'sample_ratio': 0.5,
        'by_attribute': file_info
    }
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n统计信息已保存到: {stats_file}")
    
    return total_count, file_info

def show_sequential_samples(output_dir):
    """展示生成序列推荐数据的样例"""
    print("\n" + "="*80)
    print("序列推荐数据样例展示")
    print("="*80)
    
    # 读取每个属性的第一条数据作为样例
    for attr in ['age', 'gender', 'nationality', 'ses', 'religion']:
        file_path = os.path.join(output_dir, f'sequential_with_{attr}_profiles.json')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                sample = json.loads(f.readline().strip())
            
            print(f"\n【{attr.upper()}属性样例】")
            print(f"  用户画像: {sample['user_profile']['profile']}")
            print(f"  提示语: {sample['instruction'][:150]}...")
            print(f"  输出: {sample['output']}")

def generate_explanation_by_attribute(explanation_tasks, user_profiles, output_dir):
    """
    按属性分组生成解释生成数据集
    为每个敏感属性生成独立的数据集文件
    """
    print("\n" + "="*80)
    print("解释生成任务: 按属性分组（50%任务采样）")
    print("="*80)
    
    # 按属性分组用户画像
    profiles_by_attr = defaultdict(list)
    for profile in user_profiles:
        profiles_by_attr[profile['attribute']].append(profile)
    
    print(f"\n共有 {len(profiles_by_attr)} 个敏感属性:")
    for attr, profiles in sorted(profiles_by_attr.items()):
        expected_count = len(explanation_tasks) * len(profiles)
        print(f"  • {attr:12s}: {len(profiles):2d} 个画像 → 预计生成 {expected_count:,} 条数据")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 按属性生成数据
    total_count = 0
    file_info = []
    
    for attr in sorted(profiles_by_attr.keys()):
        profiles = profiles_by_attr[attr]
        output_file = os.path.join(output_dir, f'explanation_with_{attr}_profiles.json')
        
        print(f"\n{'='*80}")
        print(f"生成【{attr.upper()}】属性数据集")
        print(f"{'='*80}")
        print(f"  输出文件: {output_file}")
        print(f"  任务数: {len(explanation_tasks):,}")
        print(f"  画像数: {len(profiles)}")
        print(f"  预计生成: {len(explanation_tasks) * len(profiles):,} 条")
        
        count = 0
        with open(output_file, 'w', encoding='utf-8') as f:
            for task_idx, task in enumerate(explanation_tasks):
                if (task_idx + 1) % 2000 == 0:
                    print(f"    进度: {task_idx + 1:,}/{len(explanation_tasks):,} ({(task_idx+1)/len(explanation_tasks)*100:.1f}%)")
                
                for profile in profiles:
                    combined = combine_explanation_task_with_profile(task, profile)
                    f.write(json.dumps(combined, ensure_ascii=False) + '\n')
                    count += 1
        
        # 获取文件大小
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        
        print(f"  ✓ 完成: {count:,} 条数据")
        print(f"  ✓ 文件大小: {file_size:.2f} MB")
        
        file_info.append({
            'attribute': attr,
            'file': os.path.basename(output_file),
            'count': count,
            'size_mb': file_size
        })
        
        total_count += count
    
    # 生成统计报告
    print("\n" + "="*80)
    print("生成完成统计")
    print("="*80)
    
    for info in file_info:
        print(f"\n【{info['attribute'].upper()}】")
        print(f"  文件: {info['file']}")
        print(f"  数据量: {info['count']:,} 条")
        print(f"  大小: {info['size_mb']:.2f} MB")
    
    print(f"\n{'='*80}")
    print(f"总计: {total_count:,} 条数据")
    print(f"输出目录: {output_dir}")
    print("="*80)
    
    # 保存统计信息
    stats_file = os.path.join(output_dir, '_explanation_statistics.json')
    stats = {
        'total_count': total_count,
        'num_tasks': len(explanation_tasks),
        'num_profiles': len(user_profiles),
        'sample_ratio': 0.5,
        'by_attribute': file_info
    }
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n统计信息已保存到: {stats_file}")
    
    return total_count, file_info

def generate_traditional_by_attribute(traditional_tasks, user_profiles, output_dir):
    """
    按属性分组生成直接推荐数据集
    为每个敏感属性生成独立的数据集文件
    """
    print("\n" + "="*80)
    print("直接推荐任务: 按属性分组（50%任务采样）")
    print("="*80)
    
    # 按属性分组用户画像
    profiles_by_attr = defaultdict(list)
    for profile in user_profiles:
        profiles_by_attr[profile['attribute']].append(profile)
    
    print(f"\n共有 {len(profiles_by_attr)} 个敏感属性:")
    for attr, profiles in sorted(profiles_by_attr.items()):
        expected_count = len(traditional_tasks) * len(profiles)
        print(f"  • {attr:12s}: {len(profiles):2d} 个画像 → 预计生成 {expected_count:,} 条数据")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 按属性生成数据
    total_count = 0
    file_info = []
    
    for attr in sorted(profiles_by_attr.keys()):
        profiles = profiles_by_attr[attr]
        output_file = os.path.join(output_dir, f'traditional_with_{attr}_profiles.json')
        
        print(f"\n{'='*80}")
        print(f"生成【{attr.upper()}】属性数据集")
        print(f"{'='*80}")
        print(f"  输出文件: {output_file}")
        print(f"  任务数: {len(traditional_tasks):,}")
        print(f"  画像数: {len(profiles)}")
        print(f"  预计生成: {len(traditional_tasks) * len(profiles):,} 条")
        
        count = 0
        with open(output_file, 'w', encoding='utf-8') as f:
            for task_idx, task in enumerate(traditional_tasks):
                if (task_idx + 1) % 2000 == 0:
                    print(f"    进度: {task_idx + 1:,}/{len(traditional_tasks):,} ({(task_idx+1)/len(traditional_tasks)*100:.1f}%)")
                
                for profile in profiles:
                    combined = combine_traditional_task_with_profile(task, profile)
                    f.write(json.dumps(combined, ensure_ascii=False) + '\n')
                    count += 1
        
        # 获取文件大小
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        
        print(f"  ✓ 完成: {count:,} 条数据")
        print(f"  ✓ 文件大小: {file_size:.2f} MB")
        
        file_info.append({
            'attribute': attr,
            'file': os.path.basename(output_file),
            'count': count,
            'size_mb': file_size
        })
        
        total_count += count
    
    # 生成统计报告
    print("\n" + "="*80)
    print("生成完成统计")
    print("="*80)
    
    for info in file_info:
        print(f"\n【{info['attribute'].upper()}】")
        print(f"  文件: {info['file']}")
        print(f"  数据量: {info['count']:,} 条")
        print(f"  大小: {info['size_mb']:.2f} MB")
    
    print(f"\n{'='*80}")
    print(f"总计: {total_count:,} 条数据")
    print(f"输出目录: {output_dir}")
    print("="*80)
    
    # 保存统计信息
    stats_file = os.path.join(output_dir, '_traditional_statistics.json')
    stats = {
        'total_count': total_count,
        'num_tasks': len(traditional_tasks),
        'num_profiles': len(user_profiles),
        'sample_ratio': 0.5,
        'by_attribute': file_info
    }
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n统计信息已保存到: {stats_file}")
    
    return total_count, file_info

def generate_review_by_attribute(review_tasks, user_profiles, output_dir):
    """
    按属性分组生成评论总结数据集
    为每个敏感属性生成独立的数据集文件
    """
    print("\n" + "="*80)
    print("评论总结任务: 按属性分组（50%任务采样）")
    print("="*80)
    
    # 按属性分组用户画像
    profiles_by_attr = defaultdict(list)
    for profile in user_profiles:
        profiles_by_attr[profile['attribute']].append(profile)
    
    print(f"\n共有 {len(profiles_by_attr)} 个敏感属性:")
    for attr, profiles in sorted(profiles_by_attr.items()):
        expected_count = len(review_tasks) * len(profiles)
        print(f"  • {attr:12s}: {len(profiles):2d} 个画像 → 预计生成 {expected_count:,} 条数据")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 按属性生成数据
    total_count = 0
    file_info = []
    
    for attr in sorted(profiles_by_attr.keys()):
        profiles = profiles_by_attr[attr]
        output_file = os.path.join(output_dir, f'review_with_{attr}_profiles.json')
        
        print(f"\n{'='*80}")
        print(f"生成【{attr.upper()}】属性数据集")
        print(f"{'='*80}")
        print(f"  输出文件: {output_file}")
        print(f"  任务数: {len(review_tasks):,}")
        print(f"  画像数: {len(profiles)}")
        print(f"  预计生成: {len(review_tasks) * len(profiles):,} 条")
        
        count = 0
        with open(output_file, 'w', encoding='utf-8') as f:
            for task_idx, task in enumerate(review_tasks):
                if (task_idx + 1) % 2000 == 0:
                    print(f"    进度: {task_idx + 1:,}/{len(review_tasks):,} ({(task_idx+1)/len(review_tasks)*100:.1f}%)")
                
                for profile in profiles:
                    combined = combine_review_task_with_profile(task, profile)
                    f.write(json.dumps(combined, ensure_ascii=False) + '\n')
                    count += 1
        
        # 获取文件大小
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        
        print(f"  ✓ 完成: {count:,} 条数据")
        print(f"  ✓ 文件大小: {file_size:.2f} MB")
        
        file_info.append({
            'attribute': attr,
            'file': os.path.basename(output_file),
            'count': count,
            'size_mb': file_size
        })
        
        total_count += count
    
    # 生成统计报告
    print("\n" + "="*80)
    print("生成完成统计")
    print("="*80)
    
    for info in file_info:
        print(f"\n【{info['attribute'].upper()}】")
        print(f"  文件: {info['file']}")
        print(f"  数据量: {info['count']:,} 条")
        print(f"  大小: {info['size_mb']:.2f} MB")
    
    print(f"\n{'='*80}")
    print(f"总计: {total_count:,} 条数据")
    print(f"输出目录: {output_dir}")
    print("="*80)
    
    # 保存统计信息
    stats_file = os.path.join(output_dir, '_review_statistics.json')
    stats = {
        'total_count': total_count,
        'num_tasks': len(review_tasks),
        'num_profiles': len(user_profiles),
        'sample_ratio': 0.5,
        'by_attribute': file_info
    }
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n统计信息已保存到: {stats_file}")
    
    return total_count, file_info

def show_explanation_samples(output_dir):
    """展示生成解释生成数据的样例"""
    print("\n" + "="*80)
    print("解释生成数据样例展示")
    print("="*80)
    
    # 读取每个属性的第一条数据作为样例
    for attr in ['age', 'gender', 'nationality', 'ses', 'religion']:
        file_path = os.path.join(output_dir, f'explanation_with_{attr}_profiles.json')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                sample = json.loads(f.readline().strip())
            
            print(f"\n【{attr.upper()}属性样例】")
            print(f"  用户画像: {sample['user_profile']['profile']}")
            print(f"  提示语: {sample['instruction'][:150]}...")
            print(f"  输出: {sample['output']}")

def show_traditional_samples(output_dir):
    """展示生成直接推荐数据的样例"""
    print("\n" + "="*80)
    print("直接推荐数据样例展示")
    print("="*80)
    
    # 读取每个属性的第一条数据作为样例
    for attr in ['age', 'gender', 'nationality', 'ses', 'religion']:
        file_path = os.path.join(output_dir, f'traditional_with_{attr}_profiles.json')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                sample = json.loads(f.readline().strip())
            
            print(f"\n【{attr.upper()}属性样例】")
            print(f"  用户画像: {sample['user_profile']['profile']}")
            print(f"  提示语: {sample['instruction'][:150]}...")
            print(f"  输出: {sample['output']}")

def show_review_samples(output_dir):
    """展示生成评论总结数据的样例"""
    print("\n" + "="*80)
    print("评论总结数据样例展示")
    print("="*80)
    
    # 读取每个属性的第一条数据作为样例
    for attr in ['age', 'gender', 'nationality', 'ses', 'religion']:
        file_path = os.path.join(output_dir, f'review_with_{attr}_profiles.json')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                sample = json.loads(f.readline().strip())
            
            print(f"\n【{attr.upper()}属性样例】")
            print(f"  用户画像: {sample['user_profile']['profile']}")
            print(f"  提示语: {sample['instruction'][:150]}...")
            print(f"  输出: {sample['output']}")

def main():
    print("="*80)
    print("评分预测任务与用户画像结合工具")
    print("策略: 按属性分组 + 50%任务采样")
    print("="*80)
    
    # 文件路径
    rating_file = '/ai/tcy/tcy-exp/renwu/tasks_by_type/rating_tasks.json'
    profiles_file = '/ai/tcy/tcy-exp/user_profiles_dataset.json'
    output_dir = '/ai/tcy/tcy-exp/renwu/combined_datasets/by_attribute'
    
    # 加载数据（50%采样）
    rating_tasks = load_rating_tasks(rating_file, sample_ratio=0.5)
    
    print("\n加载用户画像数据...")
    user_profiles = load_user_profiles(profiles_file)
    print(f"  用户画像数: {len(user_profiles):,} 条")
    
    # 显示用户画像统计
    attr_count = defaultdict(int)
    for profile in user_profiles:
        attr_count[profile['attribute']] += 1
    
    print(f"\n  按属性分布:")
    for attr, count in sorted(attr_count.items()):
        print(f"    - {attr:12s}: {count:2d} 条")
    
    # 计算总数据量
    total_expected = 0
    for attr, count in attr_count.items():
        total_expected += len(rating_tasks) * count
    
    print(f"\n预计生成总数据量: {total_expected:,} 条")
    print(f"（对比不采样: {total_expected * 2:,} 条）")
    print(f"数据量减少: 50%")
    
    # 确认
    print("\n" + "="*80)
    confirm = input("确认开始生成数据？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return
    
    # 生成数据
    total_count, file_info = generate_by_attribute(rating_tasks, user_profiles, output_dir)
    
    # 展示样例
    show_samples(output_dir)
    
    print("\n" + "="*80)
    print("✅ 所有数据生成完成！")
    print("="*80)
    print(f"\n数据位置: {output_dir}")
    print(f"总数据量: {total_count:,} 条")
    print(f"\n生成的文件:")
    for info in file_info:
        print(f"  • {info['file']:40s} ({info['count']:,} 条, {info['size_mb']:.2f} MB)")

def main_sequential():
    print("="*80)
    print("序列推荐任务与用户画像结合工具")
    print("策略: 按属性分组 + 50%任务采样")
    print("="*80)
    
    # 文件路径
    sequential_file = '/ai/tcy/tcy-exp/renwu/tasks_by_type/sequential_tasks.json'
    profiles_file = '/ai/tcy/tcy-exp/user_profiles_dataset.json'
    output_dir = '/ai/tcy/tcy-exp/renwu/combined_datasets/by_attribute'
    
    # 加载数据（50%采样）
    sequential_tasks = load_sequential_tasks(sequential_file, sample_ratio=0.5)
    
    print("\n加载用户画像数据...")
    user_profiles = load_user_profiles(profiles_file)
    print(f"  用户画像数: {len(user_profiles):,} 条")
    
    # 显示用户画像统计
    attr_count = defaultdict(int)
    for profile in user_profiles:
        attr_count[profile['attribute']] += 1
    
    print(f"\n  按属性分布:")
    for attr, count in sorted(attr_count.items()):
        print(f"    - {attr:12s}: {count:2d} 条")
    
    # 计算总数据量
    total_expected = 0
    for attr, count in attr_count.items():
        total_expected += len(sequential_tasks) * count
    
    print(f"\n预计生成总数据量: {total_expected:,} 条")
    print(f"（对比不采样: {total_expected * 2:,} 条）")
    print(f"数据量减少: 50%")
    
    # 确认
    print("\n" + "="*80)
    confirm = input("确认开始生成数据？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return
    
    # 生成数据
    total_count, file_info = generate_sequential_by_attribute(sequential_tasks, user_profiles, output_dir)
    
    # 展示样例
    show_sequential_samples(output_dir)
    
    print("\n" + "="*80)
    print("✅ 所有数据生成完成！")
    print("="*80)
    print(f"\n数据位置: {output_dir}")
    print(f"总数据量: {total_count:,} 条")
    print(f"\n生成的文件:")
    for info in file_info:
        print(f"  • {info['file']:40s} ({info['count']:,} 条, {info['size_mb']:.2f} MB)")

def main_explanation():
    print("="*80)
    print("解释生成任务与用户画像结合工具")
    print("策略: 按属性分组 + 50%任务采样")
    print("="*80)
    
    # 文件路径
    explanation_file = '/ai/tcy/tcy-exp/renwu/tasks_by_type/explanation_tasks.json'
    profiles_file = '/ai/tcy/tcy-exp/user_profiles_dataset.json'
    output_dir = '/ai/tcy/tcy-exp/renwu/combined_datasets/by_attribute'
    
    # 加载数据（50%采样）
    explanation_tasks = load_explanation_tasks(explanation_file, sample_ratio=0.5)
    
    print("\n加载用户画像数据...")
    user_profiles = load_user_profiles(profiles_file)
    print(f"  用户画像数: {len(user_profiles):,} 条")
    
    # 显示用户画像统计
    attr_count = defaultdict(int)
    for profile in user_profiles:
        attr_count[profile['attribute']] += 1
    
    print(f"\n  按属性分布:")
    for attr, count in sorted(attr_count.items()):
        print(f"    - {attr:12s}: {count:2d} 条")
    
    # 计算总数据量
    total_expected = 0
    for attr, count in attr_count.items():
        total_expected += len(explanation_tasks) * count
    
    print(f"\n预计生成总数据量: {total_expected:,} 条")
    print(f"（对比不采样: {total_expected * 2:,} 条）")
    print(f"数据量减少: 50%")
    
    # 确认
    print("\n" + "="*80)
    confirm = input("确认开始生成数据？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return
    
    # 生成数据
    total_count, file_info = generate_explanation_by_attribute(explanation_tasks, user_profiles, output_dir)
    
    # 展示样例
    show_explanation_samples(output_dir)
    
    print("\n" + "="*80)
    print("✅ 所有数据生成完成！")
    print("="*80)
    print(f"\n数据位置: {output_dir}")
    print(f"总数据量: {total_count:,} 条")
    print(f"\n生成的文件:")
    for info in file_info:
        print(f"  • {info['file']:40s} ({info['count']:,} 条, {info['size_mb']:.2f} MB)")

def main_traditional():
    print("="*80)
    print("直接推荐任务与用户画像结合工具")
    print("策略: 按属性分组 + 50%任务采样")
    print("="*80)
    
    # 文件路径
    traditional_file = '/ai/tcy/tcy-exp/renwu/tasks_by_type/traditional_tasks.json'
    profiles_file = '/ai/tcy/tcy-exp/user_profiles_dataset.json'
    output_dir = '/ai/tcy/tcy-exp/renwu/combined_datasets/by_attribute'
    
    # 加载数据（50%采样）
    traditional_tasks = load_traditional_tasks(traditional_file, sample_ratio=0.5)
    
    print("\n加载用户画像数据...")
    user_profiles = load_user_profiles(profiles_file)
    print(f"  用户画像数: {len(user_profiles):,} 条")
    
    # 显示用户画像统计
    attr_count = defaultdict(int)
    for profile in user_profiles:
        attr_count[profile['attribute']] += 1
    
    print(f"\n  按属性分布:")
    for attr, count in sorted(attr_count.items()):
        print(f"    - {attr:12s}: {count:2d} 条")
    
    # 计算总数据量
    total_expected = 0
    for attr, count in attr_count.items():
        total_expected += len(traditional_tasks) * count
    
    print(f"\n预计生成总数据量: {total_expected:,} 条")
    print(f"（对比不采样: {total_expected * 2:,} 条）")
    print(f"数据量减少: 50%")
    
    # 确认
    print("\n" + "="*80)
    confirm = input("确认开始生成数据？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return
    
    # 生成数据
    total_count, file_info = generate_traditional_by_attribute(traditional_tasks, user_profiles, output_dir)
    
    # 展示样例
    show_traditional_samples(output_dir)
    
    print("\n" + "="*80)
    print("✅ 所有数据生成完成！")
    print("="*80)
    print(f"\n数据位置: {output_dir}")
    print(f"总数据量: {total_count:,} 条")
    print(f"\n生成的文件:")
    for info in file_info:
        print(f"  • {info['file']:40s} ({info['count']:,} 条, {info['size_mb']:.2f} MB)")

def main_review():
    print("="*80)
    print("评论总结任务与用户画像结合工具")
    print("策略: 按属性分组 + 50%任务采样")
    print("="*80)
    
    # 文件路径
    review_file = '/ai/tcy/tcy-exp/renwu/tasks_by_type/review_tasks.json'
    profiles_file = '/ai/tcy/tcy-exp/user_profiles_dataset.json'
    output_dir = '/ai/tcy/tcy-exp/renwu/combined_datasets/by_attribute'
    
    # 加载数据（50%采样）
    review_tasks = load_review_tasks(review_file, sample_ratio=0.5)
    
    print("\n加载用户画像数据...")
    user_profiles = load_user_profiles(profiles_file)
    print(f"  用户画像数: {len(user_profiles):,} 条")
    
    # 显示用户画像统计
    attr_count = defaultdict(int)
    for profile in user_profiles:
        attr_count[profile['attribute']] += 1
    
    print(f"\n  按属性分布:")
    for attr, count in sorted(attr_count.items()):
        print(f"    - {attr:12s}: {count:2d} 条")
    
    # 计算总数据量
    total_expected = 0
    for attr, count in attr_count.items():
        total_expected += len(review_tasks) * count
    
    print(f"\n预计生成总数据量: {total_expected:,} 条")
    print(f"（对比不采样: {total_expected * 2:,} 条）")
    print(f"数据量减少: 50%")
    
    # 确认
    print("\n" + "="*80)
    confirm = input("确认开始生成数据？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return
    
    # 生成数据
    total_count, file_info = generate_review_by_attribute(review_tasks, user_profiles, output_dir)
    
    # 展示样例
    show_review_samples(output_dir)
    
    print("\n" + "="*80)
    print("✅ 所有数据生成完成！")
    print("="*80)
    print(f"\n数据位置: {output_dir}")
    print(f"总数据量: {total_count:,} 条")
    print(f"\n生成的文件:")
    for info in file_info:
        print(f"  • {info['file']:40s} ({info['count']:,} 条, {info['size_mb']:.2f} MB)")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        task_type = sys.argv[1].lower()
        if task_type == 'sequential':
            main_sequential()
        elif task_type == 'explanation':
            main_explanation()
        elif task_type == 'traditional':
            main_traditional()
        elif task_type == 'review':
            main_review()
        else:
            print(f"未知的任务类型: {task_type}")
            print("支持的类型: sequential, explanation, traditional, review")
            print("或运行不带参数以处理评分预测任务")
    else:
        main()

