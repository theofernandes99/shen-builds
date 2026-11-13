# Contenu de l'appli « Builds Shen top » : les builds, les catégories d'adversaires
# et le classement des champions. C'est LE fichier à modifier pour changer un conseil.
# Les noms, prix et icônes viennent automatiquement de Riot (Data Dragon) à chaque patch.
import json, re

CATS = {
  'auto': {
    'label': "Duellistes à attaques de base",
    'short': "Duellistes",
    'build': 'mitraillette',
    'why': "Leurs dégâts passent surtout par les attaques de base, que ton Refuge spirituel (W) annule pendant près de 2 secondes. Tu gagnes les duels longs, là où Tempo mortel monte à 6 charges.",
    'tips': [
      "Garde ton W pour leur all-in : il coupe leurs dégâts au moment où ils s'engagent.",
      "Combo : Rush des ombres (E) pour les provoquer, Assaut crépusculaire (Q) à travers eux, puis 3 attaques et l'actif de l'Hydre.",
      "Ne lâche pas le combat : Tempo mortel retombe si tu arrêtes de frapper plus de 6 secondes.",
    ],
  },
  'brawler': {
    'label': "Bagarreurs à sorts (AD)",
    'short': "Bagarreurs",
    'build': 'standard',
    'alt': 'garde',
    'swapRunes': {8444: 8473},
    'why': "Ils gagnent les combats longs et leurs gros dégâts viennent de sorts, donc ton W protège moins. Poigne de l'immortel récompense l'inverse : un échange court qui te soigne, puis tu recules. Plaque d'os réduit leurs combos.",
    'tips': [
      "Échange court : attaque renforcée par Poigne, Q à travers eux, puis recule avant leur riposte.",
      "Engage seulement quand leur sort principal est en recharge, sinon farme derrière ta vague.",
      "Poigne se recharge toutes les 4 s de combat : un échange toutes les 4 s, pas un all-in.",
    ],
  },
  'poke': {
    'label': "Harceleurs et poke à distance",
    'short': "Harceleurs",
    'build': 'garde',
    'items': [3748, 'BOOTS', 3073, 2502, 'DEF', 6665],
    'why': "Ils te touchent de loin et refusent les échanges courts. Tu rushes l'Hydre pour nettoyer les vagues, puis tu gagnes la partie ailleurs grâce à ton ulti.",
    'tips': [
      "Hydre titanesque d'abord : elle pousse la vague pour que tu puisses ulter sans perdre de sbires.",
      "Engage avec Rush des ombres (E) seulement quand leur sort de fuite est en recharge.",
      "Ne force pas : farm, survis, et laisse ton ulti faire la différence sur la carte.",
    ],
  },
  'ap': {
    'label': "Combattants et mages AP solides",
    'short': "AP solides",
    'build': 'impact',
    'why': "Leurs dégâts sont magiques : Sandales de Mercure, Visage spirituel et Rookern kaénique te rendent difficile à tuer, et Visage spirituel grossit tous tes boucliers de 25 %.",
    'tips': [
      "Évite les longs combats quand tous leurs sorts sont prêts : pousse la vague et ulte ailleurs.",
      "Ton bouclier passif dépend de tes PV bonus : chaque objet à PV le rend plus gros.",
      "Hexplaque expérimentale réduit le délai de ton ulti : utilise-le dès qu'un allié se bat.",
    ],
  },
  'tank': {
    'label': "Tanks et gros sacs à PV",
    'short': "Tanks",
    'build': 'carry',
    'alt': 'cleaver',
    'why': "Les tanks ne te menacent pas en lane : tu peux te permettre un objet de dégâts de plus. Poigne de l'immortel grossit à chaque échange, et Aube et crépuscule applique une seconde fois les dégâts en % des PV max de ton Q.",
    'tips': [
      "Échange souvent : chaque Poigne sur un champion te donne des PV pour toute la partie.",
      "Gagne la side lane : pousse plus vite qu'eux, puis ulte avant eux.",
      "En combat d'équipe, ignore-les et provoque leur carry.",
    ],
  },
  'squishy': {
    'label': "Fragiles : tireurs, mages, enchanteurs",
    'short': "Fragiles",
    'build': 'maraudeur',
    'alt': 'coup',
    'why': "Ils fuient ou te tiennent à distance, mais meurent vite : un seul combo leur retire 25 % de leurs PV. Assaut du maraudeur te donne alors 48 % de vitesse pour les rattraper.",
    'tips': [
      "Combo : Rush des ombres (E) pour les provoquer, puis les 3 attaques du Q : l'Assaut se déclenche presque à coup sûr.",
      "Utilise la vitesse gagnée pour les coller s'ils fuient, ou pour sortir de l'échange si leurs alliés arrivent.",
      "En combat d'équipe, arrive en ulti, provoque leur tireur et reste sur lui.",
    ],
  },
  'assassin': {
    'label': "Assassins et plongeurs",
    'short': "Assassins",
    'build': 'garde',
    'swapRunes': {8444: 8473},
    'items': [3084, 'BOOTS', 3073, 2525, 'DEF', 6665],
    'why': "Ils veulent tuer ton carry en une rafale. Tu deviens le garde du corps : Harnais protoplasmique et Plaque d'os absorbent leur burst, et ton ulti protège la cible qu'ils visent.",
    'tips': [
      "Garde ton ulti pour l'allié qu'ils vont plonger, pas pour engager.",
      "Ta provocation (E) coupe leur combo : place-la quand ils sautent sur ton carry.",
      "Ton W bloque aussi les attaques de base qui visent tes alliés dans la zone.",
    ],
  },
}

