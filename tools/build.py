#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur des pages statiques de tengumotion.com.

Le site livré est du HTML pur : ce script n'est PAS nécessaire pour le servir.
Il existe pour que les données partagées — prestations, tarifs, coordonnées,
navigation, mentions légales — ne vivent qu'à un seul endroit. Après une
modification ici :  python3 tools/build.py   puis commit des .html régénérés.
"""

import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ═══════════════════════════════════════════════════════════════════════════
# Identité
# ═══════════════════════════════════════════════════════════════════════════
SITE = {
    "name":      "Tengu Motion & Drone",
    "domain":    "tengumotion.com",
    "url":       "https://www.tengumotion.com",
    "tel":       "+33 6 33 59 87 74",
    "tel_href":  "+33633598774",
    "email":     "video@tengumotion.com",
    "zone":      "Île-de-France",
    "baseline":  "La précision est un rituel.",
    "baseline_ja": "精度は儀式である。",
    "agency":    "Shorai Consulting",
    "updated":   "01/09/2026",
}

NAV = [
    {"href": "index.html",    "label": "Accueil"},
    {"href": "services.html", "label": "Services & tarifs"},
    {"href": "contact.html",  "label": "Contact"},
]

# ═══════════════════════════════════════════════════════════════════════════
# Prestations — grille tarifaire 2026 (source : ui_kits/motion/data.jsx)
# ═══════════════════════════════════════════════════════════════════════════
FAMILIES = [
    {
        "slug": "image", "num": "壱", "ja": "映像",
        "kicker": "Image aérienne",
        "name": "Photographie & vidéo aérienne",
        "desc": "Immobilier, cinéma, corporate, promotion. Capteurs 4K/8K, "
                "stabilisation 3 axes, colorimétrie professionnelle.",
        "items": [
            ("Photo aérienne, demi-journée", "Reportage photo, jusqu'à 3 h sur site, sélection retouchée.", "450 €"),
            ("Journée photo / vidéo complète", "Captation aérienne + sol sur la journée, montage livré.", "1 250 €"),
            ("Pack immobilier, aérien + sol 8K", "Bien résidentiel ou luxe, photos + vidéo de présentation.", "350 €"),
            ("Corporate / inauguration outdoor", "Film d'entreprise, événement, tournage extérieur.", "600 €"),
            ("Clip FPV promotionnel", "Vidéo dynamique immersive, montage rythmé.", "550 €"),
            ("Film promotionnel 8K ultra", "Marque, collectivité, campagne, production haut de gamme.", "1 490 €"),
        ],
    },
    {
        "slug": "evenementiel", "num": "弐", "ja": "祭り",
        "kicker": "Mariage & événementiel",
        "name": "Mariage & événementiel",
        "desc": "Mariages, concerts, compétitions, événements corporate.",
        "items": [
            ("Mariage FPV, drone seul", "Couverture aérienne seule, film souvenir monté.", "750 €"),
            ("Mariage FPV + sol 8K", "Aérien + plans sol cinéma 8K, montage complet.", "950 €"),
            ("Événementiel, captation 4 h", "Salon, séminaire, inauguration, événement public.", "990 €"),
            ("Making-of / événement indoor", "Coulisses, événement B2B, salon en intérieur.", "400 €"),
        ],
    },
    {
        "slug": "studio", "num": "参", "ja": "室内",
        "kicker": "Studio & indoor",
        "name": "Studio & indoor, image 8K",
        "desc": "Tournage par tous temps et en intérieur : la continuité de "
                "production, hiver comme été.",
        "items": [
            ("Interview / portrait dirigeant", "Captation studio ou sur site, lumière soignée.", "350 €"),
            ("Vidéo produit / e-commerce", "Mise en valeur produit, plans détail 8K.", "290 € / produit"),
            ("Drone indoor : halls, concerts, sport", "Vol en intérieur, gymnases, salles, industrie.", "490 €"),
            ("Pack contenus réseaux, 5 vidéos", "Formats courts prêts à publier, fidélisation.", "390 €"),
        ],
    },
]

INCLUDED = [
    "Brief préalable et plan de vol personnalisé",
    "Livrables sous J+3 à J+7 selon la complexité",
    "Opérateur certifié DGAC + drone adapté à la mission",
    "Rapport d'intervention + fichiers bruts sur demande",
    "Assurance RC mission incluse, aucune surprise",
    "Support technique pendant 7 jours après livraison",
]

CONDITIONS = [
    ("Tarifs", "Prix indicatifs HT, hors options. Chaque devis est personnalisé selon la complexité, la zone et les livrables."),
    ("Zone d'intervention", "Île-de-France. Frais de déplacement au réel pour toute mission hors Île-de-France."),
    ("Devis & validité", "Devis gratuit sous 24 h. Proposition valable 30 jours à compter de son émission."),
    ("Réservation", "Acompte de 30 % à la commande, solde à la livraison. Créneau confirmé après acompte."),
    ("Météo", "Report sans frais en cas de conditions de vol non conformes (vent, pluie, zone réglementée)."),
    ("Cadre légal", "Opérations en catégorie Specific, conformes aux règlements UE 2019/945 et 2019/947. Assurance RC pro (UE 785/2004)."),
]

PRESTATION_OPTIONS = [
    "Photo / vidéo aérienne", "Pack immobilier", "Corporate / inauguration",
    "Clip FPV promotionnel", "Mariage", "Événementiel",
    "Studio & indoor", "Contenus réseaux",
]

# ═══════════════════════════════════════════════════════════════════════════
# Documents légaux.  <mark> = champ à compléter avant mise en ligne.
# ═══════════════════════════════════════════════════════════════════════════
def todo(label):
    return '<mark>[%s]</mark>' % label

LEGAL = {
    "mentions-legales": {
        "num": "壱", "eyebrow": "Informations légales",
        "title": "Mentions", "italic": "légales.",
        "lead": "Éditeur, hébergement, propriété intellectuelle et médiation.",
        "nav": "Mentions légales",
        "desc": "Mentions légales de Tengu Motion & Drone : éditeur, hébergement, propriété intellectuelle, médiation de la consommation.",
        "sections": [
            ("Éditeur du site",
             "Tengu Motion &amp; Drone — " + todo("forme juridique") + " au capital de " + todo("montant") + " €. "
             "Siège social : " + todo("adresse") + ", Île-de-France. SIREN " + todo("n°") + " · RCS " + todo("ville") + ". "
             "TVA intracommunautaire : " + todo("n°") + ". Responsable de la publication : " + todo("nom") + "."),
            ("Contact",
             'Téléphone : <a href="tel:{tel_href}">{tel}</a>. Email : <a href="mailto:{email}">{email}</a>. Site : www.{domain}.'),
            ("Activité réglementée",
             "Opérateur de drones certifié DGAC, exploitation en catégorie Specific conformément aux règlements "
             "UE 2019/945 et 2019/947. Assurance responsabilité civile professionnelle (règl. UE 785/2004)."),
            ("Hébergement",
             "Site hébergé par GitHub Pages — GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, "
             "États-Unis. https://github.com"),
            ("Propriété intellectuelle",
             "L'ensemble des contenus du site — textes, photographies, vidéos, marques et logo — est la propriété de "
             "Tengu Motion &amp; Drone. Toute reproduction ou diffusion, totale ou partielle, sans autorisation écrite "
             "préalable est interdite."),
            ("Réalisation", "Conception et réalisation du site : {agency}."),
            ("Médiation",
             "En cas de litige avec un client consommateur, recours possible au médiateur de la consommation : "
             + todo("nom et coordonnées du médiateur") + ", dans un délai d'un an à compter de la réclamation écrite."),
        ],
    },
    "confidentialite": {
        "num": "弐", "eyebrow": "Données personnelles",
        "title": "Politique de", "italic": "confidentialité.",
        "lead": "Ce que nous collectons, pourquoi, combien de temps, et comment exercer vos droits.",
        "nav": "Confidentialité",
        "desc": "Politique de confidentialité de Tengu Motion & Drone : données collectées, finalités, durées de conservation, droit à l'image et exercice de vos droits RGPD.",
        "sections": [
            ("Responsable de traitement",
             "Tengu Motion &amp; Drone, " + todo("adresse") + ", Île-de-France. Contact : <a href=\"mailto:{email}\">{email}</a>."),
            ("Données collectées",
             "Via le formulaire de devis : nom, société, email, téléphone, description de la mission. "
             "Via la navigation : données techniques strictement nécessaires au fonctionnement du site."),
            ("Finalités et base légale",
             "Répondre aux demandes de devis et gérer la relation client (exécution du contrat ou intérêt légitime). "
             "Aucune donnée n'est utilisée à des fins publicitaires sans consentement."),
            ("Durées de conservation",
             "Demandes de devis sans suite : 12 mois. Dossiers clients et documents comptables : 10 ans, conformément "
             "aux obligations légales. Images et rushes : conservés selon l'autorisation de diffusion accordée."),
            ("Destinataires",
             "Les données ne sont ni vendues ni cédées. Elles peuvent être transmises aux prestataires techniques "
             "nécessaires (hébergement, messagerie, comptabilité), agissant sur instruction."),
            ("Prises de vue aériennes",
             "Les captations sont réalisées dans le respect du droit à l'image et de la vie privée. Les personnes "
             "identifiables sur des images destinées à diffusion font l'objet d'une autorisation, ou d'un floutage à défaut."),
            ("Vos droits",
             "Accès, rectification, effacement, limitation, opposition et portabilité : écrire à "
             "<a href=\"mailto:{email}\">{email}</a>. Réponse sous un mois. Réclamation possible auprès de la CNIL "
             "(<a href=\"https://www.cnil.fr\" rel=\"noopener\">www.cnil.fr</a>)."),
            ("Cookies",
             "Le site n'utilise que des cookies techniques nécessaires à son fonctionnement. Aucun traceur publicitaire "
             "ou de mesure d'audience n'est déposé sans consentement préalable."),
        ],
    },
    "cgv": {
        "num": "参", "eyebrow": "Conditions de vente",
        "title": "Conditions générales", "italic": "de vente.",
        "lead": "Devis, réservation, réalisation, livrables et droits d'utilisation des images.",
        "nav": "CGV",
        "desc": "Conditions générales de vente de Tengu Motion & Drone : devis, réservation, report météo, livrables, droits d'utilisation des images.",
        "sections": [
            ("Objet",
             "Les présentes conditions régissent les prestations de captation photo et vidéo, aériennes et au sol, "
             "réalisées par Tengu Motion &amp; Drone. Toute commande implique leur acceptation sans réserve."),
            ("Devis et prix",
             "Prix indicatifs HT, hors options. Chaque devis est personnalisé selon la complexité, la zone et les "
             "livrables. Le devis est gratuit, émis sous 24 h et valable 30 jours à compter de son émission. "
             "Seul le devis signé fait foi."),
            ("Réservation et paiement",
             "Acompte de 30 % à la commande, solde à la livraison. Le créneau est confirmé après réception de "
             "l'acompte. Paiement par virement sous 30 jours ; pénalités de retard au taux légal et indemnité "
             "forfaitaire de 40 € en cas de retard."),
            ("Zone d'intervention",
             "Île-de-France. Frais de déplacement facturés au réel pour toute mission hors Île-de-France."),
            ("Conditions de vol et report",
             "Report sans frais en cas de conditions de vol non conformes : vent, pluie, visibilité, zone réglementée "
             "ou refus d'autorisation. Une nouvelle date est proposée dans les meilleurs délais."),
            ("Annulation",
             "Annulation par le client plus de 7 jours avant la date : acompte remboursé. Moins de 7 jours : acompte "
             "conservé au titre des frais d'organisation. En cas d'annulation par le prestataire hors cas météo, "
             "l'acompte est intégralement remboursé."),
            ("Réalisation et livrables",
             "Brief préalable et plan de vol personnalisé. Livrables sous J+3 à J+7 selon la complexité. Rapport "
             "d'intervention et fichiers bruts sur demande. Support technique pendant 7 jours après livraison."),
            ("Retouches et validation",
             "Une série de retouches ou d'ajustements de montage est incluse. Toute demande supplémentaire fait "
             "l'objet d'un devis complémentaire. À défaut de retour sous 15 jours, les livrables sont réputés acceptés."),
            ("Droits d'utilisation",
             "Les fichiers livrés sont cédés pour l'usage défini au devis. Toute exploitation étendue — publicité, "
             "revente, cession à un tiers — fait l'objet d'un avenant. Le prestataire conserve la propriété "
             "intellectuelle des œuvres et le droit de les utiliser à des fins de démonstration, sauf clause de "
             "confidentialité."),
            ("Responsabilité et assurance",
             "Opérations conduites en catégorie Specific, conformément aux règlements UE 2019/945 et 2019/947. "
             "Assurance responsabilité civile professionnelle (règl. UE 785/2004). La responsabilité du prestataire "
             "est limitée au montant de la prestation."),
            ("Droit applicable",
             "Droit français. En cas de litige, les parties recherchent une solution amiable avant toute action ; "
             "à défaut, compétence des tribunaux du ressort du siège social."),
        ],
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# Aides
# ═══════════════════════════════════════════════════════════════════════════
def min_price(fam):
    """Prix d'entrée d'une famille, mis en forme comme dans la grille."""
    best, best_txt = None, None
    for _, _, price in fam["items"]:
        n = int(re.sub(r"[^0-9]", "", price.split("/")[0]))
        if best is None or n < best:
            best, best_txt = n, price
    return best_txt


def wordmark(dark=False, size=16):
    cls = "wordmark wordmark--dark" if dark else "wordmark"
    return ('<span class="%s" style="font-size:%dpx">'
            '<span class="w-tengu">TENGU</span>'
            '<span class="w-suffix">Motion &amp; Drone</span></span>' % (cls, size))


def nav_html(current, transparent=False):
    cls = "nav nav--transparent" if transparent else "nav"
    logo = "assets/img/logo-invert.svg"
    out = ['<nav class="%s on-ink" aria-label="Navigation principale">' % cls]
    out.append('  <a class="nav__brand" href="index.html">')
    out.append('    <img src="%s" width="30" height="30" alt="">' % logo)
    out.append('    %s' % wordmark(dark=True))
    out.append('  </a>')
    out.append('  <button class="nav__toggle" type="button" aria-expanded="false" '
               'aria-controls="nav-links">Menu</button>')
    out.append('  <div class="nav__links" id="nav-links" data-open="false">')
    for link in NAV:
        cur = ' aria-current="page"' if link["href"] == current else ""
        out.append('    <a class="nav__link" href="%s"%s>%s</a>' % (link["href"], cur, link["label"]))
    if current != "contact.html":
        out.append('    <a class="btn btn--ghost-dark btn--sm" href="contact.html">Demander un devis</a>')
    out.append('  </div>')
    out.append('</nav>')
    return "\n".join(out)


def footer_html():
    services = "\n".join(
        '        <li><a href="services.html#%s">%s</a></li>' % (f["slug"], f["kicker"])
        for f in FAMILIES
    )
    legal = "\n".join(
        '      <a href="%s.html">%s</a>' % (slug, LEGAL[slug]["nav"])
        for slug in ("mentions-legales", "confidentialite", "cgv")
    )
    return """<footer class="footer on-sumi">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <div class="footer__brand">
          <img src="assets/img/logo-invert.svg" width="42" height="42" alt="">
          {wordmark}
        </div>
        <p class="footer__blurb">Vidéo, vidéo par drone et photographie en Île-de-France. Immobilier,
          corporate, mariage, événementiel, studio et indoor.</p>
        <p class="tagline" style="margin-top:22px">Precision&nbsp;is&nbsp;a&nbsp;ritual</p>
      </div>
      <div>
        <h2 class="h4">Services</h2>
        <ul>
{services}
          <li><a href="services.html">Services &amp; tarifs 2026</a></li>
        </ul>
      </div>
      <div>
        <h2 class="h4">Studio</h2>
        <ul>
          <li>Opérateurs certifiés DGAC</li>
          <li>Catégorie Specific</li>
          <li>Assurance RC professionnelle</li>
          <li>Livrables J+3 à J+7</li>
        </ul>
      </div>
      <div>
        <h2 class="h4">Contact</h2>
        <ul>
          <li><a href="tel:{tel_href}">{tel}</a></li>
          <li><a href="mailto:{email}">{email}</a></li>
          <li>www.{domain}</li>
          <li>{zone}</li>
        </ul>
      </div>
    </div>
    <div class="footer__bar">
      <span>© <span data-year>2026</span> · {name}</span>
      <nav aria-label="Informations légales">
{legal}
      </nav>
      <span>Site réalisé par {agency}</span>
      <span>Tarifs indicatifs HT · Document non contractuel</span>
    </div>
  </div>
