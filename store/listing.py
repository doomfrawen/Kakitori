"""Google Play listing text for every language, written out in the fastlane folder layout.

python3 store/listing.py <output dir>
  -> <output dir>/<locale>/title.txt, short_description.txt, full_description.txt

Play limits: title 30 characters, short description 80, full description 4000.
Play doesn't allow words like "free", "best" or "#1" in the title, so those stay in the description.
"""
import pathlib, sys

L = {}

L['en-US'] = dict(
title='Kakitori: Learn Kana & Verbs',
short='Write hiragana and katakana by hand, then drill Japanese verbs form by form.',
full='''Kakitori (書き取り) means writing from memory: the classic way Japanese students learn to read and write. Kakitori turns it into a few minutes of practice a day on your phone.

WRITE EACH KANA BY HAND
• See a sound, draw its hiragana or katakana with your finger, and get stroke-order feedback right away.
• Red numbers show the right order and direction. New kana play their strokes first, and Trace adds a guide whenever you need one.
• A picture hint for every kana helps it stick.

READ WITH CARDS AND QUIZZES
• Flashcards and quizzes train reading both ways: kana to sound, and sound to kana.
• Grade yourself after each card. Kana you miss come back within minutes, and kana you know come back days later.
• Choose exactly which rows to practice, including the ゛ and ゜ sounds.

LEARN VERBS FIVE AT A TIME
• 85 everyday verbs, from 食べる (to eat) to 結婚する (to get married).
• Practice one form at a time: polite and plain, present and past, negative, te-form, "let's" and "want to".
• The next form unlocks when you get 10 of your last 12 right, and every answer comes with a short rule that explains it.
• Look up any verb to see every form side by side.

WATCH YOUR PROGRESS
• Every kana is colored by how well you know it, for reading and for writing.
• Tap a kana to replay its stroke order and see your stats.

PRIVATE AND SIMPLE
• No ads, no accounts, no tracking.
• Works offline.
• A daily reminder that stays quiet on days you've already practiced.
• Optional sync between phones through your own private GitHub repository or Google account.
• Light and dark themes.
• In English, Español, Français, Deutsch, हिन्दी, 简体中文 and 繁體中文.

Stroke order data: KanjiVG by Ulrich Apel, CC BY-SA 3.0.''')

L['es-ES'] = dict(
title='Kakitori: kana y verbos',
short='Escribe hiragana y katakana a mano y practica verbos japoneses forma a forma.',
full='''Kakitori (書き取り) significa escribir de memoria: la forma clásica en que los estudiantes japoneses aprenden a leer y escribir. Kakitori la convierte en unos minutos de práctica al día en tu móvil.

ESCRIBE CADA KANA A MANO
• Ves un sonido, dibujas su hiragana o katakana con el dedo y recibes al momento comentarios sobre el orden de los trazos.
• Los números rojos muestran el orden y la dirección correctos. Los kana nuevos enseñan primero sus trazos, y Calcar añade una guía cuando la necesites.
• Cada kana tiene una pista visual con una palabra en español para recordarlo.

LEE CON TARJETAS Y TESTS
• Las tarjetas y los tests entrenan la lectura en los dos sentidos: de kana a sonido y de sonido a kana.
• Califícate tras cada tarjeta. Los kana que fallas vuelven en minutos y los que ya sabes, días después.
• Elige exactamente qué filas practicar, incluidos los sonidos con ゛ y ゜.

VERBOS, DE CINCO EN CINCO
• 85 verbos cotidianos, desde 食べる (comer) hasta 結婚する (casarse).
• Practica una forma cada vez: cortés y llana, presente y pasado, negativa, forma -te, «vamos a…» y «querer…».
• La siguiente forma se desbloquea cuando aciertas 10 de tus últimas 12 respuestas, y cada respuesta viene con una regla breve que la explica.
• Consulta cualquier verbo para ver todas sus formas juntas.

SIGUE TU PROGRESO
• Cada kana se colorea según lo bien que lo conoces, para leer y para escribir.
• Toca un kana para repetir su orden de trazos y ver tus estadísticas.

PRIVADA Y SENCILLA
• Sin anuncios, sin cuentas y sin rastreo.
• Funciona sin conexión.
• Un recordatorio diario que no te molesta los días que ya has practicado.
• Sincronización opcional entre móviles con tu propio repositorio privado de GitHub o tu cuenta de Google.
• Tema claro y oscuro.
• En English, Español, Français, Deutsch, हिन्दी, 简体中文 y 繁體中文.

Datos de orden de trazos: KanjiVG, de Ulrich Apel, CC BY-SA 3.0.''')

