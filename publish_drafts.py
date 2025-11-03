#!/usr/bin/env python3
import json
import os
import shutil
from datetime import datetime

# Read metadata for posts
with open('source/_drafts/posts/_meta.json', 'r', encoding='utf-8') as f:
    posts_meta = json.load(f)

# Read metadata for notes
with open('source/_drafts/notes/_meta.json', 'r', encoding='utf-8') as f:
    notes_meta = json.load(f)

# Create notes directory if it doesn't exist
os.makedirs('source/notes', exist_ok=True)

def format_date(date_str):
    """Convert ISO date to Hexo format"""
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def publish_posts():
    """Publish all posts from drafts"""
    print("Publishing posts...")
    posts_dir = 'source/_drafts/posts'
    target_dir = 'source/_posts'
    
    for filename in os.listdir(posts_dir):
        if filename == '_meta.json' or not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(posts_dir, filename)
        
        # Find metadata for this post
        meta = None
        for post_id, post_meta in posts_meta.items():
            if post_meta.get('title') and filename.startswith(post_meta['title']):
                meta = post_meta
                break
        
        if not meta:
            # If no exact match, try to find by checking the filename
            for post_id, post_meta in posts_meta.items():
                title = post_meta.get('title', '')
                # Remove special characters for comparison
                if title in filename or filename.replace('.md', '') in title:
                    meta = post_meta
                    break
        
        # Read the original file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Prepare front matter
        title = filename.replace('.md', '')
        date = format_date(meta['created']) if meta else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        categories = []
        tags = []
        
        if meta:
            title = meta.get('title', title)
            if 'category' in meta:
                categories = [meta['category'].get('name', '')]
            if 'tags' in meta and isinstance(meta['tags'], list):
                tags = meta['tags']
        
        # Build front matter
        front_matter = ['---']
        front_matter.append(f'title: {title}')
        front_matter.append(f'date: {date}')
        
        if categories:
            front_matter.append('categories:')
            for cat in categories:
                if cat:
                    front_matter.append(f'  - {cat}')
        
        if tags:
            front_matter.append('tags:')
            for tag in tags:
                if tag:
                    front_matter.append(f'  - {tag}')
        
        front_matter.append('---')
        front_matter.append('')
        
        # Write to target
        target_path = os.path.join(target_dir, filename)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(front_matter))
            # Remove existing front matter if any
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2].lstrip()
            f.write(content)
        
        print(f'  ✓ Published: {title}')

def publish_notes():
    """Publish all notes from drafts"""
    print("\nPublishing notes...")
    notes_dir = 'source/_drafts/notes'
    target_dir = 'source/notes'
    
    for filename in os.listdir(notes_dir):
        if filename == '_meta.json' or not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(notes_dir, filename)
        
        # Find metadata for this note
        meta = None
        for note_id, note_meta in notes_meta.items():
            if note_meta.get('title') and filename.startswith(note_meta['title']):
                meta = note_meta
                break
        
        if not meta:
            # Try to find by checking the filename
            for note_id, note_meta in notes_meta.items():
                title = note_meta.get('title', '')
                if title in filename or filename.replace('.md', '') in title:
                    meta = note_meta
                    break
        
        # Read the original file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Prepare front matter
        title = filename.replace('.md', '')
        date = format_date(meta['created']) if meta else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if meta:
            title = meta.get('title', title)
        
        # Build front matter
        front_matter = ['---']
        front_matter.append(f'title: {title}')
        front_matter.append(f'date: {date}')
        front_matter.append('layout: page')
        front_matter.append('---')
        front_matter.append('')
        
        # Write to target
        target_path = os.path.join(target_dir, filename)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(front_matter))
            # Remove existing front matter if any
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2].lstrip()
            f.write(content)
        
        print(f'  ✓ Published: {title}')

def create_notes_index():
    """Create an index page for notes"""
    print("\nCreating notes index page...")
    index_path = 'source/notes/index.md'
    
    # Sort notes by date (newest first)
    sorted_notes = sorted(
        notes_meta.items(), 
        key=lambda x: x[1].get('created', ''), 
        reverse=True
    )
    
    content = ['---']
    content.append('title: 随笔')
    content.append('date: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    content.append('type: notes')
    content.append('layout: page')
    content.append('---')
    content.append('')
    content.append('# 随笔')
    content.append('')
    
    for note_id, note_meta in sorted_notes:
        title = note_meta.get('title', 'Untitled')
        created = note_meta.get('created', '')
        if created:
            date_obj = datetime.fromisoformat(created.replace('Z', '+00:00'))
            date_str = date_obj.strftime('%Y-%m-%d')
        else:
            date_str = ''
        
        # Find the corresponding file
        notes_dir = 'source/notes'
        found_file = None
        for filename in os.listdir(notes_dir):
            if filename.endswith('.md') and filename != 'index.md':
                with open(os.path.join(notes_dir, filename), 'r', encoding='utf-8') as f:
                    first_lines = f.read(200)
                    if f'title: {title}' in first_lines:
                        found_file = filename
                        break
        
        if found_file:
            # Use Hexo's post path format
            link = f'/notes/{found_file.replace(".md", "")}'
            content.append(f'- [{title}]({link}) - {date_str}')
        else:
            content.append(f'- {title} - {date_str}')
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f'  ✓ Created notes index')

if __name__ == '__main__':
    publish_posts()
    publish_notes()
    create_notes_index()
    print("\n✓ All drafts published successfully!")
