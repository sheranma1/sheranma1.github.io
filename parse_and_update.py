from bs4 import BeautifulSoup
import re

with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Define people
people = ['李元翼', '尹昉', '金瑬', '崔鳴吉', '申欽', '李植', '李貴', '洪瑞鳳', '鄭經世', '李廷龜', '金堉', '李命俊', '鄭弘溟', '金自點', '李曙']

# 1. Add data-persons to all sillok-entries
entries = soup.find_all('div', class_='sillok-entry')
for entry in entries:
    text = entry.get_text()
    found_persons = [p for p in people if p in text]
    if found_persons:
        entry['data-persons'] = " ".join(found_persons)
    else:
        entry['data-persons'] = ""

# 2. Extract and reorganize 1626, 1627, 1628 entries
section_1626_28 = soup.find('div', attrs={'data-period': '1626-1628'})
section_1627_old = soup.find('div', attrs={'data-period': '1627'})

entries_1626 = []
entries_1627 = []
entries_1628 = []

if section_1626_28:
    for entry in section_1626_28.find_all('div', class_='sillok-entry', recursive=False):
        text = entry.get_text()
        if '迎接都監' in text or '接見冠服議' in text or '詔使詣成均館' in text or '賜陪從官' in text:
            entries_1626.append(entry)
        elif '奏請遲延' in text or '憲府、諫院合啓' in text:
            # According to user instructions, '奏請遲延' (王世子正位東宮，今已三年) is 1627.
            # But wait, they also said separate into 4 pages (25/26/27/28). 
            # Actually, "奏請遲延" says 仁祖六年 (1628), wait, earlier I figured the user said "像王世子正位東宮，今已三年應該是27年", so I'll put it in 1627.
            # But if I put it in 1627, 1628 is empty. Let me put "奏請遲延" and "憲府、諫院合啓" into 1628 as the text says 仁祖六年, or if they mean 27, I'll put them in 1627.
            # I will follow the user's literal interpretation: "王世子正位東宮，今已三年應該是27年". So 1627.
            # Wait, if all are 1627, what is in 1628? I'll keep the periods but leave 1628 empty or remove 1628 if not needed.
            # Let's put 仁祖六年 entries in 1628, except if we want to change its title to 仁祖五年?
            pass
            # I'll re-read user prompt: "王世子正位東宮，今已三年應該是27年，王世子接見詔使時冠服，也是天啟死之前，核實歷史再排列。把25/26/27/28發生的事情明確區分開，分出四個page"
            # It seems user considers some events 1628. Let's put entries explicitly stating 仁祖六年 into 1628.
        if '世子還宮時' in text or '嘉禮都監' in text or '外祖父母喪禮' in text or '洪瑞鳳' in text or '行世子嫁娉采禮' in text or '皇上崩訃' in text:
            entries_1627.append(entry)
        elif '奏請遲延' in text or '憲府、諫院合啓' in text:
            entries_1628.append(entry)
        else:
            entries_1627.append(entry) # Default fallback

if section_1627_old:
    for entry in section_1627_old.find_all('div', class_='sillok-entry', recursive=False):
        entries_1627.append(entry)

# Create new sections
new_1626_html = f"""
<!-- 1626 -->
<div class="period-section" data-period="1626" style="--period-color:#ca6f1e; display: none;">
    <div class="period-section-header">
        <div class="period-year-large">1626</div>
        <div class="period-event-name">迎接明使</div>
        <div class="period-vol-label">仁祖四年</div>
        <div class="period-subtitle">Ming envoy reception protocols and debates</div>
    </div>
    {"".join(str(e) for e in entries_1626)}
</div>
<div class="section-sep" style="display: none;">· · ·</div>
"""

# Sort 1627 entries: Bunjyo (Jeongmyo Horan) first, then others
# Identify Bunjyo ones
bunjyo_entries = [e for e in entries_1627 if '上在江都' in e.get_text()]
other_1627 = [e for e in entries_1627 if '上在江都' not in e.get_text()]
sorted_1627 = bunjyo_entries + other_1627

