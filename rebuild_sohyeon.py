from bs4 import BeautifulSoup
import re

# We will rebuild the entire content from scratch to ensure perfect order and selection.

people = ['李元翼','尹昉','金瑬','崔鳴吉','申欽','李植','李貴','洪瑞鳳','鄭經世','李廷龜','金堉','李命俊','鄭弘溟','金自點','李曙']

def create_entry(date, tags, text, trans, note, persons=""):
    found = [p for p in people if p in text]
    persons = " ".join(found)
    tag_html = "".join([f'<span class="tag" style="--c:{get_tag_color(t)}">{t}</span>' for t in tags])
    color = get_tag_color(tags[0]) if tags else "#7d6608"
    
    return f"""
                <div class="sillok-entry" data-persons="{persons}" data-themes="{" ".join(tags)}" style="--entry-color:{color}">
                    <div class="entry-meta">
                        <div class="entry-date">{date}</div>
                        <div class="entry-tags">{tag_html}</div>
                    </div>
                    <div class="entry-text">{text}</div>
                    <details class="translation-toggle">
                        <summary>查看白話文翻譯</summary>
                        <div class="translation-text">{trans}</div>
                    </details>
                    <div class="entry-note">{note}</div>
                </div>"""

def get_tag_color(tag):
    colors = {
        "禮制": "#7d6608",
        "論議": "#566573",
        "外交": "#1a5276",
        "戰爭": "#c0392b",
        "地圖": "#2e86c1",
        "教育": "#d35400"
    }
    return colors.get(tag, "#7d6608")

