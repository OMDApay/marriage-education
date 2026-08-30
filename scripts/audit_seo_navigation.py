from pathlib import Path
import re

root = Path('/home/ubuntu/marriage-education-website')
files = [root/'src/data/pornMediaLiteracy.js', root/'src/data/tragedyChapter.js']
all_ids = []
print('SEO/NAVIGATION AUDIT')
for path in files:
    text = path.read_text(encoding='utf-8')
    ids = re.findall(r"id: '([^']+)'", text)
    all_ids.extend(ids)
    keyword_lines = re.findall(r"keywords: '([^']+)'", text)
    print(path.name, 'articles=', len([x for x in ids if x.startswith(('pm-', 'tr-'))]), 'keyword_fields=', len(keyword_lines), 'duplicate_ids=', len(ids) != len(set(ids)))
print('duplicate_ids_total=', len(all_ids) != len(set(all_ids)))
modal = (root/'src/components/ArticleModal.jsx').read_text(encoding='utf-8')
app = (root/'src/App.jsx').read_text(encoding='utf-8')
for label, needle in [('previous', 'previousArticle'), ('next', 'nextArticle'), ('related', 'relatedArticles'), ('dynamic_title', 'document.title'), ('description_meta', 'meta[name="description"]'), ('age_gate', 'marriage_age_verified')]:
    print(label, '=', needle in modal or needle in app)
print('cross_chapter_link_scoring=', 'keywordScore' in modal)
