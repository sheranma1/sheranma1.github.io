from bs4 import BeautifulSoup
import copy

with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

people = ['李元翼','尹昉','金瑬','崔鳴吉','申欽','李植','李貴','洪瑞鳳','鄭經世','李廷龜','金堉','李命俊','鄭弘溟','金自點','李曙']

# ─── Step 1: Collect all entries from EVERY period section ────────────────
all_entries = {}  # period -> list of entry tags
for sec in soup.find_all('div', class_='period-section'):
    period = sec.get('data-period')
    all_entries[period] = [copy.copy(e) for e in sec.find_all('div', class_='sillok-entry')]

# ─── Step 2: Manually classify every entry by its TRUE year ───────────────
entries_by_year = {
    '1625': [],
    '1626': [],
    '1627': [],
    '1628': [],
}
later_periods = ['1637', '1638', '1645', '1646', '1647', '附錄']

def classify_entry(e):
    t = e.get_text()
    meta = e.find('div', class_='entry-date')
    date_str = meta.get_text() if meta else ''

    # 1625 (仁祖三年) ─ Investiture
    if '仁祖三年' in date_str or '冊封元子' in t or '東宮 官員 任命' in date_str or '史臣 按語' in date_str:
        return '1625'

    # 1626 (仁祖四年)
    # Source document year-marker 1626: entries from volumes 10-11
    # First entry: 講學 opening (成均館 講學 protocols)
    # The entry shown in user image: 成均館侍講院啓曰 "王世子以侍病..."
    # Also: 廷龜曰 (隨駕), 癸酉召見李貴, 迎接都監 (天使要見世子), 冠服議, 詔使詣成均館, 賜陪從官
    if '仁祖四年' in date_str or '侍講院啓' in t or '世子以侍病' in t:
        return '1626'
    if '廷龜曰' in t and '郊外擧動' in t:
        return '1626'
    if '癸酉王世子召見' in t:
        return '1626'
    if '迎接都監啓' in t and '天使要見' in t:
        return '1626'
    if '接見冠服議' in date_str or '接見詔使時冠服' in t:
        return '1626'
    if '詔使詣成均館' in t:
        return '1626'
    if '賜世子接見天使時陪從官' in t:
        return '1626'

    # 1627 (仁祖五年) ─ Jeongmyo Horan + Wedding + Ming mourning
    # First entry from user's image: 庚午禮曹啓曰 十四日等待近還宮時 殿下墨衲...
    # This is about funeral/mourning dress at return to palace (庚午 = 1st month 1627)
    # But wait: user says "1627年" first entry is 庚午禮曹啓曰 about 十四日等待近還宮時
    # However 庚午禮曹啓曰：「王世子正位東宮，今已三年」is also labeled 仁祖五年
    # The Horan entries (上在江都) are definitely 1627
    if '上在江都' in t:
        return '1627'
    if '丙戌引見大臣' in t and '賊已迫安州' in t:
        return '1627'
    if '庚午禮曹啓曰' in t and '十四日' in t:
        return '1627'
    if '世子還宮時' in date_str or '還宮時' in t and '拜謁' in t:
        return '1627'
    if '嘉禮都監啓' in t and '別宮' in t:
        return '1627'
    if '世子嬪外祖父母喪禮' in date_str:
        return '1627'
    if '洪瑞鳳上疏' in date_str or ('洪瑞鳳' in t and '小學' in t):
        return '1627'
    if '行世子嫁娉采禮' in t:
        return '1627'
    if '皇上崩訃' in t or '舉哀於景政殿' in t:
        return '1627'

    # 1628 (仁祖六年) ─ After Horan
    # User's document: "奏請遲延" entries, "憲府、諫院合啓"
    if '王世子正位東宮，今已三年' in t or '奏請遲延' in date_str:
        return '1628'
    if '世子受册經年' in t or '憲府、諫院合啓' in t:
        return '1628'
    if '仁祖五年 庚午 · 禮曹 啓' in date_str:
        # This date label "仁祖五年 庚午" = 1627, but the content "王世子正位東宮，今已三年" is 1628!
        # Actually 仁祖五年 = 1627. But user says "今已三年" (3 years since 1625 = 1628). 
        # Let's trust the explicit 仁祖五年 label in the date field.
        # Per user's image, 1627 starts with the 庚午 MOURNING DRESS entry, not the 奏請遲延.
        # 庚午日 in 1627 = 1627年正月庚午. Hmm both have 庚午.
        # The 奏請遲延 庚午 is in 仁祖五年 (1627) volume 15 (卷十五).
        # But the user's image shows 1627 starts with: 庚午禮曹啓曰十四日等待近還宮時... 殿下墨衲
        # So the FIRST 庚午 (墨衲 entry) is 1627, and the OTHER 庚午 (奏請) must be different date.
        # The 奏請 entry: "王世子正位東宮，今已三年" - since investiture was 1625, "三年" would be 1627 or 1628 depending on counting.
        # But user said it is 仁祖五年. So 1627.
        return '1627'
    if '仁祖五年' in date_str:
        return '1627'
    
    return None  # later period, leave alone

