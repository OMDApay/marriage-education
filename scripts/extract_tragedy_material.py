from pathlib import Path
from docx import Document

src = Path('/home/ubuntu/upload/امراضهم.docx')
out_dir = Path('/home/ubuntu/marriage-education-website/reference_materials')
out_dir.mkdir(parents=True, exist_ok=True)
doc = Document(src)
lines = []
for paragraph in doc.paragraphs:
    text = ' '.join(paragraph.text.split())
    if text:
        lines.append(text)
target = out_dir / 'امراضهم_extracted.txt'
target.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('paragraphs=', len(lines), 'chars=', sum(map(len, lines)), 'target=', target)
