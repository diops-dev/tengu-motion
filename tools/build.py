#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur des pages statiques de tengumotion.com — français, anglais, espagnol.

Le site livré est du HTML pur : ce script n'est PAS nécessaire pour le servir.
Il existe pour que le contenu partagé — prestations, tarifs, coordonnées,
navigation, mentions légales — ne vive qu'à un seul endroit, dans content.py,
et pour garder les trois langues rigoureusement synchronisées.

    python3 tools/build.py

Arborescence produite :
    /index.html  /services.html  …          français (langue de référence)
    /en/index.html  /en/services.html  …    anglais
    /es/index.html  /es/servicios.html  …   espagnol
"""

import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import (SITE, LANGS, LANG_META, SLUGS, LEGAL_KEYS, FAMILIES,
                     INCLUDED, CONDITIONS, UI, META, LEGAL, LD_DESC, LD_KNOWS)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ═══════════════════════════════════════════════════════════════════════════
# Chemins
#
# Le français vit à la racine, l'anglais et l'espagnol dans un sous-dossier.
# Tout est relatif : le site fonctionne aussi bien sur un domaine propre que
# dans un sous-répertoire (…github.io/tengu-motion/).
# ═══════════════════════════════════════════════════════════════════════════
def up(lang):
    """Préfixe pour remonter à la racine du site depuis une page de `lang`."""
    return "" if lang == "fr" else "../"


def href(key, lang, from_lang):
    """Lien vers la page `key` en `lang`, depuis une page écrite en `from_lang`."""
    return up(from_lang) + LANG_META[lang]["dir"] + SLUGS[key][lang]


def abs_url(key, lang):
    """URL absolue, pour les balises canoniques, hreflang et le sitemap."""
    slug = SLUGS[key][lang]
    path = LANG_META[lang]["dir"] + ("" if slug == "index.html" else slug)
    return SITE["url"] + "/" + path


def min_price(fam):
    """Prix d'entrée d'une famille, mis en forme comme dans la grille."""
    best, best_txt = None, None
    for _, _, price in fam["items"]:
        n = int(re.sub(r"[^0-9]", "", price.split("/")[0]))
        if best is None or n < best:
            best, best_txt = n, price
    return best_txt


def sr_only(text, ident):
    """Titre présent pour les lecteurs d'écran, invisible à l'œil."""
    return ('<h2 id="%s" style="position:absolute;width:1px;height:1px;'
            'overflow:hidden;clip:rect(0 0 0 0)">%s</h2>' % (ident, text))


def frame(inner, big=False):
    cls = "frame frame--lg" if big else "frame"
    return ('<div class="%s">%s<span class="frame-c1"></span>'
            '<span class="frame-c2"></span></div>' % (cls, inner))


# ═══════════════════════════════════════════════════════════════════════════
# Fragments communs
# ═══════════════════════════════════════════════════════════════════════════
def wordmark(dark=False, size=16):
    cls = "wordmark wordmark--dark" if dark else "wordmark"
    return ('<span class="%s" style="font-size:%dpx">'
            '<span class="w-tengu">TENGU</span>'
            '<span class="w-suffix">Motion &amp; Drone</span></span>' % (cls, size))


def lang_switch(key, lang):
    """Sélecteur FR / EN / ES — pointe vers la MÊME page dans l'autre langue."""
    out = ['<div class="langs" role="group" aria-label="%s">' % UI[lang]["lang_aria"]]
    for other in LANGS:
        cur = ' aria-current="true"' if other == lang else ""
        out.append('      <a class="langs__a" hreflang="%s" lang="%s" href="%s"%s>%s</a>'
                   % (LANG_META[other]["html"], LANG_META[other]["html"],
                      href(key, other, lang), cur, LANG_META[other]["short"]))
    out.append('    </div>')
    return "\n".join(out)


