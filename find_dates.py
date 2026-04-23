import urllib.request
import re
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Read the local html to extract all entry texts
with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    local_html = f.read()

soup = BeautifulSoup(local_html, 'html.parser')
entries = soup.find_all('div', class_='sillok-entry')

# We'll search these snippets
snippets = []
for entry in entries:
    text_el = entry.find('div', class_='entry-text')
    if text_el:
        text = text_el.get_text()
        snippets.append(text[:20].replace('○', '').replace(' ', ''))

print(f"Found {len(snippets)} entries to check.")

# Download wikisource indices for Injo Sillok
# Volumes 1-50
# Actually, I can just use a search API or fetch the pages.