BUILDS = {
  'impact': {
    'name': "Impact", 'tag': "Side lane et teamfights",
    'tree': 8000, 'runes': [8005, 9111, 9104, 8017], 'sec': 8400, 'secRunes': [8401, 8451],
    'shards': ['AttackSpeed', 'AdaptiveForce', 'HealthScaling'],
    'items': [3748, 'BOOTS', 3073, 3065, 2525, 'DEF'],
    'idea': "Maximiser tes PV et tes boucliers, et arriver en ulti avec la vitesse d'attaque d'Hexplaque.",
  },
  'cleaver': {
    'name': "Cleaver", 'tag': "Dégâts contre les tanks",
    'tree': 8000, 'runes': [8005, 9111, 9104, 8017], 'sec': 8400, 'secRunes': [8444, 8451],
    'shards': ['AttackSpeed', 'AdaptiveForce', 'HealthScaling'],
    'items': [3748, 'BOOTS', 3071, 2501, 6665, 'DEF'],
    'idea': "Réduire l'armure avec Couperet noir et transformer tes PV en dégâts avec Armure sanguine.",
  },
  'mitraillette': {
    'name': "Mitraillette", 'tag': "Duels longs",
    'tree': 8000, 'runes': [8008, 9111, 9104, 8299], 'sec': 8400, 'secRunes': [8444, 8451],
    'shards': ['AttackSpeed', 'AdaptiveForce', 'HealthScaling'],
    'items': [3748, 'BOOTS', 3153, 3091, 3053, 'DEF'],
    'idea': "Empiler la vitesse d'attaque : chaque coup applique Lame du roi déchu et Au bout du rouleau.",
  },
  'coup': {
    'name': "Coup de poing", 'tag': "Échanges éclair",
    'tree': 8100, 'runes': [9923, 8126, 8137, 8106], 'sec': 8400, 'secRunes': [8444, 8451],
    'shards': ['AttackSpeed', 'AdaptiveForce', 'HealthScaling'],
    'items': [3748, 'BOOTS', 6610, 2501, 'DEF', 6665],
    'idea': "Une rafale de 3 coups toutes les 10 secondes, alignée sur le délai de Ciel éventré.",
  },
  'garde': {
    'name': "Garde du corps", 'tag': "Survivre et protéger",
    'tree': 8400, 'runes': [8439, 8401, 8444, 8451], 'sec': 8000, 'secRunes': [9111, 9104],
    'shards': ['AttackSpeed', 'HealthScaling', 'Tenacity'],
    'items': [3084, 'BOOTS', 3073, 2502, 'DEF', 6665],
    'idea': "Empiler les PV, provoquer pour déclencher Après-coup et garder l'ulti pour ton carry.",
  },
  'standard': {
    'name': "Standard méta", 'tag': "Poigne : échanges courts",
    'tree': 8400, 'runes': [8437, 8401, 8444, 8451], 'sec': 8300, 'secRunes': [8345, 8410],
    'shards': ['AttackSpeed', 'AdaptiveForce', 'HealthScaling'],
    'items': [3748, 'BOOTS', 2510, 3075, 2504, 'DEF'],
    'def': {'AD': 3143, 'AP': 3065, 'mixte': 6665},
    'idea': "Le build le plus joué : Poigne de l'immortel pour des échanges courts qui te soignent, Aube et crépuscule pour appliquer deux fois les effets de ton Q, puis des objets tank.",
  },
  'carry': {
    'name': "Carry hybride", 'tag': "Poigne : plus de dégâts",
    'tree': 8400, 'runes': [8437, 8401, 8444, 8451], 'sec': 8300, 'secRunes': [8345, 8410],
    'shards': ['AttackSpeed', 'AdaptiveForce', 'HealthScaling'],
    'items': [3748, 'BOOTS', 2510, 2524, 'DEF', 6665],
    'idea': "Un objet tank de moins pour beaucoup plus de dégâts : Aube et crépuscule double les effets de ton Q, et Flûtes de Bandle accélère ton équipe à chaque contrôle. À prendre aussi quand ton équipe perd.",
  },
  'maraudeur': {
    'name': "Maraudeur", 'tag': "Poursuite et ulti fréquent",
    'tree': 8200, 'runes': [8230, 8224, 8210, 8236], 'sec': 8400, 'secRunes': [8401, 8451],
    'shards': ['AttackSpeed', 'AdaptiveForce', 'HealthScaling'],
    'items': [3748, 'BOOTS', 3073, 2501, 'DEF', 6665],
    'def': {'AD': 2502, 'AP': 3065, 'mixte': 2502},
    'idea': "Retirer 25 % des PV d'une cible en moins de 3 secondes pour gagner 48 % de vitesse, et ulter plus souvent grâce à Arcaniste axiomatique et Hexplaque.",
  },
}

