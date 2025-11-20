import os
import re

def get_title(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if match:
                fm = match.group(1)
                title_match = re.search(r'^title:\s*(.*)$', fm, re.MULTILINE)
                if title_match:
                    return title_match.group(1).strip()
    except Exception:
        pass
    return None

def check_notes_overlap():
    notes_drafts_dir = 'source/_drafts/notes'
    posts_dir = 'source/_posts'
    notes_dir = 'source/notes'
    
    draft_notes = set()
    if os.path.exists(notes_drafts_dir):
        for f in os.listdir(notes_drafts_dir):
            if f.endswith('.md') and f != '_meta.json':
                draft_notes.add(f)
                
    print(f"Found {len(draft_notes)} notes in drafts.")
    
    # Check if these exist in _posts
    print("\nChecking for notes mistakenly placed in _posts:")
    for filename in os.listdir(posts_dir):
        if filename in draft_notes:
            print(f"  - Found exact filename match in _posts: {filename}")
            continue
            
        # Check title match
        filepath = os.path.join(posts_dir, filename)
        title = get_title(filepath)
        if title:
            # Simple heuristic: check if title matches a draft filename (minus extension)
            # or if title matches a draft note's title (would need to read draft note title)
            pass

    # Also check if they exist in source/notes (they should)
    # But if they are in BOTH, that's fine, as long as they are not in _posts.
    # The issue is likely they are in _posts AND source/notes.
    
    # Let's check titles of all files in _posts against titles of all files in _drafts/notes
    draft_titles = {}
    for f in draft_notes:
        path = os.path.join(notes_drafts_dir, f)
        t = get_title(path)
        if t:
            draft_titles[t] = f
            
    print("\nChecking for title matches in _posts:")
    for filename in os.listdir(posts_dir):
        path = os.path.join(posts_dir, filename)
        t = get_title(path)
        if t and t in draft_titles:
            print(f"  - Post '{filename}' has same title as Note '{draft_titles[t]}': {t}")

if __name__ == "__main__":
    check_notes_overlap()
