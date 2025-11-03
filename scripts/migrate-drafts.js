const fs = require('fs');
const path = require('path');

// File paths
const POSTS_DIR = path.join(__dirname, '../source/_drafts/posts');
const NOTES_DIR = path.join(__dirname, '../source/_drafts/notes');
const TARGET_POSTS_DIR = path.join(__dirname, '../source/_posts');
const TARGET_NOTES_DIR = path.join(__dirname, '../source/_posts/notes');

// Read meta.json files
const POSTS_META_PATH = path.join(POSTS_DIR, '_meta.json');
const NOTES_META_PATH = path.join(NOTES_DIR, '_meta.json');

// Utility: Format date from ISO string to YYYY-MM-DD HH:mm:ss
function formatDate(isoString) {
  if (!isoString) return null;
  const date = new Date(isoString);
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  const hh = String(date.getHours()).padStart(2, '0');
  const min = String(date.getMinutes()).padStart(2, '0');
  const ss = String(date.getSeconds()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd} ${hh}:${min}:${ss}`;
}

// Utility: Generate safe filename from slug or title
function generateFileName(slug, title) {
  if (slug && slug !== 'null') {
    // Use slug if available
    return `${slug}.md`;
  }
  // Fallback to sanitized title
  const sanitized = title
    .replace(/[<>:"/\\|?*\x00-\x1F]/g, '') // Remove invalid characters
    .replace(/\s+/g, '-') // Replace spaces with hyphens
    .substring(0, 100); // Limit length
  return `${sanitized}.md`;
}

// Utility: Extract summary from markdown content
function extractSummary(content, maxLength = 200) {
  // Remove front matter if present
  const withoutFrontMatter = content.replace(/^---[\s\S]*?---\n*/m, '');
  // Remove markdown syntax
  const plainText = withoutFrontMatter
    .replace(/#+\s/g, '') // Remove headers
    .replace(/!\[.*?\]\(.*?\)/g, '') // Remove images
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Replace links with text
    .replace(/`{1,3}[^`]*`{1,3}/g, '') // Remove code blocks
    .replace(/[*_~]/g, '') // Remove emphasis
    .trim();
  
  // Get first maxLength characters
  return plainText.substring(0, maxLength).trim();
}

// Escape YAML value if needed
function escapeYamlValue(value) {
  if (!value) return '';
  const str = String(value);
  // Check if the value needs quoting
  const needsQuotes = /[:\n\r{}[\]&*#?|<>=!%@`]|^\s|\s$/.test(str) || 
                     str.includes('!!') ||
                     str.includes('---') ||
                     str.includes('...') ||
                     /^(true|false|yes|no|null)$/i.test(str);
  
  if (needsQuotes) {
    // Use double quotes and escape special characters
    return '"' + str.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n') + '"';
  }
  return str;
}

// Generate front matter
function generateFrontMatter(meta, content, isNote = false) {
  const lines = ['---'];
  
  // Title
  lines.push(`title: ${escapeYamlValue(meta.title || 'Untitled')}`);
  
  // Date (created)
  if (meta.created) {
    lines.push(`date: ${formatDate(meta.created)}`);
  }
  
  // Updated (modified)
  if (meta.modified) {
    lines.push(`updated: ${formatDate(meta.modified)}`);
  }
  
  // Categories
  if (isNote) {
    lines.push(`categories:`);
    lines.push(`  - 随笔`);
  } else if (meta.category && meta.category.name) {
    lines.push(`categories:`);
    lines.push(`  - ${escapeYamlValue(meta.category.name)}`);
  }
  
  // Tags
  if (meta.tags && meta.tags.length > 0) {
    lines.push(`tags:`);
    meta.tags.forEach(tag => {
      lines.push(`  - ${escapeYamlValue(tag)}`);
    });
  }
  
  // Summary - use literal block scalar for multi-line summaries
  const summary = meta.summary || extractSummary(content);
  if (summary) {
    // Check if summary is multi-line or contains special characters
    if (summary.includes('\n') || summary.length > 80) {
      lines.push(`summary: >`);
      // Split into lines and indent
      summary.split('\n').forEach(line => {
        lines.push(`  ${line}`);
      });
    } else {
      lines.push(`summary: ${escapeYamlValue(summary)}`);
    }
  }
  
  lines.push('---');
  lines.push('');
  
  return lines.join('\n');
}

// Process markdown file
function processMarkdownFile(filePath, meta, targetDir, isNote = false) {
  try {
    // Read the markdown content
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Remove existing front matter if any
    const contentWithoutFrontMatter = content.replace(/^---[\s\S]*?---\n*/m, '');
    
    // Generate new front matter
    const frontMatter = generateFrontMatter(meta, contentWithoutFrontMatter, isNote);
    
    // Combine front matter with content
    const newContent = frontMatter + contentWithoutFrontMatter;
    
    // Generate target filename
    const fileName = generateFileName(meta.slug, meta.title);
    const targetPath = path.join(targetDir, fileName);
    
    // Ensure target directory exists
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }
    
    // Write the new file
    fs.writeFileSync(targetPath, newContent, 'utf8');
    
    console.log(`✓ Migrated: ${meta.title} -> ${fileName}`);
    return true;
  } catch (error) {
    console.error(`✗ Error processing ${meta.title}:`, error.message);
    return false;
  }
}

