# Deployment Guide

## Overview
This guide explains how to deploy your updated Hexo blog with the new navigation bar and published posts/notes.

## What Was Changed

### 1. Navigation Bar Configuration
The navigation bar now includes 6 items:
- **Home** (首页) - `/`
- **博客** (Blog) - `/archives` - Shows all blog posts
- **随笔** (Essays/Notes) - `/notes` - Shows all essays/notes
- **项目** (Projects) - `/projects` - Project showcase
- **友链** (Links) - `/links` - Friend links
- **关于** (About) - `/about` - About page

### 2. Published Content
- **165 blog posts** moved from `source/_drafts/posts/` to `source/_posts/`
- **15 notes/essays** moved from `source/_drafts/notes/` to `source/notes/`
- All posts maintain their original creation dates from metadata
- A notes index page created at `source/notes/index.md`

## How to Deploy

### Step 1: Clean and Generate
```bash
cd /home/engine/project
npx hexo clean
npx hexo generate
```

### Step 2: Test Locally (Optional)
```bash
npx hexo server -p 4000
# Open http://localhost:4000 in your browser to verify
```

### Step 3: Deploy to GitHub Pages
```bash
npx hexo deploy
```

This will:
- Build the static site
- Push to the `gh-pages` branch of your repository
- Update your live site at https://moye12325.github.io

## Verification Checklist

After deployment, verify:

1. ✓ **Navigation Bar**: All 6 items are visible and clickable
2. ✓ **博客 (Blog)**: Click to see archives with all 165 posts
3. ✓ **随笔 (Essays)**: Click to see notes index with 15 entries
4. ✓ **Individual Posts**: Click any post to ensure it displays correctly
5. ✓ **Individual Notes**: Click any note to ensure it displays correctly
6. ✓ **Categories & Tags**: Verify categorization is working
7. ✓ **Mobile View**: Check navigation works on mobile devices

## File Structure

```
source/
├── _posts/          # 165 blog posts
├── notes/           # 15 notes/essays
│   └── index.md     # Notes index page
├── about/
├── archives/
├── categories/
├── links/
├── projects/
└── tags/
```

## Troubleshooting

### Issue: Posts not showing
- Run `npx hexo clean` then `npx hexo generate` again

### Issue: Navigation not displaying
- Check `_config.redefine.yml` navbar configuration
- Ensure all paths start with `/`

### Issue: Notes page empty
- Verify `source/notes/index.md` exists
- Check that note files have proper front matter

## Next Steps

After successful deployment:
1. Visit your site at https://moye12325.github.io
2. Click through each navigation item to verify functionality
3. Test a few blog posts and notes to ensure content displays correctly
4. Check mobile responsiveness

## Support

If you encounter issues:
1. Check the Hexo logs: `npx hexo generate --debug`
2. Review theme documentation: https://github.com/EvanNotFound/hexo-theme-redefine
3. Verify Git deployment settings in `_config.yml`