L['fr-FR'] = dict(
title='Kakitori : kana et verbes',
short='Écris les hiragana et katakana à la main, puis entraîne-toi aux verbes japonais.',
full='''Kakitori (書き取り) veut dire « écrire de mémoire » : la méthode classique des élèves japonais pour apprendre à lire et à écrire. Kakitori en fait quelques minutes d'entraînement par jour sur ton téléphone.

ÉCRIS CHAQUE KANA À LA MAIN
• Un son s'affiche : dessine son hiragana ou son katakana avec le doigt et vois tout de suite si l'ordre des traits est bon.
• Les numéros rouges montrent le bon ordre et le bon sens. Les nouveaux kana montrent d'abord leurs traits, et Calquer ajoute un guide quand tu en as besoin.
• Chaque kana a son aide-mémoire en image, avec un mot français.

LIS AVEC LES CARTES ET LES QUIZ
• Les cartes et les quiz entraînent la lecture dans les deux sens : du kana au son, et du son au kana.
• Note-toi après chaque carte. Les kana ratés reviennent en quelques minutes, ceux que tu connais quelques jours plus tard.
• Choisis exactement les lignes à pratiquer, y compris les sons avec ゛ et ゜.

LES VERBES, CINQ PAR CINQ
• 85 verbes courants, de 食べる (manger) à 結婚する (se marier).
• Entraîne-toi une forme à la fois : poli et neutre, présent et passé, négatif, forme en -te, « faisons » et « vouloir ».
• La forme suivante se débloque quand tu as 10 bonnes réponses sur tes 12 dernières, et chaque réponse est accompagnée d'une règle courte qui l'explique.
• Consulte n'importe quel verbe pour voir toutes ses formes côte à côte.

SUIS TES PROGRÈS
• Chaque kana prend une couleur selon ton niveau, en lecture comme en écriture.
• Touche un kana pour revoir l'ordre de ses traits et tes statistiques.

SIMPLE ET RESPECTUEUX DE TA VIE PRIVÉE
• Pas de pub, pas de compte, pas de pistage.
• Fonctionne hors ligne.
• Un rappel quotidien qui se tait les jours où tu as déjà pratiqué.
• Synchronisation facultative entre téléphones via ton propre dépôt GitHub privé ou ton compte Google.
• Thème clair et sombre.
• En English, Español, Français, Deutsch, हिन्दी, 简体中文 et 繁體中文.

Données d'ordre des traits : KanjiVG par Ulrich Apel, CC BY-SA 3.0.''')

L['de-DE'] = dict(
title='Kakitori: Kana & Verben',
short='Schreib Hiragana und Katakana von Hand und übe japanische Verben Form für Form.',
full='''Kakitori (書き取り) heißt „aus dem Gedächtnis schreiben“: die klassische Methode, mit der japanische Schulkinder lesen und schreiben lernen. Kakitori macht daraus ein paar Minuten Übung am Tag auf deinem Handy.

SCHREIB JEDES KANA VON HAND
• Du siehst einen Laut, zeichnest das passende Hiragana oder Katakana mit dem Finger und bekommst sofort Feedback zur Strichfolge.
• Rote Zahlen zeigen die richtige Reihenfolge und Richtung. Neue Kana spielen zuerst ihre Striche ab, und Nachfahren blendet jederzeit eine Vorlage ein.
• Zu jedem Kana gibt es eine Merkhilfe mit Bild und deutschem Wort.

LESEN MIT KARTEN UND QUIZ
• Karten und Quiz trainieren das Lesen in beide Richtungen: vom Kana zum Laut und vom Laut zum Kana.
• Bewerte dich nach jeder Karte. Was du nicht wusstest, kommt nach Minuten wieder, was du sicher kannst, erst nach Tagen.
• Wähle genau die Reihen, die du üben willst, auch die Laute mit ゛ und ゜.

VERBEN, FÜNF AUF EINMAL
• 85 Alltagsverben, von 食べる (essen) bis 結婚する (heiraten).
• Übe eine Form nach der anderen: höflich und einfach, Gegenwart und Vergangenheit, Verneinung, Te-Form, „lass uns“ und „wollen“.
• Die nächste Form wird frei, wenn 10 deiner letzten 12 Antworten stimmen, und zu jeder Antwort gibt es eine kurze Regel, die sie erklärt.
• Schlag jedes Verb nach und sieh alle Formen nebeneinander.

BEHALTE DEINEN FORTSCHRITT IM BLICK
• Jedes Kana wird danach eingefärbt, wie gut du es kannst, getrennt für Lesen und Schreiben.
• Tippe auf ein Kana, um seine Strichfolge abzuspielen und deine Statistik zu sehen.

EINFACH UND PRIVAT
• Keine Werbung, kein Konto, kein Tracking.
• Funktioniert offline.
• Eine tägliche Erinnerung, die an Tagen, an denen du schon geübt hast, still bleibt.
• Optionaler Sync zwischen Handys über dein eigenes privates GitHub-Repository oder dein Google-Konto.
• Helles und dunkles Design.
• Auf English, Español, Français, Deutsch, हिन्दी, 简体中文 und 繁體中文.

Strichfolge-Daten: KanjiVG von Ulrich Apel, CC BY-SA 3.0.''')

