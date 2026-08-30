import hashlib
import requests

hashes = set()
for lock in range(1, 31):
    url = f'https://loremflickr.com/800/600/health,education?lock={lock}'
    try:
        r = requests.get(url, timeout=20, allow_redirects=True)
        h = hashlib.sha256(r.content).hexdigest()
        print(lock, r.status_code, r.headers.get('content-type'), len(r.content), h[:12])
        if r.status_code == 200 and r.headers.get('content-type','').startswith('image/'):
            hashes.add(h)
    except Exception as e:
        print(lock, type(e).__name__)
print('unique=', len(hashes))
