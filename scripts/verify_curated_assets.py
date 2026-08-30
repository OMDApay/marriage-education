from pathlib import Path
import re, hashlib
ROOT=Path('/home/ubuntu/marriage-education-website')
files=[ROOT/'src/data/pornMediaLiteracy.js',ROOT/'src/data/sexualDiseases.js']
paths=[]
for f in files:
    text=f.read_text(encoding='utf-8')
    found=re.findall(r"image: '([^']+)'",text)
    print(f.name, 'images=',len(found))
    for p in found:
        path=ROOT/'public'/p.lstrip('/') if p.startswith('/') else ROOT/p
        ok=path.exists()
        print(' ',p,'OK' if ok else 'MISSING')
        if ok: paths.append((p,hashlib.sha256(path.read_bytes()).hexdigest()))
print('missing=',sum(1 for p,_ in paths if not p))
print('duplicate_content=',len(paths)!=len(set(h for _,h in paths)))
