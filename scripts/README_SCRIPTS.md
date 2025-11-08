# Hexo Blog Migration Scripts

This directory contains scripts for managing the Hexo blog content.

## migrate-drafts.js

A comprehensive migration script that moves draft posts and notes from `source/_drafts/` to their appropriate published locations.

### Features

- ✅ Reads metadata from `_meta.json` files for both posts and notes
- ✅ Pairs metadata entries with their corresponding Markdown files
- ✅ Parses existing front matter using `gray-matter`
- ✅ Rebuilds Hexo-compliant front matter with:
  - `title`: Article title
  - `date`: Creation date in `YYYY-MM-DD HH:mm:ss` format
  - `updated`: Last modification date (omitted if absent)
  - `categories`: 
    - For notes: Forced to `[随笔]`
    - For posts: Uses `meta.category.name`
  - `tags`: Tags from metadata
  - `summary`: 
    - Uses provided summary if available
    - Auto-generates from first 200 characters of body text if null
- ✅ Generates safe filenames from slugs (fallback to sanitized titles)
- ✅ Preserves 七牛云图片外链 (Qiniu cloud image links)
- ✅ Creates backup of all draft files before migration
- ✅ Idempotency: Skips files that already exist in target locations

### Directory Structure

**Source:**
- `source/_drafts/posts/` - Draft blog posts
- `source/_drafts/notes/` - Draft notes/essays

**Target:**
- `source/_posts/` - Published blog posts
- `source/_posts/notes/` - Published notes/essays

**Backup:**
- `.backup_drafts/` - Backup of original draft files

### Usage

```bash
# Run the migration
npm run migrate

# Or directly
node scripts/migrate-drafts.js
```

### After Migration

1. Clean Hexo cache:
   ```bash
   npx hexo clean
   ```

2. Generate site:
   ```bash
   npx hexo generate
   ```

3. Preview locally:
   ```bash
   npx hexo server
   ```

4. Verify the migrated content in your browser

5. If satisfied, you can optionally remove the draft directories:
   ```bash
   # Optional: Remove draft directories
   rm -rf source/_drafts/posts
   rm -rf source/_drafts/notes
   ```

### Restoration

If you need to restore the original drafts, they are backed up in `.backup_drafts/`:

```bash
# Restore from backup
cp -r .backup_drafts/posts/* source/_drafts/posts/
cp -r .backup_drafts/notes/* source/_drafts/notes/
```

### Dependencies

- `gray-matter` - Front matter parser
- `slugify` - Filename sanitization

### Technical Details

#### Timestamp Formatting

Converts ISO 8601 timestamps (e.g., `2024-07-18T12:26:14.976Z`) to Hexo format (e.g., `2024-07-18 12:26:14`).

#### Summary Generation

When a summary is null or empty:
1. Extracts the body content
2. Removes Markdown syntax (headings, bold, links, code blocks, images)
3. Takes first 200 characters
4. Preserves original summaries when provided

#### Filename Generation

1. Prefers using slug from metadata
2. Falls back to sanitized title if slug is invalid
3. For notes, uses `note-{nid}` format where possible
4. Removes problematic characters: `*+~.()'"!:@`

### Migration Statistics

The script provides detailed statistics after execution:
- Success: Number of successfully migrated files
- Skipped: Number of files that already exist (idempotency)
- Errors: Number of files that failed to migrate

### Troubleshooting

**Issue:** Script reports missing markdown files
- **Solution:** Check that filenames match the titles in `_meta.json`

**Issue:** Encoding problems with Chinese characters
- **Solution:** Ensure all files are UTF-8 encoded

**Issue:** Qiniu image links broken
- **Solution:** The script preserves all links; verify the original files contain correct URLs

### Version History

- **v1.0** (2024-11-03): Initial implementation
  - Basic migration functionality
  - Auto-summary generation
  - Idempotency support
  - Backup mechanism
