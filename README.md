# Builds Shen top

Appli qui conseille un build de Shen en top selon le champion adverse et toute la compo adverse : runes, sorts, ordre des compétences, objets, conseils de matchup.

**Adresse de l'appli :** https://theofernandes99.github.io/shen-builds/

Sur iPhone : ouvre l'adresse dans Safari › **Partager** › **Sur l'écran d'accueil**. L'appli marche aussi sans connexion.

## Quand l'appli change

Rien ne se met à jour tout seul : le patch ne change que quand tu le demandes.

| Quand | Ce que fait GitHub |
|---|---|
| Tu modifies un fichier | Reconstruit et republie l'appli (1 à 2 minutes), avec le patch indiqué dans le fichier `PATCH`. |
| Tu demandes le nouveau patch | Onglet **Actions** › **Construire et publier** › **Run workflow** › coche **Passer au dernier patch de Riot** › **Run workflow**. GitHub récupère le dernier patch, met à jour icônes, noms et prix, enregistre le nouveau `PATCH` et republie. |
| Un nouveau champion arrive avec ce patch | Il est classé automatiquement et affiché « Nouveau : classement automatique ». Pense à vérifier son classement. |

L'appli installée sur ton téléphone récupère la nouvelle version au lancement suivant, dès qu'il y a du réseau.

## Si une publication échoue

GitHub t'envoie un e-mail, et l'onglet **Actions** montre une croix rouge. Ouvre l'exécution en échec : la ligne `ERREUR : …` explique le problème. Le cas le plus probable : Riot a retiré un objet ou une rune utilisés par un build. Remplace-le dans `build/data.py` (voir ci-dessous). L'ancienne version de l'appli reste en ligne en attendant.

## Modifier un build ou un conseil

Tout le contenu est dans **`build/data.py`**. Sur GitHub : ouvre le fichier › icône crayon › modifie › **Commit changes**. L'appli se republie toute seule.

- `BUILDS` : les 8 builds (runes, fragments, ordre des objets).
- `CATS` : les 7 catégories d'adversaires, le build conseillé pour chacune, l'explication et les conseils.
- `CLASS` : quel champion va dans quelle catégorie.
- `NOTES` : les conseils propres à un champion (Fiora, Darius, Garen…).
- `ITEM_WHY` : la phrase d'explication de chaque objet.

Les objets et les runes sont désignés par leur numéro Riot (par exemple 3748 = Hydre titanesque). La liste complète : https://ddragon.leagueoflegends.com/cdn/16.22.1/data/fr_FR/item.json

## Relancer une publication à la main

Onglet **Actions** › **Construire et publier** › **Run workflow** (case non cochée : même patch, simple republication).

## Organisation du dépôt

| Fichier | Rôle |
|---|---|
| `build/data.py` | Le contenu : builds, catégories, classement des champions. |
| `build/build.py` | Télécharge les données de Riot et fabrique l'appli dans `dist/`. |
| `build/check_patch.py` | Compare le patch du dépôt au dernier patch de Riot (lancé seulement sur demande). |
| `app/index.template.html` | La page de l'appli (style et code). Les données y sont injectées à la construction. |
| `app/sw.template.js` | Le service worker : mode hors ligne et mises à jour. |
| `app/icons/` | Les icônes de l'appli. |
| `PATCH` | La version des données Riot utilisée (ex. 16.22.1 = patch 26.22). |
| `.github/workflows/publier.yml` | La publication GitHub Actions (à chaque modification, ou à la demande). |

## Mentions

Données et icônes du jeu : Riot Games, Data Dragon. *Builds Shen top* n'est ni approuvé ni soutenu par Riot Games. League of Legends est une marque de Riot Games, Inc.
