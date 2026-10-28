# How the Valley Weekender bot publishes each Thursday

Every Thursday morning the bot puts out the issue for the coming Friday to Sunday. It works in `/workspace/valley-weekender-site/` (this repo, `dvdbosch-creator/valley-weekender`, branch `main`). GitHub Pages serves the `main` branch root at https://dvdbosch-creator.github.io/valley-weekender/.

## The template

A new issue always starts as a copy of the most recent issue page:

    issues/<latest date>/index.html        (today: issues/2026-10-30/index.html)

That file holds the full design (layout, colors, the Fraunces and Inter fonts, the weather strip, the cards and the footer). Keep the markup and class names, and change only the words, links and photos. Do not edit `index.html` at the site root by hand; `tools/publish.py` writes it.

Path rules inside an issue page (the page lives two folders deep):
- shared files: `../../assets/crest_w.png`, `../../assets/landscape_w.png`, `../../assets/fonts.css`
- this week's photos: `img/<name>.jpg`
- the Past Issues link: `../`

## Step by step

1. Make the new issue folder, named for the Friday of the weekend:

       cd /workspace/valley-weekender-site
       D=2026-11-06
       mkdir -p issues/$D/img
       cp issues/2026-10-30/index.html issues/$D/index.html

2. Edit `issues/$D/index.html`: dates, weather, the headline pick, the cards, and every event link (each event name links to its official page). Put this week's photos in `issues/$D/img/` as JPEGs about 1200 px wide, under 400 KB each. No em dashes or en dashes anywhere.

3. Add the issue at the TOP of `issues/issues.json` (newest first):

       {"date": "2026-11-06", "number": "Issue No. 02", "title": "Friday, Nov 6 to Sunday, Nov 8, 2026", "teaser": "One sentence on the best things this weekend."},

4. Rebuild the front page and the Past Issues list:

       python3 tools/publish.py

   It copies the newest issue to `index.html` (fixing its paths) and rewrites the list in `issues/index.html`. It stops with an error if it finds an em or en dash.

5. Check it locally before pushing:

       python3 -m http.server 8080 &
       NODE_PATH=/workspace/valley-weekend/node_modules node tools/render_check.js http://localhost:8080/ /tmp/vw-local-390.png
       kill %1

   Look at the screenshot. The command exits with an error if any image is broken, the fonts did not load, or the page scrolls sideways at 390 px.

6. Commit and push:

       git add -A
       git commit -m "Issue $D"
       git push origin main

7. Verify the live site (allow one to two minutes for Pages to update):

       curl -s -o /dev/null -w "%{http_code}\n" https://dvdbosch-creator.github.io/valley-weekender/
       curl -s -o /dev/null -w "%{http_code}\n" https://dvdbosch-creator.github.io/valley-weekender/issues/$D/
       curl -s -o /dev/null -w "%{http_code}\n" https://dvdbosch-creator.github.io/valley-weekender/issues/
       NODE_PATH=/workspace/valley-weekend/node_modules node tools/render_check.js https://dvdbosch-creator.github.io/valley-weekender/ /tmp/vw-live-390.png

   All three must print 200 and the render check must pass. Also confirm the front page shows the new dates (`curl -s https://dvdbosch-creator.github.io/valley-weekender/ | grep -c "Nov 6"`).

## If something goes wrong

- Pages still shows last week: wait two more minutes, then check `gh api repos/dvdbosch-creator/valley-weekender/pages/builds/latest --jq .status`.
- To undo a bad issue: `git revert HEAD && git push origin main`. The previous issue comes back as the front page.
- The Notion banner never needs changing. It points at the site root (always the latest issue) and at `/issues/`, and the banner image `assets/banner.png` has no dates on it.