# 1625 Entries
e1625_1 = create_entry(
    "仁祖三年 正月 · 東宮 官員 任命 (卷八)", ["禮制"],
    "以金瑬為吏曹判書，南道兵使申景瑗為北道兵使，尹暄為兵曹參判，李元翼為世子師，尹昉為世子傅，李廷龜為左賓客，吳允謙為右賓客，鄭曄為左副賓客，鄭經世為右副賓客，李植為輔德，鄭百昌為弼善，姜碩期為兼司書，俞伯曾為兼文學，金光炫為司書，沈之源為兼說書，李楘為執義，鄭宗溟為檢詳。",
    "任命金瑬為吏曹判書，南道兵馬使申景瑗為北道兵馬使，尹暄為兵曹參判，李元翼為世子師，尹昉為世子傅，李廷龜為左賓客，吳允謙為右賓客，鄭曄為左副賓客，鄭經世為右副賓客，李植為輔德，鄭百昌為弼善，姜碩期為兼司書，俞伯曾為兼文學，金光炫為司書，沈之源為兼說書，李楘為執義，鄭宗溟為檢詳。",
    "Officials appointed to the Crown Prince's household and education staff."
)
e1625_2 = create_entry(
    "仁祖三年 · 史臣 按語", ["論議"],
    "李植、鄭百昌之文學，當今罕儔，而至於輔導世子，皆以親屬為之，則未免偏係之私。",
    "李植、鄭百昌的文學造詣當今罕有匹敵，但至於輔導世子之職，都由親屬來擔任，則未免有偏私之嫌。",
    "The historian notes that while Li Sik and Jeong Baek-chang are exceptional scholars, their appointment as the Crown Prince's tutors, given their family relations, cannot escape the suspicion of partiality."
)
e1625_3 = create_entry(
    "仁祖三年 正月 丙子日 · 冊封", ["禮制"],
    "丙子冊封元子為王世子，年十四歲也。上出御隆政殿，命近臣宣教，命又授竹冊。教命文曰：宗儲主鬯，所以順天經，貳極定名，所以固國本，須位序之早正，宜典冊之極崇。",
    "丙子日，冊封元子為王世子，當時年僅十四歲。君王駕臨隆政殿，命令近臣宣讀教旨，並授予竹冊。教旨中說：宗室儲君主管祭祀，這是為了順應天道；確立皇儲的名分，這是為了鞏固國家的根本。必須儘早端正名分和位次，理應給予最為崇高的典禮與冊封。",
    "The formal investiture of the fourteen-year-old eldest son as Crown Prince."
)
e1625_4 = create_entry(
    "仁祖三年 正月 丁丑日 · 賀冊禮成", ["禮制"],
    "丁丑上御隆政殿，受群臣賀，蓋賀王世子冊禮成也。左議政尹昉等率百官進箋，卽日宣教大赦。上下教曰：“世子師傅吳允謙、鄭曄、鄭經世及百官加親授。李廷龜族屬中六品遷轉。”廷龜已至輔國階，故有是命。師傅，元子時師傅也。",
    "丁丑日，君王駕臨隆政殿，接受群臣的祝賀，這是為了祝賀王世子的冊封典禮完成。左議政尹昉等人率領百官呈上賀箋，當天頒布教旨大赦天下。君王下達教旨說：“世子的師傅吳允謙、鄭曄、鄭經世以及百官，都給予親自授職的恩典。李廷龜的家族親屬中，六品官員予以升遷。”李廷龜已經達到了輔國的品階，所以有這樣的命令。這裡的師傅，是指世子還是元子時期的師傅。",
    "The King received congratulations for the completion of the Crown Prince's investiture ceremony."
)
e1625_5 = create_entry(
    "仁祖三年 正月 乙未日 · 憲府及持平金堉啓", ["論議"],
    "憲府啓曰：“春坊之官，極一時之選，居講筵者，固無踰於鄭百昌。今世子富於春秋，師道在嚴，前日筵臣之陳啓者，有意存焉，請遞鄭百昌兼輔德之任。”答曰：“鄭百昌固不合於講官。爾等所謂有意存焉者，是誠何心也？予不識爾等之意，故不卽允從，大抵臺官，不當如是碌碌也。”\n○乙未持平金堉啓曰：“昨論鄭百昌之事者，非有他意，只為百昌親暱於世子，而世子富於春秋，殿下之所以教導者，當示以至公無私之道。豈無他人，而使百昌兼任，使世子習知親私之可親、疏遠之可疏哉？且親私則不嚴，疏遠則生敬，開講之際，損益可知也。不然則以百昌名望，出入三司，踐歷華貫，其誰曰不可於此也。頃日筵臣之陳啓者，亦有見乎此，其意實在防微之遠慮，而未浹數旬，旋入講院。故臣發言於僚席，請遞其任，而措語之際，未能明白。殿下之不卽允從，出於不識其意而然也。反示未安之意，折之以碌碌之教者何哉？殿下之輕蔑臺臣，厭聞忠言，不啻詑詑之色，雖有古之遺直，孰肯為殿下盡言哉？緣臣措語之失，致有聖德之累，臣之罪戾，誠出自作，決不可仍冒，請罷斥臣職。”大司憲洪瑞鳳、掌令尹衡彥·李如璜亦以此引避，玉堂處置請出。",
    "司憲府上奏請求免去鄭百昌兼任輔德的職務。君王拒絕並指責言官平庸無能。持平金堉進一步進言，強調教導世子應大公無私，避免過於親近。大司憲洪瑞鳳等人也紛紛請求辭職。",
    "The Censorate argued that Jeong Baek-chang's close relationship with the Prince would undermine the strictness required in education."
)
e1625_6 = create_entry(
    "仁祖三年 正月 丁未日 · 禮曹 啓", ["外交"],
    "丁未禮曹啓曰：“王世子冊封事，當據例奏請，別遣使臣，或順付於謝恩使、或冬至·聖節使，議大臣以定何如？”答曰：“世子冊封，據例奏請，未為不可。但兩天使纔過，而繼有詔使之行，則赤立之民，決難支堪，徐待後日，更觀民力而處之可也。”",
    "禮曹建議派使臣去大明奏請冊封世子。君王因擔心連年接待使臣會加重百姓負擔而推遲。",
    "The Ministry of Rites proposed notifying Ming of the investiture, but Injo delayed it due to economic concerns."
)
e1625_7 = create_entry(
    "仁祖三年 · 領事 尹昉 啓", ["論議", "外交"],
    "領事尹昉曰：“臣再侍王世子於冊禮之後，則世子岐嶷夙成，講學之際，深解旨義，誠一國臣民之慶、祖宗社稷之福也。冊封奏請，不可遲緩，臣等欲付謝恩使之行，自上以民弊為慮，不卽允從。臣等之意，不如從速奏聞。”上曰：“此非急急之事，今番接待詔使，亦恐民力之難堪。況年年酬應詔使，則何以為國乎？姑待後日。”",
    "尹昉稱讚世子聰穎，建議儘快向大明奏報。君王再次強調民力難堪，決定緩辦。",
    "Yun Bang praised the Crown Prince's intellect and urged diplomatic notification, but Injo prioritized the people's welfare."
)

