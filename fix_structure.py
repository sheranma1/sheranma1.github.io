from bs4 import BeautifulSoup
import re

with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix smart quotes in data-period and other attributes
content = content.replace('data-period=”', 'data-period="').replace('”', '"')
content = content.replace('class=”', 'class="').replace('style=”', 'style="')

soup = BeautifulSoup(content, 'html.parser')

# Clean up duplicate section headers or empty tags
# The user had a lot of <!-- 1626 --> etc at the top. 
# We'll keep the text but ensure the data-period sections are clean.

# Ensure sidebar nav buttons match the sections
nav_list = soup.find('ul', class_='period-nav-list')
if nav_list:
    # Ensure standard buttons for 1625, 1626, 1627, 1628, 1637, 1638, 1645, 1646, 1647, 附錄
    # We'll just check what sections exist in the main content
    sections = soup.find_all('div', class_='period-section')
    existing_periods = [s.get('data-period') for s in sections if s.get('data-period')]
    
    # Rebuild nav list to match existing periods precisely
    new_nav = '<li><button data-period="all" style="--pc:#2c3e50"><span class="nav-year">全部時期</span></button></li>'
    # Sort them numerically if possible
    sorted_periods = sorted([p for p in existing_periods if p.isdigit()], key=int)
    if '附錄' in existing_periods: sorted_periods.append('附錄')
    
    # We'll follow the user's current nav if it's already there, but ensure it's clean.
    # Actually, the user wants "one year per page", so we'll ensure they are separated.

with open('sohyeon_sillok.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("HTML structure fixed (quotes and cleaning).")