# Classify entries in 1625-1628 and earlier
for period in ['1625', '1626', '1627', '1628']:
    for e in all_entries.get(period, []):
        year = classify_entry(e)
        if year:
            # Fix data-persons
            t = e.get_text()
            found = [p for p in people if p in t]
            e['data-persons'] = ' '.join(found)
            entries_by_year[year].append(e)

# Also check 1627 section entries (like 丙戌引見大臣 which was incorrectly in 1626)
# The audit above shows 1626 section has "丙戌引見大臣...賊已迫安州" which is 1627 Jeongmyo Horan!
# Already handled above.

# ─── Step 3: Rebuild the 4 period sections ────────────────────────────────

def build_section(period, color, year_label, event_name, vol_label, subtitle, entries_html, extra_html=''):
    display = '' if period == '1625' else ' display: none;'
    return f"""
<!-- {period} -->
<div class="period-section" data-period="{period}" style="--period-color:{color};{display}">
    <div class="period-section-header">
        <div class="period-year-large">{year_label}</div>
        <div class="period-event-name">{event_name}</div>
        <div class="period-vol-label">{vol_label}</div>
        <div class="period-subtitle">{subtitle}</div>
    </div>
    {extra_html}
    {entries_html}
</div>
<div class="section-sep"{' style="display: none;"' if period != '1625' else ''}>· · ·</div>
"""

entries_1625_html = ''.join(str(e) for e in entries_by_year['1625'])
entries_1626_html = ''.join(str(e) for e in entries_by_year['1626'])

# For 1627: Horan map entries first
bunjyo = [e for e in entries_by_year['1627'] if '上在江都' in e.get_text() or '賊已迫安州' in e.get_text()]
other_1627 = [e for e in entries_by_year['1627'] if e not in bunjyo]
map_html = """
    <div class="bunjyo-map-container">
        <div class="bunjyo-map-header">
            <h4 style="margin:0; font-size:15px; color:#c0392b; display:flex; align-items:center; gap:6px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                分朝 (Divided Court) Locations · 1627
            </h4>
            <button class="bunjyo-map-fs-btn" id="bunjyo-map-fs-btn" title="Fullscreen">⛶</button>
        </div>
        <div id="bunjyo-map-wrapper"><div id="bunjyo-map"></div></div>
        <div style="font-size:12px; color:#777; margin-top:8px; text-align:center;">Interactive map showing locations of the King and Crown Prince during the invasion.</div>
    </div>
""" if bunjyo else ''

entries_1627_html = ''.join(str(e) for e in bunjyo) + ''.join(str(e) for e in other_1627)
entries_1628_html = ''.join(str(e) for e in entries_by_year['1628'])

