#!/usr/bin/env python3
"""
生成单属性用户画像数据集
根据敏感属性词典生成用户画像描述
"""

import json
import os
from pathlib import Path

# 定义词典文件路径
CIYU_DIR = "/ai/tcy/tcy-exp/words/ciyu"

# 定义模板
TEMPLATES = {
    "gender": "This is a {gender} learner.",
    "age": "This is a {age}-year-old learner.",
    "nationality": "This learner is from {region}.",
    "ses": "This learner comes from a {ses} background.",
    "religion": "This learner identifies as {religion}."
}


def load_vocab(filename):
    """加载词典文件"""
    filepath = os.path.join(CIYU_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_age_profiles():
    """生成年龄相关的用户画像"""
    age_vocab = load_vocab("Age_vocab.json")
    profiles = []
    
    for category, terms in age_vocab.items():
        for term in terms:
            # 对于年龄，模板中使用 {age}，需要插入具体的年龄描述
            # 但是词典中的术语本身就是描述，所以我们需要调整模板
            if "year" in term.lower() or any(char.isdigit() for char in term):
                # 如果包含年龄数字或year，直接使用
                profile = f"This is a {term} learner."
            else:
                # 对于描述性词语（如elderly, young等），使用不同的格式
                profile = f"This is an {term} learner." if term[0].lower() in 'aeiou' else f"This is a {term} learner."
            
            profiles.append({
                "attribute": "age",
                "category": category,
                "term": term,
                "profile": profile
            })
    
    return profiles


def generate_gender_profiles():
    """生成性别相关的用户画像"""
    gender_vocab = load_vocab("Gender_identity_vocab.json")
    profiles = []
    
    # 选择主要的性别类别
    main_categories = ["man", "woman", "boy", "girl", "F", "M", "trans", "nonTrans"]
    
    for category in main_categories:
        if category in gender_vocab:
            terms = gender_vocab[category]
            for term in terms:
                # 判断是否是名字（首字母大写且不是描述性词语）
                if term[0].isupper() and " " not in term:  # 如果是名字
                    # 对于名字，根据类别生成更合理的描述
                    if category in ["F", "nonTrans_F", "trans_F"]:
                        profile = f"This is a female learner named {term}."
                    elif category in ["M", "nonTrans_M", "trans_M"]:
                        profile = f"This is a male learner named {term}."
                    else:
                        profile = f"This is a learner named {term}."
                else:
                    profile = f"This is a {term} learner."
                
                profiles.append({
                    "attribute": "gender",
                    "category": category,
                    "term": term,
                    "profile": profile
                })
    
    return profiles


def generate_nationality_profiles():
    """生成国籍/地区相关的用户画像"""
    nationality_vocab = load_vocab("Nationality_vocab.json")
    profiles = []
    
    for region, nationalities in nationality_vocab.items():
        for nationality in nationalities:
            # 使用形容词形式描述国籍
            profile = f"This is a {nationality} learner."
            
            profiles.append({
                "attribute": "nationality",
                "category": region,
                "term": nationality,
                "profile": profile
            })
    
    return profiles


def generate_ses_profiles():
    """生成社会经济地位相关的用户画像"""
    ses_vocab = load_vocab("SES_vocab.json")
    profiles = []
    
    # 定义社会经济地位描述性词语
    ses_descriptors = ["low-income", "poor", "working-class", "affluent", "rich", "wealthy", 
                       "well off", "well-to-do", "quite rich", "very wealthy", "one percenter",
                       "on public assistance", "on welfare"]
    
    # 定义家庭相关词语
    family_terms = ["family", "CEO's family", "poor family", "wealthy family", 
                   "family on public assistance", "family on welfare"]
    
    for category, terms in ses_vocab.items():
        for term in terms:
            # 判断是否是名字
            if term[0].isupper() and len(term.split()) == 1:  # 如果是名字
                # 根据类别添加SES信息
                if category == "lowSES":
                    profile = f"This is a learner named {term} from a low-income background."
                else:
                    profile = f"This is a learner named {term} from an affluent background."
            elif term in family_terms:
                # 家庭相关描述
                profile = f"This learner comes from a {term}."
            elif term in ses_descriptors:
                # SES描述性词语
                profile = f"This learner comes from a {term} background."
            else:
                # 职业描述
                article = "an" if term[0].lower() in 'aeiou' else "a"
                profile = f"This learner is {article} {term}."
            
            profiles.append({
                "attribute": "ses",
                "category": category,
                "term": term,
                "profile": profile
            })
    
    return profiles


def generate_religion_profiles():
    """生成宗教信仰相关的用户画像"""
    religion_vocab = load_vocab("Religion_vocab.json")
    profiles = []
    
    for religion, terms in religion_vocab.items():
        for term in terms:
            profile = f"This learner identifies as {term}."
            
            profiles.append({
                "attribute": "religion",
                "category": religion,
                "term": term,
                "profile": profile
            })
    
    return profiles


def main():
    """主函数：生成所有用户画像并保存"""
    print("开始生成用户画像数据集...")
    
    # 生成各类用户画像
    all_profiles = []
    
    print("  生成年龄用户画像...")
    age_profiles = generate_age_profiles()
    all_profiles.extend(age_profiles)
    print(f"    生成了 {len(age_profiles)} 条年龄画像")
    
    print("  生成性别用户画像...")
    gender_profiles = generate_gender_profiles()
    all_profiles.extend(gender_profiles)
    print(f"    生成了 {len(gender_profiles)} 条性别画像")
    
    print("  生成国籍用户画像...")
    nationality_profiles = generate_nationality_profiles()
    all_profiles.extend(nationality_profiles)
    print(f"    生成了 {len(nationality_profiles)} 条国籍画像")
    
    print("  生成社会经济地位用户画像...")
    ses_profiles = generate_ses_profiles()
    all_profiles.extend(ses_profiles)
    print(f"    生成了 {len(ses_profiles)} 条SES画像")
    
    print("  生成宗教信仰用户画像...")
    religion_profiles = generate_religion_profiles()
    all_profiles.extend(religion_profiles)
    print(f"    生成了 {len(religion_profiles)} 条宗教画像")
    
    # 保存为JSON文件
    output_file = "/ai/tcy/tcy-exp/user_profiles_dataset.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_profiles, f, ensure_ascii=False, indent=2)
    
    print(f"\n总共生成了 {len(all_profiles)} 条用户画像")
    print(f"数据集已保存到: {output_file}")
    
    # 按属性分类保存
    print("\n按属性分类保存...")
    output_dir = "/ai/tcy/tcy-exp/user_profiles"
    os.makedirs(output_dir, exist_ok=True)
    
    # 按属性分组
    profiles_by_attr = {}
    for profile in all_profiles:
        attr = profile["attribute"]
        if attr not in profiles_by_attr:
            profiles_by_attr[attr] = []
        profiles_by_attr[attr].append(profile)
    
    # 分别保存
    for attr, profiles in profiles_by_attr.items():
        attr_file = os.path.join(output_dir, f"{attr}_profiles.json")
        with open(attr_file, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, ensure_ascii=False, indent=2)
        print(f"  {attr}: {len(profiles)} 条画像 -> {attr_file}")
    
    # 生成简单的文本版本（只包含画像描述）
    print("\n生成纯文本版本...")
    text_output = "/ai/tcy/tcy-exp/user_profiles_text.txt"
    with open(text_output, 'w', encoding='utf-8') as f:
        for profile in all_profiles:
            f.write(f"{profile['profile']}\n")
    print(f"纯文本版本已保存到: {text_output}")
    
    # 生成统计信息
    print("\n=== 统计信息 ===")
    for attr in sorted(profiles_by_attr.keys()):
        profiles = profiles_by_attr[attr]
        categories = set(p["category"] for p in profiles)
        print(f"{attr}:")
        print(f"  总数: {len(profiles)}")
        print(f"  类别数: {len(categories)}")
        print(f"  类别: {', '.join(sorted(categories))}")


if __name__ == "__main__":
    main()

