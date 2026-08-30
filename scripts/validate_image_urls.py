import json
from pathlib import Path
from urllib.parse import urlparse
import requests

root = Path('/home/ubuntu/marriage-education-website')
articles = json.loads((root / 'src/data/articles.json').read_text(encoding='utf-8'))
articles_urls = [a.get('image', '') for a in articles]
text = (root / 'src/data/articles.js').read_text(encoding='utf-8')
# Extract chapter image URLs from generated JS.
import re
chapter_urls = re.findall(r'"image":\s*"(https://images\.unsplash\.com/[^"]+)"', text)
all_urls = articles_urls + chapter_urls
print(f'articles={len(articles)}')
print(f'article_unique_urls={len(set(articles_urls))}')
print(f'chapters={len(chapter_urls)}')
print(f'chapter_unique_urls={len(set(chapter_urls))}')
print(f'all_unique_urls={len(set(all_urls))}')
print('sample_urls:')
for url in all_urls[:5]:
    print(url)

statuses = []
for url in all_urls[:25]:
    try:
        r = requests.get(url, timeout=15, stream=True)
        statuses.append((r.status_code, r.headers.get('content-type',''), url))
        r.close()
    except Exception as exc:
        statuses.append((f'ERROR:{type(exc).__name__}', '', url))
for status, ctype, url in statuses:
    print(f'{status}\t{ctype}\t{url}')
print('invalid_sample_count=', sum(1 for status, _, _ in statuses if status != 200))
print('duplicate_article_source_ids=', len(articles_urls) - len(set(u.split('?')[0] for u in articles_urls)))
print('duplicate_all_source_ids=', len(all_urls) - len(set(u.split('?')[0] for u in all_urls)))