def nav_html(key, lang, transparent=False):
    t = UI[lang]
    cls = "nav nav--transparent" if transparent else "nav"
    links = [("home", t["nav_home"]), ("services", t["nav_services"]), ("contact", t["nav_contact"])]
    out = ['<nav class="%s on-ink" aria-label="%s">' % (cls, t["nav_aria"])]
    out.append('  <a class="nav__brand" href="%s">' % href("home", lang, lang))
    out.append('    <img src="%sassets/img/logo-invert.svg" width="30" height="30" alt="">' % up(lang))
    out.append('    %s' % wordmark(dark=True))
    out.append('  </a>')
    out.append('  <button class="nav__toggle" type="button" aria-expanded="false" '
               'aria-controls="nav-links" data-label-close="%s">%s</button>'
               % (t["nav_close"], t["nav_menu"]))
    out.append('  <div class="nav__links" id="nav-links" data-open="false">')
    for k, label in links:
        cur = ' aria-current="page"' if k == key else ""
        out.append('    <a class="nav__link" href="%s"%s>%s</a>' % (href(k, lang, lang), cur, label))
    if key != "contact":
        out.append('    <a class="btn btn--ghost-dark btn--sm" href="%s">%s</a>'
                   % (href("contact", lang, lang), t["nav_quote"]))
    out.append('    ' + lang_switch(key, lang))
    out.append('  </div>')
    out.append('</nav>')
    return "\n".join(out)


def footer_html(lang):
    t = UI[lang]
    services = "\n".join(
        '        <li><a href="%s#%s">%s</a></li>' % (href("services", lang, lang), f["slug"], f["kicker"])
        for f in FAMILIES[lang])
    legal = "\n".join(
        '        <a href="%s">%s</a>' % (href(k, lang, lang), LEGAL[lang][k]["nav"])
        for k in LEGAL_KEYS)
    return """<footer class="footer on-sumi">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <div class="footer__brand">
          <img src="{up}assets/img/logo-invert.svg" width="42" height="42" alt="">
          {wordmark}
        </div>
        <p class="footer__blurb">{blurb}</p>
        <p class="tagline" style="margin-top:22px">{tagline}</p>
      </div>
      <div>
        <h2 class="h4">{h_services}</h2>
        <ul>
{services}
          <li><a href="{services_href}">{all_services}</a></li>
        </ul>
      </div>
      <div>
        <h2 class="h4">{h_studio}</h2>
        <ul>
          <li>{s1}</li>
          <li>{s2}</li>
          <li>{s3}</li>
          <li>{s4}</li>
        </ul>
      </div>
      <div>
        <h2 class="h4">{h_contact}</h2>
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
      <nav aria-label="{legal_aria}">
{legal}
      </nav>
      <span>{by}</span>
      <span>{disclaimer}</span>
    </div>
  </div>
</footer>""".format(
        up=up(lang), wordmark=wordmark(dark=True, size=20), services=services, legal=legal,
        services_href=href("services", lang, lang),
        blurb=t["ft_blurb"], tagline=t["tagline"], h_services=t["ft_services"],
        all_services=t["ft_all"], h_studio=t["ft_studio"], h_contact=t["ft_contact"],
        s1=t["ft_s1"], s2=t["ft_s2"], s3=t["ft_s3"], s4=t["ft_s4"], zone=t["ft_zone"],
        legal_aria=t["ft_legal_aria"], by=t["ft_by"], disclaimer=t["ft_disclaimer"],
        **SITE)


def jsonld(lang):
    """Fiche entreprise + catalogue des 14 offres, dans la langue de la page."""
    cats = []
    for fam in FAMILIES[lang]:
        items = []
        for name, desc, price in fam["items"]:
            amount = re.sub(r"[^0-9]", "", price.split("/")[0])
            # Formatage par % : les accolades restent simples.
            items.append(
                '{"@type":"Offer","name":"%s","description":"%s","price":"%s",'
                '"priceCurrency":"EUR","valueAddedTaxIncluded":false,'
                '"availableAtOrFrom":{"@type":"AdministrativeArea","name":"Île-de-France"}}'
                % (name.replace('"', "'"), desc.replace('"', "'"), amount))
        cats.append('{"@type":"OfferCatalog","name":"%s","itemListElement":[%s]}'
                    % (fam["name"].replace("&amp;", "&"), ",".join(items)))
    knows = ",".join('"%s"' % k for k in LD_KNOWS[lang])
    return """{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": "{url}/#business",
  "name": "{name}",
  "description": "{desc}",
  "url": "{page_url}",
  "inLanguage": "{html_lang}",
  "telephone": "{tel}",
  "email": "{email}",
  "image": "{url}/assets/img/og-image.png",
  "logo": "{url}/assets/img/logo.svg",
  "priceRange": "290 € – 1 490 €",
  "areaServed": {{ "@type": "AdministrativeArea", "name": "Île-de-France" }},
  "address": {{ "@type": "PostalAddress", "addressRegion": "Île-de-France", "addressCountry": "FR" }},
  "knowsAbout": [{knows}],
  "hasOfferCatalog": {{
    "@type": "OfferCatalog",
    "name": "{catalog}",
    "itemListElement": [{cats}]
  }}
}}""".format(desc=LD_DESC[lang], html_lang=LANG_META[lang]["html"], knows=knows,
             catalog=UI[lang]["ft_all"], cats=",".join(cats),
             page_url=abs_url("home", lang), url=SITE["url"],
             name=SITE["name"], tel=SITE["tel"], email=SITE["email"])


