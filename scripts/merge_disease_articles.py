import json
from pathlib import Path

root = Path('/home/ubuntu/marriage-education-website')
long_articles = json.loads((root / 'src/data/sexualDiseasesLong.json').read_text(encoding='utf-8'))

metadata = {
'sd-01': ('ما المقصود بالأمراض المنقولة جنسياً؟','الأمراض المنقولة جنسياً، العدوى، الوقاية، الفحص','تعريف مبسط وعميق للعدوى المنقولة جنسياً وطرق انتقالها ومتى تستلزم مراجعة الطبيب.','/sexual-diseases-images/sd-01.jpg'),
'sd-02': ('الزهري: المراحل والأعراض والفحص','الزهري، اللولبية الشاحبة، قرحة، فحص الدم','شرح موسع للمراحل العامة للزهري وأهمية التشخيص المبكر وعدم الاعتماد على الشكل وحده.','/sexual-diseases-images/sd-02.jpg'),
'sd-03': ('السيلان والكلاميديا: عدوى قد تكون صامتة','السيلان، الكلاميديا، إفرازات، التهابات، عقم','دليل عملي عن العدوى البكتيرية الشائعة ومخاطر تركها دون علاج.','/verified-web-images/gonorrhea-phil.jpg'),
'sd-04': ('فيروس نقص المناعة البشرية HIV','HIV، الإيدز، الفحص، العلاج، الوقاية','فهم العدوى وطرق الفحص والعلاج الحديث دون وصمة أو تخويف.','/sexual-diseases-images/sd-04.jpg'),
'sd-05': ('الهربس التناسلي: النوبات والتعامل الطبي','الهربس، HSV، بثور، ألم، علاج','معلومات محترمة عن النوبات الجلدية وكيفية تقليل انتقال العدوى.','/sexual-diseases-images/sd-05.jpg'),
'sd-06': ('فيروس الورم الحليمي البشري HPV','HPV، الثآليل، اللقاح، عنق الرحم','التعريف بالفيروس واللقاحات والفحوصات الوقائية المرتبطة به.','/sexual-diseases-images/sd-06.jpg'),
'sd-07': ('التهاب الكبد الفيروسي والانتقال عبر الدم','التهاب الكبد B، التهاب الكبد C، اللقاح، الدم','طرق الانتقال والوقاية بالفحص والتطعيم والتعامل الآمن مع الدم.','/verified-web-images/hepatitis-c.jpg'),
'sd-08': ('العدوى الطفيلية والالتهابات التناسلية','داء المشعرات، القمل، الجرب، التهاب','التمييز بين بعض العدوى الطفيلية والحالات الجلدية التي تحتاج علاجاً متخصصاً.','/sexual-diseases-images/sd-08.jpg'),
'sd-09': ('الفحوصات والوقاية من الأمراض الجنسية','فحص قبل الزواج، فحوصات، الواقي، الوقاية','كيف تُبنى خطة وقاية وفحص مسؤولة قبل الزواج وأثناء الحياة الزوجية.','/sexual-diseases-images/sd-09.jpg'),
'sd-10': ('متى يجب مراجعة الطبيب؟ وكيف نحمي الخصوصية؟','استشارة، سرية، أعراض، علاج، شريك','علامات تستدعي المراجعة الطبية وإرشادات للتعامل الهادئ والمسؤول مع التشخيص.','/sexual-diseases-images/sd-10.jpg'),
}

lines = [
"export const sexualDiseasesChapter = {",
"  id: 'sexual-diseases',",
"  title: 'الأمراض الجنسية',",
"  subtitle: 'التعريف، الأعراض، الوقاية، الفحوصات، والعلاج بطريقة علمية محترمة',",
"  image: '/sexual-diseases-images/cover.jpg',",
"  sourceNote: 'تم إعداد هذا الباب بالاستفادة من إرشادات CDC وWHO ومواد التوعية الصحية الرسمية، مع إعادة الصياغة بأسلوب تثقيفي طبي حديث ومحايد.',",
"  articles: [",
]
for i, item in enumerate(long_articles):
    aid = item['id']
    title, keywords, description, image = metadata[aid]
    content = json.dumps(item['content'], ensure_ascii=False)
    lines.extend([
        '    {',
        f"      id: {json.dumps(aid, ensure_ascii=False)}, title: {json.dumps(title, ensure_ascii=False)},",
        f"      keywords: {json.dumps(keywords, ensure_ascii=False)},",
        f"      description: {json.dumps(description, ensure_ascii=False)},",
        f"      content: {content},",
        f"      image: {json.dumps(image, ensure_ascii=False)}",
        '    }' + (',' if i < len(long_articles) - 1 else ''),
    ])
lines.extend(['  ]', '}', '', 'export default sexualDiseasesChapter', ''])
(root / 'src/data/sexualDiseases.js').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'articles': len(long_articles), 'wordCounts': {a['id']: a['wordCount'] for a in long_articles}}, ensure_ascii=False, indent=2))
