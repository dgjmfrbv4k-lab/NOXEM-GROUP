"""Fiches produits françaises autonomes (sans Masterlayer).
Gabarit repris de seo/pages/produits.html. Usage : python3 seo/pages/build_produits.py
Chaque fiche : seo/pages/produits/<slug>.html (contenu d'un bloc wp:html) + produits/index.csv (titres/descriptions Yoast)."""
import re, csv, pathlib, html as H
D = pathlib.Path(__file__).resolve().parent
base = (D / "produits.html").read_text(encoding="utf-8")
prefix = base[:base.index('<div class="nxp-hero">')]
suffix = base[base.index('<div class="quoteform"'):]
prefix = prefix.replace("</style>\n<header>", ".nxp-faq dt{font-weight:700;margin-top:14px}.nxp-faq dd{margin:4px 0 0}.nxp-sec dd a{color:#b3262d;text-decoration:underline}</style>\n<header>", 1)

LIV = ("<li>Livraison sur votre site en France et en Belgique, ou en conteneur jusqu'à votre port à l'export : "
       "<a href=\"/fournisseur-verre-plat-france/\">livraison France</a> · <a href=\"/livraison-monde/\">export</a>.</li>"
       "<li>Conditionnement en caisses bois sécurisées, sanglage, cales et papier intercalaire entre chaque feuille.</li>"
       "<li>Achat en <b>conteneur complet</b> ou en <b>livraison panachée</b> (plusieurs références dans un même transport).</li>")

