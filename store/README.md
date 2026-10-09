# Publishing Kakitori on Google Play

Everything the Play Console asks for, ready to copy. App ID: `app.kakitori`.

## What's in this folder

| Path | What it is |
| --- | --- |
| `play/<locale>/title.txt`, `short_description.txt`, `full_description.txt` | Store listing text (30, 80 and 4000 characters at most) |
| `play/<locale>/images/phoneScreenshots/1-5.png` | Phone screenshots, 1080×1920, captioned in that language |
| `play/<locale>/images/featureGraphic.png` | Feature graphic, 1024×500 |
| `play/en-US/images/icon.png` | App icon, 512×512 |
| `listing.py` | The listing text for every language. Run `python3 store/listing.py store/play` after editing it |
| `screens.py` | Makes the screenshots and feature graphic from the Android build of the app |

The folder layout is the one [fastlane supply](https://docs.fastlane.tools/actions/supply/) uses, so uploads can be automated later.

## 1. Create the app

Play Console → **Create app**

- App name: `Kakitori: Learn Kana & Verbs`
- Default language: English (United States)
- App or game: **App**
- Free or paid: **Free**

## 2. Set up your app (Dashboard → "Set up your app")

| Section | Answer |
| --- | --- |
| Privacy policy | `https://doomfrawen.github.io/Kakitori/privacy.html` |
| App access | All functionality is available without special access |
| Ads | No, my app doesn't contain ads |
| Content rating | Category **Reference, News, or Educational**. Answer **No** to every question (no violence, sexual content, bad language, drugs, gambling, user-to-user interaction, location sharing or purchases). Expected rating: Everyone / PEGI 3 |
| Target audience | **13–15, 16–17 and 18+**. Leaving out under-13 keeps the app out of the stricter Families program |
| News app | No |
| Health apps | My app does not have any health features |
| Financial features | My app doesn't provide any financial features |
| Government app | No |
| Data safety | See below |
| App category | **Education**. Tags: Language learning |
| Store listing contact details | Use an email made just for Kakitori. It's shown publicly |

### Data safety

Kakitori only sends data off the phone when the user turns on sync, and then only to the user's own GitHub repository or Google script. Play counts any data leaving the device as "collected", so declare it honestly:

- Does your app collect or share any of the required user data types? **Yes**
- Is all user data encrypted in transit? **Yes** (sync uses HTTPS)
- Which account creation methods? **My app does not allow users to create an account**
- Data types: **App activity → App interactions** (practice progress)
  - Collected: **Yes**. Shared: **No**
  - Processed ephemerally: **No**
  - Required or optional: **Users can choose whether this data is collected** (sync is off by default)
  - Purpose: **App functionality**
- Leave every other data type unchecked. There are no analytics, ads or crash-reporting libraries in the app.

## 3. Store listing (Grow → Store presence → Main store listing)

Paste from `play/en-US/`, upload the images from `play/en-US/images/`. Then **Manage translations → Add your own translations** for each language below and paste from its folder:

| Play language | Folder |
| --- | --- |
| Spanish (Spain) / Latin America / United States | `es-ES`, `es-419`, `es-US` |
| French (France) / Canada | `fr-FR`, `fr-CA` |
| German | `de-DE` |
| Hindi | `hi-IN` |
| Chinese (Simplified) | `zh-CN` |
| Chinese (Traditional) / Hong Kong | `zh-TW`, `zh-HK` |

## 4. Closed test (required for new personal accounts)

1. **Test and release → Testing → Closed testing → Create track.**
2. Upload `Kakitori.aab`. Choose **Let Google manage and protect your app signing key** (Play App Signing); the key that signed the bundle becomes your upload key.
3. Add at least **12 testers** by email, or through a Google Group, and send them the opt-in link.
4. Testers must opt in, install from Play, and actually use the app for **14 days in a row**.
5. Then **Dashboard → Apply for production** and answer the questions about the test.

## Keep safe

The upload key (`renshu-signing.p12` and its password) is not in this repository and must never be. If it's lost, Play can reset it, but that takes a few days.