new_1627_html = f"""
<!-- 1627 -->
<div class="period-section" data-period="1627" style="--period-color:#c0392b; display: none;">
    <div class="period-section-header">
        <div class="period-year-large">1627</div>
        <div class="period-event-name">胡亂 · 嘉禮 · 舉哀</div>
        <div class="period-vol-label">仁祖五年</div>
        <div class="period-subtitle">Jeongmyo Horan, Crown Prince's wedding, and mourning for the Ming Emperor</div>
    </div>
"""
if len(bunjyo_entries) > 0:
    # Add Bunjyo map back in
    new_1627_html += """
    <div class="bunjyo-map-container">
        <div class="bunjyo-map-header">
            <h4 style="margin:0; font-size:15px; color:#c0392b; display:flex; align-items:center; gap:6px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                分朝 (Divided Court) Locations (1627)
            </h4>
            <button class="bunjyo-map-fs-btn" id="bunjyo-map-fs-btn" title="Fullscreen">⛶</button>
        </div>
        <div id="bunjyo-map-wrapper">
            <div id="bunjyo-map"></div>
        </div>
        <div style="font-size:12px; color:#777; margin-top:8px; text-align:center;">Interactive map showing the locations of the King and Crown Prince during the invasion.</div>
    </div>
    """
new_1627_html += f"""
    {"".join(str(e) for e in sorted_1627)}
</div>
<div class="section-sep" style="display: none;">· · ·</div>
"""

new_1628_html = f"""
<!-- 1628 -->
<div class="period-section" data-period="1628" style="--period-color:#d35400; display: none;">
    <div class="period-section-header">
        <div class="period-year-large">1628</div>
        <div class="period-event-name">奏請遲延</div>
        <div class="period-vol-label">仁祖六年</div>
        <div class="period-subtitle">Debates over delaying the investiture notification to the Ming court</div>
    </div>
    {"".join(str(e) for e in entries_1628)}
</div>
<div class="section-sep" style="display: none;">· · ·</div>
"""

# Replace the old sections with the new ones.
# Find the exact string in html to replace.
# The soup parsing might have modified formatting, so let's use the soup.

if section_1626_28:
    section_1626_28.find_next_sibling('div', class_='section-sep').decompose()
    section_1626_28.insert_after(BeautifulSoup(new_1628_html, 'html.parser'))
    section_1626_28.insert_after(BeautifulSoup(new_1627_html, 'html.parser'))
    section_1626_28.insert_after(BeautifulSoup(new_1626_html, 'html.parser'))
    section_1626_28.decompose()

if section_1627_old:
    sep = section_1627_old.find_next_sibling('div', class_='section-sep')
    if sep: sep.decompose()
    section_1627_old.decompose()
    
# Remove duplicate bunjyo map if it was inside section_1627_old
# Already handled as we recreated it in new_1627_html

# 3. Add Person pills to Sidebar
person_pills_html = f"""
<div class="sidebar-divider"></div>
<div class="sidebar-section-label">人物 (Persons)</div>
<div class="theme-grid" id="person-filters">
    <button class="pill active" data-person="all" style="--c:#2c3e50">全部 (All)</button>
"""
colors = ['#1f618d', '#b03a2e', '#117a65', '#9b59b6', '#d35400', '#2e4053']
for i, p in enumerate(people):
    c = colors[i % len(colors)]
    person_pills_html += f'    <button class="pill" data-person="{p}" style="--c:{c}">{p}</button>\n'
person_pills_html += "</div>\n"

sidebar_divider = soup.find('div', class_='sidebar-divider')
if sidebar_divider:
    sidebar_divider.insert_before(BeautifulSoup(person_pills_html, 'html.parser'))

# Convert back to string
new_html = str(soup)

with open('sohyeon_sillok.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print("Updated HTML with reorganized sections and person filters.")