# Objet défensif selon le type de dégâts de l'adversaire, et bottes.
DEF = {'AD': 3143, 'AP': 2504, 'mixte': 6665}
BOOTS = {'AD': 3047, 'AP': 3111, 'mixte': 3111}
FALLBACK = [2502, 3075, 3065, 2504, 3143]

SHARDS = {
  'AttackSpeed': "Vitesse d'attaque",
  'AdaptiveForce': "Force adaptative",
  'CDRScaling': "Accélération de compétence",
  'MovementSpeed': "Vitesse de déplacement",
  'HealthScaling': "PV croissants",
  'HealthPlus': "PV",
  'Tenacity': "Ténacité et résistance aux ralentissements",
}

# Pourquoi chaque objet (court, vérifié sur les descriptions du patch 26.22).
ITEM_WHY = {
  3748: "Nettoie les vagues et remet ton attaque à zéro : les 3 coups du Q passent.",
  1054: "PV et régénération après les échanges.",
  2003: "Soin de départ.",
  3047: "Réduit de 10 % les dégâts des attaques.",
  3111: "Résistance magique et 30 % de ténacité.",
  3073: "30 d'accélération d'ultime, puis vitesse d'attaque et de déplacement après ton R.",
  3065: "Tes soins et boucliers sont augmentés de 25 %.",
  2525: "PV temporaires puis soin quand tu passes sous 30 % de PV.",
  3143: "Les coups critiques te font 30 % de dégâts en moins.",
  2504: "Bouclier anti-magie après 15 s sans dégâts magiques.",
  3071: "Réduit l'armure de la cible de 6 % par charge (5 max).",
  2501: "Te donne de l'AD égal à 2,5 % de tes PV bonus.",
  6665: "Armure et RM augmentées de 30 % après 5 s de combat.",
  3075: "Renvoie des dégâts et applique Hémorragie à ceux qui te frappent.",
  3153: "Dégâts selon les PV actuels de la cible, ralentit après 3 coups.",
  3091: "50 % de vitesse d'attaque, résistance magique et ténacité.",
  3053: "Bouclier quand tu passes sous 30 % de PV, ténacité.",
  6610: "Ta première attaque sur un champion fait un critique et te soigne.",
  3084: "900 PV qui grossissent quand tu frappes un champion proche.",
  2502: "Toutes les 4 s de combat, dégâts autour de toi et soin.",
  2510: "Après un sort, ta prochaine attaque inflige des dégâts magiques, te soigne et applique une 2e fois tes effets à l'impact (dont ton Q).",
  2524: "Ralentir ou immobiliser un champion te donne de la vitesse, et de la vitesse d'attaque à tes alliés proches.",
  4401: "Résistance magique bonus après plusieurs sorts subis.",
  6609: "Tes dégâts physiques appliquent Hémorragie (anti-soin).",
}

