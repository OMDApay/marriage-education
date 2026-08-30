# Restore verification — 2026-08-30

- The final archive `/home/ubuntu/marriage-education-website-final.tar.gz` restored the project into `/home/ubuntu/marriage-education-website`.
- `package.json` is present and the project builds successfully with `npm run build`.
- Vite dev server runs on port 5183 with `server.allowedHosts: true` added to `vite.config.js` for the public preview proxy.
- Public preview URL: https://5183-i9lqah0ihe24sdtefl39f-40e4b7ee.us4.manus.computer
- The age gate appears before the home page and includes the consent and exit choices.
- After consent, the home page loads with the Arabic header image and navigation.
- Assets counted: 269 public images; 200 article images; 20 chapter images; 11 sexual-disease images; 11 media-literacy images; 11 tragedy-chapter images; 13 curated images; 3 verified web images.
- `src/data/articles.json` contains 200 article records.
- `src/data/positions.js` contains 50 position records, and `src/assets/positions` contains 59 image files; all referenced position image filenames were found.
- The positions section visibly exposes 50 `عرض التفاصيل` buttons and loads unique illustrated position cards.

The browser verification also confirmed that the `الأمراض الجنسية` section loads its 10 articles and chapter banner/images, and the `لا تصدّق الأفلام الإباحية` section loads its 10 media-literacy articles and chapter banner/images. Both sections are reachable from the main navigation and render without a blank page.

The browser verification confirmed that `نهاية مأساوية لممثلي الأفلام الإباحية؟` loads its 10 responsible-reading articles, uses the tragedy image set, and exposes navigation buttons back to the home page, media-literacy chapter, and sexual-diseases chapter, plus external reference links.

The browser verification opened an article modal successfully and showed the article image, summary, close/print controls, and `التالي` navigation. Clicking `التالي` moved to the next article and exposed both `السابق` and `التالي`, confirming in-chapter article navigation works.