L['hi-IN'] = dict(
title='Kakitori: काना और क्रियाएँ',
short='हिरागाना और काताकाना हाथ से लिखें, फिर जापानी क्रियाओं के रूप एक-एक करके सीखें।',
full='''Kakitori (書き取り) का मतलब है याद से लिखना: वही पुराना तरीका जिससे जापानी छात्र पढ़ना-लिखना सीखते हैं। Kakitori इसे आपके फ़ोन पर रोज़ कुछ मिनट के अभ्यास में बदल देता है।

हर काना हाथ से लिखें
• एक आवाज़ देखें, उसका हिरागाना या काताकाना उँगली से बनाएँ, और तुरंत जानें कि स्ट्रोक क्रम सही है या नहीं।
• लाल अंक सही क्रम और दिशा दिखाते हैं। नए काना पहले अपने स्ट्रोक चलाकर दिखाते हैं, और "ट्रेस" जब चाहें गाइड जोड़ देता है।
• हर काना के लिए एक हिंदी शब्द वाला चित्र-संकेत, ताकि वह याद रहे।

कार्ड और क्विज़ से पढ़ें
• कार्ड और क्विज़ दोनों दिशाओं में पढ़ने का अभ्यास कराते हैं: काना से आवाज़, और आवाज़ से काना।
• हर कार्ड के बाद खुद को अंक दें। जो काना याद नहीं आए, वे कुछ मिनट में लौटते हैं, और जो आते हैं, वे कुछ दिन बाद।
• ठीक-ठीक चुनें कि किन पंक्तियों का अभ्यास करना है, ゛ और ゜ वाली आवाज़ों समेत।

क्रियाएँ, एक बार में पाँच
• रोज़ की 85 क्रियाएँ, 食べる (खाना) से लेकर 結婚する (शादी करना) तक।
• एक-एक रूप का अभ्यास करें: विनम्र और सादा, वर्तमान और भूतकाल, नकारात्मक, ते-रूप, "चलो करें" और "करना चाहना"।
• पिछले 12 में से 10 जवाब सही होने पर अगला रूप खुलता है, और हर जवाब के साथ उसे समझाने वाला एक छोटा नियम दिखता है।
• किसी भी क्रिया के सभी रूप साथ-साथ देखें।

अपनी प्रगति देखें
• हर काना इस हिसाब से रंगा जाता है कि आप उसे कितना जानते हैं, पढ़ने और लिखने के लिए अलग-अलग।
• किसी काना पर टैप करके उसका स्ट्रोक क्रम दोबारा देखें और अपने आँकड़े जानें।

सादा और निजी
• कोई विज्ञापन नहीं, कोई खाता नहीं, कोई ट्रैकिंग नहीं।
• बिना इंटरनेट के चलता है।
• रोज़ का रिमाइंडर, जो उस दिन चुप रहता है जब आप अभ्यास कर चुके हों।
• चाहें तो अपनी निजी GitHub रिपॉज़िटरी या Google खाते के ज़रिए फ़ोनों के बीच सिंक करें।
• लाइट और डार्क थीम।
• English, Español, Français, Deutsch, हिन्दी, 简体中文 और 繁體中文 में।

स्ट्रोक क्रम डेटा: KanjiVG, Ulrich Apel द्वारा, CC BY-SA 3.0।''')

