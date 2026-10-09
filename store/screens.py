"""Store screenshots and feature graphic for every language.

python3 store/screens.py <offline index.html> <klee font dir> <output dir> [icon-512.png]

Writes <output dir>/<locale>/images/phoneScreenshots/1..5.png (1080x1920, a caption over the app)
and <output dir>/<locale>/images/featureGraphic.png (1024x500), plus icon.png when docs/icon-512.png is given.
Progress is seeded so the screens show a learner a week in, not an empty app.
"""
import base64, json, pathlib, shutil, sys
from PIL import Image
from playwright.sync_api import sync_playwright

APP, FONTS, OUT = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve(), pathlib.Path(sys.argv[3])
HERE = pathlib.Path(__file__).resolve().parent
JSON = next(d for d in [HERE.parent / 'i18n' / 'json', HERE.parent / 'src' / 'i18n' / 'json'] if d.exists())
LANGS = [('en', 'en-US'), ('es', 'es-ES'), ('fr', 'fr-FR'), ('de', 'de-DE'), ('hi', 'hi-IN'), ('zh-Hans', 'zh-CN'), ('zh-Hant', 'zh-TW')]
UI_FONT = {'hi': '"Noto Sans Devanagari", sans-serif', 'zh-Hans': '"Noto Sans CJK SC", "Noto Sans SC", sans-serif',
           'zh-Hant': '"Noto Sans CJK TC", "Noto Sans TC", sans-serif'}

SEED = r"""
(() => {
  if (localStorage.getItem('renshu-v1')) return;
  const now = Date.now(), DAY = 864e5, d = new Date();
  const today = d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
  const hira = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほ'.split('');
  const kata = 'アイウエオカキクケコ'.split('');
  const srs = {};
  const put = (key, b, due) => { const n = b * 2 + 2; srs[key] = {b, n, c: n - (b < 3 ? 2 : 1), d: due}; };
  hira.forEach((ch, i) => {
    const b = i < 8 ? 5 : i < 15 ? 4 : i < 21 ? 3 : i < 26 ? 2 : 1;
    put('kr:' + ch, b, now + (b + 1) * DAY);
    put('kw:' + ch, Math.max(1, b - 1), i === 0 ? now - 6e4 : now + b * DAY);
  });
  kata.forEach((ch, i) => { put('kr:' + ch, i < 4 ? 2 : 1, now + DAY); put('kw:' + ch, 1, now + DAY); });
  for (let i = 0; i < 10; i++) put('vm:' + i, i < 5 ? 3 : 1, now + 2 * DAY);
  const st = {v: 1, t: now, srs, verbs: 10, forms: 3, recent: {}, off: [], day: {date: today, count: 18, streak: 6},
    set: {tab: 'kana', script: 'h', rows: ['a', 'ka', 'sa', 'ta', 'na', 'ha'], kmode: 'write', dir: 'k2r', vmode: 'learn',
          input: 'choose', romaji: true, trace: false, pscript: 'h', pskill: 'r', theme: 'light', tour: 1, maxGap: 0, lang: '%LANG%'}};
  localStorage.setItem('renshu-v1', JSON.stringify(st));
})();
"""
NATIVE = ("window.KakitoriNative={setDark(){},reminderState(){return JSON.stringify({on:true,blocked:false,hour:19,minute:0})},"
          "setReminder(){return 'scheduled'},setStudyState(){},testReminder(){return 'sent'},openNotificationSettings(){},setNotifyText(){}};")


def frame_html(caption, img_b64, lang, dark=False):
    bg = '#1B2B47' if not dark else '#0B0F15'
    font = UI_FONT.get(lang, 'system-ui, sans-serif')
    return f"""<!doctype html><html lang="{lang}"><meta charset="utf-8"><style>
    html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:{bg};font-family:{font}}}
    .cap{{position:absolute;left:80px;right:80px;top:120px;height:230px;display:flex;align-items:center;justify-content:center;text-align:center;
      color:#fff;font-size:66px;font-weight:700;line-height:1.2;letter-spacing:-0.01em}}
    img{{position:absolute;left:150px;top:420px;width:780px;height:1440px;border-radius:44px;box-shadow:0 30px 80px rgba(0,0,0,.45);outline:10px solid rgba(255,255,255,.08)}}
    </style><div class="cap">{caption}</div><img src="data:image/png;base64,{img_b64}"></html>"""


