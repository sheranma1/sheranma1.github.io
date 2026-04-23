from bs4 import BeautifulSoup
import re

with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Define new 1625 entries based on the image exactly
entry_1625_1 = """
<div class="sillok-entry" data-persons="金瑬 申欽 尹昉 李元翼 李廷龜 吳允謙 鄭曄 鄭經世 李植 鄭百昌 姜碩期 俞伯曾 金光炫 沈之源 李楘 鄭宗溟" data-themes="禮制" style="--entry-color:#7d6608">
    <div class="entry-meta">
        <div class="entry-date">仁祖三年 正月 · 東宮 官員 任命 (卷八)</div>
        <div class="entry-tags"><span class="tag" style="--c:#7d6608">禮制</span></div>
    </div>
    <div class="entry-text">以金瑬為吏曹判書，南道兵使申景瑗為北道兵使，尹暄為兵曹參判，李元翼為世子師，尹昉為世子傅，李廷龜為左賓客，吳允謙為右賓客，鄭曄為左副賓客，鄭經世為右副賓客，李植為輔德，鄭百昌為弼善，姜碩期為兼司書，俞伯曾為兼文學，金光炫為司書，沈之源為兼說書，李楘為執義，鄭宗溟為檢詳。</div>
    <details class="translation-toggle">
        <summary>查看白話文翻譯</summary>
        <div class="translation-text">任命金瑬為吏曹判書，南道兵馬使申景瑗為北道兵馬使，尹暄為兵曹參判，李元翼為世子師，尹昉為世子傅，李廷龜為左賓客，吳允謙為右賓客，鄭曄為左副賓客，鄭經世為右副賓客，李植為輔德，鄭百昌為弼善，姜碩期為兼司書，俞伯曾為兼文學，金光炫為司書，沈之源為兼說書，李楘為執義，鄭宗溟為檢詳。</div>
    </details>
    <div class="entry-note">Officials appointed to the Crown Prince's household and education staff.</div>
</div>"""

entry_1625_2 = """
<div class="sillok-entry" data-persons="李植 鄭百昌" data-themes="論議" style="--entry-color:#566573">
    <div class="entry-meta">
        <div class="entry-date">仁祖三年 · 史臣 按語</div>
        <div class="entry-tags"><span class="tag" style="--c:#566573">論議</span></div>
    </div>
    <div class="entry-text">李植、鄭百昌之文學，當今罕儔，而至於輔導世子，皆以親屬為之，則未免偏係之私。</div>
    <details class="translation-toggle">
        <summary>查看白話文翻譯</summary>
        <div class="translation-text">李植、鄭百昌的文學造詣當今罕有匹敵，但至於輔導世子之職，都由親屬來擔任，則未免有偏私之嫌。</div>
    </details>
    <div class="entry-note">The historian notes that while Li Sik and Jeong Baek-chang are exceptional scholars, their appointment as the Crown Prince's tutors, given their family relations, cannot escape the suspicion of partiality.</div>
</div>"""

entry_1625_3 = """
<div class="sillok-entry" data-persons="" data-themes="禮制" style="--entry-color:#7d6608">
    <div class="entry-meta">
        <div class="entry-date">仁祖三年 正月 丙子日 · 冊封</div>
        <div class="entry-tags"><span class="tag" style="--c:#7d6608">禮制</span></div>
    </div>
    <div class="entry-text">丙子冊封元子為王世子，年十四歲也。上出御隆政殿，命近臣宣教，命又授竹冊。教命文曰：宗儲主鬯，所以順天經，貳極定名，所以固國本，須位序之早正，宜典冊之極崇。</div>
    <details class="translation-toggle">
        <summary>查看白話文翻譯</summary>
        <div class="translation-text">丙子日，冊封元子為王世子，當時年僅十四歲。君王駕臨隆政殿，命令近臣宣讀教旨，並授予竹冊。教旨中說：宗室儲君主管祭祀，這是為了順應天道；確立皇儲的名分，這是為了鞏固國家的根本。必須儘早端正名分和位次，理應給予最為崇高的典禮與冊封。</div>
    </details>
    <div class="entry-note">The formal investiture of the fourteen-year-old eldest son as Crown Prince at Yungjeongjeon, underscoring his crucial role in maintaining state stability and royal lineage.</div>
</div>"""