def page(key, lang, body, transparent_nav=False):
    """Assemble une page complète, avec ses balises hreflang réciproques."""
    t = UI[lang]
    title, description = META[lang][key]
    meta = LANG_META[lang]
    # hreflang : chaque page déclare ses trois variantes + x-default (français).
    alts = "\n".join(
        '<link rel="alternate" hreflang="%s" href="%s">' % (LANG_META[o]["html"], abs_url(key, o))
        for o in LANGS)
    alts += '\n<link rel="alternate" hreflang="x-default" href="%s">' % abs_url(key, "fr")
    og_alts = "\n".join('<meta property="og:locale:alternate" content="%s">' % LANG_META[o]["og"]
                        for o in LANGS if o != lang)

    return """<!doctype html>
<html lang="{html_lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
{alts}
<meta name="author" content="{name}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#3C3489">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{name}">
<meta property="og:locale" content="{og}">
{og_alts}
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

<link rel="icon" href="{up}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{up}assets/img/logo.svg">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,700&family=Lato:ital,wght@0,300;0,400;0,700;1,400&family=Noto+Serif+JP:wght@400;500;700&display=swap">
<link rel="stylesheet" href="{up}assets/css/tokens.css">
<link rel="stylesheet" href="{up}assets/css/site.css">

<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>
<a class="skip-link" href="#contenu">{skip}</a>
{nav}
<main id="contenu">
{body}
</main>
{footer}
<script src="{up}assets/js/site.js" defer></script>
</body>
</html>
""".format(html_lang=LANG_META[lang]["html"], title=title, description=description,
           canonical=abs_url(key, lang), alts=alts, og=meta["og"], og_alts=og_alts,
           up=up(lang), jsonld=jsonld(lang), skip=t["skip"],
           nav=nav_html(key, lang, transparent_nav), body=body, footer=footer_html(lang),
           url=SITE["url"], name=SITE["name"])


def included_html(lang):
    return '<ul class="included">\n%s\n    </ul>' % "\n".join(
        "      <li>%s</li>" % x for x in INCLUDED[lang])