# 1626 Entries
e1626_1 = create_entry(
    "仁祖四年 四月 · 迎接都監 啓", ["外交"],
    "迎接都監啓曰：“世子接見當否，問于館伴、大臣以啓事，傳教矣。天使要見王世子，在道中亦屢言之。今日詣闕時，欲仍與王世子相會，臣令譯官，告之以‘國王前同會則坐次非便。老爺若欲見之，世子當於閑日來拜’云，則天使曰：‘俺之欲往見，禮也；世子之來拜，亦禮也’云。其意蓋欲世子來拜也。以此觀之則要見，非文具也，其欲先為往見，乃文具之言也。世子若送拜帖請拜，則彼必喜之矣。”答曰：“依啓。”",
    "迎接都監報告，大明使臣想要見王世子。使臣認為世子來拜訪是合禮的。君王同意世子送拜帖請求拜見。",
    "The Ming envoy requested to meet the Crown Prince, leading to discussions on diplomatic protocol and the Prince's formal greeting."
)
e1626_2 = create_entry(
    "仁祖四年 四月 · 禮曹 啓 (冠服議)", ["禮制"],
    "禮曹啓曰：“王世子接見詔使時冠服，議于大臣，則左議政尹昉、右議政申欽以為：‘該曹啓辭，詳盡無餘。臣等亦記丙午年天使時，該曹以翼善冠、衮龍袍啓請，而先王以未冊封之故，初以為疑，卒從大臣之議，依該曹啓辭為之矣。若着帽子，則下同臣僚，似未妥當。今亦遵行丙午之例何如？’”答曰：“知道。依丁酉年例，着帽子相見，似為合宜，更議以啓。”大臣以為：“依上教施行，亦似無妨。”從之。",
    "討論王世子接見大明詔使時應穿的冠服。大臣建議穿翼善冠和衮龍袍，但君王決定依丁酉年例，戴帽子相見。",
    "Debate on the Crown Prince's attire for meeting Ming envoys, balancing formal status with established precedents."
)
e1626_3 = create_entry(
    "仁祖四年 四月 · 詔使 詣 成均館", ["外交"],
    "○詔使詣成均館，拜文廟後，上殿周覽，仍步往明倫堂。館伴李廷龜、遠接使金瑬，行再拜禮，各就坐。儒生入庭行禮，詔使起立，拱手答揖。詔使謂譯官曰：“貴國文廟之制，一如中朝，多士濟濟，可見禮義之風。但俺等二人當分庭行禮，而俱設拜席於東庭，此與天朝有異”云。",
    "大明使臣訪問成均館，拜祭文廟，並在明倫堂與陪同官員會面。使臣稱讚韓國的禮儀之風與中原一致。",
    "Ming envoys visited Sungkyunkwan (the National Academy), praising the Confucian rituals and the scholarly atmosphere."
)
e1626_4 = create_entry(
    "仁祖四年 四月 · 賜 陪從官", ["禮制"],
    "上賜世子接見天使時陪從官，輔德豹皮一領，弼善以下各鹿皮一領。",
    "君王賞賜在世子接見大明使臣時陪從的官員，分別賜予豹皮和鹿皮。",
    "The King granted rewards of leopard and deer skins to the officials who accompanied the Prince during the diplomatic reception."
)

