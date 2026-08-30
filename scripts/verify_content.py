import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
articles = json.loads((root / 'src/data/articles.json').read_text(encoding='utf-8'))
positions_js = (root / 'src/data/positions.js').read_text(encoding='utf-8')
position_keys = re.findall(r"image:\s*positionImages\['(.*?)'\]", positions_js)
position_stems = {p.stem for p in (root / 'src/assets/positions').iterdir() if p.is_file()}
missing_position_images = [key for key in position_keys if key not in position_stems]

counts = {}
for article in articles:
    chapter = article['category'].split(':', 1)[0]
    counts[chapter] = counts.get(chapter, 0) + 1

print(f'articles={len(articles)}')
print(f'position_entries={len(re.findall(r"\{\s*id:\s*\d+", positions_js))}')
print(f'position_image_properties={len(position_keys)}')
print(f'missing_position_image_keys={missing_position_images}')
print(f'chapter_count={len(counts)}')
print(f'chapter_article_total={sum(counts.values())}')
for chapter, count in counts.items():
    print(f'{chapter}={count}')

assert len(articles) == 200
assert len(position_keys) == 50
assert not missing_position_images
assert sum(counts.values()) == 200
assert (root / 'src/assets/male_reproductive_system_ar.jpg').exists()
assert (root / 'src/assets/female_reproductive_system_ar.jpg').exists()
print('verification=PASS')
