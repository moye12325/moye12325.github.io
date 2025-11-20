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
                    return title_match.group(1).strip().strip('"').strip("'")
    except Exception as e:
        pass
    return None

def cleanup_duplicates():
    posts_dir = 'source/_posts'
    
    title_map = defaultdict(list)
    
    print("Scanning for duplicates in _posts...")
    # Recursive walk
    for root, dirs, files in os.walk(posts_dir):
        for filename in files:
            if not filename.endswith('.md'):
                continue
                
            filepath = os.path.join(root, filename)
            title = parse_front_matter(filepath)
            
            if title:
                title_map[title].append(filepath)
            
    duplicates = {k: v for k, v in title_map.items() if len(v) > 1}
    
    print(f"Found {len(duplicates)} sets of duplicates.")
    
    deleted_count = 0
    
    for title, filepaths in duplicates.items():
        print(f"\nProcessing duplicate title: '{title}'")
        
        # Check if we have a "note-X.md" vs "Descriptive.md" pattern
        note_files = []
        other_files = []
        
        for fp in filepaths:
            filename = os.path.basename(fp)
            if re.match(r'^note-\d+\.md$', filename):
                note_files.append(fp)
            else:
                other_files.append(fp)
        
        if note_files and other_files:
            # We have at least one note-X.md and at least one other file.
            # Delete the note-X.md files.
            for nf in note_files:
                try:
                    os.remove(nf)
                    print(f"  - Deleted: {nf} (Duplicate of {other_files[0]})")
                    deleted_count += 1
                except Exception as e:
                    print(f"  - Error deleting {nf}: {e}")
        else:
            print(f"  - Skipping: No clear 'note-X.md' vs 'Descriptive.md' pattern. Files: {[os.path.basename(f) for f in filepaths]}")

    print(f"\nCleanup complete. Deleted {deleted_count} files.")

if __name__ == "__main__":
    cleanup_duplicates()