def feature_html():
    font = (FONTS / 'KleeOne-SemiBold.ttf').as_uri()
    return f"""<!doctype html><html><meta charset="utf-8"><style>
    @font-face{{font-family:Klee;src:url('{font}')}}
    html,body{{margin:0;width:1024px;height:500px;overflow:hidden;background:#EDF0EE;font-family:system-ui,sans-serif}}
    .sq{{position:absolute;left:84px;top:70px;width:360px;height:360px;background:#FAFBFA;border:4px solid #7FAF9A;border-radius:6px}}
    .sq:before,.sq:after{{content:'';position:absolute;border:0 dashed #B9D3C6}}
    .sq:before{{left:50%;top:0;bottom:0;border-left-width:3px}} .sq:after{{top:50%;left:0;right:0;border-top-width:3px}}
    .k{{position:absolute;left:84px;top:70px;width:360px;height:360px;display:flex;align-items:center;justify-content:center;
      font-family:Klee;font-size:280px;color:#C2453A;line-height:1}}
    .t{{position:absolute;left:520px;top:118px;font-family:Klee;font-size:118px;color:#1B2230;line-height:1}}
    .n{{position:absolute;left:526px;top:268px;font-size:56px;color:#2B4878;font-weight:600;letter-spacing:.01em}}
    .s{{position:absolute;left:528px;top:350px;font-size:30px;color:#4A5466}}
    </style><div class="sq"></div><div class="k">あ</div><div class="t">書き取り</div><div class="n">Kakitori</div>
    <div class="s">かな · カナ · 動詞</div></html>"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        for lang, loc in LANGS:
            shots = OUT / loc / 'images' / 'phoneScreenshots'
            shots.mkdir(parents=True, exist_ok=True)
            ctx = b.new_context(viewport={'width': 390, 'height': 720}, device_scale_factor=2, is_mobile=True, has_touch=True,
                                locale=lang, user_agent='Mozilla/5.0 (Linux; Android 16) Chrome/140 Mobile RenshuApp/1.8')
            ctx.add_init_script(NATIVE + SEED.replace('%LANG%', lang))
            pg = ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(APP.as_uri())
            pg.wait_for_timeout(900)
            ui = json.loads((JSON / f'{lang}.json').read_text(encoding='utf-8'))['ui']
            T = lambda k: ui[k]
            raw = []

            # 1. Write: show the model strokes with the picture hint
            pg.tap('[data-k="kmode"][data-v="write"]'); pg.wait_for_timeout(200)
            if pg.query_selector('[data-act="hint"]'): pg.tap('[data-act="hint"]')
            pg.tap('[data-act="check"]')
            pg.wait_for_timeout(4000)
            pg.evaluate('() => document.activeElement && document.activeElement.blur()')
            raw.append((T('tour.1.title'), pg.screenshot(), False))

            # 2. Cards: flipped, with the grade buttons
            pg.tap('[data-k="kmode"][data-v="cards"]'); pg.wait_for_timeout(200)
            pg.tap('.flash'); pg.wait_for_timeout(700)
            raw.append((T('tour.2.title'), pg.screenshot(), False))

            # 3. Verbs: a correct answer in Conjugate
            pg.tap('.tabs button[data-tab="verbs"]'); pg.tap('[data-k="vmode"][data-v="drill"]'); pg.wait_for_timeout(200)
            if pg.query_selector('[data-k="input"][data-v="choose"]'): pg.tap('[data-k="input"][data-v="choose"]')
            for _ in range(20):  # answer until one comes out right, so the screen shows a correct result
                pg.tap('[data-act="dpick"] >> nth=0'); pg.wait_for_timeout(250)
                if pg.query_selector('.result.ok'): break
                pg.tap('#dnext'); pg.wait_for_timeout(250)
            raw.append((T('tour.3.title'), pg.screenshot(), False))

            # 4. Progress, in the dark theme
            pg.tap('.tabs button[data-tab="progress"]'); pg.wait_for_timeout(200)
            def theme(v):
                pg.tap('#gear'); pg.wait_for_timeout(250)
                pg.tap(f'[data-k="theme"][data-v="{v}"]'); pg.wait_for_timeout(200)
                pg.tap('#gear'); pg.wait_for_timeout(350)
            theme('dark')
            pg.evaluate('() => window.scrollTo(0, 0)')
            raw.append((T('tour.4.title'), pg.screenshot(), True))
            theme('light')

            # 5. Look up: every form side by side
            pg.tap('.tabs button[data-tab="verbs"]'); pg.tap('[data-k="vmode"][data-v="look"]'); pg.wait_for_timeout(200)
            pg.tap('[data-act="vopen"] >> nth=0'); pg.wait_for_timeout(300)
            raw.append((T('look.table.h'), pg.screenshot(), False))

            fpage = b.new_page(viewport={'width': 1080, 'height': 1920})
            for i, (cap, png, dark) in enumerate(raw, 1):
                fpage.set_content(frame_html(cap, base64.b64encode(png).decode(), lang, dark))
                fpage.wait_for_timeout(150)
                fpage.screenshot(path=str(shots / f'{i}.png'))
            fpage.close()
            print(loc, 'screens done', 'ERRORS' if errs else '', errs[:2])
            ctx.close()

        gpage = b.new_page(viewport={'width': 1024, 'height': 500})
        gpage.set_content(feature_html()); gpage.wait_for_timeout(500)
        g = OUT / 'en-US' / 'images' / 'featureGraphic.png'
        gpage.screenshot(path=str(g))
        for _, loc in LANGS[1:]:
            (OUT / loc / 'images' / 'featureGraphic.png').write_bytes(g.read_bytes())
        b.close()
    # Regional variants use the same images; without them Play would show the English screenshots there.
    for src, dsts in {'es-ES': ['es-419', 'es-US'], 'fr-FR': ['fr-CA'], 'zh-TW': ['zh-HK']}.items():
        for d in dsts:
            shutil.copytree(OUT / src / 'images', OUT / d / 'images', dirs_exist_ok=True)
    if len(sys.argv) > 4:  # Play wants a 512x512 32-bit PNG icon
        Image.open(sys.argv[4]).convert('RGBA').resize((512, 512)).save(OUT / 'en-US' / 'images' / 'icon.png')


if __name__ == '__main__':
    main()