# 1627 Entries
e1627_1 = create_entry(
    "仁祖五年 · 禮曹 啓 (正位三年)", ["禮制"],
    "庚午禮曹啓曰：“王世子正位東宮，今已三年，尚未受冊命於天朝。臣曹據例啓請，而適值兩瑞之行，公私物力掃盡，聖上軫念民生，遂從姑待後年之議，以至於今。竊念莫大應行之典，因此稽遲，豈非未安之甚乎？詔使若問：‘既已冊封，而何不奏請？’云，則可以物力為辭乎？今於謝恩使之行，送請封奏文，則此是例典，必無持難之事，請令大臣定奪。”答曰：“啓辭甚是。但如此蕩竭之時，詔使連三年出來，則民力極難支堪。更待後日奏請，勿為重困吾民。”",
    "禮曹奏請向大明申請冊封世子，指出世子已正位三年，尚未受天朝冊命。君王因民生艱難、使臣往來頻繁而再次推遲。",
    "The Ministry of Rites urged requesting formal Ming recognition for the Prince, but Injo again refused to avoid the financial burden of hosting envoys."
)
e1627_2 = create_entry(
    "仁祖五年 · 憲府、諫院 合啓", ["論議"],
    "○憲府、諫院合啓曰：“自古有天下國家者，必首建儲貳者，乃所以固本繫望，而基不拔之勢也。世子受冊經年，名位已定，而久稽封典之降，人心鬱抑，願望益切。殿下雖軫念赤子之重困，欲待後日，而為宗廟、社稷之計，寧可以民弊，而少緩大事乎？頃日有司之請，實出於群情之所同然，請依該曹陳啓，速為奏請，以慰臣民之望。”答曰：“有民然後，有國家。百姓離散，誰與為國乎？奏請雖重，民力亦不可不顧。爾等退而思之，勿為更煩。”",
    "司憲府和司諫院聯合上奏，強調冊封世子是國本大事，不能因民弊而延誤。君王回答說有百姓才有國家，堅持先顧民力。",
    "The Censorate jointly argued that the Prince's formal investiture was a national priority, but Injo maintained that the people's survival came first."
)
e1627_3 = create_entry(
    "仁祖五年 正月 · 丁卯胡亂 分朝論議", ["戰爭"],
    "申欽曰：“元翼之言是矣。”尹昉曰：“世子雖幼沖，若向南方，則人心有所依賴矣。”上曰：“世子年幼，以此持難。大臣一人，可往南方，收拾人心。”",
    "丁卯胡亂爆發，朝廷討論是否讓世子南下分朝。大臣認為世子南下能穩定民心，但君王擔憂世子年幼。",
    "As the Manchu invasion began, the court debated dividing the royal government (Bunjo) and sending the Prince south to rally public support."
)
e1627_4 = create_entry(
    "仁祖五年 正月 · 丙戌 引見大臣", ["戰爭"],
    "丙戌引見大臣、備局堂上、兩司長官。尹昉曰：“既已分朝，世子行期，可以速定。”上曰：“欲一時發行。”上又曰：“回書，既已裁送耶？”昉曰：“臺論不止，時未舉行。崔鳴吉曰：“答書，宜稱以朝鮮國，踏印以送。”金蓋國曰：“渠既以國王前為書，不可不以國書答送。”上曰：“姜絪宜送于平壤，與靈、璿同事。”李植曰：“速定一將，領率輕兵，進救平壤，似不可已。毛將存沒，雖未闖知，其不與奴通明矣。”上曰：“將此事情，奏聞天朝，請南軍及火器，如壬辰則何如？”植曰：“勢似不及而告急一節，不可不為也。”上曰：“然。”",
    "君王召見大臣討論分朝行期及與後金的回書。討論是否向大明求援，李植認為雖然可能來不及，但仍應告急。",
    "The King and ministers finalized plans for the Prince's departure and discussed diplomatic responses to the invaders and the Ming court."
)
e1627_5 = create_entry(
    "仁祖五年 正月 · 兩司 合啓 (分朝)", ["戰爭"],
    "兩司合啓曰：“分朝之舉，自漢、唐以來，亦有行之者。況江都僻在海島，大駕一入之後，朝家之命令不行，各道之漕運不通，則豈不大可憂哉？世子雖在沖年，平日臣庶，已有愛戴之心。臨亂監撫，必有延頸之望，請依古事，亟命分朝，屬諸元老大臣，內外控制，以為恢復之計。”答曰：“從當議處。”又啓曰：“臨津把截之計，尚未堅定，只以若干之兵，候望而已。都城無所恃，長江無所賴，此無異於以國與敵也。三南軍兵，不日將至，定將把守，猶可及也。請亟令廟堂，極擇大將，急急把截。”上令備局議定，備局請以忠清兵使柳琳定為大將，上從之。",
    "兩司再次請求世子分朝監國。同時建議加強臨津江的防禦，以柳琳為大將守衛。",
    "Officials urged the Prince to lead the Divided Court to ensure command and supply lines remained open during the war."
)
e1627_6 = create_entry(
    "仁祖五年 正月 · 分朝 決定", ["戰爭"],
    "尹昉曰：“在喪人請起復。”上曰：“可矣。”李廷龜曰：“請收用罷散武弁。”上曰：“雖在竄黜之人，如其可用，用之。”小宦以西來狀啓進，上曰：“噫！義州已陷矣。”李貴曰：“事已急矣，宜有分朝之舉。但守江都，終何所賴？”昉曰：“李元翼奉世子南下，收拾人心可乎？”上曰：“世子年幼，不可遠去矣。”",
    "義州陷落的消息傳來，李貴建議世子分朝。尹昉建議由李元翼陪同世子南下收攬人心，但君王仍擔心世子年幼。",
    "With news of Uiju's fall, the court urgency for the Divided Court grew, though Injo remained protective of the young Prince."
)
# Note: I'll include the map entries here as well
e1627_map1 = create_entry("仁祖五年 二月 丁未日 · 王世子 至全州", ["地圖"], "丁未上在江都。世子至全州。", "丁未日，君王在江華島。世子抵達全州。", "The Prince reached Jeonju during his mission to the southern provinces.")
e1627_map2 = create_entry("仁祖五年 二月 庚寅日 · 王世子 還全州", ["地圖"], "庚寅上在江都。王世子還自全州。", "庚寅日，君王在江華島。王世子從全州啟程返回。", "The Prince began his return journey from Jeonju.")
e1627_map3 = create_entry("仁祖五年 二月 癸巳日 · 王世子 謁廟社", ["地圖"], "癸巳上在江都。王世子謁于廟社奉安處。", "癸巳日，君王在江華島。王世子參拜了宗廟社稷的奉安處。", "The Prince performed rituals at the temporary shrine for the royal ancestral tablets.")