</footer>""".format(wordmark=wordmark(dark=True, size=20), services=services, legal=legal, **SITE)


JSONLD = """{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": "{url}/#business",
  "name": "{name}",
  "description": "Vidéo, vidéo par drone et photographie professionnelle en Île-de-France. Opérateur certifié DGAC, catégorie Specific.",
  "url": "{url}",
  "telephone": "{tel}",
  "email": "{email}",
  "image": "{url}/assets/img/og-image.png",
  "logo": "{url}/assets/img/logo.svg",
  "priceRange": "290 € – 1 490 €",
  "slogan": "La précision est un rituel.",
  "areaServed": {{ "@type": "AdministrativeArea", "name": "Île-de-France" }},
  "address": {{ "@type": "PostalAddress", "addressRegion": "Île-de-France", "addressCountry": "FR" }},
  "knowsAbout": ["Photographie aérienne par drone", "Vidéo par drone", "Captation événementielle",
                 "Film corporate", "Vidéo immobilière", "Drone indoor"],
  "hasOfferCatalog": {{
    "@type": "OfferCatalog",
    "name": "Grille tarifaire 2026",
    "itemListElement": [{offers}]
  }}
}}"""


def jsonld():
    offers = []
    for fam in FAMILIES:
        items = []
        for name, desc, price in fam["items"]:
            amount = re.sub(r"[^0-9]", "", price.split("/")[0])
            # Formatage par %% : les accolades restent simples (pas de .format ici).
            items.append(
                '{"@type":"Offer","name":"%s","description":"%s","price":"%s",'
                '"priceCurrency":"EUR","valueAddedTaxIncluded":false,'
                '"availableAtOrFrom":{"@type":"AdministrativeArea","name":"Île-de-France"}}'
                % (name.replace('"', "'"), desc.replace('"', "'"), amount)
            )
        offers.append(
            '{"@type":"OfferCatalog","name":"%s","itemListElement":[%s]}'
            % (fam["name"].replace("&amp;", "&"), ",".join(items))
        )
    return JSONLD.format(offers=",".join(offers), **SITE)


def page(slug, title, description, body, transparent_nav=False, extra_ld=""):
    """Assemble une page complète."""
    canonical = SITE["url"] + "/" + ("" if slug == "index.html" else slug)
    return """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="author" content="{name}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#3C3489">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{name}">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{url}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{url}/assets/img/og-image.png">

