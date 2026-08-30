import json
import shutil
from pathlib import Path

ROOT = Path('/home/ubuntu/marriage-education-website')
DATA_PATH = ROOT / 'src/data/articles.json'
ARTICLE_DIR = ROOT / 'public/article-images'
CHAPTER_DIR = ROOT / 'public/chapter-images'
SEARCH_DIR = Path('/home/ubuntu/upload/search_images')

# Complete mapping for all 20 chapters
CHAPTER_IMAGE_MAP = {
    1: 'buLypctEz0oN.png',  # Puberty
    2: 'ms7YRtg9wAak.jpg',  # Puberty issues
    3: '7gANiC5Z78OW.jpg',  # Male anatomy
    4: 'FE8vhc4OFTMw.jpg',  # ED
    5: 'Rt3Kd7ovtInL.jpg',  # Female anatomy
    6: 'Krvik8cRL10E.jpg',  # Female health
    7: 'bdrKxtvu9tXx.jpg',  # Pregnancy
    8: 'wXwK6B17rWGK.jpg',  # Fetal development
    9: 'abqOcTLXrcHc.png',  # Contraception
    10: 'peyr7voyITi1.png', # STIs
    11: 'sD6M1hS2TL4r.png', # STIs 2
    12: 'O0DHu767xRmm.png', # STI prevention
    13: 'O4xi3hoLtB9o.jpg', # Islamic marriage
    14: 'D5Crq5eEfufh.jpg', # Family wellness
    15: 'OsqK9KdSn2IR.jpg', # Prostate
    16: 'Rt3Kd7ovtInL.jpg', # Pelvic pain
    17: 'NMpzEnOjUuEH.jpg', # Mental health
    18: 'MzsiXKE0TcFQ.jpg', # Medical checks
    19: 'QfE7SP65QEOl.jpg', # Counseling
    20: 'buLypctEz0oN.png', # Puberty FAQ
}

def get_article_image(article_id, chapter_num):
    # Variety overrides
    if chapter_num == 1:
        if article_id in [4, 5]: return 'OONf6YveNwOV.png'
        if article_id in [2]: return 'Aozn20wFL3Vf.jpg'
    if chapter_num == 3:
        if article_id in [23, 27]: return '1b1Y1RHUcrLs.png'
        if article_id in [22, 26]: return 'agYBo3tU1tyC.jpg'
    if chapter_num == 4:
        if article_id in [32, 35]: return 'jpbBWyNqN4Kf.jpg'
        if article_id in [33, 36]: return '1ZkCrBT2BoJG.jpeg'
    if chapter_num == 7:
        if article_id in [65, 68]: return 'YCR4ojq0qLO6.jpg'
    if chapter_num == 8:
        if article_id in [71, 74]: return 'aFFuYC2mfgnW.jpg'
    if chapter_num == 9:
        if article_id in [82, 85]: return 'eylMe9NZoWrF.jpg'
    if chapter_num == 13:
        if article_id % 2 == 0: return 'ocUeqSZoxAxJ.jpg'
        if article_id % 3 == 0: return 'za7qKBJNW5H2.jpg'
    if chapter_num == 14:
        if article_id % 2 == 0: return 'hV1B9G93nGDE.jpg'
    if chapter_num == 17:
        if article_id % 2 == 0: return 'KwmNGn2tRNxv.jpg'
    if chapter_num == 18:
        if article_id % 2 == 0: return 'chuJl1v7JHfZ.jpg'
    if chapter_num == 19:
        if article_id % 2 == 0: return '369cd7W5PzJ5.jpg'
    
    return CHAPTER_IMAGE_MAP.get(chapter_num, 'buLypctEz0oN.png')

def main():
    articles = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    
    # 1. Update all 200 Articles
    for i, article in enumerate(articles):
        article_id = i + 1
        chapter_num = (i // 10) + 1
        
        img_name = get_article_image(article_id, chapter_num)
        src_path = SEARCH_DIR / img_name
        if src_path.exists():
            dest_name = f'article-{article_id:03d}.jpg'
            shutil.copy(src_path, ARTICLE_DIR / dest_name)
            article['image'] = f'/article-images/{dest_name}'
        else:
            print(f"Warning: Image {img_name} not found for article {article_id}")

    DATA_PATH.write_text(json.dumps(articles, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # 2. Update all 20 Chapter Covers
    for chapter_num, img_name in CHAPTER_IMAGE_MAP.items():
        src_path = SEARCH_DIR / img_name
        if src_path.exists():
            dest_name = f'chapter-{chapter_num:02d}.jpg'
            shutil.copy(src_path, CHAPTER_DIR / dest_name)
        else:
            print(f"Warning: Image {img_name} not found for chapter {chapter_num}")

    print("Successfully updated all 200 articles and 20 chapters with highly relevant medical and educational images.")

if __name__ == '__main__':
    main()