def contact_form(lang):
    """Bloc de devis. Les messages du script passent par des attributs data-,
    pour que site.js reste unique et sans chaîne de caractères en dur."""
    t = UI[lang]
    options = "\n".join("            <option>%s</option>" % o for o in t["prestations"])
    return """<div class="contactblock" id="devis">
      <div class="split">
        <div>
          <p class="eyebrow"><span class="ja">天</span> {eyebrow}</p>
          <h2 style="font-size:var(--fs-h3);margin-top:16px;letter-spacing:.04em">{h_a}<br><span class="italic-accent">{h_b}</span></h2>
          <p style="font-size:13px;color:var(--fg-2);margin-top:14px">{sub}</p>
          <p class="mono">
            <a href="tel:{tel_href}">{tel}</a><br>
            <a href="mailto:{email}">{email}</a><br>
            {zone}
          </p>
        </div>

        <!-- Endpoint : remplacez VOTRE_ID par votre identifiant Formspree (voir README).
             Tant qu'il n'est pas configuré, le formulaire bascule sur un mailto. -->
        <form class="form" id="devis-form" method="post" action="https://formspree.io/f/VOTRE_ID"
              data-msg-mailto="{js_mailto}" data-msg-sending="{js_sending}"
              data-msg-ok="{js_ok}" data-msg-error="{js_error}"
              data-subject="{js_subject}" data-to="{email}"
              data-l-name="{l_name}" data-l-email="{l_email}" data-l-phone="{l_phone}"
              data-l-type="{l_type}" data-l-deliverable="{l_deliverable}">
          <div class="field">
            <label for="nom">{f_name}</label>
            <input type="text" id="nom" name="nom" placeholder="{f_name_ph}" autocomplete="organization" required>
          </div>
          <div class="field">
            <label for="email">{f_email}</label>
            <input type="email" id="email" name="email" placeholder="{f_email_ph}" autocomplete="email" required>
          </div>
          <div class="field">
            <label for="telephone">{f_phone}</label>
            <input type="tel" id="telephone" name="telephone" placeholder="{f_phone_ph}" autocomplete="tel">
          </div>
          <div class="field">
            <label for="prestation">{f_type}</label>
            <select id="prestation" name="prestation">
{options}
            </select>
          </div>
          <div class="field field--full">
            <span class="field-label" id="livrable-label">{f_deliverable}</span>
            <div class="segmented" role="radiogroup" aria-labelledby="livrable-label">
              <input type="radio" id="liv-photo" name="livrable" value="{f_photo}">
              <label for="liv-photo">{f_photo}</label>
              <input type="radio" id="liv-video" name="livrable" value="{f_video}">
              <label for="liv-video">{f_video}</label>
              <input type="radio" id="liv-deux" name="livrable" value="{f_both}" checked>
              <label for="liv-deux">{f_both}</label>
            </div>
          </div>
          <div class="field field--full">
            <label for="message">{f_msg}</label>
            <textarea id="message" name="message" placeholder="{f_msg_ph}"></textarea>
          </div>
          <p class="form__note" id="form-status" role="status" aria-live="polite"></p>
          <div class="form__foot">
            <span class="tagline">{tagline}</span>
            <button class="btn btn--primary" type="submit">{f_submit}</button>
          </div>
        </form>
      </div>
    </div>""".format(
        options=options, eyebrow=t["form_eyebrow"], h_a=t["form_h_a"], h_b=t["form_h_b"],
        sub=t["form_sub"], zone=t["ft_zone"], tagline=t["tagline"],
        f_name=t["f_name"], f_name_ph=t["f_name_ph"], f_email=t["f_email"],
        f_email_ph=t["f_email_ph"], f_phone=t["f_phone"], f_phone_ph=t["f_phone_ph"],
        f_type=t["f_type"], f_deliverable=t["f_deliverable"], f_photo=t["f_photo"],
        f_video=t["f_video"], f_both=t["f_both"], f_msg=t["f_msg"], f_msg_ph=t["f_msg_ph"],
        f_submit=t["f_submit"], js_mailto=t["js_mailto"], js_sending=t["js_sending"],
        js_ok=t["js_ok"], js_error=t["js_error"], js_subject=t["js_subject"],
        l_name=t["js_l_name"], l_email=t["js_l_email"], l_phone=t["js_l_phone"],
        l_type=t["js_l_type"], l_deliverable=t["js_l_deliverable"],
        tel_href=SITE["tel_href"], tel=SITE["tel"], email=SITE["email"])


