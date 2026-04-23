import re

with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We want to replace the sections 1626-1628 and 1627 with three new sections: 1626, 1627, 1628.
# First, let's extract all the <div class="sillok-entry">...</div> blocks from these two sections.

# Find the start of 1626-1628 section and end of 1627 section.
pattern = re.compile(r'<!-- 1626–28 -->.*?<!-- 1637 -->', re.DOTALL)
match = pattern.search(html)

if match:
    sections_html = match.group(0)
    # Extract all entries
    entry_pattern = re.compile(r'<div class="sillok-entry".*?</div>\s*(?=</div>|\s*<div class="sillok-entry"|\s*</div>\s*<div class="section-sep")|<div class="sillok-entry".*?</div>\s*</div>', re.DOTALL)
    
    entries = []
    # A better way to extract entries: split by '<div class="sillok-entry"'
    parts = sections_html.split('<div class="sillok-entry"')
    for part in parts[1:]:
        # Find the end of this entry. An entry ends where the next thing is another entry, or the end of the section.
        # But each entry is self-contained. Since there are nested divs, regex is tricky.
        pass

# Let's use BeautifulSoup