<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/logo.svg">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,700&family=Lato:ital,wght@0,300;0,400;0,700;1,400&family=Noto+Serif+JP:wght@400;500;700&display=swap">
<link rel="stylesheet" href="assets/css/tokens.css">
<link rel="stylesheet" href="assets/css/site.css">

<script type="application/ld+json">
{jsonld}
</script>{extra_ld}
</head>
<body>
<a class="skip-link" href="#contenu">Aller au contenu</a>
{nav}
<main id="contenu">
{body}
</main>
{footer}
<script src="assets/js/site.js" defer></script>
</body>
</html>
""".format(
        title=title, description=description, canonical=canonical,
        jsonld=jsonld(), extra_ld=extra_ld,
        nav=nav_html(slug, transparent_nav), body=body, footer=footer_html(),
        **SITE
    )


def frame(inner, big=False):
    cls = "frame frame--lg" if big else "frame"
    return '<div class="%s">%s<span class="frame-c1"></span><span class="frame-c2"></span></div>' % (cls, inner)


# ═══════════════════════════════════════════════════════════════════════════
# Fragments partagés
# ═══════════════════════════════════════════════════════════════════════════
def included_html(on_dark=False):
    lis = "\n".join("      <li>%s</li>" % t for t in INCLUDED)
    return '<ul class="included">\n%s\n    </ul>' % lis


def contact_form():
    options = "\n".join("            <option>%s</option>" % o for o in PRESTATION_OPTIONS)
    return """<div class="contactblock" id="devis">
      <div class="split">
        <div>
          <p class="eyebrow"><span class="ja">天</span> Prenons contact</p>
          <h2 style="font-size:var(--fs-h3);margin-top:16px;letter-spacing:.04em">Parlons de<br><span class="italic-accent">votre mission.</span></h2>
          <p style="font-size:13px;color:var(--fg-2);margin-top:14px">Devis personnalisé, gratuit sous 24 h.</p>
          <p class="mono">
            <a href="tel:{tel_href}">{tel}</a><br>
            <a href="mailto:{email}">{email}</a><br>
            {zone}
          </p>
        </div>

        <!-- Endpoint : remplacez VOTRE_ID par votre identifiant Formspree (voir README).
             Tant qu'il n'est pas configuré, le formulaire bascule sur un mailto. -->
        <form class="form" id="devis-form" method="post" action="https://formspree.io/f/VOTRE_ID">
          <div class="field">
            <label for="nom">Nom</label>
            <input type="text" id="nom" name="nom" placeholder="Nom et société" autocomplete="organization" required>
          </div>
          <div class="field">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" placeholder="contact@societe.fr" autocomplete="email" required>
          </div>
          <div class="field">
            <label for="telephone">Téléphone</label>
            <input type="tel" id="telephone" name="telephone" placeholder="06 00 00 00 00" autocomplete="tel">
          </div>
          <div class="field">
            <label for="prestation">Type de prestation</label>
            <select id="prestation" name="prestation">
{options}
            </select>
          </div>
          <div class="field field--full">
            <span class="field-label" id="livrable-label">Livrable</span>
            <div class="segmented" role="radiogroup" aria-labelledby="livrable-label">
              <input type="radio" id="liv-photo" name="livrable" value="Photo">
              <label for="liv-photo">Photo</label>
              <input type="radio" id="liv-video" name="livrable" value="Vidéo">
              <label for="liv-video">Vidéo</label>
              <input type="radio" id="liv-deux" name="livrable" value="Les deux" checked>
              <label for="liv-deux">Les deux</label>
            </div>
          </div>
          <div class="field field--full">
            <label for="message">Votre mission</label>
            <textarea id="message" name="message" placeholder="Lieu, date souhaitée, durée, livrables attendus."></textarea>
          </div>
          <p class="form__note" id="form-status" role="status" aria-live="polite"></p>
          <div class="form__foot">
            <span class="tagline">Precision&nbsp;is&nbsp;a&nbsp;ritual</span>
            <button class="btn btn--primary" type="submit">Demander un devis</button>
          </div>
        </form>
      </div>
    </div>""".format(options=options, **SITE)


# ═══════════════════════════════════════════════════════════════════════════
# Pages
# ═══════════════════════════════════════════════════════════════════════════
def build_index():
    cards = []
    for fam in FAMILIES:
        cards.append("""        <a class="card" href="services.html#{slug}">
          <div>
            <div class="card__num">{num}</div>
            <h3 class="card__title">{kicker} <span class="ja">{ja}</span></h3>
            <p class="card__desc">{desc}</p>
          </div>
          <div>
            <p class="card__price"><span>Dès</span><strong>{price}</strong></p>
            <p class="card__more">En savoir plus</p>
          </div>
        </a>""".format(price=min_price(fam), **fam))

    body = """<header class="hero on-ink techgrid glow">
  <span class="hanko hanko--corner" aria-hidden="true">天</span>
  <div class="wrap">
    <div class="hero__grid">
      <div>
        <p class="hero__kicker">Vidéo · Vidéo par drone · Photographie <span class="ja">映像</span></p>
        <h1>La précision<br><span class="italic-accent">est un rituel.</span></h1>
        <p class="lead">Des opérations aériennes sur mesure pour les professionnels qui refusent
          l'approximation. De l'image à la donnée, chaque prestation est conduite avec la même
          rigueur opérationnelle.</p>
        <p class="btn-row">
          <a class="btn btn--seal" href="contact.html">Demander un devis</a>
          <a class="btn btn--ghost-dark" href="services.html">Services &amp; tarifs</a>
        </p>
      </div>
      {plate}
    </div>
    <div class="hero__rail">
      <span>Édition 2026 · MMXXVI</span>
      <nav aria-label="Familles de prestations">
        <a href="services.html#image">Image aérienne</a>
        <a href="services.html#evenementiel">Mariage</a>
        <a href="services.html#evenementiel">Événementiel</a>
        <a href="services.html#studio">Studio &amp; indoor</a>
      </nav>
      <span>Certifié DGAC · Île-de-France</span>
    </div>
  </div>
