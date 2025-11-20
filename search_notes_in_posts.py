import os

def search_posts():
    posts_dir = 'source/_posts'
    keywords = ['记录', '随笔', '总结', '归校', '看法', '我回来了']
    
    print(f"Searching {posts_dir} for keywords: {keywords}")
    
    found = []
    for filename in os.listdir(posts_dir):
        if any(k in filename for k in keywords):
            found.append(filename)
            
    print(f"Found {len(found)} files:")
    for f in found:
        print(f"  - {f}")

if __name__ == "__main__":
    search_posts()