entry_1625_4 = """
<div class="sillok-entry" data-persons="尹昉 吳允謙 鄭曄 鄭經世 李廷龜" data-themes="禮制" style="--entry-color:#7d6608">
    <div class="entry-meta">
        <div class="entry-date">仁祖三年 正月 丁丑日 · 賀冊禮成</div>
        <div class="entry-tags"><span class="tag" style="--c:#7d6608">禮制</span></div>
    </div>
    <div class="entry-text">丁丑上御隆政殿，受群臣賀，蓋賀王世子冊禮成也。左議政尹昉等率百官進箋，卽日宣教大赦。上下教曰：“世子師傅吳允謙、鄭曄、鄭經世及百官加親授。李廷龜族屬中六品遷轉。”廷龜已至輔國階，故有是命。師傅，元子時師傅也。</div>
    <details class="translation-toggle">
        <summary>查看白話文翻譯</summary>
        <div class="translation-text">丁丑日，君王駕臨隆政殿，接受群臣的祝賀，這是為了祝賀王世子的冊封典禮完成。左議政尹昉等人率領百官呈上賀箋，當天頒布教旨大赦天下。君王下達教旨說：“世子的師傅吳允謙、鄭曄、鄭經世以及百官，都給予親自授職的恩典。李廷龜的家族親屬中，六品官員予以升遷。”李廷龜已經達到了輔國的品階，所以有這樣的命令。這裡的師傅，是指世子還是元子時期的師傅。</div>
    </details>
    <div class="entry-note">The King received congratulations from the officials for the completion of the Crown Prince's investiture ceremony. A general amnesty was declared, and the Crown Prince's tutors and officials were granted promotions and honors.</div>
</div>"""

