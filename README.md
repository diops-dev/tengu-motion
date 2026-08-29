# Tengu Motion &amp; Drone — site vitrine

Site statique **trilingue** de **Tengu Motion &amp; Drone** — vidéo, vidéo par drone et
photographie professionnelle en Île-de-France. Français, anglais, espagnol.

> « La précision est un rituel. » · 精度は儀式である

HTML, CSS et JavaScript purs. **Aucune dépendance, aucun build, aucun framework** :
le dépôt est le site. On le sert tel quel depuis GitHub Pages, Netlify, un OVH ou
n'importe quel hébergeur statique.

---

## Sommaire

- [Les trois langues](#les-trois-langues)
- [Mise en ligne](#mise-en-ligne)
- [Avant la première publication](#avant-la-première-publication)
- [Structure](#structure)
- [Modifier le contenu](#modifier-le-contenu)
- [Système de design](#système-de-design)
- [Développement local](#développement-local)

---

## Les trois langues

| Langue | Racine | Exemple |
|---|---|---|
| Français (référence) | `/` | `/services.html` |
| English | `/en/` | `/en/services.html` |
| Español | `/es/` | `/es/servicios.html` |

Les slugs sont **traduits** : `/es/servicios.html`, `/en/privacy-policy.html`. La
correspondance est déclarée une seule fois, dans `SLUGS` (`tools/content.py`) — le
sélecteur de langue, les balises `hreflang` et le `sitemap.xml` en découlent tous.

**Pas de redirection automatique.** Le visiteur choisit via le sélecteur FR / EN / ES
dans la navigation, qui pointe toujours vers *la même page* dans l'autre langue — pas
vers l'accueil. Les moteurs de recherche sont guidés par les balises `hreflang`
réciproques, avec le français en `x-default`.

### Pages légales

Les versions anglaise et espagnole sont des **traductions de courtoisie**. Chacune
porte en tête un encart rappelant que seule la version française fait foi, avec un lien
vers celle-ci. Les CGV restent régies par le droit français quelle que soit la langue
consultée.

### Page 404

GitHub Pages ne sert que le `404.html` de la racine, quelle que soit l'URL demandée.
La version française porte donc un rappel en anglais et en espagnol, pour ne laisser
aucun visiteur sans porte de sortie. Les `404.html` des sous-dossiers existent pour un
accès direct et pour les hébergeurs qui, eux, les servent.

### Ajouter une quatrième langue

1. Ajouter le code dans `LANGS` et `LANG_META` (`tools/content.py`).
2. Ajouter la colonne correspondante dans `SLUGS`.
3. Dupliquer et traduire les blocs `FAMILIES`, `INCLUDED`, `CONDITIONS`, `UI`,
   `META`, `LEGAL`, `LD_DESC` et `LD_KNOWS`.
4. `python3 tools/build.py`.

Aucune modification de `build.py` n'est nécessaire. Un contrôle utile après coup :

```bash
python3 -c "
import sys; sys.path.insert(0,'tools'); import content as C
ref = set(C.UI['fr'])
for l in C.LANGS:
    manque = ref - set(C.UI[l])
    print(l, 'OK' if not manque else manque)"
```

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

Ils se corrigent dans `tools/content.py` (dictionnaire `LEGAL`) — **dans les trois
langues**, les mêmes champs y figurent — puis :

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

Le même formulaire sert les trois langues : `assets/js/site.js` ne contient **aucun
texte**, il lit ses messages dans les attributs `data-*` posés par le générateur.

**Tant que l'identifiant n'est pas renseigné**, `assets/js/site.js` bascule
automatiquement sur un `mailto:` pré-rempli vers `video@tengumotion.com` :
aucune demande n'est perdue, même sans configuration. Alternatives équivalentes
si vous préférez : Formspark, Basin, Web3Forms, ou un webhook Netlify Forms.

### 3. Le domaine dans les métadonnées

`SITE["url"]` (dans `tools/content.py`) vaut aujourd'hui l'adresse réellement servie :

```python
"url": "https://diops-dev.github.io/tengu-motion",
```

Elle alimente les balises canoniques, les `hreflang`, l'Open Graph et le `sitemap.xml`.
Le jour où `tengumotion.com` est branché, passez-la à `https://www.tengumotion.com` et
régénérez — sinon les moteurs de recherche indexent un domaine qui ne répond pas.

---

## Structure

```
.
├── index.html               Accueil FR
├── services.html            Grille tarifaire 2026 · 14 prestations
├── contact.html             Formulaire de devis et coordonnées
├── mentions-legales.html    ⚠ champs à compléter
├── confidentialite.html     ⚠ champs à compléter
├── cgv.html                 Conditions générales de vente
├── 404.html                 Erreur — sert tout le site, rappel EN/ES inclus
│
├── en/                      index · services · contact · legal-notice
│                            privacy-policy · terms · 404
├── es/                      index · servicios · contacto · aviso-legal
│                            privacidad · condiciones · 404
│
├── assets/
│   ├── css/tokens.css       Jetons du design system
│   ├── css/site.css         Composants et mise en page
│   ├── js/site.js           Menu mobile, formulaire — sans texte en dur
│   └── img/                 logo.svg · logo-invert.svg · favicon.svg · og-image.png
│
├── tools/
│   ├── content.py           TOUT le contenu, dans les trois langues
│   └── build.py             Gabarits et génération
│
├── sitemap.xml              18 URL, chacune déclarant ses trois variantes
├── robots.txt
├── CNAME                    Domaine personnalisé (voir ci-dessus)
└── .github/workflows/deploy.yml
```

---

## Modifier le contenu

**Deux façons, au choix.**

### Directement dans le HTML

Les pages sont lisibles et indentées. Pour un prix, un mot, une date : ouvrez le
`.html`, modifiez, commitez. Rien d'autre à faire.

Attention : la navigation, le pied de page et le bloc de devis sont dupliqués dans
**21 pages**. Une modification de ces éléments devrait être répercutée partout — c'est
précisément ce que le générateur évite. À ce volume, l'édition manuelle n'est plus
raisonnable que pour une coquille isolée.

### Via `tools/build.py` (recommandé pour tout ce qui est partagé)

Le script rassemble en un seul endroit ce qui apparaît sur plusieurs pages.
Il ne nécessite que Python 3, sans aucune bibliothèque externe.

Tout le contenu vit dans **`tools/content.py`**, indexé par langue.

| À modifier | Dictionnaire |
|---|---|
| Téléphone, email, URL du site | `SITE` |
| Prestations, descriptions, prix | `FAMILIES` |
| « Inclus dans chaque prestation » | `INCLUDED` |
| Conditions commerciales | `CONDITIONS` |
| Tous les libellés d'interface | `UI` |
| Titres et descriptions SEO | `META` |
| Mentions légales, RGPD, CGV | `LEGAL` |
| Noms de fichiers par langue | `SLUGS` |

Une modification de prix dans `FAMILIES["fr"]` **ne se propage pas** aux deux autres
langues : les prix y sont répétés pour que chaque version reste relisible telle quelle.
Pensez à modifier les trois.

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
  domaine que dans un sous-dossier (`/tengu-motion/`), et les pages `/en/` et `/es/`
  remontent d'un cran vers `assets/`.
- Le JavaScript est **non bloquant** : sans lui, la navigation, tous les
  contenus et le formulaire (en `POST` classique) restent opérationnels.
- Le site est **imprimable** : une feuille `@media print` masque la navigation
  et les fonds encrés — utile pour sortir la grille tarifaire en PDF.

---

## Licence

Code sous licence MIT (voir `LICENSE`). **La marque, l'emblème Ha-Uchiwa, le
sceau 天, les logotypes et les textes commerciaux en sont exclus** et restent la
propriété de Tengu Motion &amp; Drone.
