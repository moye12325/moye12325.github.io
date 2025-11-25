import os
import re
from pathlib import Path

# 定义分类规则
CATEGORY_RULES = {
    '数据结构与算法': [
        '稀疏数组', '队列', '链表', '栈', '递归', '排序', '查找', '哈希',
        'HashTable', 'HashMap', '波兰式', '中缀', '后缀'
    ],
    '深度学习': [
        '深度学习', '李沐', '神经网络', 'CNN', 'RNN', 'LSTM', 'GRU',
        'Transformer', 'BERT', 'ResNet', 'AlexNet', 'NiN', 'seq2seq',
        '注意力', 'Attention', '卷积', '池化', '优化算法', 'GPU'
    ],
    '机器学习': [
        '机器学习', '李宏毅', 'GAN', 'Domain Adaptation', 'Life long learning',
        '强化学习', 'Reinforcement Learning', 'Explainable AI', 'NLP',
        '自监督', 'Self-supervised'
    ],
    'Python开发': [
        'Python', 'python', 'conda', 'pip', '模块', 'setup.py', '.pth',
        'pyproject.toml', 'requirements.txt'
    ],
    'Web开发': [
        'nginx', 'MyBatis', 'RabbitMQ', 'JumpServer', '部署', '端口转发',
        '403', '服务器'
    ],
    '开发工具': [
        'VSCode', 'vscode', 'Git', 'GitHub', 'Navicat', 'wallhaven', '爬虫'
    ],
    '量子计算': [
        'Llama', 'LLM', '大模型', '神经符号', '知识图'
    ],
    '面试笔试': [
        '校招', '笔试', '面试', '编程题', '360', '百度', '美团', '小米',
        '西山居', '米哈游'
    ],
    '学习笔记': [
        'Homework', 'HW', 'hw', '词性对照表', '比赛记录'
    ]
}

def detect_category(title, content):
    """根据标题和内容检测分类"""
    text = title + ' ' + content[:500]  # 只检查前500字符
    
    scores = {}
    for category, keywords in CATEGORY_RULES.items():
        score = sum(1 for keyword in keywords if keyword.lower() in text.lower())
        if score > 0:
            scores[category] = score
    
    if scores:
        return max(scores, key=scores.get)
    return '其他'

def extract_tags(title, content):
    """从标题和内容中提取标签"""
    tags = set()
    text = title + ' ' + content[:1000]
    
    # 技术栈标签
    tech_keywords = {
        'Python': ['python', 'Python'],
        'Java': ['java', 'Java'],
        'JavaScript': ['javascript', 'js'],
        'C++': ['c++', 'C++'],
        '深度学习': ['深度学习', 'Deep Learning'],
        '机器学习': ['机器学习', 'Machine Learning'],
        'PyTorch': ['pytorch', 'PyTorch'],
        'TensorFlow': ['tensorflow', 'TensorFlow'],
        'Nginx': ['nginx', 'Nginx'],
        'Docker': ['docker', 'Docker'],
        'Git': ['git', 'Git'],
        '算法': ['算法', 'Algorithm'],
        '数据结构': ['数据结构', 'Data Structure'],
    }
    
    for tag, keywords in tech_keywords.items():
        if any(kw in text for kw in keywords):
            tags.add(tag)
    
    return list(tags)[:5]  # 最多5个标签

def update_frontmatter(filepath):
    """更新文章的front matter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取现有的front matter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        print(f"跳过 {filepath.name}: 没有front matter")
        return False
    
    frontmatter = match.group(1)
    body = match.group(2)
    
    # 提取标题
    title_match = re.search(r'title:\s*(.+)', frontmatter)
    if not title_match:
        print(f"跳过 {filepath.name}: 没有标题")
        return False
    
    title = title_match.group(1).strip()
    
    # 检测分类和标签
    category = detect_category(title, body)
    tags = extract_tags(title, body)
    
    # 提取现有的date
    date_match = re.search(r'date:\s*(.+)', frontmatter)
    date = date_match.group(1).strip() if date_match else '2024-07-22 00:00:00'
    
    # 构建新的front matter
    new_frontmatter = f"""---
title: {title}
date: {date}
categories: [{category}]
tags: {tags}
---"""
    
    new_content = new_frontmatter + '\n' + body
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 更新 {filepath.name}: {category} | {tags}")
    return True

def main():
    posts_dir = Path('source/_posts')
    
    if not posts_dir.exists():
        print("错误: source/_posts 目录不存在")
        return
    
    md_files = list(posts_dir.glob('*.md'))
    print(f"找到 {len(md_files)} 篇文章\n")
    
    updated = 0
    for filepath in md_files:
        if filepath.name == 'hello-world.md':
            continue  # 跳过默认文章
        
        try:
            if update_frontmatter(filepath):
                updated += 1
        except Exception as e:
            print(f"❌ 处理 {filepath.name} 时出错: {e}")
    
    print(f"\n完成! 共更新 {updated}/{len(md_files)} 篇文章")

if __name__ == '__main__':
    main()
