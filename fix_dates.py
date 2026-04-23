from bs4 import BeautifulSoup

with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Fix 1628 entries: change 仁祖五年 -> 仁祖六年 in date labels
sec_1628 = soup.find('div', attrs={'data-period': '1628'})
if sec_1628:
    for e in sec_1628.find_all('div', class_='entry-date'):
        if '仁祖五年' in e.get_text():
            e.string = e.get_text().replace('仁祖五年', '仁祖六年')

# Add the missing 1626 first entry (侍講院啓) per user's image
sec_1626 = soup.find('div', attrs={'data-period': '1626'})
if sec_1626:
    first_entry_html = """
<div class="sillok-entry" data-persons="李廷龜" data-themes="禮制" style="--entry-color:#7d6608">
    <div class="entry-meta">
        <div class="entry-date">仁祖四年 · 成均館侍講院 啓 (世子講學)</div>
        <div class="entry-tags"><span class="tag" style="--c:#7d6608">禮制</span></div>
    </div>
    <div class="entry-text">成均館侍講院啓曰：「王世子以侍病，自歲前終講，終值大慼，迄未開筵，冲年講學，寸陰可惜，而廢講之久，殆至三箇月，事極可惜。稗以《禮經》，未葬讓喪禮之義，則卒哭前專廢講業，似未妥當。會講、朝講，雖不可為，常時開筵，不可久停，而前受《小學》，實與《禮經》無異。來月月始，開筵何如？師傅之意如此。」敬啓。從之。</div>
    <details class="translation-toggle">
        <summary>查看白話文翻譯</summary>
        <div class="translation-text">成均館侍講院上奏說："王世子因為侍奉病患，從年前就停止了講學，然後又遇到大喪，一直未能開筵，以冲齡學習，寸陰可惜，但廢講已久，幾乎到了三個月，事情極為可惜。依照《禮經》，在未葬之前，喪禮的義理是卒哭之前專門廢止講業，這似乎不太妥當。大會講、朝講，雖然不可為，但平常的開筵，不可久停，而之前受講的《小學》，實際上與《禮經》並無不同。下月月初，開筵如何？師傅的意思如此。"請旨照辦。君王批准。</div>
    </details>
    <div class="entry-note"><em>(Powered by Gemini)</em> The Royal Tutorial Institute petitioned to resume the Crown Prince's studies, which had been suspended for nearly three months due to mourning obligations. They argued that the <em>Xiaoxue</em> (小學) texts already being studied were comparable to the <em>Lijing</em> (禮經) mourning texts, and thus the lectures should not be further delayed.</div>
</div>"""
    from bs4 import BeautifulSoup as BS
    new_entry = BS(first_entry_html, 'html.parser').div
    # Insert at the beginning of the section content (after the header)
    header = sec_1626.find('div', class_='period-section-header')
    if header:
        header.insert_after(new_entry)

with open('sohyeon_sillok.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Fixed date labels and added 1626 first entry.")
