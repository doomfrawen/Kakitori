# Kakitori

Practice hiragana, katakana and Japanese verbs on your phone.

Kakitori (書き取り) means writing from memory: the classic drill where you hear a sound and write the character. That's what the app's Write mode does.

- **Kana:** write each character with your finger and get stroke-order feedback, or review with flashcards and quizzes.
- **Verbs:** learn common verbs five at a time, then drill their forms one at a time: polite and plain, present and past, negative, te-form, "let's" and "want to".
- **Progress:** reviews are spaced out, so characters you miss come back soon and ones you know come back days later.
- **Languages:** English, Español, Français, Deutsch, हिन्दी, 简体中文 and 繁體中文, each with its own memory hints. Kakitori follows your phone's language, or you can pick one in Settings.

## Use it

**iPhone:** open `https://doomfrawen.github.io/kakitori/` in Safari, tap Share, then Add to Home Screen. It opens full screen and works offline.

**Android:** install `Kakitori.apk`.

## Sync between phones

In the app, open Settings (the gear), then Sync, then Use GitHub. Your progress is saved to a separate **private** repository, `kakitori-progress`, using a token that can only reach that repository. This repository holds only the app and never any progress.

Google sync (through a small Apps Script) and backup codes are also available in Settings.

## What's in this repository

| Path | What it is |
| --- | --- |
| `docs/` | The iPhone web app, served by GitHub Pages |
| `src/app.html` | The built app: one HTML file with every language inside |
| `src/app.template.html` | The app's source, without the translations |
| `src/i18n/` | One catalog per language: interface text, kana memory hints and verb meanings |
| `src/build_app.py` | Checks every catalog and merges them into `src/app.html` |
| `android/` | The Android wrapper: a WebView that loads the app offline |
| `sync/KakitoriSync.gs` | The optional Google Apps Script for Google sync |
| `tools/make_offline.py` | Builds `docs/` and the Android page from `src/app.html`, embedding the font |

## Translations

Each language lives in `src/i18n/<code>.py` with three parts: `UI` (interface text, keyed like `en.py`), `HINTS` (a memory hint for each kana) and `VERBS` (the 85 verb meanings, in the same order as English). Placeholders such as `{n}` must stay as they are.

```sh
python3 src/build_app.py
```

This writes `src/app.html` and stops with a list if a catalog is missing keys, hints, verbs or placeholders. Text missing from a language falls back to English in the app.

The non-English translations and hints were written with AI help. Corrections from native speakers are welcome.

## Building

Needs Python 3 with `fonttools`, `brotli` and `Pillow`, plus the Klee One `.ttf` files.

```sh
python3 tools/make_offline.py <font-dir> src/app.html iphone docs
python3 tools/make_offline.py <font-dir> src/app.html android android/assets/index.html
```

`android/build.sh` builds and signs the APK. It takes a tools folder (aapt2, android.jar, dex2jar, uber-apk-signer), a keystore and its password. The signing key is not in this repository.

## Credits

- Stroke order data from [KanjiVG](https://kanjivg.tagaini.net) by Ulrich Apel, licensed [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). The stroke data included in this app is shared under the same license.
- [Klee One](https://github.com/fontworks-fonts/Klee) by Fontworks, licensed under the SIL Open Font License 1.1. See `LICENSES/OFL-KleeOne.txt`.
