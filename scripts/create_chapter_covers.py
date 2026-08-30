import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path('/home/ubuntu/marriage-education-website')
DATA_PATH = ROOT / 'src/data/articles.json'
CHAPTER_DIR = ROOT / 'public/chapter-images'
CHAPTER_DIR.mkdir(parents=True, exist_ok=True)

try:
    arabic_font_path = '/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf'
    arabic_small_path = '/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf'
except Exception:
    arabic_font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    arabic_small_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

font_large = ImageFont.truetype(arabic_font_path, 42)
font_medium = ImageFont.truetype(arabic_small_path, 25)
font_label = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)

# Distinct palettes and visual motifs prevent visual repetition among the 20 covers.
palettes = [
    ((31, 78, 121), (77, 166, 255)), ((103, 58, 183), (224, 176, 255)),
    ((0, 121, 107), (128, 203, 196)), ((198, 40, 40), (255, 138, 128)),
    ((230, 81, 0), (255, 204, 128)), ((21, 101, 192), (144, 202, 249)),
    ((46, 125, 50), (165, 214, 167)), ((173, 20, 87), (244, 143, 177)),
    ((69, 90, 100), (176, 190, 197)), ((0, 96, 100), (128, 222, 234)),
    ((123, 31, 162), (206, 147, 216)), ((239, 108, 0), (255, 183, 77)),
    ((63, 81, 181), (159, 168, 218)), ((0, 105, 92), (128, 203, 196)),
    ((173, 20, 87), (240, 98, 146)), ((85, 56, 40), (196, 148, 102)),
    ((26, 35, 126), (121, 134, 203)), ((46, 125, 50), (200, 230, 201)),
    ((156, 39, 176), (225, 190, 231)), ((38, 50, 56), (144, 164, 174)),
]