P = [
 dict(slug="verre-float", nom="Verre float", h1="Verre float clair et extra-clair en gros",
  t="Verre float clair et extra-clair en gros | Noxem Group",
  d="Verre float clair, extra-clair et teinté de 3 à 19 mm, plateaux jusqu'à 3300 × 5100 mm, norme EN 572. Conteneur complet ou panaché pour transformateurs. Demandez un prix.",
  intro="Le verre float est un verre plat transparent obtenu par flottaison du verre en fusion sur un bain d'étain : sa surface est parfaitement lisse et sa qualité optique homogène. C'est le produit de base de toutes les transformations : trempe, feuilletage, laquage, argenture, double vitrage.",
  car=["Clair, extra-clair (faible teneur en fer) ou teinté : gris clair et foncé, bronze clair et foncé, vert, bleu.",
       "Épaisseurs : 3 – 4 – 5 – 5,5 – 6 – 8 – 10 – 12 – 15 – 19 mm ; autres épaisseurs sur étude.",
       "Formats standards : 1220 × 1830, 1650 × 2140, 2140 × 3300, 2440 × 3660, 3300 × 5100 mm ; dimensions maximales 3300 × 5100 mm.",
       "Finitions possibles : coupe brute ou bord poli, chanfreinage, perçage, sablage, impression digitale, émaillage, découpe à forme.",
       "Livré brut, transformé ou prêt à usiner."],
  norme="EN 572", pour="Transformateurs et trempeurs (support de trempe, feuilletage, argenture), miroiteries, agenceurs, fabricants de mobilier.",
  lie=["verre-colore","verre-feuillete","verre-trempe","miroirs-professionnels"],
  art=[("/verre-float-clair-vs-verre-float-extra-clair-quelles-differences-guide-complet/","Float clair ou extra-clair : quelles différences ?"),("/combien-m2-verre-conteneur-20-40-pieds/","Combien de m² de verre dans un conteneur 20 et 40 pieds ?")]),
 dict(slug="verre-trempe", nom="Verre trempé", h1="Verre trempé sur mesure pour les professionnels",
  t="Verre trempé sur mesure pour professionnels | Noxem Group",
  d="Verre trempé clair ou teinté, façonné sur plan, conforme EN 12150, pour menuisiers, façadiers et agenceurs. Livraison en France et à l'export. Demandez un prix.",
  intro="Le verre trempé est un verre de sécurité qui subit un traitement thermique contrôlé : il devient jusqu'à cinq fois plus résistant qu'un verre ordinaire. En cas de casse, il se fragmente en petits morceaux peu coupants.",
  car=["Clair ou teinté, dans différents formats, épaisseurs et teintes.","Réalisé sur plan, pour des besoins courants comme pour des séries ou des projets techniques.","Trempé HST (Heat Soak Test) sur demande."],
  norme="EN 12150", pour="Fabricants de menuiseries, façadiers, agenceurs, fabricants de garde-corps et de cabines de douche.",
  lie=["verre-feuillete","verre-float","vitrages-techniques","double-vitrage"],
  art=[("/les-verres-de-securite-comprendre-les-differences-entre-verre-trempe-feuillete-feuillete-trempe-arme-et-blinde/","Verres de sécurité : trempé, feuilleté, armé, blindé"),("/garde-corps-en-verre-dtu-normes-dimensions-minimales-et-epaisseurs-recommandees/","Garde-corps en verre : normes et épaisseurs")]),
 dict(slug="verre-feuillete", nom="Verre feuilleté", h1="Verre feuilleté de sécurité en gros",
  t="Verre feuilleté 33.1, 44.2, 55.2 en gros | Noxem Group",
  d="Verre feuilleté de sécurité PVB, SGP ou EVA, normes EN ISO 12543 et EN 14449, pour transformateurs et menuisiers. Conteneur complet ou panaché. Demandez un prix.",
  intro="Le verre feuilleté est un vitrage de sécurité composé d'au moins deux feuilles de verre assemblées par un intercalaire (PVB, SGP ou EVA). En cas de choc, les fragments restent collés à l'intercalaire, ce qui protège les personnes et les biens. Il apporte aussi une bonne isolation acoustique et filtre naturellement les UV.",
  car=["Intercalaire PVB, SGP ou EVA.","Des compositions standards (33.1, 44.2, 55.2…) aux solutions techniques.","Options : feuilleté trempé, acoustique, opale ou décoratif."],
  norme="EN ISO 12543 et EN 14449", pour="Transformateurs, fabricants de menuiseries, façadiers, fabricants de garde-corps.",
  lie=["verre-trempe","verre-float","double-vitrage","vitrages-techniques"],
  art=[("/verre-feuillete-33-1-44-2-55-2-signification/","Verre feuilleté 33.1, 44.2, 55.2 : que signifient ces chiffres ?"),("/verre-feuillete-pvb-vs-eva-avantages-usages-certifications-en-14449/","Verre feuilleté PVB ou EVA")]),
 dict(slug="double-vitrage", nom="Double vitrage", h1="Double vitrage isolant sur mesure",
  t="Double vitrage sur mesure pour menuisiers | Noxem Group",
  d="Double vitrage isolant réalisé sur plan (Low-E, feuilleté, trempé, argon), norme EN 1279, pour fabricants de menuiseries, vérandas et façades. Demandez votre prix.",
  intro="Le double vitrage est un vitrage isolant composé de deux verres séparés par une lame d'air ou de gaz (argon ou krypton). Il assure l'isolation thermique et acoustique des menuiseries extérieures, façades, cloisons techniques et vérandas.",
  car=["Configurations sur mesure combinant verre clair, trempé, feuilleté, teinté, décoratif ou à couche (Low-E, contrôle solaire).","Réalisé à vos dimensions exactes."],
  norme="EN 1279", pour="Fabricants de menuiseries, constructeurs de vérandas, façadiers.",
  lie=["triple-vitrage","verre-a-faible-emissivite","verre-feuillete","verre-reflechissant"],
  art=[("/double-vitrage-ou-triple-vitrage-que-choisir-pour-vos-projets-residentiels-et-tertiaires/","Double ou triple vitrage : que choisir ?")]),
 dict(slug="triple-vitrage", nom="Triple vitrage", h1="Triple vitrage isolant sur mesure",
  t="Triple vitrage sur mesure pour professionnels | Noxem Group",
  d="Triple vitrage isolant sur plan pour menuiseries et façades à haute performance thermique, norme EN 1279. Étude de votre composition et prix sur demande.",
  intro="Le triple vitrage associe trois verres séparés par deux lames d'air ou de gaz, le plus souvent de l'argon. Il isole mieux que le double vitrage, tout en conservant un bon confort acoustique et une bonne transmission lumineuse selon la composition.",
  car=["Configurations définies selon votre besoin.","Pour bâtiments à haute performance énergétique, maisons passives, façades techniques, climats froids."],
  norme="EN 1279", pour="Fabricants de menuiseries haut de gamme, façadiers.",
  lie=["double-vitrage","verre-a-faible-emissivite","verre-feuillete"],
  art=[("/double-vitrage-ou-triple-vitrage-que-choisir-pour-vos-projets-residentiels-et-tertiaires/","Double ou triple vitrage : que choisir ?")]),
 dict(slug="verre-a-faible-emissivite", nom="Verre Low-E", h1="Verre à faible émissivité (Low-E)",
  t="Verre Low-E à faible émissivité en gros | Noxem Group",
  d="Verre Low-E à couche faiblement émissive, norme EN 1096, pour fabricants de doubles vitrages et de menuiseries. Plateaux en conteneur, France et export.",
  intro="Le verre Low-E est un verre float revêtu d'une couche métallique invisible, faiblement émissive, qui limite les pertes de chaleur tout en laissant passer un maximum de lumière naturelle. Il améliore la performance énergétique des bâtiments.",
  car=["Plusieurs types de verre Low-E.","Fourni en verre simple ou intégré à un double ou triple vitrage."],
  norme="EN 1096", pour="Fabricants de doubles vitrages et de menuiseries, façadiers.",
  lie=["double-vitrage","triple-vitrage","verre-reflechissant"],
  art=[("/low-e-ou-verre-reflechissant-climat-chaud/","Low-E ou verre réfléchissant : lequel choisir ?"),("/verre-de-controle-solaire-comprendre-les-g-values-shgc-tl-reflexion-et-absorption/","Contrôle solaire : g-value, SHGC, TL")]),
 dict(slug="verre-reflechissant", nom="Verre réfléchissant", h1="Verre réfléchissant de contrôle solaire",
  t="Verre réfléchissant et contrôle solaire | Noxem Group",
  d="Verre réfléchissant à couche de contrôle solaire, norme EN 1096, pour façades et climats chauds. Teintes et épaisseurs selon projet, en conteneur. Demandez un prix.",
  intro="Le verre réfléchissant est un verre float revêtu d'une couche métallique (déposée par pyrolyse ou sous vide) qui renvoie une partie de l'énergie solaire tout en laissant passer la lumière. Il améliore le confort des bâtiments très exposés et donne un effet miroir de jour.",
  car=["Plusieurs couleurs et finitions.","Pour façades, verrières et vitrages isolants.","Certains modèles doivent être trempés ou feuilletés selon l'usage."],
  norme="EN 1096", pour="Façadiers, fabricants de doubles vitrages, projets en climat chaud.",
  lie=["verre-a-faible-emissivite","double-vitrage","verre-colore"],
  art=[("/low-e-ou-verre-reflechissant-climat-chaud/","Low-E ou verre réfléchissant : lequel choisir ?")]),
 dict(slug="verre-colore", nom="Verre teinté", h1="Verre teinté dans la masse",
  t="Verre teinté dans la masse : gris, bronze, vert | Noxem Group",
  d="Verre float teinté dans la masse pour façades, agencement et transformation. Livré brut, trempé, feuilleté ou en double vitrage. Prix sur demande.",
  intro="Le verre teinté est un verre float auquel on ajoute des oxydes métalliques pendant la fusion : la teinte est homogène dans toute l'épaisseur. Il filtre une partie de la lumière, réduit les apports solaires et crée des effets esthétiques discrets ou contrastés.",
  car=["Sélection de teintes standards (gris, bronze, vert, bleu) en différentes épaisseurs et formats.","Fourni brut, trempé, feuilleté ou intégré à un double vitrage."],
  norme="EN 572", pour="Façadiers, agenceurs, transformateurs.",
  lie=["verre-float","verre-reflechissant","verre-trempe"], art=[]),
 dict(slug="verre-a-motifs", nom="Verre imprimé à motifs", h1="Verre imprimé à motifs",
  t="Verre imprimé à motifs en gros | Noxem Group",
  d="Verre imprimé à motifs pour menuiseries, portes, douches et cloisons. Plateaux en caisses bois, conteneur complet ou panaché. Demandez votre prix.",
  intro="Le verre imprimé est un verre texturé obtenu en faisant passer le verre en fusion entre des rouleaux gravés. Il laisse passer la lumière tout en préservant l'intimité.",
  car=["Large choix de motifs, classiques ou modernes, de teintes et d'épaisseurs.","Trempe ou découpe sur mesure possibles sur demande."],
  norme="EN 572", pour="Fabricants de menuiseries et de portes, cabines de douche, agenceurs.",
  lie=["verre-depoli","verre-trempe","verre-float"], art=[]),
 dict(slug="verre-depoli", nom="Verre dépoli", h1="Verre dépoli (acidé ou sablé)",
  t="Verre dépoli (acidé) pour professionnels | Noxem Group",
  d="Verre dépoli acidé ou sablé pour cloisons, portes et agencement. Standard, trempé ou feuilleté, livraison en France et à l'export. Demandez un prix.",
  intro="Le verre dépoli est un verre float dont la surface est traitée à l'acide ou par sablage, ce qui lui donne un aspect satiné. Il préserve l'intimité tout en laissant passer une lumière diffuse.",
  car=["Disponible en version standard, trempée ou feuilletée."],
  norme="EN 572", pour="Agenceurs, miroiteries, fabricants de cloisons et de portes.",
  lie=["verre-a-motifs","verre-laque","verre-trempe"], art=[]),
 dict(slug="verre-laque", nom="Verre laqué", h1="Verre laqué en plateaux",
  t="Verre laqué en plateaux pour agencement | Noxem Group",
  d="Verre laqué blanc, noir, gris, rouge ou teinte RAL et Pantone sur demande, pour agenceurs, cuisinistes et miroiteries. Découpe possible. Demandez un prix.",
  intro="Le verre laqué est un verre float recouvert au dos d'une laque colorée, pour un rendu brillant et opaque. Il est très utilisé en agencement, mobilier et signalétique, et s'entretient facilement.",
  car=["Teintes standards : blanc, noir, gris, rouge…","Teintes sur mesure sur demande, d'après une référence RAL ou Pantone.","Différentes épaisseurs, finitions et dimensions ; découpe sur mesure possible."],
  norme=None, pour="Agenceurs, cuisinistes, miroiteries, fabricants de mobilier.",
  lie=["miroirs-professionnels","verre-depoli","verre-float"], art=[]),
 dict(slug="miroirs-professionnels", nom="Miroirs professionnels", h1="Miroirs en plateaux pour les professionnels",
  t="Miroir argenté en plateaux pour miroiteries | Noxem Group",
  d="Miroirs argentés, sans cuivre, de sécurité, colorés ou antiques, sur float clair, extra-clair ou teinté. Conteneur complet ou panaché. Demandez votre prix.",
  intro="Noxem Group fournit une gamme complète de miroirs pour l'agencement, l'architecture et la décoration. Ils sont fabriqués sur verre float clair, extra-clair ou teinté, avec une couche réfléchissante (argent ou aluminium) protégée par plusieurs couches de peinture technique.",
  car=["Miroir argenté classique, miroir sans cuivre, miroir de sécurité (film au dos), miroir aluminium.","Miroirs décoratifs colorés, teintés ou antiques.","Plusieurs teintes et finitions."],
  norme=None, pour="Miroiteries, agenceurs, fabricants de mobilier et de salles de bains.",
  lie=["miroir-sans-cuivre-ni-plomb","miroir-antique","verre-laque","verre-float"],
  art=[("/les-differents-types-de-miroirs-composition-proprietes-et-usages/","Les différents types de miroirs")]),
 dict(slug="miroir-sans-cuivre-ni-plomb", nom="Miroir sans cuivre ni plomb", h1="Miroir sans cuivre ni plomb",
  t="Miroir sans cuivre ni plomb en plateaux | Noxem Group",
  d="Miroir sans cuivre ni plomb, résistant à la corrosion en milieu humide, pour miroiteries et agencement. Découpe et film de sécurité possibles. Demandez un prix.",
  intro="Le miroir sans cuivre est une alternative plus respectueuse de l'environnement au miroir traditionnel. Fabriqué sans cuivre ni plomb, il résiste mieux à la corrosion, notamment en milieu humide (salles de bains, spas, hôtels).",
  car=["Plusieurs épaisseurs, finitions et teintes.","Découpe sur mesure et film de sécurité au dos possibles."],
  norme=None, pour="Miroiteries, agenceurs, hôtellerie, fabricants de salles de bains.",
  lie=["miroirs-professionnels","miroir-antique"],
  art=[("/les-differents-types-de-miroirs-composition-proprietes-et-usages/","Les différents types de miroirs")]),
 dict(slug="miroir-antique", nom="Miroir antique", h1="Miroir antique à effet vieilli",
  t="Miroir antique (vieilli) pour agenceurs | Noxem Group",
  d="Miroir antique à effet vieilli (bronze, gris, argent, or patiné) pour agenceurs, décorateurs et miroiteries. Découpe et film de sécurité possibles.",
  intro="Le miroir antique est un miroir décoratif obtenu par une oxydation contrôlée ou un traitement spécifique de la couche réfléchissante : il présente un aspect vieilli, tacheté, marbré ou craquelé. Chaque feuille est unique.",
  car=["Finitions bronze, gris, argent, or patiné.","Film de sécurité et découpe sur mesure possibles."],
  norme=None, pour="Agenceurs, décorateurs, hôtellerie, commerces haut de gamme.",
  lie=["miroirs-professionnels","miroir-sans-cuivre-ni-plomb"], art=[]),
 dict(slug="verre-emaille-ou-imprime", nom="Verre émaillé ou imprimé", h1="Verre émaillé ou imprimé",
  t="Verre émaillé et imprimé numérique sur mesure | Noxem Group",
  d="Verre émaillé, sérigraphié ou imprimé numériquement, fixé par traitement thermique, pour façades, allèges et agencement. Étude de projet et prix sur demande.",
  intro="Le verre émaillé ou imprimé reçoit un émail, une encre céramique ou une image numérique, fixés par traitement thermique (trempe ou fusion). Il est utilisé pour son rendu esthétique, pour la signalétique ou pour sa durabilité.",
  car=["Émaillage, sérigraphie, impression numérique.","Motifs répétitifs, visuels haute définition ou éléments techniques sur mesure."],
  norme=None, pour="Façadiers, agenceurs, architectes d'intérieur.",
  lie=["verre-trempe","verre-laque","vitrages-techniques"], art=[]),
 dict(slug="vitrages-techniques", nom="Vitrages techniques", h1="Vitrages techniques et innovants sur demande",
  t="Vitrages techniques sur demande | Noxem Group",
  d="Vitrages techniques étudiés au cas par cas : performance thermique, sécurité renforcée, design, fonctions intelligentes. Pour professionnels du bâtiment.",
  intro="Noxem Group propose sur demande une sélection de vitrages techniques et innovants, pour des exigences particulières : performance thermique, sécurité renforcée, design, intégration technologique ou fonctions intelligentes.",
  car=["Chaque projet est étudié individuellement : choix des composants, faisabilité, formats, quantités minimales et délais."],
  norme=None, pour="Façadiers, bureaux d'études, entreprises générales.",
  lie=["verre-feuillete","verre-trempe","double-vitrage"],
  art=[("/verres-isolants-coupe-feu-comprendre-choisir-et-proteger-vos-batiments/","Verres coupe-feu"),("/murs-rideaux-les-elements-cruciaux-pour-reussir-son-projet/","Murs-rideaux : les éléments clés")]),
 dict(slug="verre-photovoltaique", nom="Verre photovoltaïque", h1="Verre photovoltaïque (BIPV)",
  t="Verre photovoltaïque pour le bâtiment (BIPV) | Noxem Group",
  d="Vitrage photovoltaïque intégré au bâtiment (BIPV) pour façades, verrières, garde-corps et ombrières. Étude et prix sur demande.",
  intro="Le verre photovoltaïque est un vitrage technique qui intègre des cellules solaires (silicium amorphe, monocristallin ou polycristallin). Il produit de l'électricité tout en jouant un rôle architectural : protection, isolation, design.",
  car=["Utilisé en façades, verrières, garde-corps, toitures vitrées et ombrières solaires."],
  norme=None, pour="Façadiers, architectes, bureaux d'études, constructeurs d'ombrières.",
  lie=["vitrages-techniques","verre-feuillete"], art=[]),
]
NAMES = {p["slug"]: p["nom"] for p in P}