entry_1625_5 = """
<div class="sillok-entry" data-persons="鄭百昌 金堉 洪瑞鳳 尹衡彥 李如璜" data-themes="論議" style="--entry-color:#566573">
    <div class="entry-meta">
        <div class="entry-date">仁祖三年 正月 乙未日 · 憲府及持平金堉啓</div>
        <div class="entry-tags"><span class="tag" style="--c:#566573">論議</span></div>
    </div>
    <div class="entry-text">憲府啓曰：“春坊之官，極一時之選，居講筵者，固無踰於鄭百昌。今世子富於春秋，師道在嚴，前日筵臣之陳啓者，有意存焉，請遞鄭百昌兼輔德之任。”答曰：“鄭百昌固不合於講官。爾等所謂有意存焉者，是誠何心也？予不識爾等之意，故不卽允從，大抵臺官，不當如是碌碌也。”
○乙未持平金堉啓曰：“昨論鄭百昌之事者，非有他意，只為百昌親暱於世子，而世子富於春秋，殿下之所以教導者，當示以至公無私之道。豈無他人，而使百昌兼任，使世子習知親私之可親、疏遠之可疏哉？且親私則不嚴，疏遠則生敬，開講之際，損益可知也。不然則以百昌名望，出入三司，踐歷華貫，其誰曰不可於此也。頃日筵臣之陳啓者，亦有見乎此，其意實在防微之遠慮，而未浹數旬，旋入講院。故臣發言於僚席，請遞其任，而措語之際，未能明白。殿下之不卽允從，出於不識其意而然也。反示未安之意，折之以碌碌之教者何哉？殿下之輕蔑臺臣，厭聞忠言，不啻詑詑之色，雖有古之遺直，孰肯為殿下盡言哉？緣臣措語之失，致有聖德之累，臣之罪戾，誠出自作，決不可仍冒，請罷斥臣職。”大司憲洪瑞鳳、掌令尹衡彥·李如璜亦以此引避，玉堂處置請出。</div>
    <details class="translation-toggle">
        <summary>查看白話文翻譯</summary>
        <div class="translation-text">司憲府上奏說：“春坊（太子宮）的官員，都是一時的精選，在講筵（為君王或太子講學的地方）任職的人中，確實沒有超過鄭百昌的。現在世子年紀還小，為師之道在於嚴格，前幾天在講筵上陳奏的臣子，是有其深意的，請求免去鄭百昌兼任輔德的職務。”君王回答說：“鄭百昌本來就不適合做講官。你們所說的‘有其深意’，到底是存著什麼心思？我不明白你們的意思，所以沒有立刻答應，總之言官不應該像這樣平庸無能。”
○乙未日，持平金堉上奏說：“昨天討論鄭百昌的事情，並沒有別的意思，只是因為鄭百昌與世子過於親近，而世子年紀尚小，殿下用來教導世子的，應當是展現大公無私的道理。難道沒有其他人了嗎，非要讓鄭百昌兼任，讓世子習慣性地知道親近的人可以親近、疏遠的人可以疏遠嗎？而且過於親近就不會嚴格，保持距離才會產生敬畏，在講課的時候，這對世子學業的損益是顯而易見的。如果不是因為這個原因，以鄭百昌的名望，出入三司（弘文館、司憲府、司諫院），歷任顯要官職，誰會說他不適合這個職位呢？前幾天在講筵上陳奏的臣子，也是看到了這一點，他的本意確實是出於防微杜漸的深謀遠慮，但還不到幾十天，鄭百昌就又進入了講院。所以臣在同僚中發言，請求免去他的職務，但在措辭的時候，沒有說得夠明白。殿下沒有立刻答應，是因為不明白臣的意思。但殿下反而表現出不悅，用‘平庸無能’的教訓來挫傷臣等，這是為什麼呢？殿下輕視言官，討厭聽忠言，不僅僅是表現出不耐煩的神色，就算有古代那樣遺留下來的正直之臣，誰又肯為殿下暢所欲言呢？因為臣措辭的失誤，導致聖上的德行受到牽連，臣的罪過實在是咎由自取，絕對不能再繼續擔任這個職位，請罷免臣的官職。”大司憲洪瑞鳳、掌令尹衡彥、李如璜也因此請求辭職避嫌，弘文館（玉堂）經過討論後請求讓他們復職。</div>
    </details>
    <div class="entry-note">The Censorate requested the removal of Jeong Baek-chang as the Crown Prince's tutor, arguing that his close relationship with the Prince would undermine the strictness required in education. King Injo rejected the request, leading to further protests and resignations from officials including Gim Yuk and Hong Seo-bong.</div>
</div>"""

entry_1625_6 = """
<div class="sillok-entry" data-persons="" data-themes="外交" style="--entry-color:#1a5276">
    <div class="entry-meta">
        <div class="entry-date">仁祖三年 正月 丁未日 · 禮曹 啓</div>
        <div class="entry-tags"><span class="tag" style="--c:#1a5276">外交</span></div>
    </div>
    <div class="entry-text">丁未禮曹啓曰：“王世子冊封事，當據例奏請，別遣使臣，或順付於謝恩使、或冬至·聖節使，議大臣以定何如？”答曰：“世子冊封，據例奏請，未為不可。但兩天使纔過，而繼有詔使之行，則赤立之民，決難支堪，徐待後日，更觀民力而處之可也。”</div>
    <details class="translation-toggle">
        <summary>查看白話文翻譯</summary>
        <div class="translation-text">丁未日，禮曹上奏說：“王世子冊封的事情，應當按照慣例向大明奏請，是另外派遣使臣，還是順便委託給謝恩使，或者是冬至使、聖節使，請與大臣們商議後決定如何？”君王回答說：“世子冊封，按照慣例奏請，這並不是不可以。但是兩位大明天使才剛剛過去，如果接著又有迎接詔使的活動，那麼赤貧的百姓絕對難以支撐，還是暫且等到以後，再觀察民力情況來處理吧。”</div>
    </details>
    <div class="entry-note">The Ministry of Rites proposed sending an envoy to the Ming court to announce the Crown Prince's investiture. King Injo delayed the request, citing the severe economic strain on the people caused by recent diplomatic receptions.</div>
</div>"""

