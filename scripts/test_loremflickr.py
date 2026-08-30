from pathlib import Path
import hashlib
import requests

out = Path('/home/ubuntu/marriage-education-website/tmp_image_test')
out.mkdir(exist_ok=True)
urls = [
    'https://loremflickr.com/800/600/medical,health?lock=1',
    'https://loremflickr.com/800/600/medical,health?lock=2',
    'https://loremflickr.com/800/600/pregnancy,baby?lock=3',
    'https://loremflickr.com/800/600/family,couple?lock=4',
]
hashes = []
for i, url in enumerate(urls, 1):
    r = requests.get(url, timeout=30, allow_redirects=True)
    data = r.content
    path = out / f'{i}.jpg'
    path.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    hashes.append(digest)
    print(i, r.status_code, r.headers.get('content-type'), len(data), digest, r.url)
print('unique_hashes=', len(set(hashes)))