# 173 champions -> catégorie.
CLASS = {
 'auto': "Fiora Jax Tryndamere MasterYi Yasuo Yone Irelia Kayle Belveth Nilah XinZhao Warwick Olaf Trundle Udyr Viego Camille Nasus Shyvana",
 'brawler': "Darius Garen Sett Renekton Riven Aatrox Kled Illaoi MonkeyKing Ambessa Zaahen Pantheon Hecarim JarvanIV RekSai Briar Volibear Yorick Urgot",
 'poke': "Vayne Quinn Teemo Jayce Akshan Kennen Gnar Varus Smolder Gangplank Heimerdinger Singed Graves",
 'ap': "Mordekaiser Gwen Rumble Vladimir Sylas Swain Cassiopeia Ryze Lillia Gragas Aurora Karma",
 'tank': "Ornn Sion Maokai Malphite Chogath DrMundo KSante Poppy Sejuani Zac Rammus Amumu Nautilus Leona Braum Alistar TahmKench Galio Nunu Rell Skarner Taric Thresh Blitzcrank Shen",
 'squishy': "Aphelios Ashe Caitlyn Draven Ezreal Jhin Jinx Kaisa Kalista KogMaw Lucian MissFortune Samira Sivir Tristana Twitch Xayah Zeri Yunara Corki Senna Kindred Bard Janna Lulu Milio Nami Renata Seraphine Sona Soraka Yuumi Zilean Ivern Morgana Rakan Lux Xerath Veigar Syndra Ziggs Velkoz Annie Orianna Zoe Neeko Hwei Mel Brand Zyra Karthus Malzahar Anivia Viktor Azir TwistedFate Taliyah Lissandra AurelionSol Ahri Vex Fiddlesticks",
 'assassin': "Zed Talon Akali Katarina Khazix Rengar Evelynn Fizz Ekko Leblanc Qiyana Pyke Shaco Nocturne Kayn Naafiri Locke LeeSin Kassadin Elise Nidalee Diana Vi",
}

DMG_OVERRIDE = {
 'AD': "Akshan Qiyana Locke Nasus Belveth Hecarim Varus Jayce Gangplank Gnar Graves Ezreal Naafiri Ambessa Zaahen KSante Riven Sett Darius Garen Aatrox Kled Urgot Pantheon Camille Viego Yone Yasuo Irelia Fiora Tryndamere MasterYi XinZhao Warwick Olaf Trundle RekSai Vi LeeSin Briar Zed Talon Khazix Rengar Kayn Pyke Nocturne Quinn Vayne Smolder",
 'AP': "Rell Seraphine Vex Lillia Teemo Kennen Gwen Rumble Ekko Fizz Diana Elise Evelynn Kassadin Nidalee Akali Katarina Sylas Gragas Galio Malphite Chogath Amumu Zac Azir Hwei Mordekaiser Singed Heimerdinger Aurora Vladimir Swain Cassiopeia Ryze Karma Leblanc Fiddlesticks",
 'mixte': "Jax Shyvana Kayle Udyr Volibear DrMundo Corki Kaisa TwistedFate KogMaw Shaco Yorick Illaoi Renekton MonkeyKing Shen",
}

