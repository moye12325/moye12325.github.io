import os
import hashlib
from collections import defaultdict

def get_content_hash(filepath):
    """Calculate MD5 hash of file content, ignoring front matter."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Remove front matter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2].strip()
            return hashlib.md5(content.encode('utf-8')).hexdigest()
    except Exception:
        return None

def find_cross_duplicates():
    posts_dir = 'source/_posts'
    notes_dir = 'source/notes'
    
    # Map hash to list of (directory, filename)
    content_map = defaultdict(list)
    
    print("Scanning for cross-directory duplicates...")
    
    # Scan posts
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            c_hash = get_content_hash(filepath)
            if c_hash:
                content_map[c_hash].append(('posts', filename))
                
    # Scan notes
    if os.path.exists(notes_dir):
        for filename in os.listdir(notes_dir):
            if filename.endswith('.md') and filename != 'index.md':
                filepath = os.path.join(notes_dir, filename)
                c_hash = get_content_hash(filepath)
                if c_hash:
                    content_map[c_hash].append(('notes', filename))
    
    # Report duplicates
    dupes = {k: v for k, v in content_map.items() if len(v) > 1}
    if dupes:
        print(f"\nFound {len(dupes)} sets of duplicates:")
        for h, files in dupes.items():
            print(f"  Hash {h}:")
            for d, f in files:
                print(f"    - [{d}] {f}")
    else:
        print("\nNo duplicates found between posts and notes.")

if __name__ == "__main__":
    find_cross_duplicates()