# ═══════════════════════════════════════════════════════════════════════════
# Pages
# ═══════════════════════════════════════════════════════════════════════════
def build_home(lang):
    t = UI[lang]
    srv = href("services", lang, lang)
    cards = []
    for fam in FAMILIES[lang]:
        cards.append("""        <a class="card" href="{srv}#{slug}">
          <div>
            <div class="card__num">{num}</div>
            <h3 class="card__title">{kicker} <span class="ja">{ja}</span></h3>
            <p class="card__desc">{desc}</p>
          </div>
          <div>
            <p class="card__price"><span>{from_}</span><strong>{price}</strong></p>
            <p class="card__more">{more}</p>
          </div>
        </a>""".format(srv=srv, price=min_price(fam), from_=t["from"], more=t["more"], **fam))

    plate = frame('<div class="hero__plate"><img src="%sassets/img/logo-invert.svg" alt="%s" '
                  'width="200" height="200"></div>' % (up(lang), t["logo_alt"]), big=True)
    plate = plate.replace('<div class="frame frame--lg">',
                          '<div class="frame frame--lg" style="align-self:stretch">')
    featured = frame('<img src="%sassets/img/logo-invert.svg" alt="" width="200" height="200">'
                     '<p class="featured__meta"><span>%s</span><span>%s</span></p>'
                     % (up(lang), t["feat_cat"], t["feat_dgac"]))

    body = """<header class="hero on-ink techgrid glow">
  <span class="hanko hanko--corner" aria-hidden="true">天</span>
  <div class="wrap">
    <div class="hero__grid">
      <div>
        <p class="hero__kicker">{hero_kicker} <span class="ja">映像</span></p>
        <h1>{hero_h1_a}<br><span class="italic-accent">{hero_h1_b}</span></h1>
        <p class="lead">{hero_lead}</p>
        <p class="btn-row">
          <a class="btn btn--seal" href="{contact}">{nav_quote}</a>
          <a class="btn btn--ghost-dark" href="{srv}">{nav_services}</a>
        </p>
      </div>
      {plate}
    </div>
    <div class="hero__rail">
      <span>{hero_edition}</span>
      <nav aria-label="{families_aria}">
{rail_links}
      </nav>
      <span>{hero_cert}</span>
    </div>
  </div>
</header>

<section class="section" aria-labelledby="familles">
  <div class="wrap">
    <div class="split" style="margin-bottom:56px">
      <p class="eyebrow"><span class="ja">一</span> {fam_eyebrow}</p>
      <div>
        <h2 id="familles" style="font-size:var(--fs-h1)">{fam_h2_a}
          <span class="italic-accent">{fam_h2_b}</span></h2>
        <p class="lead" style="margin-top:18px">{fam_lead}</p>
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
        <p class="eyebrow"><span class="ja">二</span> {feat_eyebrow}</p>
        <h2 id="phare" style="font-size:var(--fs-h1);margin-top:18px">{feat_h2_a}
          <span class="accent-dark">{feat_h2_b}</span></h2>
        <p class="ja" style="font-size:22px;color:var(--t-bamboo);margin-top:12px">{feat_ja}</p>
        <p class="lead" style="margin-top:22px">{feat_lead}</p>
        <dl class="specs">
          <div><dt class="caps">{spec_sensor}</dt><dd style="margin:0">8K · gimbal-3</dd></div>
          <div><dt class="caps">{spec_delivery}</dt><dd style="margin:0">{spec_days}</dd></div>
          <div><dt class="caps">{from_}</dt><dd style="margin:0">1 490 €</dd></div>
        </dl>
        <p class="btn-row"><a class="btn btn--ghost-dark" href="{srv}">{nav_services}</a></p>
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
      <p class="eyebrow"><span class="ja">三</span> {manifesto_eyebrow}</p>
      <div>
        <h2 id="manifeste" class="manifesto">{manifesto}</h2>
        <div class="manifesto__foot">
          <span class="tagline">{tagline}</span>
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
        <p class="eyebrow"><span class="ja">四</span> {incl_eyebrow}</p>
        <p style="font-size:12px;color:var(--fg-2);margin-top:8px">{incl_sub}</p>
      </div>
      <div>
        {incl_h2}
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
        cards="\n".join(cards), plate=plate, featured=featured,
        included=included_html(lang), form=contact_form(lang),
        incl_h2=sr_only(t["incl_h2"], "inclus"),
        contact=href("contact", lang, lang), srv=srv,
        families_aria=t["hero_families_aria"], from_=t["from"],
        rail_links="\n".join(
            '        <a href="%s#%s">%s</a>' % (srv, f["slug"], f["kicker"])
            for f in FAMILIES[lang]),
        **{k: t[k] for k in ("hero_kicker", "hero_h1_a", "hero_h1_b", "hero_lead",
                             "hero_edition", "hero_cert", "nav_quote", "nav_services",
                             "fam_eyebrow", "fam_h2_a", "fam_h2_b", "fam_lead",
                             "feat_eyebrow", "feat_h2_a", "feat_h2_b", "feat_ja", "feat_lead",
                             "spec_sensor", "spec_delivery", "spec_days",
                             "manifesto_eyebrow", "manifesto", "tagline",
                             "incl_eyebrow", "incl_sub")})
    return page("home", lang, body, transparent_nav=True)


def build_services(lang):
    t = UI[lang]
    groups = []
    for fam in FAMILIES[lang]:
        rows = "\n".join("""        <div class="pricerow">
          <div>
            <p class="pricerow__name">{name}</p>
            <p class="pricerow__desc">{desc}</p>
          </div>
          <p class="pricerow__price"><span class="caps">{from_}</span><strong>{price}</strong></p>
        </div>""".format(name=n, desc=d, price=p, from_=t["from"]) for n, d, p in fam["items"])
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

    terms = "\n".join('        <div><dt>%s</dt><dd>%s</dd></div>' % (a, b)
                      for a, b in CONDITIONS[lang])

    body = """<header class="pagehead on-ink techgrid glow">
  <span class="hanko hanko--corner" aria-hidden="true">天</span>
  <div class="wrap">
    <p class="hero__kicker"><span class="ja">値</span> {srv_eyebrow}</p>
    <h1>{srv_h1_a}<br><span class="italic-accent">{srv_h1_b}</span></h1>
    <p class="lead">{srv_lead}</p>
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
        <p class="eyebrow"><span class="ja">含</span> {incl_eyebrow}</p>
        <p style="font-size:12px;color:var(--t-bambou-200);margin-top:8px">{incl_sub}</p>
      </div>
      <div>
        {incl_h2}
        {included}
      </div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="conditions">
  <div class="wrap">
    <div class="split split--top">
      <div>
        <p class="eyebrow"><span class="ja">約</span> {cond_eyebrow}</p>
        <p style="font-size:12px;color:var(--fg-2);margin-top:8px">{cond_sub}</p>
      </div>
      <div>
        {cond_h2}
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
</section>""".format(
        groups="\n".join(groups), terms=terms, included=included_html(lang),
        form=contact_form(lang), incl_h2=sr_only(t["incl_h2"], "inclus"),
        cond_h2=sr_only(t["cond_h2"], "conditions"),
        **{k: t[k] for k in ("srv_eyebrow", "srv_h1_a", "srv_h1_b", "srv_lead",
                             "incl_eyebrow", "incl_sub", "cond_eyebrow", "cond_sub")})
    return page("services", lang, body)


def build_contact(lang):
    t = UI[lang]
    body = """<header class="pagehead on-ink techgrid glow">
  <span class="hanko hanko--corner" aria-hidden="true">天</span>
  <div class="wrap">
    <p class="hero__kicker"><span class="ja">天</span> {ct_eyebrow}</p>
    <h1>{ct_h1_a}<br><span class="italic-accent">{ct_h1_b}</span></h1>
    <p class="lead">{ct_lead}</p>
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
        <p class="eyebrow"><span class="ja">所</span> {ct_coord_eyebrow}</p>
      </div>
      <div>
        {coord_h2}
        <dl class="terms">
          <div><dt>{ct_phone}</dt><dd><a href="tel:{tel_href}" class="link-strong">{tel}</a></dd></div>
          <div><dt>{ct_email}</dt><dd><a href="mailto:{email}" class="link-strong">{email}</a></dd></div>
          <div><dt>{ct_zone}</dt><dd>{ct_zone_v}</dd></div>
          <div><dt>{ct_delay}</dt><dd>{ct_delay_v}</dd></div>
          <div><dt>{ct_reg}</dt><dd>{ct_reg_v}</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>""".format(
        form=contact_form(lang), coord_h2=sr_only(t["ct_coord_h2"], "coord"),
        tel_href=SITE["tel_href"], tel=SITE["tel"], email=SITE["email"],
        **{k: t[k] for k in ("ct_eyebrow", "ct_h1_a", "ct_h1_b", "ct_lead",
                             "ct_coord_eyebrow", "ct_phone", "ct_email", "ct_zone",
                             "ct_zone_v", "ct_delay", "ct_delay_v", "ct_reg", "ct_reg_v")})
    return page("contact", lang, body)


def build_legal(key, lang):
    t = UI[lang]
    doc = LEGAL[lang][key]
    sections = "\n".join(
        '        <div>\n          <h2>%s</h2>\n          <p>%s</p>\n        </div>'
        % (label, text.format(**SITE))
        for label, text in doc["sections"])

    # Encart de prévalence : uniquement sur les traductions, avec renvoi vers
    # le document français qui, lui, fait foi.
    prevail = ""
    if t["lg_prevail"]:
        prevail = ('      <p class="prevail">%s<br><a href="%s" hreflang="fr">%s: '
                   '<span lang="fr">%s</span></a></p>\n'
                   % (t["lg_prevail"], href(key, "fr", lang), t["lg_prevail_link"],
                      LEGAL["fr"][key]["nav"]))

    nav_items = "\n".join(
        '            <li><a href="%s"%s>%s</a></li>'
        % (href(k, lang, lang), ' aria-current="page"' if k == key else "", LEGAL[lang][k]["nav"])
        for k in LEGAL_KEYS)

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
        <p class="eyebrow"><span class="ja">条</span> {docs}</p>
        <nav aria-label="{nav_aria}">
          <ul>
{nav_items}
          </ul>
        </nav>
        <p class="legal-nav__date">{updated_label}{sep}{updated}</p>
      </div>
      <div>
{prevail}        <div class="legal-doc">
{sections}
        </div>
      </div>
    </div>
  </div>
</section>""".format(
        num=doc["num"], eyebrow=doc["eyebrow"], title=doc["title"], italic=doc["italic"],
        lead=doc["lead"], docs=t["lg_docs"], nav_aria=t["lg_nav_aria"],
        nav_items=nav_items, updated_label=t["lg_updated"], sep=t["lg_sep"], updated=t["lg_date"],
        prevail=prevail, sections=sections)
    return page(key, lang, body)


