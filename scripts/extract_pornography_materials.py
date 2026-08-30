from pathlib import Path
from docx import Document

sources = [
    Path('/home/ubuntu/upload/اضرارالمصواللحس.docx'),
    Path('/home/ubuntu/upload/A2M.docx'),
]
out = Path('/home/ubuntu/marriage-education-website/reference_materials')
out.mkdir(parents=True, exist_ok=True)
for src in sources:
    doc = Document(src)
    lines = []
    for p in doc.paragraphs:
        text = ' '.join(p.text.split())
        if text:
            lines.append(text)
    target = out / f'{src.stem}_extracted.txt'
    target.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(src.name, 'paragraphs=', len(lines), 'chars=', sum(map(len, lines)), '->', target)
