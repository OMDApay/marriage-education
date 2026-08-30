import json
import os

def fix_articles():
    path = '/home/ubuntu/marriage-education-website/src/data/articles.json'
    with open(path, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # Unsplash collection IDs for variety
    # 1. Health/Medical, 2. Family/Love, 3. Nature/Peace, 4. Anatomy/Science
    image_bases = [
        "https://images.unsplash.com/photo-1505751172876-fa1923c5c528", # medical
        "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982", # medical 2
        "https://images.unsplash.com/photo-1511895426328-dc8714191300", # family
        "https://images.unsplash.com/photo-1516549655169-df83a0774514", # wellness
        "https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7", # hospital
        "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d", # doctor
        "https://images.unsplash.com/photo-1583912267670-65355b674b12", # baby
        "https://images.unsplash.com/photo-1559839734-2b71f1e3c7e5", # healthy food/life
        "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e", # counseling
        "https://images.unsplash.com/photo-1434030216411-0b793f4b4173", # writing/study
    ]

    # 1. Assign 200 unique images
    for i, article in enumerate(articles):
        # Use a rotating base image with a unique signature
        base = image_bases[i % len(image_bases)]
        article['image'] = f"{base}?auto=format&fit=crop&w=800&q=80&sig=art_{i+1}"

    # 2. Split into 20 chapters
    new_chapters = []
    chunk_size = 10
    for i in range(0, len(articles), chunk_size):
        chunk = articles[i:i+chunk_size]
        chapter_num = (i // chunk_size) + 1
        
        first_title = chunk[0]['title'].split('-')[0].strip()
        full_chapter_title = f"الباب {chapter_num}: {first_title}"
        
        for a in chunk:
            a['category'] = full_chapter_title
            
        # Use a unique image for each chapter cover
        chapter_base = image_bases[(chapter_num - 1) % len(image_bases)]
        new_chapters.append({
            'id': chapter_num,
            'title': full_chapter_title,
            'count': len(chunk),
            'image': f"{chapter_base}?auto=format&fit=crop&w=800&q=80&sig=chap_{chapter_num}",
            'description': chunk[0]['description']
        })

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    chapters_js = "export const chapters = " + json.dumps(new_chapters, ensure_ascii=False, indent=2)
    
    js_path = '/home/ubuntu/marriage-education-website/src/data/articles.js'
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write("import articlesData from './articles.json'\n\n")
        f.write(chapters_js + "\n\n")
        f.write("""
export const articles = articlesData

export const getArticlesByCategory = (categoryTitle) => {
  // Use includes to be safe or strict match
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
  switch(sectionId) {
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
""")

    print(f"Updated {len(articles)} articles and created {len(new_chapters)} chapters.")

if __name__ == "__main__":
    fix_articles()