def build_404(lang):
    t = UI[lang]
    # GitHub Pages ne sert que le 404.html de la racine, quelle que soit l'URL
    # demandée : la version française porte donc un rappel dans les deux autres
    # langues, pour ne laisser personne sans porte de sortie.
    extra = ""
    if lang == "fr":
        extra = "\n".join(
            '      <p class="nf-alt" lang="%s"><span>%s</span> '
            '<a href="%s">%s</a></p>'
            % (LANG_META[o]["html"], UI[o]["nf_lead"].split(".")[0] + ".",
               href("home", o, "fr"), UI[o]["nf_home"])
            for o in LANGS if o != "fr")
        extra = '\n    <div class="nf-alts">\n%s\n    </div>' % extra

    body = """<header class="pagehead on-ink techgrid glow">
  <span class="hanko hanko--corner" aria-hidden="true">天</span>
  <div class="wrap">
    <p class="hero__kicker"><span class="ja">空</span> {nf_eyebrow}</p>
    <h1>{nf_h1_a}<br><span class="italic-accent">{nf_h1_b}</span></h1>
    <p class="lead">{nf_lead}</p>
    <p class="btn-row">
      <a class="btn btn--seal" href="{home}">{nf_home}</a>
      <a class="btn btn--ghost-dark" href="{srv}">{nav_services}</a>
    </p>{extra}
  </div>
</header>""".format(home=href("home", lang, lang), srv=href("services", lang, lang),
                    extra=extra,
                    **{k: t[k] for k in ("nf_eyebrow", "nf_h1_a", "nf_h1_b", "nf_lead",
                                         "nf_home", "nav_services")})
    return page("notfound", lang, body)


