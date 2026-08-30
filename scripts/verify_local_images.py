import hashlib
import json
from pathlib import Path

root = Path('/home/ubuntu/marriage-education-website')
articles = json.loads((root / 'src/data/articles.json').read_text(encoding='utf-8'))
article_files = [root / 'public' / a['image'].lstrip('/') for a in articles]
chapter_files = sorted((root / 'public/chapter-images').glob('chapter-*.jpg'))
all_files = article_files + chapter_files
missing = [str(p) for p in all_files if not p.exists()]
hashes = [hashlib.sha256(p.read_bytes()).hexdigest() for p in all_files if p.exists()]
print('articles=', len(articles))
print('article_files=', len(article_files))
print('chapter_files=', len(chapter_files))
print('missing_files=', len(missing))
print('unique_content_hashes=', len(set(hashes)))
print('total_files=', len(all_files))
if missing:
    print('missing_sample=', missing[:10])
assert len(articles) == 200
assert len(article_files) == 200
assert len(chapter_files) == 20
assert not missing
assert len(set(hashes)) == 220
print('verification=PASS')