html_1625 = build_section('1625', '#c9a227', '1625', '冊封', '卷八 · 仁祖三年',
    'The formal investiture of the Crown Prince and related diplomatic considerations',
    entries_1625_html)

html_1626 = build_section('1626', '#ca6f1e', '1626', '保傅與明使', '仁祖四年',
    'Discussions on the Crown Prince\'s education and Ming envoy reception protocols',
    entries_1626_html)

html_1627 = build_section('1627', '#c0392b', '1627', '胡亂 · 嘉禮 · 舉哀', '仁祖五年',
    'Jeongmyo Horan, Crown Prince\'s wedding, and mourning for the Ming Emperor',
    entries_1627_html, map_html)

html_1628 = build_section('1628', '#d35400', '1628', '丁卯後遺事', '仁祖六年',
    'Events and debates in the aftermath of the invasion',
    entries_1628_html)

# ─── Step 4: Remove all old 1625-1628 period sections from soup ───────────
for period in ['1625', '1626-1628', '1626', '1627', '1628']:
    sec = soup.find('div', attrs={'data-period': period})
    while sec:
        sep = sec.find_next_sibling('div', class_='section-sep')
        if sep: sep.decompose()
        sec.decompose()
        sec = soup.find('div', attrs={'data-period': period})

# ─── Step 5: Insert before 1637 ───────────────────────────────────────────
sec_1637 = soup.find('div', attrs={'data-period': '1637'})
new_sections = BeautifulSoup(html_1628 + html_1627 + html_1626 + html_1625, 'html.parser')
# Insert in reverse so the order ends up 1625, 1626, 1627, 1628, 1637
for tag in reversed(list(new_sections.children)):
    if tag.name:
        sec_1637.insert_before(copy.copy(tag))

# ─── Step 6: Fix sidebar nav ──────────────────────────────────────────────
nav_list = soup.find('ul', class_='period-nav-list')
if nav_list:
    for btn in nav_list.find_all('button'):
        p = btn.get('data-period', '')
        if p in ['1625', '1626-1628', '1626', '1627', '1628']:
            btn.parent.decompose()
    
    new_navs = BeautifulSoup("""
    <li><button class="active" data-period="1625" style="--pc:#c9a227">
        <span class="nav-year">1625</span>
        <span class="nav-event">冊封</span>
    </button></li>
    <li><button data-period="1626" style="--pc:#ca6f1e">
        <span class="nav-year">1626</span>
        <span class="nav-event">保傅與明使</span>
    </button></li>
    <li><button data-period="1627" style="--pc:#c0392b">
        <span class="nav-year">1627</span>
        <span class="nav-event">胡亂 · 嘉禮</span>
    </button></li>
    <li><button data-period="1628" style="--pc:#d35400">
        <span class="nav-year">1628</span>
        <span class="nav-event">丁卯後遺事</span>
    </button></li>
    """, 'html.parser')
    all_btn = nav_list.find('button', attrs={'data-period': 'all'})
    if all_btn:
        for li in reversed(list(new_navs.find_all('li'))):
            all_btn.parent.insert_after(copy.copy(li))

# ─── Step 7: Update JS periods array ──────────────────────────────────────
html_out = str(soup)
html_out = html_out.replace(
    "const periods = ['1625', '1626-1628', '1627',",
    "const periods = ['1625', '1626', '1627', '1628',")
html_out = html_out.replace(
    "const periods = ['1625', '1626', '1627', '1628', '1628',",  # avoid double
    "const periods = ['1625', '1626', '1627', '1628',")

with open('sohyeon_sillok.html', 'w', encoding='utf-8') as f:
    f.write(html_out)
print("Done. Verifying...")

# Verify
with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    soup2 = BeautifulSoup(f.read(), 'html.parser')
for sec in soup2.find_all('div', class_='period-section'):
    entries = sec.find_all('div', class_='sillok-entry')
    print(f"Period {sec['data-period']}: {len(entries)} entries")
