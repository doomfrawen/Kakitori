"""Merge the language catalogs into app.template.html -> app.html, and check them.

Each language module in i18n/ defines UI (dict), HINTS (dict kana -> text) and VERBS (85 meanings).
English is the fallback, so a missing key shows English rather than breaking the page.
"""
import importlib.util, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
LANGS = [('en', 'en'), ('es', 'es'), ('fr', 'fr'), ('de', 'de'), ('hi', 'hi'), ('zh-Hans', 'zh_hans'), ('zh-Hant', 'zh_hant')]


def load(mod):
    p = ROOT / 'i18n' / (mod + '.py')
    if not p.exists():
        return None
    spec = importlib.util.spec_from_file_location('i18n_' + mod, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def placeholders(s):
    return sorted(set(re.findall(r'\{(\w+)\}', s)))


def main():
    tpl = (ROOT / 'app.template.html').read_text(encoding='utf-8')
    en_data = json.loads((ROOT / 'i18n' / '_en_data.json').read_text(encoding='utf-8'))
    en = load('en')
    en_hints = getattr(en, 'HINTS', None) or en_data['hints']
    out = {'en': {'ui': en.UI, 'hints': en_hints, 'verbs': en_data['verbs']}}
    problems = []

    # every literal key the page asks for must exist in English
    used = set(re.findall(r"\bt\('([\w.]+)'", tpl)) | set(re.findall(r"\btn\('([\w.]+)'", tpl))
    used |= set(re.findall(r"t\([^()]*?\?'([\w.]+)':'([\w.]+)'", tpl) and sum(re.findall(r"t\([^()]*?\?'([\w.]+)':'([\w.]+)'", tpl), ()))
    used |= set(re.findall(r'data-i18n(?:-aria)?="([\w.]+)"', tpl))
    plural_bases = set(re.findall(r"\btn\('([\w.]+)'", tpl))
    for k in sorted(k for k in used if not k.endswith('.')):
        if k in plural_bases:
            if k + '.other' not in en.UI:
                problems.append(f'en: plural key {k}.other missing')
        elif k not in en.UI:
            problems.append(f'en: key {k} used by the page but missing')

    for code, mod in LANGS[1:]:
        m = load(mod)
        if not m:
            print(f'  {code}: not written yet, skipped')
            continue
        ui, hints, verbs = m.UI, m.HINTS, m.VERBS
        plural = {re.sub(r'\.(one|other)$', '', k) for k in en.UI if re.search(r'\.(one|other)$', k)}
        plural = {b for b in plural if b + '.other' in en.UI}
        missing = [k for k in en.UI if k not in ui and not (re.sub(r'\.(one|other)$', '', k) in plural)]
        for base in plural:
            if base + '.other' not in ui:
                missing.append(base + '.other')
        for k in missing:
            problems.append(f'{code}: missing {k}')
        for k, v in ui.items():
            base = re.sub(r'\.(zero|one|two|few|many|other)$', '', k)
            if base in plural:
                want = sorted(set(placeholders(en.UI[base + '.other'])) | set(placeholders(en.UI.get(base + '.one', ''))) | {'n'})
            elif k in en.UI:
                want = placeholders(en.UI[k])
            else:
                problems.append(f'{code}: unknown key {k}')
                continue
            got = placeholders(v)
            # a plural form may drop {n} (e.g. "one review"), but may not invent placeholders
            if not set(got) <= set(want) or (set(want) - set(got) - {'n'}):
                problems.append(f'{code}: placeholders differ in {k}: {got} vs {want}')
        if len(verbs) != 85:
            problems.append(f'{code}: {len(verbs)} verb meanings, expected 85')
        miss_h = [c for c in en_hints if c not in hints]
        if miss_h:
            problems.append(f'{code}: {len(miss_h)} hints missing: ' + ''.join(miss_h))
        out[code] = {'ui': ui, 'hints': hints, 'verbs': verbs}

    blob = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
    assert tpl.count('/*I18N*/null') == 1
    html = tpl.replace('/*I18N*/null', blob)
    (ROOT / 'app.html').write_text(html, encoding='utf-8')
    jdir = ROOT / 'i18n' / 'json'
    jdir.mkdir(parents=True, exist_ok=True)
    for code, data in out.items():
        (jdir / f'{code}.json').write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'app.html written with {len(out)} language(s): {", ".join(out)} ({len(html.encode())} bytes)')
    if problems:
        print(f'{len(problems)} problem(s):')
        for p in problems[:80]:
            print('  -', p)
        sys.exit(1)


if __name__ == '__main__':
    main()
