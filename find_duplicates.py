import os
import re
from collections import defaultdict

def parse_front_matter(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if match:
                fm = match.group(1)
                title_match = re.search(r'^title:\s*(.*)$', fm, re.MULTILINE)
                if title_match:
                    return title_match.group(1).strip()
    except Exception as e:
        pass
    return None

def find_duplicates():
    posts_dir = 'source/_posts'
    drafts_dir = 'source/_drafts/posts'
    
    draft_files = set(os.listdir(drafts_dir)) if os.path.exists(drafts_dir) else set()
    
    title_map = defaultdict(list)
    
    for filename in os.listdir(posts_dir):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(posts_dir, filename)
        title = parse_front_matter(filepath)
        
        if title:
            # Normalize title to handle potential minor differences if needed, 
            # but exact match is usually what causes "duplicate posts" in Hexo if slugs differ but titles are same.
            # Actually Hexo allows same titles, but they show up as two posts.
            title_map[title].append(filename)
            
    duplicates = {k: v for k, v in title_map.items() if len(v) > 1}
    
    print(f"Found {len(duplicates)} sets of duplicates.")
    
    for title, filenames in duplicates.items():
        print(f"\nTitle: {title}")
        for fname in filenames:
            in_drafts = fname in draft_files
            print(f"  - {fname} (In Drafts: {in_drafts})")

if __name__ == "__main__":
    find_duplicates()