L['zh-CN'] = dict(
title='Kakitori：假名与动词',
short='手写平假名和片假名，再逐个练习日语动词的变形。',
full='''Kakitori（書き取り）的意思是“默写”：日本学生学习读写的经典方法。Kakitori 把它变成每天在手机上几分钟的练习。

手写每个假名
• 看到读音后，用手指写出对应的平假名或片假名，立刻知道笔顺对不对。
• 红色数字标出正确的笔顺和方向。新假名会先演示笔画，「描红」随时可以打开辅助线。
• 每个假名都标出它的来源汉字，比如 あ 来自「安」，看一眼就能记住。

用卡片和测验练认读
• 卡片和测验双向练习认读：从假名到读音，也从读音到假名。
• 每张卡片之后给自己打分。没记住的几分钟后再出现，已经掌握的几天后才出现。
• 自由选择要练的行，包括带 ゛ 和 ゜ 的音。

动词，每次 5 个
• 85 个常用动词，从 食べる（吃）到 結婚する（结婚）。
• 一次练一种变形：敬体和简体，现在和过去，否定，て形，“一起…吧”和“想…”。
• 最近 12 题答对 10 题就解锁下一种变形；每次作答后都会显示一条简短的规则来解释。
• 随时查阅任何动词，所有变形一目了然。

查看你的进度
• 每个假名按掌握程度上色，认读和书写分开统计。
• 点一个假名即可重播笔顺，查看你的统计。

简单、注重隐私
• 没有广告，无需注册，没有追踪。
• 可离线使用。
• 每日提醒；当天已经练过就不会打扰你。
• 可选同步：通过你自己的私有 GitHub 仓库或 Google 账户在手机之间同步。
• 浅色和深色主题。
• 支持 English、Español、Français、Deutsch、हिन्दी、简体中文和繁體中文。

笔顺数据：KanjiVG，作者 Ulrich Apel，CC BY-SA 3.0。''')

L['zh-TW'] = dict(
title='Kakitori：假名與動詞',
short='手寫平假名和片假名，再逐一練習日語動詞的變化。',
full='''Kakitori（書き取り）的意思是「默寫」：日本學生學習讀寫的經典方法。Kakitori 把它變成每天在手機上幾分鐘的練習。

手寫每個假名
• 看到讀音後，用手指寫出對應的平假名或片假名，馬上知道筆順對不對。
• 紅色數字標出正確的筆順和方向。新假名會先示範筆畫，「描紅」隨時可以開啟輔助線。
• 每個假名都標出它的來源漢字，例如 あ 來自「安」，看一眼就記得住。

用卡片和測驗練認讀
• 卡片和測驗雙向練習認讀：從假名到讀音，也從讀音到假名。
• 每張卡片之後幫自己評分。沒記住的幾分鐘後再出現，已經熟悉的幾天後才出現。
• 自由選擇要練的行，包括帶 ゛ 和 ゜ 的音。

動詞，每次 5 個
• 85 個常用動詞，從 食べる（吃）到 結婚する（結婚）。
• 一次練一種變化：敬體和常體、現在和過去、否定、て形、「一起…吧」和「想…」。
• 最近 12 題答對 10 題就解鎖下一種變化；每次作答後都會顯示一條簡短的規則來說明。
• 隨時查閱任何動詞，所有變化一目了然。

查看你的進度
• 每個假名依熟悉程度上色，認讀和書寫分開統計。
• 點一下假名即可重播筆順，查看你的統計。

簡單、重視隱私
• 沒有廣告，不必註冊，沒有追蹤。
• 可離線使用。
• 每日提醒；當天已經練習過就不會打擾你。
• 可選同步：透過你自己的私人 GitHub 儲存庫或 Google 帳戶在手機之間同步。
• 淺色和深色主題。
• 支援 English、Español、Français、Deutsch、हिन्दी、简体中文和繁體中文。

筆順資料：KanjiVG，作者 Ulrich Apel，CC BY-SA 3.0。''')

# Play also offers these regional variants; the same text reads naturally there.
L['es-419'] = L['es-ES']
L['es-US'] = L['es-ES']
L['fr-CA'] = L['fr-FR']
L['en-GB'] = L['en-US']
L['en-CA'] = L['en-US']
L['en-AU'] = L['en-US']
L['en-IN'] = L['en-US']
L['zh-HK'] = L['zh-TW']

LIMITS = {'title': 30, 'short': 80, 'full': 4000}

if __name__ == '__main__':
    out = pathlib.Path(sys.argv[1])
    bad = []
    for loc, d in L.items():
        for k, n in LIMITS.items():
            if len(d[k]) > n:
                bad.append(f'{loc} {k}: {len(d[k])} > {n}')
        p = out / loc
        p.mkdir(parents=True, exist_ok=True)
        (p / 'title.txt').write_text(d['title'] + '\n', encoding='utf-8')
        (p / 'short_description.txt').write_text(d['short'] + '\n', encoding='utf-8')
        (p / 'full_description.txt').write_text(d['full'] + '\n', encoding='utf-8')
    for loc in ['en-US', 'es-ES', 'fr-FR', 'de-DE', 'hi-IN', 'zh-CN', 'zh-TW']:
        d = L[loc]
        print(f"{loc}: title {len(d['title'])}, short {len(d['short'])}, full {len(d['full'])}")
    if bad:
        print('Too long:', *bad, sep='\n  ')
        sys.exit(1)
