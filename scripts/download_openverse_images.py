from pathlib import Path
import json, time, re
import requests

ROOT = Path('/home/ubuntu/marriage-education-website')
OUT = ROOT / 'public' / 'curated-web-images'
OUT.mkdir(parents=True, exist_ok=True)
queries = {
    'pm-01': 'film camera documentary production',
    'pm-02': 'film editing timeline video production',
    'pm-03': 'diverse people portrait wellbeing',
    'pm-04': 'consent communication counseling',
    'pm-05': 'couple communication relationship counseling',
    'pm-06': 'conversation couple counseling',
    'pm-07': 'health safety medical consultation',
    'pm-08': 'medical research books library',
    'pm-09': 'mental health support therapist conversation',
    'pm-10': 'healthy relationship couple conversation',
    'sd-01': 'sexually transmitted infection medical illustration',
    'sd-02': 'syphilis medical illustration',
    'sd-03': 'gonorrhea medical illustration',
    'sd-04': 'HIV medical illustration immune system',
    'sd-05': 'herpes simplex medical illustration',
    'sd-06': 'human papillomavirus medical illustration',
    'sd-07': 'hepatitis liver medical illustration',
    'sd-08': 'parasitic infection medical illustration',
    'sd-09': 'sexual health screening clinic',
    'sd-10': 'doctor patient consultation health',
}
headers = {'User-Agent': 'MarriageEducationWebsite/1.0 (educational project)'}
credits = []
seen = set()
for key, query in queries.items():
    data = requests.get('https://api.openverse.org/v1/images/', params={'q': query, 'page_size': 30}, headers=headers, timeout=30).json()
    chosen = None
    for item in data.get('results', []):
        url = item.get('url')
        if not url or url in seen:
            continue
        if item.get('license') not in {'cc0', 'by', 'by-sa', 'by-nc', 'by-nc-sa'}:
            continue
        chosen = item
        break
    if not chosen:
        print('NO_MATCH', key, query)
        continue
    url = chosen['url']
    ext = '.jpg'
    if '.png' in url.lower(): ext = '.png'
    if '.webp' in url.lower(): ext = '.webp'
    path = OUT / f'{key}{ext}'
    try:
        r = requests.get(url, headers=headers, timeout=45)
        r.raise_for_status()
        if len(r.content) < 8000:
            print('TOO_SMALL', key, url)
            continue
        path.write_bytes(r.content)
        seen.add(url)
        credits.append({
            'key': key, 'query': query, 'file': str(path.relative_to(ROOT)),
            'title': chosen.get('title'), 'creator': chosen.get('creator'),
            'license': chosen.get('license'), 'license_version': chosen.get('license_version'),
            'source': chosen.get('foreign_landing_url') or chosen.get('source'), 'original_url': url,
        })
        print('OK', key, chosen.get('license'), path.name)
    except Exception as exc:
        print('DOWNLOAD_ERROR', key, type(exc).__name__, str(exc))
    time.sleep(0.3)
(ROOT / 'CURATED_IMAGE_CREDITS.json').write_text(json.dumps(credits, ensure_ascii=False, indent=2), encoding='utf-8')
print('downloaded=', len(credits), 'of', len(queries))