</header>

<section class="section" aria-labelledby="familles">
  <div class="wrap">
    <div class="split" style="margin-bottom:56px">
      <p class="eyebrow"><span class="ja">一</span> Trois familles</p>
      <div>
        <h2 id="familles" style="font-size:var(--fs-h1)">L'image aérienne,
          <span class="italic-accent">conduite comme une opération.</span></h2>
        <p class="lead" style="margin-top:18px">Vidéo, vidéo par drone et photographie : mariage et
          événementiel, studio et indoor. Quatorze prestations, une seule discipline.</p>
      </div>
    </div>
    <div class="cols-3">
{cards}
    </div>
  </div>
</section>

<section class="section on-sumi techgrid glow" aria-labelledby="phare">
  <div class="wrap">
    <div class="cols-2" style="align-items:center">
      <div>
        <p class="eyebrow"><span class="ja">二</span> Production haut de gamme</p>
        <h2 id="phare" style="font-size:var(--fs-h1);margin-top:18px">Film promotionnel
          <span class="accent-dark">8K ultra</span></h2>
        <p class="ja" style="font-size:22px;color:var(--t-bamboo);margin-top:12px">映像 · Marque, collectivité, campagne</p>
        <p class="lead" style="margin-top:22px">Captation aérienne et sol, stabilisation trois axes,
          colorimétrie professionnelle. Repérage, plan de vol, montage : une production menée de bout en bout.</p>
        <dl class="specs">
          <div><dt class="caps">Capteur</dt><dd style="margin:0">8K · gimbal-3</dd></div>
          <div><dt class="caps">Livraison</dt><dd style="margin:0">J+3 à J+7</dd></div>
          <div><dt class="caps">Dès</dt><dd style="margin:0">1 490 €</dd></div>
        </dl>
        <p class="btn-row"><a class="btn btn--ghost-dark" href="services.html">Services &amp; tarifs</a></p>
      </div>
      <div class="featured__plate">
        {featured}
      </div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="manifeste">
  <div class="wrap">
    <div class="split">
      <p class="eyebrow"><span class="ja">三</span> Manifeste</p>
      <div>
        <h2 id="manifeste" class="manifesto">« La précision est un rituel. »</h2>
        <div class="manifesto__foot">
          <span class="tagline">Precision&nbsp;is&nbsp;a&nbsp;ritual</span>
          <span class="ja">精度は儀式である。</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section--tight" aria-labelledby="inclus">
  <div class="wrap">
    <div class="split split--top">
      <div>
        <p class="eyebrow"><span class="ja">四</span> Inclus</p>
        <p style="font-size:12px;color:var(--fg-2);margin-top:8px">Ce que comprend chaque prestation.</p>
      </div>
      <div>
        <h2 id="inclus" class="visually-hidden" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Inclus dans chaque prestation</h2>
        {included}
      </div>
    </div>
  </div>
