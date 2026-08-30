from pathlib import Path
import json, time, requests
from urllib.parse import quote
ROOT=Path('/home/ubuntu/marriage-education-website'); OUT=ROOT/'public/curated-web-images'; OUT.mkdir(parents=True,exist_ok=True)
queries={
'pm-01':'film camera','pm-02':'film studio','pm-03':'human portrait','pm-04':'conversation','pm-05':'couple conversation','pm-06':'counseling','pm-07':'health clinic','pm-08':'library books','pm-09':'support group','pm-10':'family conversation',
'sd-01':'medical infection illustration','sd-02':'syphilis','sd-03':'gonorrhea','sd-04':'HIV virus','sd-05':'herpes virus','sd-06':'human papillomavirus','sd-07':'hepatitis liver','sd-08':'parasite microscope','sd-09':'medical screening','sd-10':'doctor patient'}
h={'User-Agent':'MarriageEducationWebsite/1.0 (educational project)'}; credits=[]; seen=set()
for key,q in queries.items():
 try:
  p={'action':'query','generator':'search','gsrsearch':q,'gsrnamespace':'6','gsrlimit':'30','prop':'imageinfo','iiprop':'url|extmetadata','format':'json'}
  pages=requests.get('https://commons.wikimedia.org/w/api.php',params=p,headers=h,timeout=30).json().get('query',{}).get('pages',{}).values()
 except Exception as e: print('API_ERROR',key,type(e).__name__); continue
 chosen=None
 for page in pages:
  info=(page.get('imageinfo') or [{}])[0]; meta=info.get('extmetadata') or {}; lic=(meta.get('LicenseShortName') or {}).get('value',''); title=page.get('title','')
  if not title or title in seen or not any(x in lic.lower() for x in ['public domain','cc0','cc by','cc-by','cc by-sa','cc-by-sa']): continue
  chosen=(page,meta,lic); break
 if not chosen: print('NO_MATCH',key,q); continue
 page,meta,lic=chosen; title=page['title']; file_url='https://commons.wikimedia.org/wiki/Special:FilePath/'+quote(title.replace('File:',''),safe='')+'?width=1400'
 try:
  r=requests.get(file_url,headers=h,timeout=60,allow_redirects=True); r.raise_for_status()
  if len(r.content)<10000: print('TOO_SMALL',key); continue
  path=OUT/f'{key}.jpg'; path.write_bytes(r.content); seen.add(title)
  credits.append({'key':key,'query':q,'file':str(path.relative_to(ROOT)),'title':title,'creator':(meta.get('Artist') or {}).get('value'),'license':lic,'source':'https://commons.wikimedia.org/wiki/'+quote(title.replace(' ','_')),'download_url':file_url})
  print('OK',key,lic,path.name,len(r.content))
 except Exception as e: print('DOWNLOAD_ERROR',key,type(e).__name__,str(e))
 time.sleep(.2)
(ROOT/'CURATED_IMAGE_CREDITS.json').write_text(json.dumps(credits,ensure_ascii=False,indent=2),encoding='utf-8')
print('downloaded=',len(credits),'of',len(queries))
