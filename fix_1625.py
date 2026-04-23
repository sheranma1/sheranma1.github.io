import re

with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We'll locate the 1625 section and replace it with the correct entries
# First, let's just make the changes to the 1625 entries.

entry_new_4 = """                <div class="sillok-entry" data-persons="尹昉 吳允謙 鄭曄 鄭經世 李廷龜" data-themes="禮制" style="--entry-color:#7d6608">
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

# For the 5th entry, we combine 憲府啓曰 and 乙未持平金堉啓曰.
# We'll just replace the existing 乙未持平金堉啓曰 entry.