</section>

<section class="section--tight">
  <div class="wrap">
    {form}
  </div>
</section>""".format(
        cards="\n".join(cards),
        plate=frame('<div class="hero__plate"><img src="assets/img/logo-invert.svg" alt="Emblème Ha-Uchiwa de Tengu Motion &amp; Drone" width="200" height="200"></div>', big=True).replace('<div class="frame frame--lg">', '<div class="frame frame--lg" style="align-self:stretch">'),
        featured=frame('<img src="assets/img/logo-invert.svg" alt="" width="200" height="200">'
                       '<p class="featured__meta"><span>Catégorie Specific</span><span>Certifié DGAC</span></p>'),
        included=included_html(),
        form=contact_form(),
    )
    return page(
        "index.html",
        "Tengu Motion & Drone — Vidéo, drone et photographie en Île-de-France",
        "Vidéo, vidéo par drone et photographie professionnelle en Île-de-France : immobilier, "
        "corporate, mariage, événementiel, studio et indoor. Opérateur certifié DGAC, devis gratuit sous 24 h.",
        body, transparent_nav=True,
    )


def build_services():
    groups = []
    for fam in FAMILIES:
        rows = "\n".join(
            """        <div class="pricerow">
          <div>
            <p class="pricerow__name">{name}</p>
            <p class="pricerow__desc">{desc}</p>
          </div>
          <p class="pricerow__price"><span class="caps">Dès</span><strong>{price}</strong></p>
        </div>""".format(name=n, desc=d, price=p)
            for n, d, p in fam["items"]
        )
        groups.append("""      <div class="pricegroup" id="{slug}">
        <div class="pricegroup__head">
          <span class="ja" style="font-size:20px;color:var(--accent)">{num}</span>
          <h2>{name} <span class="ja">{ja}</span></h2>
          <p>{desc}</p>
        </div>
        <div class="pricetable">
{rows}
        </div>
      </div>""".format(rows=rows, **fam))

    terms = "\n".join(
        '        <div><dt>%s</dt><dd>%s</dd></div>' % (label, text)
        for label, text in CONDITIONS
    )

    body = """<header class="pagehead on-ink techgrid glow">
  <span class="hanko hanko--corner" aria-hidden="true">天</span>
  <div class="wrap">
    <p class="hero__kicker"><span class="ja">値</span> Services &amp; tarifs · MMXXVI</p>
    <h1>Vidéo, vidéo par drone,<br><span class="italic-accent">photographie.</span></h1>
    <p class="lead">Trois familles de prestations, quatorze formules. Prix indicatifs HT,
      devis gratuit sous 24 h, valable 30 jours à compter de son émission.</p>
  </div>