def rounded_rectangle(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_motif(draw, index, c1, c2):
    # Abstract, non-explicit educational motifs, one different composition per cover.
    cx, cy = 595, 280
    variant = index % 10
    if variant == 0:
        for y in range(130, 470, 52):
            draw.line((420, y, 730, y), fill=c2, width=5)
        points = [(450, 420), (505, 360), (560, 375), (625, 250), (700, 175)]
        draw.line(points, fill=(255, 255, 255), width=12, joint='curve')
        for x, y in points:
            draw.ellipse((x-13, y-13, x+13, y+13), fill=(255, 255, 255))
    elif variant == 1:
        draw.ellipse((420, 130, 760, 470), outline=c2, width=16)
        draw.ellipse((500, 190, 680, 370), outline=(255, 255, 255), width=12)
        draw.line((590, 130, 590, 470), fill=(255, 255, 255), width=10)
        draw.line((420, 300, 760, 300), fill=(255, 255, 255), width=10)
    elif variant == 2:
        draw.arc((420, 120, 750, 450), 200, 340, fill=c2, width=20)
        draw.arc((460, 160, 710, 410), 20, 160, fill=(255, 255, 255), width=18)
        draw.ellipse((560, 255, 620, 315), fill=c2)
        draw.ellipse((640, 335, 700, 395), fill=(255, 255, 255))
    elif variant == 3:
        for x, y, r in [(450, 260, 42), (565, 180, 65), (660, 295, 52), (535, 390, 58), (715, 420, 35)]:
            draw.ellipse((x-r, y-r, x+r, y+r), fill=c2, outline=(255, 255, 255), width=5)
        draw.line((450, 260, 565, 180, 660, 295, 535, 390, 715, 420), fill=(255, 255, 255), width=8)
    elif variant == 4:
        draw.rectangle((430, 150, 750, 440), outline=(255, 255, 255), width=8)
        for x in range(470, 730, 48):
            draw.line((x, 170, x, 420), fill=c2, width=7)
        draw.line((440, 290, 740, 290), fill=c2, width=10)
        draw.ellipse((565, 255, 615, 305), fill=(255, 255, 255))
    elif variant == 5:
        draw.pieslice((420, 125, 760, 465), 30, 150, fill=c2)
        draw.pieslice((420, 125, 760, 465), 150, 270, fill=(255, 255, 255))
        draw.pieslice((420, 125, 760, 465), 270, 30, fill=(255, 221, 126))
        draw.ellipse((545, 250, 635, 340), fill=c1, outline=(255, 255, 255), width=7)
    elif variant == 6:
        draw.line((450, 400, 730, 150), fill=(255, 255, 255), width=16)
        for x, y in [(490, 360), (550, 305), (610, 250), (670, 195)]:
            draw.ellipse((x-22, y-22, x+22, y+22), fill=c2)
        draw.polygon([(420, 420), (500, 420), (460, 350)], fill=(255, 255, 255))
    elif variant == 7:
        draw.ellipse((430, 150, 750, 470), outline=(255, 255, 255), width=10)
        draw.arc((480, 200, 700, 420), 40, 320, fill=c2, width=22)
        draw.line((590, 200, 590, 420), fill=(255, 255, 255), width=8)
        draw.line((480, 310, 700, 310), fill=(255, 255, 255), width=8)
    elif variant == 8:
        draw.rounded_rectangle((425, 145, 755, 450), radius=32, fill=(255, 255, 255))
        draw.rectangle((470, 205, 710, 245), fill=c2)
        draw.rectangle((470, 280, 650, 320), fill=c1)
        draw.rectangle((470, 355, 685, 395), fill=(255, 193, 7))
        for y in [225, 300, 375]:
            draw.ellipse((675, y-15, 705, y+15), fill=c1)
    else:
        draw.polygon([(590, 120), (735, 250), (680, 440), (500, 440), (445, 250)], outline=(255, 255, 255), fill=None)
        draw.line((590, 120, 590, 440), fill=c2, width=10)
        draw.line((445, 250, 735, 250), fill=c2, width=10)
        draw.ellipse((550, 210, 630, 290), fill=(255, 255, 255))


def main():
    articles = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    chapter_groups = []
    for i in range(20):
        chunk = articles[i * 10:(i + 1) * 10]
        category = chunk[0].get('category', f'الباب {i + 1}') if chunk else f'الباب {i + 1}'
        c1, c2 = palettes[i]
        image = Image.new('RGB', (800, 600), c1)
        draw = ImageDraw.Draw(image)
        # Layered diagonal background unique to every chapter.
        for step in range(0, 800, 40):
            alpha = int(70 + (step % 160) / 3)
            color = tuple(min(255, int(c1[j] * 0.65 + c2[j] * 0.35)) for j in range(3))
            draw.polygon([(step, 0), (800, max(0, 800-step)), (800, max(0, 860-step)), (step, 60)], fill=color)
        draw_motif(draw, i, c1, c2)
        rounded_rectangle(draw, (42, 38, 758, 560), 30, fill=None, outline=(255, 255, 255), width=3)
        label = f'EDUCATIONAL CHAPTER {i + 1:02d}'
        draw.text((58, 62), label, font=font_label, fill=(255, 255, 255))
        # The main title is placed on a high-contrast panel for readability.
        rounded_rectangle(draw, (50, 470, 750, 548), 20, fill=(0, 0, 0))
        title = f'الباب {i + 1}'
        draw.text((400, 485), title, font=font_large, fill=(255, 255, 255), anchor='mm')
        image = image.filter(ImageFilter.GaussianBlur(radius=0.15))
        image.save(CHAPTER_DIR / f'chapter-{i + 1:02d}.jpg', quality=92, optimize=True)
        chapter_groups.append({
            'id': i + 1,
            'title': category,
            'count': len(chunk),
            'image': f'/chapter-images/chapter-{i + 1:02d}.jpg',
            'description': chunk[0].get('description', '') if chunk else ''
        })

    for i, article in enumerate(articles, start=1):
        article['image'] = f'/article-images/article-{i:03d}.jpg'
    DATA_PATH.write_text(json.dumps(articles, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    js_path = ROOT / 'src/data/articles.js'
    js_path.write_text(
        "import articlesData from './articles.json'\n\n"
        + 'export const chapters = ' + json.dumps(chapter_groups, ensure_ascii=False, indent=2)
        + "\n\n"
        + """export const articles = articlesData

export const getArticlesByCategory = (categoryTitle) => articles.filter(article => article.category === categoryTitle)

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
    case 'intro': return articles.filter(a => a.category.includes('الباب 1:') || a.category.includes('الباب 7:')).slice(0, 10)
    case 'anatomy': return articles.filter(a => a.category.includes('الباب 3:') || a.category.includes('الباب 5:')).slice(0, 10)
    case 'tips': return articles.filter(a => a.category.includes('الباب 13:') || a.category.includes('الباب 14:')).slice(0, 10)
    case 'faq': return articles.filter(a => a.category.includes('الباب 20:')).slice(0, 10)
    default: return []
  }
}
""",
        encoding='utf-8'
    )
    print('chapter_covers=20')
    print('article_records=', len(articles))


if __name__ == '__main__':
    main()
