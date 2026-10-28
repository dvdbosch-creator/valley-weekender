"""Rebuild the front page and the Past Issues list after adding a new issue.

Weekly steps:
  1. Add issues/YYYY-MM-DD/index.html (paths relative to that folder, so shared
     files are ../../assets/... and photos are img/...) plus issues/YYYY-MM-DD/img/.
  2. Add an entry at the top of issues/issues.json.
  3. Run: python3 tools/publish.py
  4. Commit and push. GitHub Pages serves the new issue within a minute or two.
"""
import json, pathlib, re, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
issues = json.loads((ROOT / 'issues/issues.json').read_text())
latest = issues[0]['date']

# Front page = latest issue with paths rewritten from issues/DATE/ to the site root.
src = (ROOT / f'issues/{latest}/index.html').read_text()
front = src.replace('../../', '')
front = re.sub(r'(src|href)="img/', rf'\1="issues/{latest}/img/', front)
(ROOT / 'index.html').write_text(front)

# Past Issues list, rebuilt from issues.json (newest first).
arch_path = ROOT / 'issues/index.html'
arch = arch_path.read_text()
rows = '\n'.join(
    f'  <a class="iss" href="{i["date"]}/"><span class="no">{html.escape(i["number"])}</span>'
    f'<span class="dt">{html.escape(i["title"])}</span><span class="tz">{html.escape(i["teaser"])}</span></a>'
    for i in issues)
arch = re.sub(r'<nav>.*?</nav>', '<nav>\n' + rows + '\n</nav>', arch, flags=re.S)
arch_path.write_text(arch)
for p in (ROOT / 'index.html', arch_path):
    t = p.read_text(); assert '\u2014' not in t and '\u2013' not in t, p
print('front page ->', latest, '|', len(issues), 'issues listed')
