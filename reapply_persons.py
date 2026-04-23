from bs4 import BeautifulSoup

people = ['李元翼','尹昉','金瑬','崔鳴吉','申欽','李植','李貴','洪瑞鳳','鄭經世','李廷龜','金堉','李命俊','鄭弘溟','金自點','李曙']

with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

entries = soup.find_all('div', class_='sillok-entry')
for entry in entries:
    t = entry.get_text()
    found = [p for p in people if p in t]
    entry['data-persons'] = " ".join(found)

with open('sohyeon_sillok.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("data-persons reapplied.")
