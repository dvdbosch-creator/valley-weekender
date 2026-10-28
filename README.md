# The Valley Weekender

A weekly guide to what is special in the Santa Ynez Valley and nearby, brought to you by the Los Olivos Outfitters Men's Club.

- `index.html` is this week's issue.
- `issues/` holds every issue in its own dated folder, plus the Past Issues list.
- `assets/` holds the crest, the landscape and the bundled fonts (Fraunces and Inter, SIL Open Font License).

## Publishing a new issue
1. Add `issues/YYYY-MM-DD/index.html` and its `img/` folder.
2. Add the issue at the top of `issues/issues.json`.
3. Run `python3 tools/publish.py` to refresh `index.html` and `issues/index.html`.
4. Commit and push to `main`. GitHub Pages (main branch, root folder) updates in a minute or two.
