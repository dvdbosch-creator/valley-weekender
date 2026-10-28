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

The club link must stay on every issue. The club's public page is:

    https://spectacled-mosquito-c7e.notion.site/Outfitters-Men-s-Club-31eb0e79c9378176ba0dd2f8404c4ca6

It appears three times in an issue page, and copying the template keeps all three: the club name in the masthead "Brought to you by" line (`<a class="club">`), the same line in the footer, and the footer box `<a class="join">Learn more or join the Los Olivos Outfitters Men's Club</a>`. The Past Issues page (`issues/index.html`) has it in its "Brought to you by" line and in the same `join` box; `publish.py` only rewrites the list inside `<nav>`, so those stay put. Before pushing, `grep -c spectacled-mosquito index.html` must print 3 and `grep -c spectacled-mosquito issues/index.html` must print 2.

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

## Notion section update (once Derek is an Outfitters member)

The Outfitters Men's Club Notion page gets a small Valley Weekender section, a copy of the mockup on Derek's personal page "TEST: Outfitters banner mockup" (https://app.notion.com/p/406f5195cbbf814b8160f678e7e894a0). The section is built so the weekly bot changes exactly two lines and nothing else on the page:

    <banner image>  assets/banner.png, caption links to the site root      (never changes)
    ### Read this week's Valley Weekender (links to the site root)          (never changes)
    This week: [Friday, Oct 30 to Sunday, Nov 1, 2026](.../issues/2026-10-30/)   <- EDIT 1
    Past issues · see them all (links to /issues/)                         (never changes)
    - [Oct 30 to Nov 1, 2026](.../issues/2026-10-30/)                      <- EDIT 2 adds a line above this
    Learn more or join the Los Olivos Outfitters Men's Club (links to the club page)  (never changes)
    New every Thursday. Brought to you by the Los Olivos Outfitters Men's Club.  (never changes)

The banner and the heading link point at the site root, which is always the newest issue, so they keep working even if a Notion edit fails.

Weekly steps, after the live site check in step 7 passes:

1. Fetch the Outfitters page with the Outfitters Notion connector (`user-Notion--outfitters`, `notion-fetch`) and confirm the "This week:" line and the first "Past issues" bullet are there exactly as written last week. If they are not, stop and report; do not rewrite the page.

2. Make ONE `notion-update-page` call with `command: "update_content"` and two `content_updates` (example for the Nov 6 issue, where last week was Oct 30):

   Edit 1, the this-week line:

       old_str: This week: [Friday, Oct 30 to Sunday, Nov 1, 2026](https://dvdbosch-creator.github.io/valley-weekender/issues/2026-10-30/)
       new_str: This week: [Friday, Nov 6 to Sunday, Nov 8, 2026](https://dvdbosch-creator.github.io/valley-weekender/issues/2026-11-06/)

   Edit 2, add one line at the top of the past list (newest first; this week's issue is listed too):

       old_str: - [Oct 30 to Nov 1, 2026](https://dvdbosch-creator.github.io/valley-weekender/issues/2026-10-30/)
       new_str: - [Nov 6 to Nov 8, 2026](https://dvdbosch-creator.github.io/valley-weekender/issues/2026-11-06/)
                - [Oct 30 to Nov 1, 2026](https://dvdbosch-creator.github.io/valley-weekender/issues/2026-10-30/)

   (In the actual call new_str is the two bullet lines joined by a newline, no leading spaces.) Never use `replace_content` or `allow_deleting_content` on the Outfitters page. Text strings come from `issues/issues.json` (`title` for the this-week line; a short "Mon D to Mon D, YYYY" form for the bullet).

3. Check the call result for warnings. A warning means an old_str did not match; fetch the page, report what changed, and do not retry with a broader edit.

4. Undo: run the same call with old_str and new_str swapped.

The list will grow by one line a week. After about 12 bullets, the bot may remove the oldest bullet with one more targeted edit (old_str = that bullet plus its leading newline, new_str empty); the full archive always lives at /issues/.
