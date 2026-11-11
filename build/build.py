"""Construit l'appli dans le dossier dist/ à partir des données officielles de Riot.

Usage : python build/build.py            (version lue dans le fichier PATCH)
        python build/build.py 16.23.1    (version imposée)

Étapes : télécharge les données en français (Data Dragon), vérifie que les objets
et runes de build/data.py existent toujours, télécharge et compresse les icônes,
puis écrit dist/index.html (tout intégré), le service worker, le manifeste et les icônes.
"""
import base64, concurrent.futures as cf, hashlib, io, json, os, shutil, sys, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'build'))
import data as content  # noqa: E402

DDRAGON = 'https://ddragon.leagueoflegends.com/cdn'
MIRROR = 'https://raw.githubusercontent.com/noxelisdev/LoL_DDragon/master'  # copie de secours de Data Dragon
LANG = 'fr_FR'


def http(url, tries=3):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'shen-builds'})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception as e:  # réseau capricieux : on réessaie
            last = e
    raise last


class Source:
    """Chemins Data Dragon officiels, ou la copie de secours si Riot ne répond pas."""

    def __init__(self, version):
        self.v = version
        try:
            http(f'{DDRAGON}/{version}/data/{LANG}/summoner.json', tries=1)
            self.base = 'ddragon'
        except Exception:
            mirror_v = json.loads(http(f'{MIRROR}/latest/manifest.json'))['v']
            if mirror_v != version:
                sys.exit(f"Data Dragon injoignable et la copie de secours est en {mirror_v}, pas en {version}.")
            self.base = 'mirror'
        print(f'Source des données : {self.base} ({version})')

    def data(self, name):
        return f'{DDRAGON}/{self.v}/data/{LANG}/{name}' if self.base == 'ddragon' else f'{MIRROR}/latest/data/{LANG}/{name}'

    def img(self, kind, file):
        return f'{DDRAGON}/{self.v}/img/{kind}/{file}' if self.base == 'ddragon' else f'{MIRROR}/latest/img/{kind}/{file}'

    def perk(self, path):
        return f'{DDRAGON}/img/{path}' if self.base == 'ddragon' else f'{MIRROR}/img/{path}'


def to_webp(raw, size):
    im = Image.open(io.BytesIO(raw)).convert('RGBA').resize((size, size), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, 'WEBP', quality=82, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else open(os.path.join(ROOT, 'PATCH')).read().strip()
    src = Source(version)
    dd = os.path.join(ROOT, '.cache', version)
    os.makedirs(dd, exist_ok=True)
    for name in ['champion.json', 'item.json', 'runesReforged.json', 'summoner.json', 'champion/Shen.json']:
        out = os.path.join(dd, os.path.basename(name))
        if not os.path.exists(out):
            open(out, 'wb').write(http(src.data(name)))

    try:
        d = content.load(dd)
    except content.DataError as e:
        sys.exit(f'ERREUR : {e}')
    for w in d['warnings']:
        print('ATTENTION :', w)

    champs = json.load(open(os.path.join(dd, 'champion.json')))['data']
    runes = json.load(open(os.path.join(dd, 'runesReforged.json')))
    jobs = {}
    for k, v in champs.items():
        jobs['c_' + k] = (src.img('champion', v['image']['full']), 64)
    for i in d['items']:
        jobs[f'i_{i}'] = (src.img('item', f'{i}.png'), 48)
    wanted = content.used_rune_ids()
    for t in runes:
        jobs[f"t_{t['id']}"] = (src.perk(t['icon']), 40)
        for n, sl in enumerate(t['slots']):
            for r in sl['runes']:
                if r['id'] in wanted:
                    jobs[f"r_{r['id']}"] = (src.perk(r['icon']), 64 if n == 0 else 48)
    for s in content.SHARDS:
        jobs['s_' + s] = (src.perk(f'perk-images/StatMods/StatMods{s}Icon.png'), 32)
    for s in ['SummonerFlash', 'SummonerDot']:
        jobs['ss_' + s] = (src.img('spell', f'{s}.png'), 48)
    for s in ['ShenQ', 'ShenW', 'ShenE', 'ShenR']:
        jobs['sp_' + s] = (src.img('spell', f'{s}.png'), 40)

    def get(item):
        key, (url, size) = item
        try:
            return key, to_webp(http(url), size), None
        except Exception as e:
            return key, None, f'{url} : {e}'

    icons, fails = {}, []
    with cf.ThreadPoolExecutor(12) as ex:
        for key, val, err in ex.map(get, jobs.items()):
            if val: icons[key] = val
            else: fails.append(err)
    if fails:
        sys.exit('ERREUR : icônes introuvables :\n' + '\n'.join(fails[:20]))
    print(f'{len(icons)} icônes')

    dist = os.path.join(ROOT, 'dist')
    shutil.rmtree(dist, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, 'app', 'icons'), os.path.join(dist, 'icons'))
    d.pop('warnings')
    html = open(os.path.join(ROOT, 'app', 'index.template.html')).read()
    html = html.replace('__DATA__', json.dumps(d, ensure_ascii=False)).replace('__ICONS__', json.dumps(icons))
    open(os.path.join(dist, 'index.html'), 'w').write(html)

    stamp = hashlib.sha1(html.encode()).hexdigest()[:10]
    sw = open(os.path.join(ROOT, 'app', 'sw.template.js')).read().replace('__VERSION__', stamp)
    open(os.path.join(dist, 'sw.js'), 'w').write(sw)
    manifest = {
        "name": "Builds Shen top", "short_name": "Shen", "lang": "fr",
        "description": "Builds de Shen top selon l'adversaire et la compo adverse.",
        "start_url": "./", "scope": "./", "display": "standalone", "orientation": "any",
        "background_color": "#0a0e1c", "theme_color": "#0a0e1c",
        "icons": [
            {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    json.dump(manifest, open(os.path.join(dist, 'manifest.webmanifest'), 'w'), ensure_ascii=False, indent=2)
    print(f"dist/ prêt : patch {d['patch']}, {len(d['champs'])} champions, {round(len(html) / 1e6, 2)} Mo")


if __name__ == '__main__':
    main()