e1627_7 = create_entry(
    "仁祖五年 三月 · 下教旨 (世子還宮)", ["禮制"],
    "上下教曰：“世子還宮時，歷入廟所，拜謁而來，似合情禮。言于禮曹。”",
    "君王下達教旨，認為世子回宮時應先去廟所參拜，這才符合情理。",
    "The King ordered the Prince to pay respects at the royal shrine upon his return to the capital."
)
e1627_8 = create_entry(
    "仁祖五年 九月 · 嘉禮都監 啓 (親迎之禮)", ["禮制"],
    "嘉禮都監啓曰：“別宮既有世子嬪所御之處，則世子親迎之禮，當行於別宮，而或有親迎於太平館之時。此雖謬禮，既有是規，何以處之？”答曰：“別宮非但狹隘，親迎於太平館，乃是前規，依前例施行。”",
    "嘉禮都監討論世子婚禮的親迎禮地點。君王決定在太平館舉行，因為別宮狹窄且有前例可循。",
    "Discussion on the wedding venue for the Prince, opting for Taepyeonggwan due to space and precedent."
)
e1627_9 = create_entry(
    "仁祖五年 十月 · 丁酉 禮曹 啓 (世子嬪外祖父母喪禮)", ["禮制"],
    "丁酉禮曹啓曰：“以王世子臨外祖父母喪儀注，考諸《五禮儀》則無正文，只有臨師傅、貳師喪儀注，而禮貌繁多。考諸《大明集禮》，東宮臨外祖父母喪，則頗似詳明，而節目太略，故就《五禮儀》及《大明集禮》，乘與臨王公大大臣喪儀注，參酌刪潤以入矣。”",
    "禮曹討論世子參見外祖父母喪禮的儀軌。因《五禮儀》無明文，故參照《大明集禮》並參酌刪改後呈上。",
    "The court defined the mourning etiquette for the Prince's maternal grandparents, referencing both Korean and Ming codes."
)
e1627_10 = create_entry(
    "仁祖五年 十月 · 右贊成 李貴 上箚 (世子教養)", ["教育"],
    "右贊成李貴上箚曰：閭閻教兒，科業為主，故必以先通文理為急，而儲君之學，異於是，必於知思未定之前，俾格言、至論，日陳於前，而浸灌薰陶。……近世，先正臣李珥，於《擊蒙要訣》，論為學之要甚詳，尤當觀玩，而研窮者也。世子乃一國之本也。其教養之方，不法先聖所訓，乃以閭閻家子弟之先文藝，而取科第者為法，先讀《史記》等書，如是而年歲積久，習與智長，化與心成，而為外物所誘，則雖欲變化氣質，扞格難入。必先讀《小學》，次讀四書，次讀五經，一如古學者課程可也。及其心志既正，德器已成，則不患文理之不通也。",
    "李貴上奏討論世子教育。建議不要像平民那樣以科舉文藝為主，而應先讀《小學》、四書五經，以格言至論薰陶，正其心志。",
    "Yi Gwi advised a curriculum focused on character building and classical texts over mere literary skill for the Prince's education."
)
e1627_11 = create_entry(
    "仁祖五年 十一月 · 辛酉 行世子嫁娉采禮", ["禮制"],
    "辛酉上以冕服，御崇政殿，行世子嬪納采禮如儀。",
    "辛酉日，君王著冕服駕臨崇政殿，正式舉行世子嬪的納采儀式。",
    "The formal betrothal ritual (Nachae) for the Prince's marriage was conducted at Sungjeongjeon."
)
e1627_12 = create_entry(
    "仁祖五年 十一月 · 皇上 崩訃 · 舉哀", ["外交", "禮制"],
    "禮曹啓曰：“皇上崩逝，訃報已至，請行舉哀之禮。”上率王世子、百官，舉哀於崇政殿階上。備局啓曰：“請差秩高官員具摺，以慰毛將。”從之。",
    "大明熹宗天啟帝駕崩的消息傳到，君王率世子及百官在崇政殿舉哀。",
    "Upon news of the Ming Emperor's death, Injo and the Prince led the court in official mourning rites."
)

