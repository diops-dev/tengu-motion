# Tengu Motion &amp; Drone — site vitrine

Site statique de **Tengu Motion &amp; Drone** — vidéo, vidéo par drone et photographie
professionnelle en Île-de-France.

> « La précision est un rituel. » · 精度は儀式である

HTML, CSS et JavaScript purs. **Aucune dépendance, aucun build, aucun framework** :
le dépôt est le site. On le sert tel quel depuis GitHub Pages, Netlify, un OVH ou
n'importe quel hébergeur statique.

---

## Sommaire

- [Mise en ligne](#mise-en-ligne)
- [Avant la première publication](#avant-la-première-publication)
- [Structure](#structure)
- [Modifier le contenu](#modifier-le-contenu)
- [Système de design](#système-de-design)
- [Développement local](#développement-local)

---

## Mise en ligne

Le workflow `.github/workflows/deploy.yml` publie automatiquement à chaque push
sur `main`. Une seule chose à faire côté GitHub :

**Settings → Pages → Build and deployment → Source : `GitHub Actions`**

Le premier push déclenche le déploiement. L'URL apparaît dans l'onglet *Actions*
puis dans *Settings → Pages*.

### Nom de domaine

Le fichier `CNAME` pointe le site vers `tengumotion.com`.

- **Domaine pas encore configuré ? Supprimez `CNAME`** avant le premier push,
  sinon Pages refuse de servir le site. L'adresse sera alors
  `https://diops-dev.github.io/tengu-motion/`.
- **Domaine prêt ?** Gardez `CNAME` et créez chez votre registrar :

  | Type    | Nom   | Valeur                    |
  |---------|-------|---------------------------|
  | `A`     | `@`   | `185.199.108.153`         |
  | `A`     | `@`   | `185.199.109.153`         |
  | `A`     | `@`   | `185.199.110.153`         |
  | `A`     | `@`   | `185.199.111.153`         |
  | `CNAME` | `www` | `diops-dev.github.io.`    |

  Puis, dans *Settings → Pages*, saisissez le domaine et cochez
  **Enforce HTTPS** une fois le certificat émis (quelques minutes à 24 h).

---

## Avant la première publication

Trois points à traiter — ils sont volontairement visibles plutôt que silencieux.

### 1. Champs légaux à compléter

Les mentions légales et la politique de confidentialité contiennent des champs
`[entre crochets]`, **surlignés en jaune** dans le navigateur pour qu'aucun
n'échappe à la relecture : forme juridique, capital, adresse du siège, SIREN,
RCS, TVA, responsable de la publication, médiateur de la consommation.

Ils se corrigent dans `tools/build.py` (dictionnaire `LEGAL`), puis :

```bash
python3 tools/build.py
```

Ces mentions sont **obligatoires** pour un site professionnel français
(art. 6-III de la LCEN). Le surlignage disparaît dès que les crochets sont
remplacés par le texte réel.

### 2. Formulaire de devis

Un site statique n'a pas de serveur : le formulaire a besoin d'un service tiers.
Il est câblé pour [Formspree](https://formspree.io) (offre gratuite : 50
soumissions/mois).

1. Créez un formulaire sur Formspree, récupérez son identifiant (`xayzbwqr`).
2. Dans `tools/build.py`, remplacez `VOTRE_ID` par cet identifiant.
3. Régénérez : `python3 tools/build.py`.

**Tant que l'identifiant n'est pas renseigné**, `assets/js/site.js` bascule
automatiquement sur un `mailto:` pré-rempli vers `video@tengumotion.com` :
aucune demande n'est perdue, même sans configuration. Alternatives équivalentes
si vous préférez : Formspark, Basin, Web3Forms, ou un webhook Netlify Forms.

### 3. Le domaine dans les métadonnées

`SITE["url"]` dans `tools/build.py` alimente les balises canoniques, Open Graph
et le `sitemap.xml`. S'il ne s'agit pas de `https://www.tengumotion.com`,
changez-le puis régénérez.

---

## Structure

```
.
├── index.html               Accueil : hero, 3 familles, production 8K, manifeste, devis
├── services.html            Grille tarifaire 2026 · 14 prestations, inclus, conditions
├── contact.html             Formulaire de devis et coordonnées
├── mentions-legales.html    ⚠ champs à compléter
├── confidentialite.html     ⚠ champs à compléter
├── cgv.html                 Conditions générales de vente
├── 404.html                 Page d'erreur (servie automatiquement par Pages)
│
├── assets/
│   ├── css/tokens.css       Jetons du système de design (couleurs, type, espacement)
│   ├── css/site.css         Composants et mise en page
│   ├── js/site.js           Menu mobile, formulaire, année du copyright
│   └── img/                 logo.svg · logo-invert.svg · favicon.svg · og-image.png
│
├── tools/build.py           Générateur des pages (facultatif — voir ci-dessous)
├── sitemap.xml              Régénéré par build.py
├── robots.txt
├── CNAME                    Domaine personnalisé
└── .github/workflows/deploy.yml
```

---

## Modifier le contenu

**Deux façons, au choix.**

### Directement dans le HTML

Les pages sont lisibles et indentées. Pour un prix, un mot, une date : ouvrez le
`.html`, modifiez, commitez. Rien d'autre à faire.

Attention : la navigation, le pied de page et le bloc de devis sont dupliqués
dans chaque page. Une modification de ces éléments doit être répercutée partout —
c'est précisément ce que le générateur évite.

### Via `tools/build.py` (recommandé pour tout ce qui est partagé)

Le script rassemble en un seul endroit ce qui apparaît sur plusieurs pages.
Il ne nécessite que Python 3, sans aucune bibliothèque externe.

| À modifier | Où, dans `build.py` |
|---|---|
| Téléphone, email, domaine, zone | `SITE` |
| Prestations, descriptions, prix | `FAMILIES` |
| « Inclus dans chaque prestation » | `INCLUDED` |
| Conditions commerciales | `CONDITIONS` |
| Mentions légales, RGPD, CGV | `LEGAL` |
| Choix du menu déroulant du devis | `PRESTATION_OPTIONS` |
| Liens de navigation | `NAV` |

```bash
python3 tools/build.py     # réécrit les .html, le sitemap et robots.txt
```

Les prix d'appel affichés sur les cartes d'accueil (« dès 350 € ») et le
`JSON-LD` d'offres sont **calculés** depuis `FAMILIES` : ils ne se désynchronisent
jamais de la grille.

---

## Système de design

Repris du *Tengu Drone Design System*, kit `ui_kits/motion`.

| Jeton | Valeur | Rôle |
|---|---|---|
| `--t-ink` | `#3C3489` | Encre de Nuit — primaire, ~60 % |
| `--t-lacquer` | `#9B2226` | Rouge Laque — accent et sceau, 6–15 % |
| `--t-bamboo` | `#C4A882` | Bambou Doré — chaud, 10–15 % |
| `--t-washi` | `#F5F5F0` | Washi — surface, ~50 % |
| `--t-sumi` | `#2D2D2D` | Sumi — texte, 4–5 % |

Typographie : **Cormorant Garamond** (titres), **Lato** (texte),
**Noto Serif JP** (japonais). Servies par Google Fonts — c'est le seul appel
réseau externe du site.

### Deux écarts assumés par rapport au kit

Le kit d'origine est un prototype ; deux valeurs ne passaient pas le contraste
WCAG AA et ont été ajustées :

- `--t-mist` (`#7B7591`) tombe à **4.38:1** sur blanc. Il reste disponible pour
  les usages décoratifs, mais le texte secondaire utilise `--t-mist-text`
  (`#6B6580`, **5.53:1**).
- `--t-laque-500` (`#C73E42`) tombe à **2.75:1** sur fond sumi. Les accents
  rouges sur fond sombre passent par `--t-laque-300` (`#E05A5E`, **3.80:1**,
  conforme pour les grands titres) via la classe `.accent-dark`.

Toutes les autres paires du site sont à 4.5:1 ou au-delà.

### Le sceau 天

Le hanko est ponctuel, jamais décoratif : un seul par page, en haut à droite du
bloc d'en-tête. Il est masqué sous 720 px de large, où il entrerait en conflit
avec le menu.

---

## Développement local

Ouvrir `index.html` dans un navigateur suffit. Pour un rendu identique à la
production (chemins et polices) :

```bash
python3 -m http.server 8000
# puis http://localhost:8000
```

### Points d'attention

- Les chemins sont **relatifs** : le site fonctionne aussi bien à la racine d'un
  domaine que dans un sous-dossier (`/tengu-motion/`).
- Le JavaScript est **non bloquant** : sans lui, la navigation, tous les
  contenus et le formulaire (en `POST` classique) restent opérationnels.
- Le site est **imprimable** : une feuille `@media print` masque la navigation
  et les fonds encrés — utile pour sortir la grille tarifaire en PDF.

---

## Licence

Code sous licence MIT (voir `LICENSE`). **La marque, l'emblème Ha-Uchiwa, le
sceau 天, les logotypes et les textes commerciaux en sont exclus** et restent la
propriété de Tengu Motion &amp; Drone.
