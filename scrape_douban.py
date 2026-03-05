import urllib.request
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

def get_html(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8')

all_books = []
start = 0

while True:
    url = f'https://www.douban.com/doulist/162980002/?start={start}&sort=time&playable=0&sub_type='
    print(f'Fetching page starting at {start}...')
    try:
        html = get_html(url)
    except Exception as e:
        print(f'Error: {e}')
        break

    titles = re.findall(r'<div class="title">\s*<a href="([^"]+)"[^>]*>\s*([^\n<]+)\s*</a>', html)
    abstracts = re.findall(r'<div class="abstract">\s*(.*?)\s*</div>', html, re.DOTALL)
    print(f'  Found {len(titles)} titles, {len(abstracts)} abstracts')

    for i, (link, title) in enumerate(titles):
        info = abstracts[i].strip() if i < len(abstracts) else ''
        all_books.append({'title': title.strip(), 'link': link.strip(), 'info': info.strip()})

    if len(titles) == 0 or ('下一页' not in html and f'start={start + 25}' not in html):
        break
    start += 25
    if start > 300:
        break

print(f'\nTotal books found: {len(all_books)}')
for b in all_books:
    print(f"  - {b['title']} | {b['info'][:100]} | {b['link']}")