# 1628 Entry (Empty or based on previous logic if any found)
# Actually, the user's images don't show 1628. I'll omit 1628 or put a placeholder.
# Wait, I'll search for anything about 1628 Sohyeon.
# 仁祖六年 (1628): 
# I will leave 1628 empty for now as it's not in the doc.

with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Update Period Sections
def update_section(period, entries_list):
    sec = soup.find('div', attrs={'data-period': period})
    if sec:
        # Clear old entries
        for e in sec.find_all('div', class_='sillok-entry'):
            e.decompose()
        # Remove map container if any
        map_c = sec.find('div', class_='bunjyo-map-container')
        if map_c: map_c.decompose()
        
        # Add new entries
        for entry_html in entries_list:
            sec.append(BeautifulSoup(entry_html, 'html.parser'))

update_section('1625', [e1625_1, e1625_2, e1625_3, e1625_4, e1625_5, e1625_6, e1625_7])
update_section('1626', [e1626_1, e1626_2, e1626_3, e1626_4])

# For 1627, we need to handle the map
sec1627 = soup.find('div', attrs={'data-period': '1627'})
if sec1627:
    for e in sec1627.find_all('div', class_='sillok-entry'): e.decompose()
    map_c = sec1627.find('div', class_='bunjyo-map-container')
    if map_c: map_c.decompose()
    
    sec1627.append(BeautifulSoup(e1627_1, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_2, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_3, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_4, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_5, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_6, 'html.parser'))
    
    # Map
    map_html = """
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
    </div>"""
    sec1627.append(BeautifulSoup(map_html, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_map1, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_map2, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_map3, 'html.parser'))
    
    sec1627.append(BeautifulSoup(e1627_7, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_8, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_9, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_10, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_11, 'html.parser'))
    sec1627.append(BeautifulSoup(e1627_12, 'html.parser'))

# Clear 1628
update_section('1628', [])

# Update Sidebar Nav Labels
nav_1626 = soup.find('button', attrs={'data-period': '1626'})
if nav_1626:
    nav_1626.find('span', class_='nav-event').string = "迎接詔使"
nav_1627 = soup.find('button', attrs={'data-period': '1627'})
if nav_1627:
    nav_1627.find('span', class_='nav-event').string = "胡亂 · 嘉禮"

with open('sohyeon_sillok.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