// Main migration function
function migrate() {
  console.log('Starting migration...\n');
  
  let successCount = 0;
  let errorCount = 0;
  
  // Process posts
  if (fs.existsSync(POSTS_META_PATH)) {
    console.log('Processing posts...');
    const postsMeta = JSON.parse(fs.readFileSync(POSTS_META_PATH, 'utf8'));
    
    Object.values(postsMeta).forEach(meta => {
      // Find corresponding markdown file
      const files = fs.readdirSync(POSTS_DIR).filter(f => 
        f.endsWith('.md') && f !== '_meta.json'
      );
      
      // Try to match by title
      const matchingFile = files.find(f => {
        const fileName = f.replace('.md', '');
        return fileName === meta.title || 
               fileName.includes(meta.title) || 
               meta.title.includes(fileName);
      });
      
      if (matchingFile) {
        const filePath = path.join(POSTS_DIR, matchingFile);
        const success = processMarkdownFile(filePath, meta, TARGET_POSTS_DIR, false);
        if (success) successCount++;
        else errorCount++;
      } else {
        console.log(`⚠ No matching file found for: ${meta.title}`);
      }
    });
  }
  
  // Process notes
  if (fs.existsSync(NOTES_META_PATH)) {
    console.log('\nProcessing notes...');
    const notesMeta = JSON.parse(fs.readFileSync(NOTES_META_PATH, 'utf8'));
    
    Object.values(notesMeta).forEach(meta => {
      // Find corresponding markdown file
      const files = fs.readdirSync(NOTES_DIR).filter(f => 
        f.endsWith('.md') && f !== '_meta.json'
      );
      
      // Try to match by title
      const matchingFile = files.find(f => {
        const fileName = f.replace('.md', '');
        return fileName === meta.title || 
               fileName.includes(meta.title) || 
               meta.title.includes(fileName);
      });
      
      if (matchingFile) {
        const filePath = path.join(NOTES_DIR, matchingFile);
        const success = processMarkdownFile(filePath, meta, TARGET_NOTES_DIR, true);
        if (success) successCount++;
        else errorCount++;
      } else {
        console.log(`⚠ No matching file found for: ${meta.title}`);
      }
    });
  }
  
  console.log('\n' + '='.repeat(50));
  console.log(`Migration complete!`);
  console.log(`✓ Success: ${successCount}`);
  console.log(`✗ Errors: ${errorCount}`);
  console.log('='.repeat(50));
}

// Run migration
migrate();
