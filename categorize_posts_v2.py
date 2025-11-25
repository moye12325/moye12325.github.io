import os
import re
from pathlib import Path
from collections import defaultdict

# 详细的分类规则和关键词
CATEGORY_KEYWORDS = {
    '深度学习': {
        'keywords': [
            '深度学习', '李沐', '神经网络', 'CNN', 'RNN', 'LSTM', 'GRU', 'Transformer',
            'BERT', 'ResNet', 'AlexNet', 'NiN', 'seq2seq', '注意力', 'Attention',
            '卷积', '池化', '优化算法', 'BatchSize', '梯度', '反向传播', '前向传播',
            '批量规范化', 'Dropout', '权重衰退', 'FCN', 'R-CNN', 'YOLO', 'SSD',
            '语义分割', '目标检测', '图像分类', '样式迁移', '微调'
        ],
        'weight': 1.5
    },
    '机器学习': {
        'keywords': [
            '机器学习', '李宏毅', 'GAN', 'Domain Adaptation', 'Life long learning',
            '强化学习', 'Reinforcement Learning', 'Explainable AI', 'NLP',
            '自监督', 'Self-supervised', 'Homework', 'HW'
        ],
        'weight': 1.3
    },
    '数据结构与算法': {
        'keywords': [
            '稀疏数组', '队列', '链表', '栈', '递归', '排序', '查找', '哈希',
            'HashTable', 'HashMap', '波兰式', '中缀', '后缀', 'LeetCode',
            '算法', '数据结构', '二叉树', '图', '动态规划', '贪心', '回溯',
            '滑动窗口', '双指针', '快慢指针'
        ],
        'weight': 1.2
    },
    'Python开发': {
        'keywords': [
            'Python', 'python', 'conda', 'pip', '模块', 'setup.py', '.pth',
            'pyproject.toml', 'requirements.txt', '多线程', '多进程', '协程',
            'asyncio', 'PyTorch', 'TensorFlow', 'numpy', 'pandas'
        ],
        'weight': 1.0
    },
    'Java开发': {
        'keywords': [
            'Java', 'java', 'JVM', '并发', '集合', '数据类型', '位运算',
            'Spring', 'SpringBoot', '双亲委派'
        ],
        'weight': 1.0
    },
    'Web开发': {
        'keywords': [
            'nginx', 'Nginx', 'MyBatis', 'RabbitMQ', 'JumpServer', '部署',
            '端口转发', '403', '404', '服务器', 'server', 'MySQL', 'Redis',
            'MVCC', '数据库', '前后端分离'
        ],
        'weight': 1.0
    },
    '开发工具': {
        'keywords': [
            'VSCode', 'vscode', 'Git', 'GitHub', 'Navicat', 'Docker',
            'docker', 'WSL', 'Windows Server', 'sftp', 'ZeroMQ'
        ],
        'weight': 1.0
    },
    '测试': {
        'keywords': [
            '测试', 'Test', 'testing', '缺陷', '接口测试', 'Software Testing',
            'Test Design'
        ],
        'weight': 1.0
    },
    '面试笔试': {
        'keywords': [
            '校招', '笔试', '面试', '编程题', '360', '百度', '美团', '小米',
            '西山居', '米哈游', '去哪儿'
        ],
        'weight': 1.0
    },
    '量子计算': {
        'keywords': [
            'Llama', 'LLM', '大模型', '神经符号', '知识图', '量子门', '量子'
        ],
        'weight': 1.0
    },
    '随笔': {
        'keywords': [
            '共鸣', '记录', '归校', '美元潮汐', '伸手党', '词性对照表',
            '比赛记录', 'resume', 'reasoning'
        ],
        'weight': 0.8
    }
}