# Champions avec au moins un contrôle dur fiable (étourdissement, projection, entrave, charme, peur, provocation, suppression).
HARD_CC = set("""Aatrox Ahri Alistar Amumu Anivia Annie Ashe Bard Blitzcrank Braum Camille Cassiopeia Chogath Ekko Elise
Fiddlesticks Galio Gnar Gragas Hecarim Heimerdinger Irelia Ivern Janna JarvanIV Jax Jhin Karma Kennen KSante Leblanc
LeeSin Leona Lillia Lissandra Lulu Lux Malphite Malzahar Maokai Morgana Nami Nautilus Neeko Nocturne Nunu Orianna
Pantheon Poppy Pyke Qiyana Rakan Rammus Rell Renata Renekton Riven Ryze Sejuani Seraphine Sett Shen Singed Sion Skarner
Sona Soraka Swain Sylas Syndra TahmKench Taliyah Taric Thresh TwistedFate Udyr Urgot Varus Veigar Velkoz Vi Viktor
Volibear Warwick MonkeyKing Xayah Xerath XinZhao Yasuo Yone Zac Zilean Zyra Hwei Ambessa Vayne Fizz Shaco Vex""".split())

# Champions qui construisent des coups critiques (Présage de Randuin utile).
CRIT = set("""Aphelios Ashe Caitlyn Draven Jhin Jinx Lucian MissFortune Samira Sivir Tristana Twitch Xayah Zeri Yunara
Yasuo Yone Tryndamere MasterYi Gangplank Nilah Vayne Akshan Kindred Kalista""".split())

HEALERS = set("Aatrox Vladimir Warwick DrMundo Sylas Swain Fiora Olaf Illaoi Briar Soraka Yuumi Nasus Trundle Gwen Volibear Zac Maokai Kayn".split())

# Pourquoi proposer un build en alternative.
ALT_WHY = {
 'maraudeur': "Assaut du maraudeur te donne 48 % de vitesse après un gros combo : utile pour coller un champion mobile.",
 'coup': "Déluge de lames : trois coups quasi instantanés, pour une rafale encore plus rapide au contact.",
 'garde': "Après-coup et beaucoup de PV, si tu préfères encaisser leurs all-in plutôt qu'échanger court.",
 'cleaver': "Couperet noir et Armure sanguine : dégâts physiques et réduction d'armure, si leurs tanks empilent la résistance magique.",
}

# Notes propres à quelques matchups (tes matchups difficiles + classiques).
NOTES = {
 'Fiora': "Sa Riposte (W) bloque ta provocation et peut t'étourdir : lance Rush des ombres juste après sa parade.",
 'Garen': "Son Coup décisif (Q) est une attaque de base renforcée : ton W la bloque. Sa toupie (E), elle, passe.",
 'Darius': "Ses saignements montent à 5 charges dans les échanges longs : frappe et recule avant qu'il les cumule.",
 'Vayne': "Ton W bloque ses attaques, donc ses dégâts bruts : garde-le pour le moment où elle s'engage.",
 'Gangplank': "Ses barils sont des sorts, ton W ne les bloque pas. Hydre d'abord pour tenir la vague.",
 'Singed': "Ne le poursuis pas. Laisse-le pousser et gagne la partie avec ton ulti.",
 'Jax': "Sa Contre-attaque (E) esquive les attaques de base : place ton combo une fois qu'elle est terminée.",
 'Tryndamere': "Ton W bloque ses coups critiques : c'est ta meilleure arme contre son all-in.",
}

# Champions mobiles : le build Maraudeur leur est proposé en alternative.
MOBILE = set("Ambessa Riven Irelia Camille Yone Yasuo Hecarim Briar Belveth Nilah Viego Akshan Quinn Kayn".split())


class DataError(Exception):
    """Erreur lisible : un objet, une rune ou un champion du fichier n'existe plus au nouveau patch."""


def auto_cat(v):
    """Classement automatique d'un champion absent de CLASS (nouveau champion)."""
    tags, rng = v['tags'] or ['Fighter'], v['stats']['attackrange']
    t = tags[0]
    if t == 'Tank': return 'tank'
    if t == 'Assassin': return 'assassin'
    if t == 'Marksman': return 'squishy'
    if t in ('Mage', 'Support'): return 'ap' if rng <= 200 else 'squishy'
    return 'brawler'


def used_item_ids():
    ids = set([1054, 2003, 2510, 3075, 6609, 4401, 3053] + list(DEF.values()) + list(BOOTS.values()) + FALLBACK)
    for b in BUILDS.values():
        ids |= {i for i in b['items'] if isinstance(i, int)} | set(b.get('def', {}).values())
    for c in CATS.values(): ids |= {i for i in c.get('items', []) if isinstance(i, int)}
    return ids