entry_1625_7 = """
<div class="sillok-entry" data-persons="尹昉" data-themes="論議 外交" style="--entry-color:#566573">
    <div class="entry-meta">
        <div class="entry-date">仁祖三年 · 領事 尹昉 啓</div>
        <div class="entry-tags"><span class="tag" style="--c:#566573">論議</span><span class="tag" style="--c:#1a5276">外交</span></div>
    </div>
    <div class="entry-text">領事尹昉曰：“臣再侍王世子於冊禮之後，則世子岐嶷夙成，講學之際，深解旨義，誠一國臣民之慶、祖宗社稷之福也。冊封奏請，不可遲緩，臣等欲付謝恩使之行，自上以民弊為慮，不卽允從。臣等之意，不如從速奏聞。”上曰：“此非急急之事，今番接待詔使，亦恐民力之難堪。況年年酬應詔使，則何以為國乎？姑待後日。”</div>
    <details class="translation-toggle">
        <summary>查看白話文翻譯</summary>
        <div class="translation-text">領事尹昉說：“臣在冊封典禮之後再次侍奉王世子，發現世子聰穎早熟，在講學的時候，能深刻理解其中的含義，這實在是全國臣民的慶幸、祖宗社稷的福氣。冊封奏請的事情，不能遲緩，臣等本想委託謝恩使一併辦理，但殿下因為擔心百姓的負擔，沒有立刻答應。臣等的意思是，不如儘快向大明奏報。”君王說：“這不是非常緊急的事情，這次接待大明詔使，也擔心民力難以承受。況且如果年年都要應酬詔使，那還拿什麼來治理國家呢？暫且等到以後再說吧。”</div>
    </details>
    <div class="entry-note">Yun Bang praised the Crown Prince's early maturity and intellect, urging the King to promptly notify the Ming court of the investiture. Injo again refused, prioritizing the alleviation of the people's financial burdens over immediate diplomatic protocols.</div>
</div>"""

entries_1625 = [entry_1625_1, entry_1625_2, entry_1625_3, entry_1625_4, entry_1625_5, entry_1625_6, entry_1625_7]

# Extract all existing entries to redistribute
all_old_entries = soup.find_all('div', class_='sillok-entry')
entries_1626 = []
entries_1627 = []
entries_1628 = []

for entry in all_old_entries:
    t = entry.get_text()
    meta = entry.find('div', class_='entry-date')
    if not meta: continue
    
    # Check if this entry is one of the old 1625 ones we just replaced
    if '丙子冊封元子' in t or '李植、鄭百昌之文學' in t or '以金瑬為吏曹判書' in t or '乙未持平金堉啓' in t or '丁未禮曹啓' in t or '領事尹昉曰' in t:
        continue # Skip, we already have the new formatted ones

    # Now, assign to 1626, 1627, 1628
    
    # 1626 (Injo 4) entries
    # The 4 orphaned entries from old 1625:
    if '掌令鄭弘溟啓曰' in t or '領議政李元翼啓曰' in t or '廷龜曰' in t or '癸酉王世子召見延平府院君李貴' in t:
        meta.string = meta.string.replace('三年', '四年')
        entries_1626.append(entry)
    # Ming envoy entries (before Tianqi death)
    elif '迎接都監啓' in t or '接見冠服議' in t or '詔使詣成均館' in t or '賜陪從官' in t:
        meta.string = meta.string.replace('六年', '四年')
        entries_1626.append(entry)
        
    # 1627 (Injo 5) entries
    # "正位東宮，今已三年" -> User specified 1627
    elif '奏請遲延' in t or '王世子正位東宮，今已三年' in t or '世子受册經年' in t:
        meta.string = meta.string.replace('六年', '五年')
        entries_1627.append(entry)
    # Jeongmyo Horan, Wedding, etc.
    elif '世子還宮時' in t or '嘉禮都監' in t or '外祖父母喪禮' in t or '洪瑞鳳上疏' in t or '行世子嫁娉采禮' in t or '皇上崩訃' in t or '上在江都' in t:
        entries_1627.append(entry)
        
    # 1628 (Injo 6) entries
    # Anything else? We'll leave 1628 empty if there's nothing, or if any entry was explicitly meant for 1628.
    else:
        # If it belongs to later years (1637+), skip.
        # This script only re-organizes the entries we extracted from 1626-28 and 1625.
        pass

