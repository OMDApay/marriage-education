import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path('/home/ubuntu/marriage-education-website')
PUBLIC = ROOT / 'public'
ARTICLE_DIR = PUBLIC / 'article-images'
CHAPTER_DIR = PUBLIC / 'chapter-images'
DATA_PATH = ROOT / 'src/data/articles.json'

ARTICLE_DIR.mkdir(parents=True, exist_ok=True)
CHAPTER_DIR.mkdir(parents=True, exist_ok=True)

# Safe, non-explicit visual search vocabulary. Arabic article terms map to English tags
# because the image provider indexes English Flickr tags.
TERM_TAGS = [
    ('البلوغ', 'adolescent,education'),
    ('الهرمون', 'hormone,medical'),
    ('الجهاز التناسلي الذكري', 'male,anatomy,medical'),
    ('الجهاز التناسلي الأنثوي', 'female,anatomy,medical'),
    ('تشريح', 'anatomy,biology'),
    ('الخصية', 'medical,anatomy'),
    ('البروستاتا', 'medical,health'),
    ('القضيب', 'medical,anatomy'),
    ('الثدي', 'women,health'),
    ('الحيض', 'women,health'),
    ('الدورة', 'women,health'),
    ('الحمل', 'pregnancy,maternity'),
    ('الرضاعة', 'mother,baby'),
    ('الإنجاب', 'family,health'),
    ('منع الحمل', 'healthcare,medicine'),
    ('الأمراض المنقولة', 'doctor,health'),
    ('العدوى', 'health,medicine'),
    ('الوقاية', 'hygiene,health'),
    ('الإسلام', 'family,peace'),
    ('الأسرة', 'family,relationship'),
    ('الزوج', 'couple,relationship'),
    ('العلاقة', 'couple,communication'),
    ('الصحة النفسية', 'psychology,wellness'),
    ('النفسية', 'psychology,wellness'),
    ('القلق', 'mentalhealth,wellness'),
    ('الاكتئاب', 'mentalhealth,wellness'),
    ('الألم', 'healthcare,doctor'),
    ('الفحص', 'doctor,medical'),
    ('الاستشارة', 'counseling,conversation'),
    ('العلاج', 'doctor,healthcare'),
    ('النظافة', 'hygiene,clean'),
    ('الغذاء', 'nutrition,healthy'),
    ('الرياضة', 'fitness,wellness'),
    ('السؤال', 'education,question'),
    ('أسئلة', 'education,question'),
]

DEFAULT_TAGS = 'health,education'


def tags_for(text: str) -> str:
    for arabic, tags in TERM_TAGS:
        if arabic in text:
            return tags
    return DEFAULT_TAGS


def download_unique(url_base: str, target: Path, used_hashes: set[str], start_lock: int) -> tuple[str, int]:
    # Try several related tags first; some narrow Flickr tag combinations have few results.
    tag_variants = [
        'health,education',
        'medical,science',
        'family,wellness',
        'health,wellness',
        url_base,
        f'{url_base},education',
    ]
    lock = start_lock
    for attempt in range(240):
        tags = tag_variants[attempt % len(tag_variants)]
        url = f'https://loremflickr.com/800/600/{quote(tags, safe=",")}?lock={lock}'
        try:
            response = requests.get(url, timeout=20, allow_redirects=True)
            content_type = response.headers.get('content-type', '')
            data = response.content
            digest = hashlib.sha256(data).hexdigest()
            if response.status_code == 200 and content_type.startswith('image/') and len(data) > 5000 and digest not in used_hashes:
                target.write_bytes(data)
                used_hashes.add(digest)
                return digest, lock
        except requests.RequestException:
            pass
        lock += 1
        time.sleep(0.05)

    # Guaranteed local fallback: Picsum produces a deterministic image for each seed.
    # We still hash-check it so no duplicate file is accepted.
    for fallback_lock in range(start_lock, start_lock + 10000):
        url = f'https://picsum.photos/seed/marriage-education-{fallback_lock}/800/600'
        try:
            response = requests.get(url, timeout=20, allow_redirects=True)
            content_type = response.headers.get('content-type', '')
            data = response.content
            digest = hashlib.sha256(data).hexdigest()
            if response.status_code == 200 and content_type.startswith('image/') and len(data) > 5000 and digest not in used_hashes:
                target.write_bytes(data)
                used_hashes.add(digest)
                return digest, fallback_lock
        except requests.RequestException:
            pass
    raise RuntimeError(f'Could not download a unique image for {url_base} starting at lock {start_lock}')


def main() -> None:
    articles = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    used_hashes: set[str] = set()
    article_count = 0
    chapter_count = 0

    # Each article gets a local path. The lock range is disjoint from chapter locks.
    for index, article in enumerate(articles, start=1):
        tags = tags_for(article['title'] + ' ' + article.get('keywords', '') + ' ' + article.get('category', ''))
        target = ARTICLE_DIR / f'article-{index:03d}.jpg'
        digest, lock = download_unique(tags, target, used_hashes, 10000 + index * 13)
        article['image'] = f'/article-images/article-{index:03d}.jpg'
        article_count += 1
        if index % 20 == 0:
            print(f'downloaded_articles={index}')

    # Chapter cover images use different lock space and always stay distinct from articles.
    chapter_groups = []
    for index in range(20):
        chapter_articles = articles[index * 10:(index + 1) * 10]
        category = chapter_articles[0].get('category', '') if chapter_articles else ''
        tags = tags_for(category)
        target = CHAPTER_DIR / f'chapter-{index + 1:02d}.jpg'
        digest, lock = download_unique(tags, target, used_hashes, 30000 + (index + 1) * 17)
        chapter_count += 1
        chapter_groups.append({
            'id': index + 1,
            'title': category,
            'count': len(chapter_articles),
            'image': f'/chapter-images/chapter-{index + 1:02d}.jpg',
            'description': chapter_articles[0].get('description', '') if chapter_articles else ''
        })

    DATA_PATH.write_text(json.dumps(articles, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    js_path = ROOT / 'src/data/articles.js'
    js_path.write_text(
        "import articlesData from './articles.json'\n\n"
        + 'export const chapters = ' + json.dumps(chapter_groups, ensure_ascii=False, indent=2)
        + "\n\n"
        + """export const articles = articlesData

export const getArticlesByCategory = (categoryTitle) => {
  return articles.filter(article => article.category === categoryTitle)
}

export const searchArticles = (query) => {
  const lowercaseQuery = query.toLowerCase()
  return articles.filter(article =>
    article.title.toLowerCase().includes(lowercaseQuery) ||
    article.content.toLowerCase().includes(lowercaseQuery) ||
    article.keywords.toLowerCase().includes(lowercaseQuery)
  )
}

export const getArticlesForSection = (sectionId) => {
  switch (sectionId) {
    case 'intro':
      return articles.filter(a => a.category.includes('الباب 1:') || a.category.includes('الباب 7:')).slice(0, 10)
    case 'anatomy':
      return articles.filter(a => a.category.includes('الباب 3:') || a.category.includes('الباب 5:')).slice(0, 10)
    case 'tips':
      return articles.filter(a => a.category.includes('الباب 13:') || a.category.includes('الباب 14:')).slice(0, 10)
    case 'faq':
      return articles.filter(a => a.category.includes('الباب 20:')).slice(0, 10)
    default:
      return []
  }
}
""",
        encoding='utf-8'
    )
    print(f'articles_downloaded={article_count}')
    print(f'chapters_downloaded={chapter_count}')
    print(f'unique_image_hashes={len(used_hashes)}')


if __name__ == '__main__':
    main()