</header>

<section class="section">
  <div class="wrap">
{groups}
  </div>
</section>

<section class="section on-sumi techgrid" aria-labelledby="inclus">
  <div class="wrap">
    <div class="split split--top">
      <div>
        <p class="eyebrow"><span class="ja">含</span> Inclus</p>
        <p style="font-size:12px;color:var(--t-bambou-200);margin-top:8px">Ce que comprend chaque prestation.</p>
      </div>
      <div>
        <h2 id="inclus" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Inclus dans chaque prestation</h2>
        {included}
      </div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="conditions">
  <div class="wrap">
    <div class="split split--top">
      <div>
        <p class="eyebrow"><span class="ja">約</span> Conditions</p>
        <p style="font-size:12px;color:var(--fg-2);margin-top:8px">Le cadre de chaque mission.</p>
      </div>
      <div>
        <h2 id="conditions" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Conditions générales</h2>
        <dl class="terms">
{terms}
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="section--tight">
  <div class="wrap">
    {form}
  </div>
</section>""".format(groups="\n".join(groups), terms=terms,
                     included=included_html(True), form=contact_form())

    return page(
        "services.html",
        "Services & tarifs 2026 — Tengu Motion & Drone",
        "Grille tarifaire 2026 : 14 prestations vidéo, drone et photo en Île-de-France. "
        "Pack immobilier dès 350 €, mariage dès 750 €, film 8K dès 1 490 €. Devis gratuit sous 24 h.",
        body,
    )


def build_contact():
    body = """<header class="pagehead on-ink techgrid glow">
  <span class="hanko hanko--corner" aria-hidden="true">天</span>
  <div class="wrap">
    <p class="hero__kicker"><span class="ja">天</span> Prenons contact</p>
    <h1>Parlons de<br><span class="italic-accent">votre mission.</span></h1>
    <p class="lead">Décrivez le lieu, la date et les livrables attendus : vous recevez un devis
      personnalisé sous 24 h, avec plan de vol et fenêtres de tournage.</p>
  </div>
