import json
import shutil
from pathlib import Path

ROOT = Path('/home/ubuntu/marriage-education-website')
DATA_PATH = ROOT / 'src/data/articles.json'
ARTICLE_DIR = ROOT / 'public/article-images'
CHAPTER_DIR = ROOT / 'public/chapter-images'
SEARCH_DIR = Path('/home/ubuntu/upload/search_images')

# Mapping of chapters to specific high-quality search result images
# Based on the visual content of the search results
CHAPTER_IMAGE_MAP = {
    1: 'buLypctEz0oN.png',  # Puberty stages
    2: 'ms7YRtg9wAak.jpg',  # Precocious/Delayed puberty
    3: '7gANiC5Z78OW.jpg',  # Male anatomy
    4: 'FE8vhc4OFTMw.jpg',  # Erectile Dysfunction
    5: 'Rt3Kd7ovtInL.jpg',  # Female anatomy
    6: 'Krvik8cRL10E.jpg',  # Female reproductive system
    7: 'bdrKxtvu9tXx.jpg',  # Pregnancy trimesters
    8: 'wXwK6B17rWGK.jpg',  # Fetal development
    9: 'abqOcTLXrcHc.png',  # Contraception types
    10: 'peyr7voyITi1.png', # STI types
}

# More specific article-level mapping for variety within chapters where possible
# We'll use the chapter default but can override for specific ones
def get_article_image(article_id, chapter_num):
    # For variety, we use some other related images from search results
    if chapter_num == 1:
        if article_id in [4, 5]: return 'OONf6YveNwOV.png' # Growth spurt
        if article_id in [2]: return 'Aozn20wFL3Vf.jpg' # Hormonal
    if chapter_num == 3:
        if article_id in [23, 27]: return '1b1Y1RHUcrLs.png' # Testicles
        if article_id in [22, 26]: return 'agYBo3tU1tyC.jpg' # Penis/Epididymis
    if chapter_num == 4:
        if article_id in [32, 35]: return 'jpbBWyNqN4Kf.jpg' # ED causes
        if article_id in [33, 36]: return '1ZkCrBT2BoJG.jpeg' # Psychological/PE
    if chapter_num == 7:
        if article_id in [65, 68]: return 'YCR4ojq0qLO6.jpg' # Pregnancy poster
    if chapter_num == 8:
        if article_id in [71, 74]: return 'aFFuYC2mfgnW.jpg' # Embryo development
    if chapter_num == 9:
        if article_id in [82, 85]: return 'eylMe9NZoWrF.jpg' # Contraception methods
    
    return CHAPTER_IMAGE_MAP.get(chapter_num, 'buLypctEz0oN.png')

def main():
    articles = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    
    # 1. Update Articles 1-100 (Chapters 1-10)
    for i, article in enumerate(articles):
        article_id = i + 1
        chapter_num = (i // 10) + 1
        
        if chapter_num <= 10:
            img_name = get_article_image(article_id, chapter_num)
            src_path = SEARCH_DIR / img_name
            if src_path.exists():
                dest_name = f'article-{article_id:03d}.jpg'
                shutil.copy(src_path, ARTICLE_DIR / dest_name)
                article['image'] = f'/article-images/{dest_name}'
            else:
                print(f"Warning: Image {img_name} not found for article {article_id}")

    DATA_PATH.write_text(json.dumps(articles, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # 2. Update Chapter Covers for 1-10
    for chapter_num, img_name in CHAPTER_IMAGE_MAP.items():
        src_path = SEARCH_DIR / img_name
        if src_path.exists():
            dest_name = f'chapter-{chapter_num:02d}.jpg'
            shutil.copy(src_path, CHAPTER_DIR / dest_name)
        else:
            print(f"Warning: Image {img_name} not found for chapter {chapter_num}")

    print("Successfully updated 100 articles and 10 chapters with curated medical images.")

if __name__ == '__main__':
    main()