def page(p):
    car = "".join(f"<li>{c}</li>" for c in p["car"])
    norme = f'<tr><th>Norme</th><td>{p["norme"]}</td></tr>' if p["norme"] else ""
    lie = "".join(f'<a class="nxp-card" href="/service/{s}/"><b>{NAMES[s]}</b><span>Voir la fiche</span></a>' for s in p["lie"])
    art = ""
    if p["art"]:
        art = '<p style="margin-top:14px">À lire aussi : ' + " · ".join(f'<a href="{u}">{t}</a>' for u, t in p["art"]) + "</p>"
    body = f"""<div class="nxp-hero"><div class="wrap">
  <span class="eyebrow"><a href="/produits/">Produits</a> · {p["nom"]}</span>
  <h1>{p["h1"]}</h1>
  <p>{p["intro"]}</p>
  <div class="ctas"><a class="btn" href="#devis">Demander un prix <span class="arr">→</span></a> <a class="btn ghost" href="https://noxemgroup.com/wp-content/uploads/2026/09/NOXEM-GROUP-Catalogue-2026-FR.pdf" target="_blank" rel="noopener">Catalogue 2026 (PDF)</a></div>
</div></div>

<section class="nxp-sec"><div class="wrap">
  <h2>Caractéristiques</h2>
  <ul class="nxp-list">{car}</ul>
  <table class="nxp-tbl" style="margin-top:18px">{norme}<tr><th>Pour qui</th><td>{p["pour"]}</td></tr></table>
  <p style="margin-top:14px">Une variante ne figure pas ici ? Nous la recherchons pour vous auprès de nos verriers.</p>
</div></section>

<section class="nxp-sec nxp-alt"><div class="wrap">
  <h2>Conditionnement et livraison</h2>
  <ul class="nxp-list">{LIV}</ul>
  {art}
</div></section>

<section class="nxp-sec"><div class="wrap">
  <h2>Produits associés</h2>
  <div class="nxp-grid">{lie}<a class="nxp-card" href="/produits/"><b>Toute la gamme</b><span>Verre plat en gros</span></a></div>
</div></section>
"""
    out = prefix + body + suffix
    out = re.sub(r'"name":"Produits","item":"https://noxemgroup.com/produits/"\}\]',
                 f'"name":"Produits","item":"https://noxemgroup.com/produits/"}},{{"@type":"ListItem","position":3,"name":"{p["nom"]}","item":"https://noxemgroup.com/service/{p["slug"]}/"}}]', out)
    return out

(D / "produits").mkdir(exist_ok=True)
with open(D / "produits" / "index.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["slug", "url_cible", "titre_page", "titre_seo", "meta_description"])
    for p in P:
        (D / "produits" / f'{p["slug"]}.html').write_text(page(p), encoding="utf-8")
        w.writerow([p["slug"], f'/service/{p["slug"]}/', p["nom"], p["t"], p["d"]])
print(len(P), "fiches")
