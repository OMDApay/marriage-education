from pathlib import Path
import json, time, requests

ROOT = Path('/home/ubuntu/marriage-education-website')
OUT = ROOT / 'public' / 'curated-web-images'
OUT.mkdir(parents=True, exist_ok=True)
queries = {
    'pm-01': 'documentary film camera', 'pm-02': 'film editing video production',
    'pm-03': 'portrait diversity wellbeing', 'pm-04': 'consent counseling communication',
    'pm-05': 'couple counseling communication', 'pm-06': 'conversation counseling',
    'pm-07': 'health clinic consultation', 'pm-08': 'medical research library',
    'pm-09': 'mental health support group', 'pm-10': 'healthy relationship conversation',
    'sd-01': 'sexually transmitted disease medical illustration', 'sd-02': 'syphilis medical illustration',
    'sd-03': 'gonorrhea medical illustration', 'sd-04': 'HIV medical illustration',
    'sd-05': 'herpes simplex medical illustration', 'sd-06': 'human papillomavirus illustration',
    'sd-07': 'hepatitis liver medical illustration', 'sd-08': 'parasitic infection medical illustration',
    'sd-09': 'medical screening clinic', 'sd-10': 'doctor patient consultation',
}
headers = {'User-Agent': 'MarriageEducationWebsite/1.0 educational project'}
credits=[]; seen=set()
for key, term in queries.items():
    params={'action':'query','generator':'search','gsrsearch':term,'gsrnamespace':'6','gsrlimit':'30','prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':'1400','format':'json'}
    try:
        response=requests.get('https://commons.wikimedia.org/w/api.php', params=params, headers=headers, timeout=35)
        response.raise_for_status(); pages=response.json().get('query',{}).get('pages',{}).values()
    except Exception as exc:
        print('API_ERROR', key, type(exc).__name__); continue
    chosen=None
    for page in pages:
        info=(page.get('imageinfo') or [{}])[0]; meta=info.get('extmetadata') or {}
        lic=(meta.get('LicenseShortName') or {}).get('value','')
        url=info.get('thumburl') or info.get('url')
        if not url or url in seen: continue
        if not any(x in lic.lower() for x in ['cc0','public domain','cc by','cc-by','cc by-sa','cc-by-sa']): continue
        chosen=(page,info,meta,lic); break
    if not chosen:
        print('NO_LICENSED_MATCH', key, term); continue
    page,info,meta,lic=chosen; url=info.get('thumburl') or info.get('url'); ext='.jpg'
    path=OUT/f'{key}{ext}'
    try:
        r=requests.get(url, headers=headers, timeout=50); r.raise_for_status()
        if len(r.content)<8000: print('TOO_SMALL',key); continue
        path.write_bytes(r.content); seen.add(url)
        credits.append({'key':key,'query':term,'file':str(path.relative_to(ROOT)),'title':page.get('title'),'creator':(meta.get('Artist') or {}).get('value'),'license':lic,'source':'https://commons.wikimedia.org/wiki/'+page.get('title','').replace(' ','_'),'original_url':info.get('url')})
        print('OK',key,lic,path.name)
    except Exception as exc: print('DOWNLOAD_ERROR',key,type(exc).__name__)
    time.sleep(.25)
(ROOT/'CURATED_IMAGE_CREDITS.json').write_text(json.dumps(credits,ensure_ascii=False,indent=2),encoding='utf-8')
print('downloaded=',len(credits),'of',len(queries))
