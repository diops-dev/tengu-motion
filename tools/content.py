#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contenu du site, dans les trois langues.

Ce fichier ne contient QUE des données : identité, prestations, tarifs,
libellés d'interface et documents légaux. La mise en page vit dans build.py.
Pour changer un prix ou une phrase, c'est ici — puis `python3 tools/build.py`.

Chaque dictionnaire est indexé par code de langue : "fr", "en", "es".
Le français est la version de référence ; les traductions en découlent.
"""

# ═══════════════════════════════════════════════════════════════════════════
# Identité — commune aux trois langues
# ═══════════════════════════════════════════════════════════════════════════
SITE = {
    "name":     "Tengu Motion & Drone",
    "domain":   "tengumotion.com",
    # URL réellement servie. À basculer sur https://www.tengumotion.com le jour
    # où le domaine est branché : elle alimente les balises canoniques, hreflang,
    # Open Graph et le sitemap. Une valeur fausse ici fait indexer un domaine mort.
    "url":      "https://diops-dev.github.io/tengu-motion",
    "tel":      "+33 6 33 59 87 74",
    "tel_href": "+33633598774",
    "email":    "video@tengumotion.com",
    "agency":   "Shorai Consulting",
    "updated":  "01/09/2026",
}

LANGS = ["fr", "en", "es"]

LANG_META = {
    "fr": {"label": "Français", "short": "FR", "html": "fr", "og": "fr_FR", "dir": ""},
    "en": {"label": "English",  "short": "EN", "html": "en", "og": "en_GB", "dir": "en/"},
    "es": {"label": "Español",  "short": "ES", "html": "es", "og": "es_ES", "dir": "es/"},
}

# Clé de page → nom de fichier, par langue. Les slugs sont traduits : un
# hispanophone qui voit /es/servicios.html comprend où il est, et les moteurs
# de recherche indexent des URL dans la bonne langue.
SLUGS = {
    "home":     {"fr": "index.html",            "en": "index.html",         "es": "index.html"},
    "services": {"fr": "services.html",         "en": "services.html",      "es": "servicios.html"},
    "contact":  {"fr": "contact.html",          "en": "contact.html",       "es": "contacto.html"},
    "legal":    {"fr": "mentions-legales.html", "en": "legal-notice.html",  "es": "aviso-legal.html"},
    "privacy":  {"fr": "confidentialite.html",  "en": "privacy-policy.html","es": "privacidad.html"},
    "terms":    {"fr": "cgv.html",              "en": "terms.html",         "es": "condiciones.html"},
    "notfound": {"fr": "404.html",              "en": "404.html",           "es": "404.html"},
}

LEGAL_KEYS = ["legal", "privacy", "terms"]

# ═══════════════════════════════════════════════════════════════════════════
# Prestations — grille tarifaire 2026
# Les prix sont identiques dans les trois langues ; seuls les libellés changent.
# ═══════════════════════════════════════════════════════════════════════════
FAMILIES = {
"fr": [
    {"slug": "image", "num": "壱", "ja": "映像",
     "kicker": "Image aérienne",
     "name": "Photographie & vidéo aérienne",
     "desc": "Immobilier, cinéma, corporate, promotion. Capteurs 4K/8K, stabilisation 3 axes, colorimétrie professionnelle.",
     "items": [
        ("Photo aérienne, demi-journée", "Reportage photo, jusqu'à 3 h sur site, sélection retouchée.", "450 €"),
        ("Journée photo / vidéo complète", "Captation aérienne + sol sur la journée, montage livré.", "1 250 €"),
        ("Pack immobilier, aérien + sol 8K", "Bien résidentiel ou luxe, photos + vidéo de présentation.", "350 €"),
        ("Corporate / inauguration outdoor", "Film d'entreprise, événement, tournage extérieur.", "600 €"),
        ("Clip FPV promotionnel", "Vidéo dynamique immersive, montage rythmé.", "550 €"),
        ("Film promotionnel 8K ultra", "Marque, collectivité, campagne, production haut de gamme.", "1 490 €"),
     ]},
    {"slug": "evenementiel", "num": "弐", "ja": "祭り",
     "kicker": "Mariage & événementiel",
     "name": "Mariage & événementiel",
     "desc": "Mariages, concerts, compétitions, événements corporate.",
     "items": [
        ("Mariage FPV, drone seul", "Couverture aérienne seule, film souvenir monté.", "750 €"),
        ("Mariage FPV + sol 8K", "Aérien + plans sol cinéma 8K, montage complet.", "950 €"),
        ("Événementiel, captation 4 h", "Salon, séminaire, inauguration, événement public.", "990 €"),
        ("Making-of / événement indoor", "Coulisses, événement B2B, salon en intérieur.", "400 €"),
     ]},
    {"slug": "studio", "num": "参", "ja": "室内",
     "kicker": "Studio & indoor",
     "name": "Studio & indoor, image 8K",
     "desc": "Tournage par tous temps et en intérieur : la continuité de production, hiver comme été.",
     "items": [
        ("Interview / portrait dirigeant", "Captation studio ou sur site, lumière soignée.", "350 €"),
        ("Vidéo produit / e-commerce", "Mise en valeur produit, plans détail 8K.", "290 € / produit"),
        ("Drone indoor : halls, concerts, sport", "Vol en intérieur, gymnases, salles, industrie.", "490 €"),
        ("Pack contenus réseaux, 5 vidéos", "Formats courts prêts à publier, fidélisation.", "390 €"),
     ]},
],
"en": [
    {"slug": "image", "num": "壱", "ja": "映像",
     "kicker": "Aerial imaging",
     "name": "Aerial photography & video",
     "desc": "Real estate, film, corporate, promotion. 4K/8K sensors, 3-axis stabilisation, professional colour grading.",
     "items": [
        ("Aerial photography, half-day", "Photo shoot, up to 3 h on site, retouched selection.", "450 €"),
        ("Full day, photo and video", "Aerial and ground capture across the day, edit delivered.", "1 250 €"),
        ("Real-estate pack, aerial + 8K ground", "Residential or luxury property, photos plus a presentation film.", "350 €"),
        ("Corporate / outdoor opening", "Company film, event, outdoor shoot.", "600 €"),
        ("FPV promotional clip", "Immersive, fast-moving video with a tightly cut edit.", "550 €"),
        ("8K ultra promotional film", "Brand, public body, campaign — high-end production.", "1 490 €"),
     ]},
    {"slug": "evenementiel", "num": "弐", "ja": "祭り",
     "kicker": "Weddings & events",
     "name": "Weddings & events",
     "desc": "Weddings, concerts, competitions, corporate events.",
     "items": [
        ("FPV wedding, drone only", "Aerial coverage alone, edited keepsake film.", "750 €"),
        ("FPV wedding + 8K ground", "Aerial plus 8K cinematic ground shots, full edit.", "950 €"),
        ("Events, 4-hour coverage", "Trade show, seminar, opening, public event.", "990 €"),
        ("Making-of / indoor event", "Behind the scenes, B2B event, indoor trade show.", "400 €"),
     ]},
    {"slug": "studio", "num": "参", "ja": "室内",
     "kicker": "Studio & indoor",
     "name": "Studio & indoor, 8K imaging",
     "desc": "Shooting indoors and in any weather: production continuity, winter and summer alike.",
     "items": [
        ("Interview / executive portrait", "Studio or on-site capture, carefully lit.", "350 €"),
        ("Product / e-commerce video", "Product showcase with 8K detail shots.", "290 € / product"),
        ("Indoor drone: halls, concerts, sport", "Indoor flight — gyms, venues, industrial sites.", "490 €"),
        ("Social content pack, 5 videos", "Short-form, ready to publish, built for retention.", "390 €"),
     ]},
],
"es": [
    {"slug": "image", "num": "壱", "ja": "映像",
     "kicker": "Imagen aérea",
     "name": "Fotografía y vídeo aéreos",
     "desc": "Inmobiliario, cine, corporativo, promoción. Sensores 4K/8K, estabilización de 3 ejes, etalonaje profesional.",
     "items": [
        ("Fotografía aérea, media jornada", "Reportaje fotográfico, hasta 3 h en el lugar, selección retocada.", "450 €"),
        ("Jornada completa, foto y vídeo", "Captación aérea y terrestre durante la jornada, montaje entregado.", "1 250 €"),
        ("Pack inmobiliario, aéreo + suelo 8K", "Vivienda residencial o de lujo, fotos y vídeo de presentación.", "350 €"),
        ("Corporativo / inauguración exterior", "Vídeo de empresa, evento, rodaje en exteriores.", "600 €"),
        ("Clip FPV promocional", "Vídeo inmersivo y dinámico, montaje rítmico.", "550 €"),
        ("Película promocional 8K ultra", "Marca, administración, campaña — producción de alta gama.", "1 490 €"),
     ]},
    {"slug": "evenementiel", "num": "弐", "ja": "祭り",
     "kicker": "Bodas y eventos",
     "name": "Bodas y eventos",
     "desc": "Bodas, conciertos, competiciones, eventos corporativos.",
     "items": [
        ("Boda FPV, solo dron", "Cobertura aérea únicamente, película recuerdo montada.", "750 €"),
        ("Boda FPV + suelo 8K", "Aéreo más planos de suelo cine 8K, montaje completo.", "950 €"),
        ("Eventos, captación de 4 h", "Feria, seminario, inauguración, evento público.", "990 €"),
        ("Making-of / evento en interior", "Entre bastidores, evento B2B, feria en interior.", "400 €"),
     ]},
    {"slug": "studio", "num": "参", "ja": "室内",
     "kicker": "Estudio e interior",
     "name": "Estudio e interior, imagen 8K",
     "desc": "Rodaje en interiores y con cualquier tiempo: continuidad de producción, en invierno como en verano.",
     "items": [
        ("Entrevista / retrato de directivo", "Captación en estudio o in situ, iluminación cuidada.", "350 €"),
        ("Vídeo de producto / e-commerce", "Puesta en valor del producto, planos de detalle en 8K.", "290 € / producto"),
        ("Dron en interior: naves, conciertos, deporte", "Vuelo en interior: gimnasios, salas, industria.", "490 €"),
        ("Pack de contenidos para redes, 5 vídeos", "Formatos cortos listos para publicar, orientados a fidelizar.", "390 €"),
     ]},
],
}

INCLUDED = {
"fr": [
    "Brief préalable et plan de vol personnalisé",
    "Livrables sous J+3 à J+7 selon la complexité",
    "Opérateur certifié DGAC + drone adapté à la mission",
    "Rapport d'intervention + fichiers bruts sur demande",
    "Assurance RC mission incluse, aucune surprise",
    "Support technique pendant 7 jours après livraison",
],
"en": [
    "Preliminary brief and tailored flight plan",
    "Delivery in 3 to 7 days depending on complexity",
    "DGAC-certified operator and a drone matched to the mission",
    "Operation report and raw files on request",
    "Mission liability insurance included, no surprises",
    "Technical support for 7 days after delivery",
],
"es": [
    "Briefing previo y plan de vuelo personalizado",
    "Entrega en 3 a 7 días según la complejidad",
    "Operador certificado por la DGAC y dron adaptado a la misión",
    "Informe de intervención y archivos en bruto a petición",
    "Seguro de responsabilidad civil incluido, sin sorpresas",
    "Soporte técnico durante 7 días tras la entrega",
],
}

CONDITIONS = {
"fr": [
    ("Tarifs", "Prix indicatifs HT, hors options. Chaque devis est personnalisé selon la complexité, la zone et les livrables."),
    ("Zone d'intervention", "Île-de-France. Frais de déplacement au réel pour toute mission hors Île-de-France."),
    ("Devis & validité", "Devis gratuit sous 24 h. Proposition valable 30 jours à compter de son émission."),
    ("Réservation", "Acompte de 30 % à la commande, solde à la livraison. Créneau confirmé après acompte."),
    ("Météo", "Report sans frais en cas de conditions de vol non conformes (vent, pluie, zone réglementée)."),
    ("Cadre légal", "Opérations en catégorie Specific, conformes aux règlements UE 2019/945 et 2019/947. Assurance RC pro (UE 785/2004)."),
],
"en": [
    ("Pricing", "Indicative prices excluding VAT and options. Every quote is tailored to complexity, location and deliverables."),
    ("Service area", "Île-de-France. Travel charged at cost for any assignment outside the region."),
    ("Quotes & validity", "Free quote within 24 hours, valid for 30 days from the date of issue."),
    ("Booking", "30 % deposit on order, balance on delivery. The slot is confirmed once the deposit is received."),
    ("Weather", "Free rescheduling if flight conditions are unsuitable (wind, rain, restricted airspace)."),
    ("Legal framework", "Operations in the Specific category, compliant with EU regulations 2019/945 and 2019/947. Professional liability insurance (EU 785/2004)."),
],
"es": [
    ("Tarifas", "Precios indicativos sin IVA y sin opciones. Cada presupuesto se adapta a la complejidad, la zona y los entregables."),
    ("Zona de intervención", "Île-de-France. Gastos de desplazamiento a coste real fuera de la región."),
    ("Presupuesto y validez", "Presupuesto gratuito en 24 h, válido 30 días desde su emisión."),
    ("Reserva", "Anticipo del 30 % al encargar, resto a la entrega. La fecha se confirma tras recibir el anticipo."),
    ("Meteorología", "Aplazamiento sin coste si las condiciones de vuelo no son aptas (viento, lluvia, zona restringida)."),
    ("Marco legal", "Operaciones en categoría Specific, conformes a los reglamentos UE 2019/945 y 2019/947. Seguro de RC profesional (UE 785/2004)."),
],
}

# ═══════════════════════════════════════════════════════════════════════════
# Libellés d'interface et textes de pages
# ═══════════════════════════════════════════════════════════════════════════
UI = {
"fr": {
    # Navigation
    "nav_home": "Accueil", "nav_services": "Services & tarifs", "nav_contact": "Contact",
    "nav_quote": "Demander un devis", "nav_menu": "Menu", "nav_close": "Fermer",
    "nav_aria": "Navigation principale", "lang_aria": "Choix de la langue",
    "skip": "Aller au contenu",

    # Hero
    "hero_kicker": "Vidéo · Vidéo par drone · Photographie",
    "hero_h1_a": "La précision", "hero_h1_b": "est un rituel.",
    "hero_lead": "Des opérations aériennes sur mesure pour les professionnels qui refusent "
                 "l'approximation. De l'image à la donnée, chaque prestation est conduite avec "
                 "la même rigueur opérationnelle.",
    "hero_edition": "Édition 2026 · MMXXVI",
    "hero_cert": "Certifié DGAC · Île-de-France",
    "hero_families_aria": "Familles de prestations",
    "logo_alt": "Emblème Ha-Uchiwa de Tengu Motion & Drone",

    # Accueil — familles
    "fam_eyebrow": "Trois familles",
    "fam_h2_a": "L'image aérienne,", "fam_h2_b": "conduite comme une opération.",
    "fam_lead": "Vidéo, vidéo par drone et photographie : mariage et événementiel, studio et "
                "indoor. Quatorze prestations, une seule discipline.",
    "from": "Dès", "more": "En savoir plus",

    # Accueil — production phare
    "feat_eyebrow": "Production haut de gamme",
    "feat_h2_a": "Film promotionnel", "feat_h2_b": "8K ultra",
    "feat_ja": "映像 · Marque, collectivité, campagne",
    "feat_lead": "Captation aérienne et sol, stabilisation trois axes, colorimétrie "
                 "professionnelle. Repérage, plan de vol, montage : une production menée de "
                 "bout en bout.",
    "spec_sensor": "Capteur", "spec_delivery": "Livraison", "spec_days": "J+3 à J+7",
    "feat_cat": "Catégorie Specific", "feat_dgac": "Certifié DGAC",

    # Accueil — manifeste et inclus
    "manifesto_eyebrow": "Manifeste",
    "manifesto": "« La précision est un rituel. »",
    "tagline": "Precision&nbsp;is&nbsp;a&nbsp;ritual",
    "incl_eyebrow": "Inclus",
    "incl_sub": "Ce que comprend chaque prestation.",
    "incl_h2": "Inclus dans chaque prestation",

    # Formulaire
    "form_eyebrow": "Prenons contact",
    "form_h_a": "Parlons de", "form_h_b": "votre mission.",
    "form_sub": "Devis personnalisé, gratuit sous 24 h.",
    "f_name": "Nom", "f_name_ph": "Nom et société",
    "f_email": "Email", "f_email_ph": "contact@societe.fr",
    "f_phone": "Téléphone", "f_phone_ph": "06 00 00 00 00",
    "f_type": "Type de prestation", "f_deliverable": "Livrable",
    "f_photo": "Photo", "f_video": "Vidéo", "f_both": "Les deux",
    "f_msg": "Votre mission",
    "f_msg_ph": "Lieu, date souhaitée, durée, livrables attendus.",
    "f_submit": "Demander un devis",
    # Messages du script — repris par site.js via des attributs data-
    "js_mailto": "Votre logiciel de messagerie s'ouvre avec la demande pré-remplie.",
    "js_sending": "Envoi en cours…",
    "js_ok": "Demande reçue. Devis personnalisé sous 24 h, avec plan de vol et fenêtres de tournage.",
    "js_error": "L'envoi a échoué. Écrivez-nous à video@tengumotion.com ou appelez le +33 6 33 59 87 74.",
    "js_subject": "Demande de devis",
    "js_l_name": "Nom / société", "js_l_email": "Email", "js_l_phone": "Téléphone",
    "js_l_type": "Prestation", "js_l_deliverable": "Livrable",
    "prestations": ["Photo / vidéo aérienne", "Pack immobilier", "Corporate / inauguration",
                    "Clip FPV promotionnel", "Mariage", "Événementiel",
                    "Studio & indoor", "Contenus réseaux"],

    # Page services
    "srv_eyebrow": "Services & tarifs · MMXXVI",
    "srv_h1_a": "Vidéo, vidéo par drone,", "srv_h1_b": "photographie.",
    "srv_lead": "Trois familles de prestations, quatorze formules. Prix indicatifs HT, devis "
                "gratuit sous 24 h, valable 30 jours à compter de son émission.",
    "cond_eyebrow": "Conditions", "cond_sub": "Le cadre de chaque mission.",
    "cond_h2": "Conditions générales",

    # Page contact
    "ct_eyebrow": "Prenons contact",
    "ct_h1_a": "Parlons de", "ct_h1_b": "votre mission.",
    "ct_lead": "Décrivez le lieu, la date et les livrables attendus : vous recevez un devis "
               "personnalisé sous 24 h, avec plan de vol et fenêtres de tournage.",
    "ct_coord_eyebrow": "Coordonnées", "ct_coord_h2": "Coordonnées",
    "ct_phone": "Téléphone", "ct_email": "Email",
    "ct_zone": "Zone d'intervention",
    "ct_zone_v": "Île-de-France. Frais de déplacement au réel pour toute mission hors Île-de-France.",
    "ct_delay": "Délai de réponse",
    "ct_delay_v": "Devis gratuit sous 24 h, valable 30 jours à compter de son émission.",
    "ct_reg": "Cadre réglementaire",
    "ct_reg_v": "Opérateur certifié DGAC, catégorie Specific (règl. UE 2019/945 et 2019/947). "
                "Assurance RC professionnelle (règl. UE 785/2004).",

    # Pied de page
    "ft_blurb": "Vidéo, vidéo par drone et photographie en Île-de-France. Immobilier, "
                "corporate, mariage, événementiel, studio et indoor.",
    "ft_services": "Services", "ft_studio": "Studio", "ft_contact": "Contact",
    "ft_all": "Services & tarifs 2026",
    "ft_s1": "Opérateurs certifiés DGAC", "ft_s2": "Catégorie Specific",
    "ft_s3": "Assurance RC professionnelle", "ft_s4": "Livrables J+3 à J+7",
    "ft_zone": "Île-de-France",
    "ft_legal_aria": "Informations légales",
    "ft_by": "Site réalisé par Shorai Consulting",
    "ft_disclaimer": "Tarifs indicatifs HT · Document non contractuel",

    # 404
    "nf_eyebrow": "Erreur 404",
    "nf_h1_a": "Cette page", "nf_h1_b": "n'existe pas.",
    "nf_lead": "Le lien est peut-être obsolète. Reprenez depuis l'accueil, ou consultez "
               "directement la grille tarifaire 2026.",
    "nf_home": "Retour à l'accueil",

    # Documents légaux
    "lg_docs": "Documents", "lg_updated": "Mise à jour",
    "lg_sep": "&nbsp;: ", "lg_date": "01/09/2026",
    "lg_nav_aria": "Documents légaux",
    "lg_prevail": "",   # vide en français : c'est la version de référence
    "lg_prevail_link": "",
},

"en": {
    "nav_home": "Home", "nav_services": "Services & pricing", "nav_contact": "Contact",
    "nav_quote": "Request a quote", "nav_menu": "Menu", "nav_close": "Close",
    "nav_aria": "Main navigation", "lang_aria": "Language selection",
    "skip": "Skip to content",

    "hero_kicker": "Video · Drone video · Photography",
    "hero_h1_a": "Precision", "hero_h1_b": "is a ritual.",
    "hero_lead": "Bespoke aerial operations for professionals who refuse to settle for "
                 "approximate. From image to data, every assignment is run with the same "
                 "operational rigour.",
    "hero_edition": "2026 edition · MMXXVI",
    "hero_cert": "DGAC certified · Île-de-France",
    "hero_families_aria": "Service families",
    "logo_alt": "Ha-Uchiwa emblem of Tengu Motion & Drone",

    "fam_eyebrow": "Three families",
    "fam_h2_a": "Aerial imaging,", "fam_h2_b": "run like an operation.",
    "fam_lead": "Video, drone video and photography: weddings and events, studio and indoor. "
                "Fourteen services, one discipline.",
    "from": "From", "more": "Learn more",

    "feat_eyebrow": "High-end production",
    "feat_h2_a": "Promotional film", "feat_h2_b": "8K ultra",
    "feat_ja": "映像 · Brand, public body, campaign",
    "feat_lead": "Aerial and ground capture, three-axis stabilisation, professional colour "
                 "grading. Location scouting, flight plan, edit — a production run end to end.",
    "spec_sensor": "Sensor", "spec_delivery": "Delivery", "spec_days": "3 to 7 days",
    "feat_cat": "Specific category", "feat_dgac": "DGAC certified",

    "manifesto_eyebrow": "Manifesto",
    "manifesto": "“Precision is a ritual.”",
    "tagline": "Precision&nbsp;is&nbsp;a&nbsp;ritual",
    "incl_eyebrow": "Included",
    "incl_sub": "What every assignment covers.",
    "incl_h2": "Included in every assignment",

    "form_eyebrow": "Get in touch",
    "form_h_a": "Let's talk about", "form_h_b": "your project.",
    "form_sub": "Tailored quote, free within 24 hours.",
    "f_name": "Name", "f_name_ph": "Name and company",
    "f_email": "Email", "f_email_ph": "contact@company.com",
    "f_phone": "Phone", "f_phone_ph": "+33 6 00 00 00 00",
    "f_type": "Type of service", "f_deliverable": "Deliverable",
    "f_photo": "Photo", "f_video": "Video", "f_both": "Both",
    "f_msg": "Your project",
    "f_msg_ph": "Location, preferred date, duration, expected deliverables.",
    "f_submit": "Request a quote",
    "js_mailto": "Your email client is opening with the request pre-filled.",
    "js_sending": "Sending…",
    "js_ok": "Request received. A tailored quote within 24 hours, with a flight plan and shooting windows.",
    "js_error": "Sending failed. Write to video@tengumotion.com or call +33 6 33 59 87 74.",
    "js_subject": "Quote request",
    "js_l_name": "Name / company", "js_l_email": "Email", "js_l_phone": "Phone",
    "js_l_type": "Service", "js_l_deliverable": "Deliverable",
    "prestations": ["Aerial photo / video", "Real-estate pack", "Corporate / opening",
                    "FPV promotional clip", "Wedding", "Events",
                    "Studio & indoor", "Social content"],

    "srv_eyebrow": "Services & pricing · MMXXVI",
    "srv_h1_a": "Video, drone video,", "srv_h1_b": "photography.",
    "srv_lead": "Three families of services, fourteen packages. Indicative prices excluding "
                "VAT; free quote within 24 hours, valid for 30 days from the date of issue.",
    "cond_eyebrow": "Terms", "cond_sub": "The framework for every assignment.",
    "cond_h2": "General terms",

    "ct_eyebrow": "Get in touch",
    "ct_h1_a": "Let's talk about", "ct_h1_b": "your project.",
    "ct_lead": "Tell us the location, the date and the deliverables you need: you receive a "
               "tailored quote within 24 hours, with a flight plan and shooting windows.",
    "ct_coord_eyebrow": "Contact details", "ct_coord_h2": "Contact details",
    "ct_phone": "Phone", "ct_email": "Email",
    "ct_zone": "Service area",
    "ct_zone_v": "Île-de-France. Travel charged at cost for any assignment outside the region.",
    "ct_delay": "Response time",
    "ct_delay_v": "Free quote within 24 hours, valid for 30 days from the date of issue.",
    "ct_reg": "Regulatory framework",
    "ct_reg_v": "DGAC-certified operator, Specific category (EU reg. 2019/945 and 2019/947). "
                "Professional liability insurance (EU reg. 785/2004).",

    "ft_blurb": "Video, drone video and photography across the Île-de-France region. Real "
                "estate, corporate, weddings, events, studio and indoor.",
    "ft_services": "Services", "ft_studio": "Studio", "ft_contact": "Contact",
    "ft_all": "Services & pricing 2026",
    "ft_s1": "DGAC-certified operators", "ft_s2": "Specific category",
    "ft_s3": "Professional liability insurance", "ft_s4": "Delivery in 3 to 7 days",
    "ft_zone": "Île-de-France, France",
    "ft_legal_aria": "Legal information",
    "ft_by": "Site by Shorai Consulting",
    "ft_disclaimer": "Indicative prices excl. VAT · Non-contractual document",

    "nf_eyebrow": "Error 404",
    "nf_h1_a": "This page", "nf_h1_b": "does not exist.",
    "nf_lead": "The link may be out of date. Start again from the home page, or go straight "
               "to the 2026 price list.",
    "nf_home": "Back to home",

    "lg_docs": "Documents", "lg_updated": "Last updated",
    "lg_sep": ": ", "lg_date": "1 September 2026",
    "lg_nav_aria": "Legal documents",
    "lg_prevail": "Courtesy translation. Only the French version of this document has legal "
                  "force; in the event of any discrepancy, the French text prevails.",
    "lg_prevail_link": "Read the French version",
},

"es": {
    "nav_home": "Inicio", "nav_services": "Servicios y tarifas", "nav_contact": "Contacto",
    "nav_quote": "Solicitar presupuesto", "nav_menu": "Menú", "nav_close": "Cerrar",
    "nav_aria": "Navegación principal", "lang_aria": "Selección de idioma",
    "skip": "Ir al contenido",

    "hero_kicker": "Vídeo · Vídeo con dron · Fotografía",
    "hero_h1_a": "La precisión", "hero_h1_b": "es un ritual.",
    "hero_lead": "Operaciones aéreas a medida para profesionales que no se conforman con la "
                 "aproximación. De la imagen al dato, cada encargo se ejecuta con el mismo "
                 "rigor operativo.",
    "hero_edition": "Edición 2026 · MMXXVI",
    "hero_cert": "Certificado DGAC · Île-de-France",
    "hero_families_aria": "Familias de servicios",
    "logo_alt": "Emblema Ha-Uchiwa de Tengu Motion & Drone",

    "fam_eyebrow": "Tres familias",
    "fam_h2_a": "La imagen aérea,", "fam_h2_b": "dirigida como una operación.",
    "fam_lead": "Vídeo, vídeo con dron y fotografía: bodas y eventos, estudio e interior. "
                "Catorce servicios, una sola disciplina.",
    "from": "Desde", "more": "Saber más",

    "feat_eyebrow": "Producción de alta gama",
    "feat_h2_a": "Película promocional", "feat_h2_b": "8K ultra",
    "feat_ja": "映像 · Marca, administración, campaña",
    "feat_lead": "Captación aérea y terrestre, estabilización de tres ejes, etalonaje "
                 "profesional. Localización, plan de vuelo, montaje: una producción de "
                 "principio a fin.",
    "spec_sensor": "Sensor", "spec_delivery": "Entrega", "spec_days": "3 a 7 días",
    "feat_cat": "Categoría Specific", "feat_dgac": "Certificado DGAC",

    "manifesto_eyebrow": "Manifiesto",
    "manifesto": "«La precisión es un ritual.»",
    "tagline": "Precision&nbsp;is&nbsp;a&nbsp;ritual",
    "incl_eyebrow": "Incluido",
    "incl_sub": "Lo que comprende cada servicio.",
    "incl_h2": "Incluido en cada servicio",

    "form_eyebrow": "Hablemos",
    "form_h_a": "Hablemos de", "form_h_b": "su proyecto.",
    "form_sub": "Presupuesto personalizado y gratuito en 24 h.",
    "f_name": "Nombre", "f_name_ph": "Nombre y empresa",
    "f_email": "Email", "f_email_ph": "contacto@empresa.es",
    "f_phone": "Teléfono", "f_phone_ph": "+33 6 00 00 00 00",
    "f_type": "Tipo de servicio", "f_deliverable": "Entregable",
    "f_photo": "Foto", "f_video": "Vídeo", "f_both": "Ambos",
    "f_msg": "Su proyecto",
    "f_msg_ph": "Lugar, fecha deseada, duración, entregables previstos.",
    "f_submit": "Solicitar presupuesto",
    "js_mailto": "Su gestor de correo se abre con la solicitud rellenada.",
    "js_sending": "Enviando…",
    "js_ok": "Solicitud recibida. Presupuesto personalizado en 24 h, con plan de vuelo y ventanas de rodaje.",
    "js_error": "El envío ha fallado. Escríbanos a video@tengumotion.com o llame al +33 6 33 59 87 74.",
    "js_subject": "Solicitud de presupuesto",
    "js_l_name": "Nombre / empresa", "js_l_email": "Email", "js_l_phone": "Teléfono",
    "js_l_type": "Servicio", "js_l_deliverable": "Entregable",
    "prestations": ["Foto / vídeo aéreo", "Pack inmobiliario", "Corporativo / inauguración",
                    "Clip FPV promocional", "Boda", "Eventos",
                    "Estudio e interior", "Contenidos para redes"],

    "srv_eyebrow": "Servicios y tarifas · MMXXVI",
    "srv_h1_a": "Vídeo, vídeo con dron,", "srv_h1_b": "fotografía.",
    "srv_lead": "Tres familias de servicios, catorce fórmulas. Precios indicativos sin IVA; "
                "presupuesto gratuito en 24 h, válido 30 días desde su emisión.",
    "cond_eyebrow": "Condiciones", "cond_sub": "El marco de cada encargo.",
    "cond_h2": "Condiciones generales",

    "ct_eyebrow": "Hablemos",
    "ct_h1_a": "Hablemos de", "ct_h1_b": "su proyecto.",
    "ct_lead": "Indíquenos el lugar, la fecha y los entregables previstos: recibirá un "
               "presupuesto personalizado en 24 h, con plan de vuelo y ventanas de rodaje.",
    "ct_coord_eyebrow": "Datos de contacto", "ct_coord_h2": "Datos de contacto",
    "ct_phone": "Teléfono", "ct_email": "Email",
    "ct_zone": "Zona de intervención",
    "ct_zone_v": "Île-de-France. Gastos de desplazamiento a coste real fuera de la región.",
    "ct_delay": "Plazo de respuesta",
    "ct_delay_v": "Presupuesto gratuito en 24 h, válido 30 días desde su emisión.",
    "ct_reg": "Marco normativo",
    "ct_reg_v": "Operador certificado por la DGAC, categoría Specific (regl. UE 2019/945 y "
                "2019/947). Seguro de responsabilidad civil profesional (regl. UE 785/2004).",

    "ft_blurb": "Vídeo, vídeo con dron y fotografía en la región de Île-de-France. "
                "Inmobiliario, corporativo, bodas, eventos, estudio e interior.",
    "ft_services": "Servicios", "ft_studio": "Estudio", "ft_contact": "Contacto",
    "ft_all": "Servicios y tarifas 2026",
    "ft_s1": "Operadores certificados DGAC", "ft_s2": "Categoría Specific",
    "ft_s3": "Seguro de RC profesional", "ft_s4": "Entrega en 3 a 7 días",
    "ft_zone": "Île-de-France, Francia",
    "ft_legal_aria": "Información legal",
    "ft_by": "Sitio realizado por Shorai Consulting",
    "ft_disclaimer": "Precios indicativos sin IVA · Documento no contractual",

    "nf_eyebrow": "Error 404",
    "nf_h1_a": "Esta página", "nf_h1_b": "no existe.",
    "nf_lead": "Puede que el enlace esté obsoleto. Vuelva al inicio o consulte directamente "
               "las tarifas 2026.",
    "nf_home": "Volver al inicio",

    "lg_docs": "Documentos", "lg_updated": "Actualización",
    "lg_sep": ": ", "lg_date": "1 de septiembre de 2026",
    "lg_nav_aria": "Documentos legales",
    "lg_prevail": "Traducción de cortesía. Solo la versión francesa de este documento tiene "
                  "valor legal; en caso de discrepancia, prevalece el texto francés.",
    "lg_prevail_link": "Leer la versión francesa",
},
}

# Métadonnées SEO par page et par langue : (titre, description)
META = {
"fr": {
  "home": ("Tengu Motion & Drone — Vidéo, drone et photographie en Île-de-France",
           "Vidéo, vidéo par drone et photographie professionnelle en Île-de-France : immobilier, corporate, mariage, événementiel, studio et indoor. Opérateur certifié DGAC, devis gratuit sous 24 h."),
  "services": ("Services & tarifs 2026 — Tengu Motion & Drone",
           "Grille tarifaire 2026 : 14 prestations vidéo, drone et photo en Île-de-France. Pack immobilier dès 350 €, mariage dès 750 €, film 8K dès 1 490 €. Devis gratuit sous 24 h."),
  "contact": ("Contact & devis — Tengu Motion & Drone",
           "Demandez un devis gratuit sous 24 h pour une prestation vidéo, drone ou photo en Île-de-France. Téléphone +33 6 33 59 87 74 — video@tengumotion.com."),
  "legal": ("Mentions légales — Tengu Motion & Drone",
           "Mentions légales de Tengu Motion & Drone : éditeur, hébergement, propriété intellectuelle, médiation de la consommation."),
  "privacy": ("Confidentialité — Tengu Motion & Drone",
           "Politique de confidentialité de Tengu Motion & Drone : données collectées, finalités, durées de conservation, droit à l'image et exercice de vos droits RGPD."),
  "terms": ("CGV — Tengu Motion & Drone",
           "Conditions générales de vente de Tengu Motion & Drone : devis, réservation, report météo, livrables, droits d'utilisation des images."),
  "notfound": ("Page introuvable — Tengu Motion & Drone",
           "La page demandée n'existe pas. Retour à l'accueil de Tengu Motion & Drone."),
},
"en": {
  "home": ("Tengu Motion & Drone — Video, drone and photography near Paris",
           "Professional video, drone video and photography in the Île-de-France region: real estate, corporate, weddings, events, studio and indoor. DGAC-certified operator, free quote within 24 hours."),
  "services": ("Services & pricing 2026 — Tengu Motion & Drone",
           "2026 price list: 14 video, drone and photography services in the Paris region. Real-estate pack from €350, weddings from €750, 8K film from €1,490. Free quote within 24 hours."),
  "contact": ("Contact & quotes — Tengu Motion & Drone",
           "Request a free quote within 24 hours for video, drone or photography work in the Paris region. Phone +33 6 33 59 87 74 — video@tengumotion.com."),
  "legal": ("Legal notice — Tengu Motion & Drone",
           "Legal notice for Tengu Motion & Drone: publisher, hosting, intellectual property and consumer mediation. Courtesy translation of the French original."),
  "privacy": ("Privacy policy — Tengu Motion & Drone",
           "Privacy policy of Tengu Motion & Drone: data collected, purposes, retention periods, image rights and how to exercise your GDPR rights."),
  "terms": ("Terms of sale — Tengu Motion & Drone",
           "General terms of sale of Tengu Motion & Drone: quotes, booking, weather postponement, deliverables and image usage rights."),
  "notfound": ("Page not found — Tengu Motion & Drone",
           "The page you requested does not exist. Back to the Tengu Motion & Drone home page."),
},
"es": {
  "home": ("Tengu Motion & Drone — Vídeo, dron y fotografía cerca de París",
           "Vídeo, vídeo con dron y fotografía profesional en la región de Île-de-France: inmobiliario, corporativo, bodas, eventos, estudio e interior. Operador certificado DGAC, presupuesto gratuito en 24 h."),
  "services": ("Servicios y tarifas 2026 — Tengu Motion & Drone",
           "Tarifas 2026: 14 servicios de vídeo, dron y fotografía en la región de París. Pack inmobiliario desde 350 €, bodas desde 750 €, película 8K desde 1490 €. Presupuesto gratuito en 24 h."),
  "contact": ("Contacto y presupuesto — Tengu Motion & Drone",
           "Solicite un presupuesto gratuito en 24 h para servicios de vídeo, dron o fotografía en la región de París. Teléfono +33 6 33 59 87 74 — video@tengumotion.com."),
  "legal": ("Aviso legal — Tengu Motion & Drone",
           "Aviso legal de Tengu Motion & Drone: editor, alojamiento, propiedad intelectual y mediación de consumo. Traducción de cortesía del original francés."),
  "privacy": ("Privacidad — Tengu Motion & Drone",
           "Política de privacidad de Tengu Motion & Drone: datos recogidos, finalidades, plazos de conservación, derecho a la imagen y ejercicio de sus derechos RGPD."),
  "terms": ("Condiciones de venta — Tengu Motion & Drone",
           "Condiciones generales de venta de Tengu Motion & Drone: presupuesto, reserva, aplazamiento por meteorología, entregables y derechos de uso de las imágenes."),
  "notfound": ("Página no encontrada — Tengu Motion & Drone",
           "La página solicitada no existe. Volver al inicio de Tengu Motion & Drone."),
},
}

# Description de l'entreprise pour le JSON-LD
LD_DESC = {
  "fr": "Vidéo, vidéo par drone et photographie professionnelle en Île-de-France. Opérateur certifié DGAC, catégorie Specific.",
  "en": "Professional video, drone video and photography in the Île-de-France region, France. DGAC-certified operator, Specific category.",
  "es": "Vídeo, vídeo con dron y fotografía profesional en la región de Île-de-France, Francia. Operador certificado DGAC, categoría Specific.",
}
LD_KNOWS = {
  "fr": ["Photographie aérienne par drone", "Vidéo par drone", "Captation événementielle",
         "Film corporate", "Vidéo immobilière", "Drone indoor"],
  "en": ["Aerial drone photography", "Drone video", "Event filming",
         "Corporate film", "Real estate video", "Indoor drone"],
  "es": ["Fotografía aérea con dron", "Vídeo con dron", "Grabación de eventos",
         "Vídeo corporativo", "Vídeo inmobiliario", "Dron en interior"],
}

# ═══════════════════════════════════════════════════════════════════════════
# Documents légaux
#
# <mark>[…]</mark> marque un champ à compléter avant mise en ligne : le
# surlignage jaune le rend impossible à manquer dans le navigateur.
# Les versions EN et ES sont des traductions de courtoisie ; un encart en tête
# de page rappelle que seul le texte français fait foi (UI["…"]["lg_prevail"]).
# ═══════════════════════════════════════════════════════════════════════════
def _m(x):
    """Champ à compléter, surligné dans la page."""
    return '<mark>[%s]</mark>' % x


LEGAL = {
"fr": {
  "legal": {
    "num": "壱", "eyebrow": "Informations légales",
    "title": "Mentions", "italic": "légales.", "nav": "Mentions légales",
    "lead": "Éditeur, hébergement, propriété intellectuelle et médiation.",
    "sections": [
      ("Éditeur du site",
       "Tengu Motion &amp; Drone — " + _m("forme juridique") + " au capital de " + _m("montant") + " €. "
       "Siège social : " + _m("adresse") + ", Île-de-France. SIREN " + _m("n°") + " · RCS " + _m("ville") + ". "
       "TVA intracommunautaire : " + _m("n°") + ". Responsable de la publication : " + _m("nom") + "."),
      ("Contact",
       'Téléphone : <a href="tel:{tel_href}">{tel}</a>. Email : <a href="mailto:{email}">{email}</a>. Site : www.{domain}.'),
      ("Activité réglementée",
       "Opérateur de drones certifié DGAC, exploitation en catégorie Specific conformément aux "
       "règlements UE 2019/945 et 2019/947. Assurance responsabilité civile professionnelle "
       "(règl. UE 785/2004)."),
      ("Hébergement",
       "Site hébergé par GitHub Pages — GitHub, Inc., 88 Colin P. Kelly Jr. Street, "
       "San Francisco, CA 94107, États-Unis. https://github.com"),
      ("Propriété intellectuelle",
       "L'ensemble des contenus du site — textes, photographies, vidéos, marques et logo — est la "
       "propriété de Tengu Motion &amp; Drone. Toute reproduction ou diffusion, totale ou partielle, "
       "sans autorisation écrite préalable est interdite."),
      ("Réalisation", "Conception et réalisation du site : {agency}."),
      ("Médiation",
       "En cas de litige avec un client consommateur, recours possible au médiateur de la "
       "consommation : " + _m("nom et coordonnées du médiateur") + ", dans un délai d'un an à "
       "compter de la réclamation écrite."),
    ]},
  "privacy": {
    "num": "弐", "eyebrow": "Données personnelles",
    "title": "Politique de", "italic": "confidentialité.", "nav": "Confidentialité",
    "lead": "Ce que nous collectons, pourquoi, combien de temps, et comment exercer vos droits.",
    "sections": [
      ("Responsable de traitement",
       "Tengu Motion &amp; Drone, " + _m("adresse") + ", Île-de-France. "
       'Contact : <a href="mailto:{email}">{email}</a>.'),
      ("Données collectées",
       "Via le formulaire de devis : nom, société, email, téléphone, description de la mission. "
       "Via la navigation : données techniques strictement nécessaires au fonctionnement du site."),
      ("Finalités et base légale",
       "Répondre aux demandes de devis et gérer la relation client (exécution du contrat ou "
       "intérêt légitime). Aucune donnée n'est utilisée à des fins publicitaires sans consentement."),
      ("Durées de conservation",
       "Demandes de devis sans suite : 12 mois. Dossiers clients et documents comptables : 10 ans, "
       "conformément aux obligations légales. Images et rushes : conservés selon l'autorisation de "
       "diffusion accordée."),
      ("Destinataires",
       "Les données ne sont ni vendues ni cédées. Elles peuvent être transmises aux prestataires "
       "techniques nécessaires (hébergement, messagerie, comptabilité), agissant sur instruction."),
      ("Prises de vue aériennes",
       "Les captations sont réalisées dans le respect du droit à l'image et de la vie privée. Les "
       "personnes identifiables sur des images destinées à diffusion font l'objet d'une "
       "autorisation, ou d'un floutage à défaut."),
      ("Vos droits",
       "Accès, rectification, effacement, limitation, opposition et portabilité : écrire à "
       '<a href="mailto:{email}">{email}</a>. Réponse sous un mois. Réclamation possible auprès de '
       'la CNIL (<a href="https://www.cnil.fr" rel="noopener">www.cnil.fr</a>).'),
      ("Cookies",
       "Le site n'utilise que des cookies techniques nécessaires à son fonctionnement. Aucun "
       "traceur publicitaire ou de mesure d'audience n'est déposé sans consentement préalable."),
    ]},
  "terms": {
    "num": "参", "eyebrow": "Conditions de vente",
    "title": "Conditions générales", "italic": "de vente.", "nav": "CGV",
    "lead": "Devis, réservation, réalisation, livrables et droits d'utilisation des images.",
    "sections": [
      ("Objet",
       "Les présentes conditions régissent les prestations de captation photo et vidéo, aériennes "
       "et au sol, réalisées par Tengu Motion &amp; Drone. Toute commande implique leur acceptation "
       "sans réserve."),
      ("Devis et prix",
       "Prix indicatifs HT, hors options. Chaque devis est personnalisé selon la complexité, la "
       "zone et les livrables. Le devis est gratuit, émis sous 24 h et valable 30 jours à compter "
       "de son émission. Seul le devis signé fait foi."),
      ("Réservation et paiement",
       "Acompte de 30 % à la commande, solde à la livraison. Le créneau est confirmé après "
       "réception de l'acompte. Paiement par virement sous 30 jours ; pénalités de retard au taux "
       "légal et indemnité forfaitaire de 40 € en cas de retard."),
      ("Zone d'intervention",
       "Île-de-France. Frais de déplacement facturés au réel pour toute mission hors Île-de-France."),
      ("Conditions de vol et report",
       "Report sans frais en cas de conditions de vol non conformes : vent, pluie, visibilité, zone "
       "réglementée ou refus d'autorisation. Une nouvelle date est proposée dans les meilleurs délais."),
      ("Annulation",
       "Annulation par le client plus de 7 jours avant la date : acompte remboursé. Moins de "
       "7 jours : acompte conservé au titre des frais d'organisation. En cas d'annulation par le "
       "prestataire hors cas météo, l'acompte est intégralement remboursé."),
      ("Réalisation et livrables",
       "Brief préalable et plan de vol personnalisé. Livrables sous J+3 à J+7 selon la complexité. "
       "Rapport d'intervention et fichiers bruts sur demande. Support technique pendant 7 jours "
       "après livraison."),
      ("Retouches et validation",
       "Une série de retouches ou d'ajustements de montage est incluse. Toute demande "
       "supplémentaire fait l'objet d'un devis complémentaire. À défaut de retour sous 15 jours, "
       "les livrables sont réputés acceptés."),
      ("Droits d'utilisation",
       "Les fichiers livrés sont cédés pour l'usage défini au devis. Toute exploitation étendue — "
       "publicité, revente, cession à un tiers — fait l'objet d'un avenant. Le prestataire conserve "
       "la propriété intellectuelle des œuvres et le droit de les utiliser à des fins de "
       "démonstration, sauf clause de confidentialité."),
      ("Responsabilité et assurance",
       "Opérations conduites en catégorie Specific, conformément aux règlements UE 2019/945 et "
       "2019/947. Assurance responsabilité civile professionnelle (règl. UE 785/2004). La "
       "responsabilité du prestataire est limitée au montant de la prestation."),
      ("Droit applicable",
       "Droit français. En cas de litige, les parties recherchent une solution amiable avant toute "
       "action ; à défaut, compétence des tribunaux du ressort du siège social."),
    ]},
},

"en": {
  "legal": {
    "num": "壱", "eyebrow": "Legal information",
    "title": "Legal", "italic": "notice.", "nav": "Legal notice",
    "lead": "Publisher, hosting, intellectual property and mediation.",
    "sections": [
      ("Site publisher",
       "Tengu Motion &amp; Drone — " + _m("legal form") + " with share capital of " + _m("amount") + " €. "
       "Registered office: " + _m("address") + ", Île-de-France, France. SIREN " + _m("number") + " · "
       "Trade register " + _m("city") + ". EU VAT number: " + _m("number") + ". "
       "Publication director: " + _m("name") + "."),
      ("Contact",
       'Phone: <a href="tel:{tel_href}">{tel}</a>. Email: <a href="mailto:{email}">{email}</a>. '
       'Website: www.{domain}.'),
      ("Regulated activity",
       "DGAC-certified drone operator, operating in the Specific category in accordance with EU "
       "regulations 2019/945 and 2019/947. Professional liability insurance (EU reg. 785/2004)."),
      ("Hosting",
       "Site hosted by GitHub Pages — GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, "
       "CA 94107, United States. https://github.com"),
      ("Intellectual property",
       "All content on this site — text, photographs, videos, trademarks and logo — is the property "
       "of Tengu Motion &amp; Drone. Any reproduction or distribution, in whole or in part, without "
       "prior written permission is prohibited."),
      ("Design and build", "Site designed and built by {agency}."),
      ("Mediation",
       "In the event of a dispute with a consumer client, recourse to the consumer mediator is "
       "available: " + _m("mediator name and contact details") + ", within one year of the written "
       "complaint."),
    ]},
  "privacy": {
    "num": "弐", "eyebrow": "Personal data",
    "title": "Privacy", "italic": "policy.", "nav": "Privacy",
    "lead": "What we collect, why, for how long, and how to exercise your rights.",
    "sections": [
      ("Data controller",
       "Tengu Motion &amp; Drone, " + _m("address") + ", Île-de-France, France. "
       'Contact: <a href="mailto:{email}">{email}</a>.'),
      ("Data collected",
       "Through the quote form: name, company, email, phone and a description of the assignment. "
       "Through browsing: technical data strictly necessary for the site to function."),
      ("Purposes and legal basis",
       "To answer quote requests and manage the client relationship (performance of the contract or "
       "legitimate interest). No data is used for advertising purposes without consent."),
      ("Retention periods",
       "Quote requests with no follow-up: 12 months. Client files and accounting records: 10 years, "
       "in accordance with legal obligations. Images and raw footage: retained according to the "
       "distribution permission granted."),
      ("Recipients",
       "Data is neither sold nor transferred. It may be passed to the technical providers required "
       "(hosting, email, accounting), acting on instruction."),
      ("Aerial filming",
       "Filming is carried out with due respect for image rights and privacy. Identifiable people "
       "appearing in images intended for distribution are covered by a release, or blurred where "
       "no release has been obtained."),
      ("Your rights",
       "Access, rectification, erasure, restriction, objection and portability: write to "
       '<a href="mailto:{email}">{email}</a>. Response within one month. You may also lodge a '
       'complaint with the CNIL, the French data protection authority '
       '(<a href="https://www.cnil.fr/en" rel="noopener">www.cnil.fr</a>).'),
      ("Cookies",
       "The site uses only technical cookies necessary for it to function. No advertising or "
       "analytics tracker is placed without prior consent."),
    ]},
  "terms": {
    "num": "参", "eyebrow": "Terms of sale",
    "title": "General terms", "italic": "of sale.", "nav": "Terms of sale",
    "lead": "Quotes, booking, production, deliverables and image usage rights.",
    "sections": [
      ("Purpose",
       "These terms govern the photo and video capture services, aerial and ground, provided by "
       "Tengu Motion &amp; Drone. Placing an order implies unreserved acceptance of them."),
      ("Quotes and prices",
       "Indicative prices excluding VAT and options. Every quote is tailored to complexity, "
       "location and deliverables. Quotes are free, issued within 24 hours and valid for 30 days "
       "from the date of issue. Only the signed quote is binding."),
      ("Booking and payment",
       "30 % deposit on order, balance on delivery. The slot is confirmed once the deposit is "
       "received. Payment by bank transfer within 30 days; late payment interest at the statutory "
       "rate plus a fixed €40 recovery indemnity."),
      ("Service area",
       "Île-de-France. Travel costs charged at cost for any assignment outside the region."),
      ("Flight conditions and postponement",
       "Free postponement where flight conditions are unsuitable: wind, rain, visibility, "
       "restricted airspace or refusal of authorisation. A new date is offered as soon as possible."),
      ("Cancellation",
       "Cancellation by the client more than 7 days before the date: deposit refunded. Less than "
       "7 days: the deposit is retained to cover organisation costs. If the provider cancels for "
       "reasons other than weather, the deposit is refunded in full."),
      ("Production and deliverables",
       "Preliminary brief and tailored flight plan. Delivery in 3 to 7 days depending on "
       "complexity. Operation report and raw files on request. Technical support for 7 days after "
       "delivery."),
      ("Revisions and approval",
       "One round of retouching or editing adjustments is included. Any further request is subject "
       "to an additional quote. Failing feedback within 15 days, deliverables are deemed accepted."),
      ("Usage rights",
       "Delivered files are licensed for the use defined in the quote. Any extended exploitation — "
       "advertising, resale, transfer to a third party — requires an amendment. The provider "
       "retains intellectual property in the works and the right to use them for demonstration "
       "purposes, unless a confidentiality clause applies."),
      ("Liability and insurance",
       "Operations conducted in the Specific category, in accordance with EU regulations 2019/945 "
       "and 2019/947. Professional liability insurance (EU reg. 785/2004). The provider's "
       "liability is limited to the amount of the service."),
      ("Governing law",
       "French law. In the event of a dispute, the parties shall seek an amicable settlement before "
       "any action; failing that, the courts of the registered office's jurisdiction have "
       "jurisdiction."),
    ]},
},

"es": {
  "legal": {
    "num": "壱", "eyebrow": "Información legal",
    "title": "Aviso", "italic": "legal.", "nav": "Aviso legal",
    "lead": "Editor, alojamiento, propiedad intelectual y mediación.",
    "sections": [
      ("Editor del sitio",
       "Tengu Motion &amp; Drone — " + _m("forma jurídica") + " con un capital de " + _m("importe") + " €. "
       "Domicilio social: " + _m("dirección") + ", Île-de-France, Francia. SIREN " + _m("n.º") + " · "
       "Registro mercantil " + _m("ciudad") + ". NIF intracomunitario: " + _m("n.º") + ". "
       "Responsable de la publicación: " + _m("nombre") + "."),
      ("Contacto",
       'Teléfono: <a href="tel:{tel_href}">{tel}</a>. Email: <a href="mailto:{email}">{email}</a>. '
       'Sitio: www.{domain}.'),
      ("Actividad regulada",
       "Operador de drones certificado por la DGAC, con explotación en categoría Specific conforme "
       "a los reglamentos UE 2019/945 y 2019/947. Seguro de responsabilidad civil profesional "
       "(regl. UE 785/2004)."),
      ("Alojamiento",
       "Sitio alojado por GitHub Pages — GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, "
       "CA 94107, Estados Unidos. https://github.com"),
      ("Propiedad intelectual",
       "Todos los contenidos del sitio — textos, fotografías, vídeos, marcas y logotipo — son "
       "propiedad de Tengu Motion &amp; Drone. Queda prohibida cualquier reproducción o difusión, "
       "total o parcial, sin autorización previa por escrito."),
      ("Realización", "Diseño y realización del sitio: {agency}."),
      ("Mediación",
       "En caso de litigio con un cliente consumidor, cabe recurrir al mediador de consumo: "
       + _m("nombre y datos del mediador") + ", en el plazo de un año desde la reclamación escrita."),
    ]},
  "privacy": {
    "num": "弐", "eyebrow": "Datos personales",
    "title": "Política de", "italic": "privacidad.", "nav": "Privacidad",
    "lead": "Qué recogemos, para qué, durante cuánto tiempo y cómo ejercer sus derechos.",
    "sections": [
      ("Responsable del tratamiento",
       "Tengu Motion &amp; Drone, " + _m("dirección") + ", Île-de-France, Francia. "
       'Contacto: <a href="mailto:{email}">{email}</a>.'),
      ("Datos recogidos",
       "A través del formulario de presupuesto: nombre, empresa, email, teléfono y descripción del "
       "encargo. A través de la navegación: datos técnicos estrictamente necesarios para el "
       "funcionamiento del sitio."),
      ("Finalidades y base jurídica",
       "Responder a las solicitudes de presupuesto y gestionar la relación con el cliente "
       "(ejecución del contrato o interés legítimo). Ningún dato se utiliza con fines publicitarios "
       "sin consentimiento."),
      ("Plazos de conservación",
       "Solicitudes de presupuesto sin continuidad: 12 meses. Expedientes de clientes y documentos "
       "contables: 10 años, conforme a las obligaciones legales. Imágenes y material en bruto: se "
       "conservan según la autorización de difusión concedida."),
      ("Destinatarios",
       "Los datos no se venden ni se ceden. Pueden transmitirse a los proveedores técnicos "
       "necesarios (alojamiento, correo, contabilidad), que actúan siguiendo instrucciones."),
      ("Tomas aéreas",
       "Las grabaciones se realizan respetando el derecho a la imagen y la intimidad. Las personas "
       "identificables en imágenes destinadas a difusión cuentan con una autorización o, en su "
       "defecto, se difuminan."),
      ("Sus derechos",
       "Acceso, rectificación, supresión, limitación, oposición y portabilidad: escriba a "
       '<a href="mailto:{email}">{email}</a>. Respuesta en el plazo de un mes. También puede '
       'presentar una reclamación ante la CNIL, la autoridad francesa de protección de datos '
       '(<a href="https://www.cnil.fr" rel="noopener">www.cnil.fr</a>).'),
      ("Cookies",
       "El sitio solo utiliza cookies técnicas necesarias para su funcionamiento. No se instala "
       "ningún rastreador publicitario o de medición de audiencia sin consentimiento previo."),
    ]},
  "terms": {
    "num": "参", "eyebrow": "Condiciones de venta",
    "title": "Condiciones generales", "italic": "de venta.", "nav": "Condiciones de venta",
    "lead": "Presupuesto, reserva, realización, entregables y derechos de uso de las imágenes.",
    "sections": [
      ("Objeto",
       "Las presentes condiciones regulan los servicios de captación fotográfica y de vídeo, "
       "aéreos y terrestres, realizados por Tengu Motion &amp; Drone. Todo encargo implica su "
       "aceptación sin reservas."),
      ("Presupuesto y precios",
       "Precios indicativos sin IVA y sin opciones. Cada presupuesto se adapta a la complejidad, la "
       "zona y los entregables. El presupuesto es gratuito, se emite en 24 h y tiene una validez de "
       "30 días desde su emisión. Solo el presupuesto firmado da fe."),
      ("Reserva y pago",
       "Anticipo del 30 % al encargar, resto a la entrega. La fecha se confirma tras recibir el "
       "anticipo. Pago por transferencia en 30 días; intereses de demora al tipo legal e "
       "indemnización a tanto alzado de 40 € en caso de retraso."),
      ("Zona de intervención",
       "Île-de-France. Gastos de desplazamiento facturados a coste real fuera de la región."),
      ("Condiciones de vuelo y aplazamiento",
       "Aplazamiento sin coste si las condiciones de vuelo no son aptas: viento, lluvia, "
       "visibilidad, zona restringida o denegación de autorización. Se propone una nueva fecha con "
       "la mayor brevedad."),
      ("Cancelación",
       "Cancelación por el cliente con más de 7 días de antelación: anticipo reembolsado. Con menos "
       "de 7 días: el anticipo se retiene en concepto de gastos de organización. Si cancela el "
       "prestador por motivos ajenos a la meteorología, el anticipo se reembolsa íntegramente."),
      ("Realización y entregables",
       "Briefing previo y plan de vuelo personalizado. Entrega en 3 a 7 días según la complejidad. "
       "Informe de intervención y archivos en bruto a petición. Soporte técnico durante 7 días tras "
       "la entrega."),
      ("Retoques y validación",
       "Se incluye una ronda de retoques o ajustes de montaje. Cualquier petición adicional será "
       "objeto de un presupuesto complementario. A falta de respuesta en 15 días, los entregables "
       "se consideran aceptados."),
      ("Derechos de uso",
       "Los archivos entregados se ceden para el uso definido en el presupuesto. Toda explotación "
       "ampliada — publicidad, reventa, cesión a terceros — requiere una adenda. El prestador "
       "conserva la propiedad intelectual de las obras y el derecho a utilizarlas con fines de "
       "demostración, salvo cláusula de confidencialidad."),
      ("Responsabilidad y seguro",
       "Operaciones realizadas en categoría Specific, conforme a los reglamentos UE 2019/945 y "
       "2019/947. Seguro de responsabilidad civil profesional (regl. UE 785/2004). La "
       "responsabilidad del prestador se limita al importe del servicio."),
      ("Derecho aplicable",
       "Derecho francés. En caso de litigio, las partes buscarán una solución amistosa antes de "
       "emprender acciones; en su defecto, serán competentes los tribunales de la jurisdicción del "
       "domicilio social."),
    ]},
},
}