# Now reconstruct the sections in the soup

# 1. 1625
section_1625 = soup.find('div', attrs={'data-period': '1625'})
if section_1625:
    # Clear old entries
    for e in section_1625.find_all('div', class_='sillok-entry'):
        e.decompose()
    # Insert new entries
    for html_str in entries_1625:
        section_1625.append(BeautifulSoup(html_str, 'html.parser'))

# Find the 1626-1628 section to decompose
section_1626_28 = soup.find('div', attrs={'data-period': '1626-1628'})
if section_1626_28:
    section_1626_28.decompose()
section_1627_old = soup.find('div', attrs={'data-period': '1627'})
if section_1627_old:
    section_1627_old.decompose()

# Ensure we don't have multiple copies of separated sections
for p in ['1626', '1627', '1628']:
    s = soup.find('div', attrs={'data-period': p})
    if s: s.decompose()

new_1626_html = f"""
<!-- 1626 -->
<div class="period-section" data-period="1626" style="--period-color:#ca6f1e; display: none;">
    <div class="period-section-header">
        <div class="period-year-large">1626</div>
        <div class="period-event-name">保傅與明使</div>
        <div class="period-vol-label">仁祖四年</div>
        <div class="period-subtitle">Discussions on the Crown Prince's education and Ming envoy reception protocols</div>
    </div>
    {"".join(str(e) for e in entries_1626)}
</div>
<div class="section-sep" style="display: none;">· · ·</div>
"""

# Sort 1627: Bunjyo first
bunjyo_entries = [e for e in entries_1627 if '上在江都' in e.get_text()]
other_1627 = [e for e in entries_1627 if '上在江都' not in e.get_text()]

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
if bunjyo_entries:
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
    new_1627_html += "".join(str(e) for e in bunjyo_entries)
new_1627_html += "".join(str(e) for e in other_1627)
new_1627_html += """
</div>
<div class="section-sep" style="display: none;">· · ·</div>
"""

new_1628_html = f"""
<!-- 1628 -->
<div class="period-section" data-period="1628" style="--period-color:#d35400; display: none;">
    <div class="period-section-header">
        <div class="period-year-large">1628</div>
        <div class="period-event-name">丁卯後遺事</div>
        <div class="period-vol-label">仁祖六年</div>
        <div class="period-subtitle">Events and debates in the aftermath of the invasion</div>
    </div>
    {"".join(str(e) for e in entries_1628)}
</div>
<div class="section-sep" style="display: none;">· · ·</div>
"""

# Find where to insert them. Right after 1625 section.
sep_1625 = section_1625.find_next_sibling('div', class_='section-sep')
if sep_1625:
    sep_1625.insert_after(BeautifulSoup(new_1628_html, 'html.parser'))
    sep_1625.insert_after(BeautifulSoup(new_1627_html, 'html.parser'))
    sep_1625.insert_after(BeautifulSoup(new_1626_html, 'html.parser'))

# Make sure Sidebar buttons are 1625, 1626, 1627, 1628
nav_list = soup.find('ul', class_='period-nav-list')
if nav_list:
    # clear old ones
    for btn in nav_list.find_all('button'):
        p = btn.get('data-period')
        if p in ['1626-1628', '1627']:
            btn.parent.decompose()
    
    # insert new ones after 1625
    li_1625 = None
    for li in nav_list.find_all('li'):
        if li.find('button', attrs={'data-period': '1625'}):
            li_1625 = li
            break
            
    if li_1625:
        new_navs = """
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
        """
        li_1625.insert_after(BeautifulSoup(new_navs, 'html.parser'))

with open('sohyeon_sillok.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