</header>

<section class="section">
  <div class="wrap">
    {form}
  </div>
</section>

<section class="section--tight" aria-labelledby="coord">
  <div class="wrap">
    <div class="split split--top">
      <div>
        <p class="eyebrow"><span class="ja">所</span> Coordonnées</p>
      </div>
      <div>
        <h2 id="coord" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Coordonnées</h2>
        <dl class="terms">
          <div><dt>Téléphone</dt><dd><a href="tel:{tel_href}" style="text-decoration:none;color:var(--t-ink);font-weight:700">{tel}</a></dd></div>
          <div><dt>Email</dt><dd><a href="mailto:{email}" style="text-decoration:none;color:var(--t-ink);font-weight:700">{email}</a></dd></div>
          <div><dt>Zone d'intervention</dt><dd>Île-de-France. Frais de déplacement au réel pour toute mission hors Île-de-France.</dd></div>
          <div><dt>Délai de réponse</dt><dd>Devis gratuit sous 24 h, valable 30 jours à compter de son émission.</dd></div>
          <div><dt>Cadre réglementaire</dt><dd>Opérateur certifié DGAC, catégorie Specific (règl. UE 2019/945 et 2019/947). Assurance RC professionnelle (règl. UE 785/2004).</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>""".format(form=contact_form(), **SITE)

    return page(
        "contact.html",
        "Contact & devis — Tengu Motion & Drone",
        "Demandez un devis gratuit sous 24 h pour une prestation vidéo, drone ou photo en "
        "Île-de-France. Téléphone +33 6 33 59 87 74 — video@tengumotion.com.",
        body,
    )


def build_legal(slug):
    doc = LEGAL[slug]
    sections = "\n".join(
        '        <div>\n          <h2>%s</h2>\n          <p>%s</p>\n        </div>'
        % (label, text.format(**SITE))
        for label, text in doc["sections"]
    )
    nav_items = "\n".join(
        '            <li><a href="%s.html"%s>%s</a></li>'
        % (s, ' aria-current="page"' if s == slug else "", LEGAL[s]["nav"])
        for s in ("mentions-legales", "confidentialite", "cgv")
    )
    body = """<header class="pagehead on-ink techgrid glow">
  <span class="hanko hanko--corner" aria-hidden="true">天</span>
  <div class="wrap">
    <p class="hero__kicker"><span class="ja">{num}</span> {eyebrow}</p>
    <h1>{title}<br><span class="italic-accent">{italic}</span></h1>
    <p class="lead">{lead}</p>
  </div>