# 标签提取规则
TAG_RULES = {
    # 编程语言
    'Python': ['python', 'Python', '.py', 'pip', 'conda'],
    'Java': ['java', 'Java', '.java', 'JVM'],
    'JavaScript': ['javascript', 'js', 'JavaScript', 'JS'],
    
    # 深度学习框架
    'PyTorch': ['pytorch', 'PyTorch', 'torch'],
    'TensorFlow': ['tensorflow', 'TensorFlow'],
    
    # 深度学习相关
    '深度学习': ['深度学习', 'Deep Learning', 'DL'],
    '机器学习': ['机器学习', 'Machine Learning', 'ML'],
    '神经网络': ['神经网络', 'Neural Network', 'CNN', 'RNN'],
    'Transformer': ['Transformer', 'transformer', 'BERT', 'GPT'],
    '计算机视觉': ['CV', '图像', '目标检测', '语义分割', '图像分类'],
    'NLP': ['NLP', '自然语言', 'Natural Language'],
    
    # 数据结构与算法
    '算法': ['算法', 'Algorithm', 'algorithm'],
    '数据结构': ['数据结构', 'Data Structure', '链表', '栈', '队列', '树'],
    'LeetCode': ['LeetCode', 'leetcode', 'Leetcode'],
    
    # Web开发
    'Nginx': ['nginx', 'Nginx'],
    'MyBatis': ['mybatis', 'MyBatis'],
    'Spring': ['spring', 'Spring', 'SpringBoot'],
    'Redis': ['redis', 'Redis'],
    'MySQL': ['mysql', 'MySQL', 'sql', 'SQL'],
    'Docker': ['docker', 'Docker', '容器'],
    
    # 工具
    'Git': ['git', 'Git', 'GitHub', 'github'],
    'VSCode': ['vscode', 'VSCode', 'VS Code'],
    
    # 其他
    '部署': ['部署', 'deploy', 'deployment'],
    '测试': ['测试', 'test', 'Test', 'Testing'],
    '面试': ['面试', '笔试', 'interview'],
    '性能优化': ['优化', '性能', 'performance', 'optimization'],
}

def analyze_content(title, content):
    """深度分析文章内容"""
    # 合并标题和内容前2000字符
    text = f"{title} " * 3 + content[:2000]  # 标题权重更高
    text_lower = text.lower()
    
    # 计算每个分类的得分
    category_scores = defaultdict(float)
    
    for category, config in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in config['keywords']:
            # 关键词匹配次数
            count = text.count(keyword)
            if count > 0:
                score += count * config['weight']
        
        if score > 0:
            category_scores[category] = score
    
    # 选择得分最高的分类
    if category_scores:
        best_category = max(category_scores, key=category_scores.get)
        return best_category
    
    return '其他'

def extract_tags(title, content):
    """提取标签"""
    text = title + ' ' + content[:1500]
    tags = set()
    
    for tag, keywords in TAG_RULES.items():
        for keyword in keywords:
            if keyword in text:
                tags.add(tag)
                break
    
    # 限制标签数量
    return sorted(list(tags))[:6]

def update_article_metadata(filepath):
    """更新单篇文章的元数据"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 读取失败 {filepath.name}: {e}")
        return False
    
    # 提取front matter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        print(f"⚠️  跳过 {filepath.name}: 没有front matter")
        return False
    
    frontmatter = match.group(1)
    body = match.group(2)
    
    # 提取标题
    title_match = re.search(r'title:\s*(.+)', frontmatter)
    if not title_match:
        print(f"⚠️  跳过 {filepath.name}: 没有标题")
        return False
    
    title = title_match.group(1).strip()
    
    # 提取日期
    date_match = re.search(r'date:\s*(.+)', frontmatter)
    date = date_match.group(1).strip() if date_match else '2024-07-22 00:00:00'
    
    # 检查是否有密码保护
    password_match = re.search(r'password:\s*(.+)', frontmatter)
    password = password_match.group(1).strip() if password_match else None
    
    # 分析内容
    category = analyze_content(title, body)
    tags = extract_tags(title, body)
    
    # 构建新的front matter
    new_frontmatter = f"""---
title: {title}
date: {date}
categories: [{category}]
tags: {tags}"""
    
    if password:
        new_frontmatter += f"\npassword: {password}"
    
    new_frontmatter += "\n---"
    
    new_content = new_frontmatter + '\n' + body
    
    # 写回文件
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ {filepath.name}")
        print(f"   分类: {category} | 标签: {tags}")
        return True
    except Exception as e:
        print(f"❌ 写入失败 {filepath.name}: {e}")
        return False

def main():
    posts_dir = Path('source/_posts')
    
    if not posts_dir.exists():
        print("❌ 错误: source/_posts 目录不存在")
        return
    
    md_files = sorted(posts_dir.glob('*.md'))
    print(f"📚 找到 {len(md_files)} 篇文章\n")
    
    # 统计
    stats = defaultdict(int)
    updated = 0
    
    for filepath in md_files:
        if filepath.name == 'hello-world.md':
            continue
        
        if update_article_metadata(filepath):
            updated += 1
    
    print(f"\n✨ 完成! 成功更新 {updated}/{len(md_files)} 篇文章")

if __name__ == '__main__':
    main()
