"""Build offline copies of Kakitori from app.html.

usage: make_offline.py <font dir> <app.html> android <out index.html>
       make_offline.py <font dir> <app.html> iphone  <out folder>

Fonts are subset to the characters the app uses and embedded, so the page
needs no network for anything except optional sync.
"""
import base64, json, os, sys
from fontTools import subset
from PIL import Image, ImageDraw, ImageFont

FONT_DIR, SRC, TARGET, OUT = sys.argv[1:5]
src = open(SRC, encoding='utf-8').read()

LINKS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Klee+One:wght@400;600&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap">
'''
assert LINKS in src, 'font links not found'

# Klee One only draws Japanese (the --kana stack), so skip the translations when picking glyphs:
# their Chinese and Devanagari text uses the system font and would only bloat the subset.
_i = src.index('const I18N = ') + len('const I18N = ')
_, _end = json.JSONDecoder().raw_decode(src, _i)
glyph_src = src[:_i] + src[_end:]
chars = set(c for c in glyph_src if ord(c) > 127) | set(chr(c) for c in range(32, 127)) | set('ー〜、。…・「」゛゜×')
faces = ''
for weight, name in [(400, 'KleeOne-Regular'), (600, 'KleeOne-SemiBold')]:
    opts = subset.Options()
    opts.flavor = 'woff2'; opts.layout_features = ['*']; opts.name_IDs = ['*']; opts.notdef_outline = True
    font = subset.load_font(os.path.join(FONT_DIR, name + '.ttf'), opts)
    sub = subset.Subsetter(opts); sub.populate(text=''.join(chars)); sub.subset(font)
    tmp = os.path.join(os.path.dirname(os.path.abspath(OUT)) or '.', '.' + name + '.woff2')
    subset.save_font(font, tmp, opts)
    data = base64.b64encode(open(tmp, 'rb').read()).decode()
    os.remove(tmp)
    faces += ("@font-face{font-family:'Klee One';font-weight:%d;font-style:normal;font-display:swap;"
              "src:url(data:font/woff2;base64,%s) format('woff2')}\n" % (weight, data))

head = '<style>\n' + faces + '</style>\n'

if TARGET == 'android':
    html = src.replace(LINKS, head)
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote', OUT, len(html.encode()))
    sys.exit(0)

# ---------- iPhone home-screen web app ----------
os.makedirs(OUT, exist_ok=True)
VERSION = '1.8.0'
head = '''<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Kakitori">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#EDF0EE" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#10141B" media="(prefers-color-scheme: dark)">
<script>window.RENSHU_PLATFORM='ios';</script>
''' + head
html = src.replace(LINKS, head)
reg = '''<script>
if ('serviceWorker' in navigator && (location.protocol === 'https:')) {
  window.addEventListener('load', function () { navigator.serviceWorker.register('sw.js').catch(function () {}); });
}
</script>
</body>'''
assert html.count('</body>') == 1
html = html.replace('</body>', reg)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html)

manifest = {
    "name": "Kakitori",
    "short_name": "Kakitori",
    "description": "Practice hiragana, katakana and Japanese verbs.",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#EDF0EE",
    "theme_color": "#EDF0EE",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
    ]
}
json.dump(manifest, open(os.path.join(OUT, 'manifest.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

sw = '''// Kakitori offline cache. Network first, so updates show up; cache when offline.
const CACHE = 'renshu-%s';
const FILES = ['./', './index.html', './manifest.webmanifest', './apple-touch-icon.png', './icon-192.png', './icon-512.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  e.respondWith(
    fetch(e.request).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
      return res;
    }).catch(() => caches.match(e.request, {ignoreSearch: true})
      .then(r => r || caches.match('./index.html')))
  );
});
''' % VERSION
open(os.path.join(OUT, 'sw.js'), 'w', encoding='utf-8').write(sw)


def icon(size, pad, path, rounded_bg=True):
    S = size
    img = Image.new('RGB', (S, S), (237, 240, 238))
    d = ImageDraw.Draw(img)
    grid = (121, 172, 150); c = S // 2; w = max(2, round(S * 5 / 432)); dash = S * 14 / 432; gap = S * 12 / 432
    x = 0.0
    while x < S:
        d.line([(x, c), (min(x + dash, S), c)], fill=grid, width=w)
        d.line([(c, x), (c, min(x + dash, S))], fill=grid, width=w)
        x += dash + gap
    font = ImageFont.truetype(os.path.join(FONT_DIR, 'KleeOne-SemiBold.ttf'), round(S * pad))
    bb = d.textbbox((0, 0), 'あ', font=font)
    d.text(((S - (bb[2] - bb[0])) / 2 - bb[0], (S - (bb[3] - bb[1])) / 2 - bb[1] + S * 0.01), 'あ', font=font, fill=(26, 33, 48))
    img.save(path)


icon(180, 0.66, os.path.join(OUT, 'apple-touch-icon.png'))
icon(192, 0.66, os.path.join(OUT, 'icon-192.png'))
icon(512, 0.66, os.path.join(OUT, 'icon-512.png'))
icon(512, 0.53, os.path.join(OUT, 'icon-maskable-512.png'))

open(os.path.join(OUT, 'README.txt'), 'w', encoding='utf-8').write(
    'Kakitori for iPhone\n\n'
    'Upload every file in this folder to a free static web host (GitHub Pages, Netlify, Cloudflare Pages).\n'
    'Open the address in Safari on the iPhone, tap Share, then Add to Home Screen.\n\n'
    'Stroke order data: KanjiVG by Ulrich Apel, CC BY-SA 3.0. Font: Klee One, SIL Open Font License.\n')
print('wrote', OUT, sorted(os.listdir(OUT)))