</header>

<section class="section">
  <div class="wrap">
    <div class="split split--top">
      <div class="legal-nav">
        <p class="eyebrow"><span class="ja">条</span> Documents</p>
        <nav aria-label="Documents légaux">
          <ul>
{nav_items}
          </ul>
        </nav>
        <p class="legal-nav__date">Mise à jour : {updated}</p>
      </div>
      <div class="legal-doc">
{sections}
      </div>
    </div>
  </div>
</section>""".format(nav_items=nav_items, sections=sections, updated=SITE["updated"],
           num=doc["num"], eyebrow=doc["eyebrow"], title=doc["title"],
           italic=doc["italic"], lead=doc["lead"])

    return page(slug + ".html", doc["nav"] + " — " + SITE["name"], doc["desc"], body)


def build_404():
    body = """<header class="pagehead on-ink techgrid glow">
  <span class="hanko hanko--corner" aria-hidden="true">天</span>
  <div class="wrap">
    <p class="hero__kicker"><span class="ja">空</span> Erreur 404</p>
    <h1>Cette page<br><span class="italic-accent">n'existe pas.</span></h1>
    <p class="lead">Le lien est peut-être obsolète. Reprenez depuis l'accueil, ou consultez
      directement la grille tarifaire 2026.</p>
    <p class="btn-row">
      <a class="btn btn--seal" href="index.html">Retour à l'accueil</a>
      <a class="btn btn--ghost-dark" href="services.html">Services &amp; tarifs</a>
    </p>
  </div>
</header>"""
    return page("404.html", "Page introuvable — " + SITE["name"],
                "La page demandée n'existe pas. Retour à l'accueil de Tengu Motion & Drone.", body)


# ═══════════════════════════════════════════════════════════════════════════
def write(name, content):
    path = os.path.join(ROOT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print("  %-24s %6d o" % (name, len(content.encode("utf-8"))))


def build_sitemap():
    pages = ["", "services.html", "contact.html",
             "mentions-legales.html", "confidentialite.html", "cgv.html"]
    today = date.today().isoformat()
    urls = "\n".join(
        "  <url>\n    <loc>%s/%s</loc>\n    <lastmod>%s</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>"
        % (SITE["url"], p, today, "1.0" if p == "" else ("0.9" if p == "services.html" else "0.5"))
        for p in pages
    )
    return '<?xml version="1.0" encoding="UTF-8"?>\n' \
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % urls


def main():
    print("Génération de %s :" % SITE["domain"])
    write("index.html", build_index())
    write("services.html", build_services())
    write("contact.html", build_contact())
    for slug in ("mentions-legales", "confidentialite", "cgv"):
        write(slug + ".html", build_legal(slug))
    write("404.html", build_404())
    write("sitemap.xml", build_sitemap())
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE["url"])
    print("Terminé.")


if __name__ == "__main__":
    main()
