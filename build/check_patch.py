"""Regarde si Riot a publié un nouveau patch. Si oui, met à jour le fichier PATCH.

Écrit pour GitHub Actions : changed=true|false, version=…, patch=… (dans $GITHUB_OUTPUT).
"""
import json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'build'))
from data import patch_label  # noqa: E402

current = open(os.path.join(ROOT, 'PATCH')).read().strip()
try:
    req = urllib.request.Request('https://ddragon.leagueoflegends.com/api/versions.json', headers={'User-Agent': 'shen-builds'})
    latest = json.loads(urllib.request.urlopen(req, timeout=30).read())[0]
except Exception as e:
    print(f'Data Dragon injoignable ({e}) : on garde {current}.')
    latest = current


def key(v):
    return [int(x) for x in v.split('.') if x.isdigit()]


changed = key(latest) > key(current)
if changed:
    open(os.path.join(ROOT, 'PATCH'), 'w').write(latest + '\n')
    print(f'Nouveau patch : {patch_label(current)} -> {patch_label(latest)} ({latest})')
else:
    print(f'Pas de nouveau patch (actuel : {patch_label(current)}, {current})')

out = os.environ.get('GITHUB_OUTPUT')
if out:
    with open(out, 'a') as f:
        v = latest if changed else current
        f.write(f'changed={"true" if changed else "false"}\nversion={v}\npatch={patch_label(v)}\n')