def used_rune_ids():
    ids = {8473}
    for c in CATS.values(): ids |= set(c.get('swapRunes', {}).values())
    for b in BUILDS.values(): ids |= set(b['runes'] + b['secRunes'] + [b['tree'], b['sec']])
    return ids


def patch_label(version):
    # Data Dragon 16.22.1 = patch 26.22 (Riot numérote les patchs par année depuis 2025).
    major, minor = version.split('.')[:2]
    return f"{int(major) + 10}.{minor}" if int(major) >= 15 else f"{major}.{minor}"


def load(dd):
    """dd : dossier contenant champion.json, item.json, runesReforged.json, summoner.json, Shen.json (fr_FR)."""
    champs = json.load(open(f'{dd}/champion.json'))['data']
    items = json.load(open(f'{dd}/item.json'))['data']
    runes = json.load(open(f'{dd}/runesReforged.json'))
    summ = json.load(open(f'{dd}/summoner.json'))['data']
    shen = json.load(open(f'{dd}/Shen.json'))['data']['Shen']
    version = champs['Shen']['version']
    warnings = []

    cat_of = {}
    for cat, s in CLASS.items():
        for c in s.split():
            if c in cat_of: raise DataError(f"{c} est classé deux fois dans CLASS (build/data.py).")
            cat_of[c] = cat
    for gone in sorted(set(cat_of) - set(champs)):
        warnings.append(f"{gone} n'existe plus dans le jeu : ignoré.")
    new = sorted(set(champs) - set(cat_of))
    for k in new:
        cat_of[k] = auto_cat(champs[k])
        warnings.append(f"Nouveau champion {champs[k]['name']} classé automatiquement dans « {CATS[cat_of[k]]['short']} » : à vérifier.")

    dmg_of = {}
    for t, s in DMG_OVERRIDE.items():
        for c in s.split():
            if c in champs: dmg_of[c] = t
    for k, v in champs.items():
        if k in dmg_of: continue
        a, m = v['info']['attack'], v['info']['magic']
        dmg_of[k] = 'AD' if a >= m + 3 else 'AP' if m >= a + 3 else 'mixte'

    clist = [{'id': k, 'name': v['name'], 'cat': cat_of[k], 'dmg': dmg_of[k],
              'heal': k in HEALERS, 'cc': k in HARD_CC, 'crit': k in CRIT,
              **({'note': NOTES[k]} if k in NOTES else {}),
              **({'alt': 'maraudeur'} if k in MOBILE else {}),
              **({'new': True} if k in new else {})}
             for k, v in sorted(champs.items(), key=lambda kv: kv[1]['name'])]

    idata = {}
    for i in sorted(used_item_ids()):
        v = items.get(str(i))
        if not v or not v.get('maps', {}).get('11') or not v['gold'].get('purchasable', True):
            raise DataError(f"L'objet n°{i} ({ITEM_WHY.get(i, 'sans description')}) n'existe plus ou n'est plus achetable "
                            f"au patch {patch_label(version)}. Remplace-le dans build/data.py.")
        idata[i] = {'name': v['name'], 'gold': v['gold']['total'], 'why': ITEM_WHY.get(i, '')}

    rdata = {}
    for t in runes:
        rdata[t['id']] = {'name': t['name']}
        for sl in t['slots']:
            for r in sl['runes']:
                rdata[r['id']] = {'name': r['name'].replace('\xa0', ' '),
                                  'desc': re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', r['shortDesc'])).strip()}

    for r in sorted(used_rune_ids()):
        if r not in rdata:
            raise DataError(f"La rune n°{r} n'existe plus au patch {patch_label(version)}. Remplace-la dans build/data.py.")

    spells = {'P': shen['passive']['name']}
    for sp in shen['spells']: spells[sp['id']] = sp['name']
    sums = {k: summ[k]['name'] for k in ['SummonerFlash', 'SummonerDot']}

    return {'cats': CATS, 'builds': BUILDS, 'def': DEF, 'boots': BOOTS, 'fallback': FALLBACK,
            'shards': SHARDS, 'champs': clist, 'items': idata, 'runes': rdata,
            'spells': spells, 'sums': sums, 'version': version, 'patch': patch_label(version),
            'altWhy': ALT_WHY, 'warnings': warnings}