# ═══════════════════════════════════════════════════════════════════════════
# Écriture
# ═══════════════════════════════════════════════════════════════════════════
BUILDERS = {
    "home": build_home, "services": build_services, "contact": build_contact,
    "notfound": build_404,
}


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return len(content.encode("utf-8"))


def build_sitemap():
    """Un <url> par page et par langue, chacun déclarant ses variantes."""
    today = date.today().isoformat()
    prio = {"home": "1.0", "services": "0.9", "contact": "0.8"}
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for key in ["home", "services", "contact"] + LEGAL_KEYS:
        for lang in LANGS:
            out.append("  <url>")
            out.append("    <loc>%s</loc>" % abs_url(key, lang))
            for other in LANGS:
                out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
                           % (LANG_META[other]["html"], abs_url(key, other)))
            out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>'
                       % abs_url(key, "fr"))
            out.append("    <lastmod>%s</lastmod>" % today)
            out.append("    <changefreq>monthly</changefreq>")
            out.append("    <priority>%s</priority>" % prio.get(key, "0.4"))
            out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main():
    print("Génération de %s — %s" % (SITE["domain"], ", ".join(LANGS)))
    total = 0
    for lang in LANGS:
        print("\n  [%s]" % LANG_META[lang]["label"])
        for key in ["home", "services", "contact"] + LEGAL_KEYS + ["notfound"]:
            html = BUILDERS[key](lang) if key in BUILDERS else build_legal(key, lang)
            rel = LANG_META[lang]["dir"] + SLUGS[key][lang]
            n = write(rel, html)
            total += n
            print("    %-34s %6d o" % (rel, n))
    print()
    write("sitemap.xml", build_sitemap())
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE["url"])
    print("  sitemap.xml + robots.txt")
    print("\n  %d pages · %.0f Ko" % (len(LANGS) * 7, total / 1024))


if __name__ == "__main__":
    main()
