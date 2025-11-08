const fs = require('fs');
const path = require('path');

// Try to load gray-matter, but don't fail if it's not available
let matter;
try {
  matter = require('gray-matter');
} catch (e) {
  console.warn('Warning: gray-matter module not found. Migration script will not work.');
  console.warn('To use migration, run: npm install gray-matter');
  matter = null;
}

// Try to load slugify, but don't fail if it's not available
let slugify;
try {
  slugify = require('slugify');
} catch (e) {
  console.warn('Warning: slugify module not found. Migration script will not work.');
  console.warn('To use migration, run: npm install slugify');
  slugify = null;
}

// Paths
const DRAFTS_POSTS_DIR = path.join(__dirname, '../source/_drafts/posts');
const DRAFTS_NOTES_DIR = path.join(__dirname, '../source/_drafts/notes');
const POSTS_DIR = path.join(__dirname, '../source/_posts');
const NOTES_DIR = path.join(__dirname, '../source/_posts/notes');
const BACKUP_DIR = path.join(__dirname, '../.backup_drafts');

// Ensure target directories exist
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// Format timestamp to YYYY-MM-DD HH:mm:ss
function formatTimestamp(timestamp) {
  if (!timestamp) return null;
  const date = new Date(timestamp);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

// Generate safe filename from slug or title
function generateSafeFilename(slug, title) {
  // If slug exists and is meaningful, use it
  if (slug && slug !== 'null' && slug !== 'undefined' && slug.trim() !== '') {
    return slugify(slug, { lower: false, strict: false, remove: /[*+~.()'"!:@]/g });
  }
  
  // Fallback to sanitized title
  return slugify(title, { lower: false, strict: false, remove: /[*+~.()'"!:@]/g });
}

// Extract first 200 characters from markdown body for summary
function extractSummary(content, maxLength = 200) {
  // Remove front matter
  const { content: bodyContent } = matter(content);
  
  // Remove markdown syntax
  let text = bodyContent
    .replace(/^#{1,6}\s+/gm, '') // Remove headings
    .replace(/\*\*(.+?)\*\*/g, '$1') // Remove bold
    .replace(/\*(.+?)\*/g, '$1') // Remove italic
    .replace(/\[(.+?)\]\(.+?\)/g, '$1') // Remove links
    .replace(/```[\s\S]*?```/g, '') // Remove code blocks
    .replace(/`(.+?)`/g, '$1') // Remove inline code
    .replace(/!\[.*?\]\(.*?\)/g, '') // Remove images
    .replace(/\n+/g, ' ') // Replace newlines with spaces
    .trim();
  
  // Return first maxLength characters
  return text.length > maxLength ? text.substring(0, maxLength) : text;
}

// Backup drafts before migration
function backupDrafts() {
  console.log('📦 Creating backup of draft files...');
  ensureDir(BACKUP_DIR);
  
  const backupPosts = path.join(BACKUP_DIR, 'posts');
  const backupNotes = path.join(BACKUP_DIR, 'notes');
  
  ensureDir(backupPosts);
  ensureDir(backupNotes);
  
  // Backup posts
  if (fs.existsSync(DRAFTS_POSTS_DIR)) {
    const files = fs.readdirSync(DRAFTS_POSTS_DIR);
    files.forEach(file => {
      const srcPath = path.join(DRAFTS_POSTS_DIR, file);
      const destPath = path.join(backupPosts, file);
      fs.copyFileSync(srcPath, destPath);
    });
  }
  
  // Backup notes
  if (fs.existsSync(DRAFTS_NOTES_DIR)) {
    const files = fs.readdirSync(DRAFTS_NOTES_DIR);
    files.forEach(file => {
      const srcPath = path.join(DRAFTS_NOTES_DIR, file);
      const destPath = path.join(backupNotes, file);
      fs.copyFileSync(srcPath, destPath);
    });
  }
  
  console.log('✅ Backup completed at:', BACKUP_DIR);
}

// Migrate posts
function migratePosts() {
  console.log('\n📝 Migrating blog posts...');
  
  const metaPath = path.join(DRAFTS_POSTS_DIR, '_meta.json');
  if (!fs.existsSync(metaPath)) {
    console.log('⚠️  No _meta.json found for posts');
    return;
  }
  
  const metadata = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
  let successCount = 0;
  let skipCount = 0;
  let errorCount = 0;
  
  Object.entries(metadata).forEach(([id, meta]) => {
    try {
      const title = meta.title;
      const slug = meta.slug;
      
      // Find matching markdown file
      const files = fs.readdirSync(DRAFTS_POSTS_DIR).filter(f => f.endsWith('.md'));
      let matchedFile = null;
      
      for (const file of files) {
        const content = fs.readFileSync(path.join(DRAFTS_POSTS_DIR, file), 'utf8');
        const parsed = matter(content);
        if (parsed.data.title === title || parsed.data.oid === id || file.includes(title)) {
          matchedFile = file;
          break;
        }
      }
      
      if (!matchedFile) {
        console.log(`⚠️  No markdown file found for: ${title}`);
        skipCount++;
        return;
      }
      
      const filePath = path.join(DRAFTS_POSTS_DIR, matchedFile);
      const content = fs.readFileSync(filePath, 'utf8');
      const parsed = matter(content);
      
      // Build new front matter
      const newFrontMatter = {
        title: title,
        date: formatTimestamp(meta.created),
      };
      
      // Add updated if exists
      if (meta.modified) {
        newFrontMatter.updated = formatTimestamp(meta.modified);
      }
      
      // Add categories
      if (meta.category && meta.category.name) {
        newFrontMatter.categories = [meta.category.name];
      }
      
      // Add tags
      if (meta.tags && meta.tags.length > 0) {
        newFrontMatter.tags = meta.tags;
      }
      
      // Add summary
      if (meta.summary && meta.summary !== null && meta.summary.trim() !== '') {
        newFrontMatter.summary = meta.summary;
      } else {
        // Generate summary from first 200 chars of body
        const autoSummary = extractSummary(content);
        if (autoSummary) {
          newFrontMatter.summary = autoSummary;
        }
      }
      
      // Generate safe filename
      const safeFilename = generateSafeFilename(slug, title) + '.md';
      const targetPath = path.join(POSTS_DIR, safeFilename);
      
      // Check if file already exists (idempotency)
      if (fs.existsSync(targetPath)) {
        console.log(`⏭️  Skipping (already exists): ${safeFilename}`);
        skipCount++;
        return;
      }
      
      // Create new file with updated front matter
      const newContent = matter.stringify(parsed.content, newFrontMatter);
      
      // Write to target location
      fs.writeFileSync(targetPath, newContent, 'utf8');
      console.log(`✅ Migrated: ${matchedFile} → ${safeFilename}`);
      successCount++;
      
    } catch (error) {
      console.error(`❌ Error migrating post ${meta.title}:`, error.message);
      errorCount++;
    }
  });
  
  console.log(`\n📊 Posts migration summary:`);
  console.log(`   Success: ${successCount}`);
  console.log(`   Skipped: ${skipCount}`);
  console.log(`   Errors: ${errorCount}`);
}

// Migrate notes
function migrateNotes() {
  console.log('\n📓 Migrating notes...');
  
  const metaPath = path.join(DRAFTS_NOTES_DIR, '_meta.json');
  if (!fs.existsSync(metaPath)) {
    console.log('⚠️  No _meta.json found for notes');
    return;
  }
  
  const metadata = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
  let successCount = 0;
  let skipCount = 0;
  let errorCount = 0;
  
  Object.entries(metadata).forEach(([id, meta]) => {
    try {
      const title = meta.title;
      const nid = meta.nid;
      
      // Find matching markdown file
      const files = fs.readdirSync(DRAFTS_NOTES_DIR).filter(f => f.endsWith('.md'));
      let matchedFile = null;
      
      for (const file of files) {
        const content = fs.readFileSync(path.join(DRAFTS_NOTES_DIR, file), 'utf8');
        const parsed = matter(content);
        if (parsed.data.title === title || parsed.data.oid === id || file.includes(title)) {
          matchedFile = file;
          break;
        }
      }
      
      if (!matchedFile) {
        console.log(`⚠️  No markdown file found for: ${title}`);
        skipCount++;
        return;
      }
      
      const filePath = path.join(DRAFTS_NOTES_DIR, matchedFile);
      const content = fs.readFileSync(filePath, 'utf8');
      const parsed = matter(content);
      
      // Build new front matter
      const newFrontMatter = {
        title: title,
        date: formatTimestamp(meta.created),
      };
      
      // Add updated if exists
      if (meta.modified) {
        newFrontMatter.updated = formatTimestamp(meta.modified);
      }
      
      // Force categories to [随笔] for notes
      newFrontMatter.categories = ['随笔'];
      
      // Add tags if exists
      if (meta.tags && meta.tags.length > 0) {
        newFrontMatter.tags = meta.tags;
      }
      
      // Add summary
      if (meta.summary && meta.summary !== null && meta.summary.trim() !== '') {
        newFrontMatter.summary = meta.summary;
      } else {
        // Generate summary from first 200 chars of body
        const autoSummary = extractSummary(content);
        if (autoSummary) {
          newFrontMatter.summary = autoSummary;
        }
      }
      
      // Generate safe filename (prefer using nid for notes)
      const safeFilename = generateSafeFilename(nid ? `note-${nid}` : null, title) + '.md';
      const targetPath = path.join(NOTES_DIR, safeFilename);
      
      // Check if file already exists (idempotency)
      if (fs.existsSync(targetPath)) {
        console.log(`⏭️  Skipping (already exists): ${safeFilename}`);
        skipCount++;
        return;
      }
      
      // Create new file with updated front matter
      const newContent = matter.stringify(parsed.content, newFrontMatter);
      
      // Write to target location
      fs.writeFileSync(targetPath, newContent, 'utf8');
      console.log(`✅ Migrated: ${matchedFile} → ${safeFilename}`);
      successCount++;
      
    } catch (error) {
      console.error(`❌ Error migrating note ${meta.title}:`, error.message);
      errorCount++;
    }
  });
  
  console.log(`\n📊 Notes migration summary:`);
  console.log(`   Success: ${successCount}`);
  console.log(`   Skipped: ${skipCount}`);
  console.log(`   Errors: ${errorCount}`);
}

// Main migration function
function main() {
  // Check if required modules are available
  if (!matter || !slugify) {
    console.error('❌ Error: Required modules are not installed.');
    if (!matter) console.error('  - gray-matter');
    if (!slugify) console.error('  - slugify');
    console.error('Please install them with: npm install gray-matter slugify');
    process.exit(1);
  }

  console.log('🚀 Starting draft migration...\n');

  // Ensure target directories exist
  ensureDir(POSTS_DIR);
  ensureDir(NOTES_DIR);

  // Backup drafts
  backupDrafts();

  // Migrate posts
  migratePosts();

  // Migrate notes
  migrateNotes();

  console.log('\n✨ Migration completed!');
  console.log('\nNext steps:');
  console.log('  1. Run: npx hexo clean');
  console.log('  2. Run: npx hexo generate');
  console.log('  3. Verify the migrated content');
  console.log('  4. If satisfied, you can remove source/_drafts/posts and source/_drafts/notes directories');
  console.log('\nBackup location:', BACKUP_DIR);
}

// Run migration only if this file is executed directly
if (require.main === module) {
  main();
}
