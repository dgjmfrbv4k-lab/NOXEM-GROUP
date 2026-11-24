"""Pages métiers (gabarit de seo/pages/produits.html). Usage : python3 seo/pages/build_metiers.py"""
import re, csv, pathlib
D = pathlib.Path(__file__).resolve().parent
base = (D / "produits.html").read_text(encoding="utf-8")
prefix = base[:base.index('<div class="nxp-hero">')]
suffix = base[base.index('<div class="quoteform"'):]
prefix = prefix.replace("</style>\n<header>", ".nxp-faq dt{font-weight:700;margin-top:14px}.nxp-faq dd{margin:4px 0 0}.nxp-sec dd a{color:#b3262d;text-decoration:underline}</style>\n<header>", 1)

def cards(items):
    return '<div class="nxp-grid">' + "".join(f'<a class="nxp-card" href="/service/{s}/"><b>{t}</b><span>{d}</span></a>' for s, t, d in items) + "</div>"

M = [
 dict(slug="verre-menuiseries-facades", nom="Menuiseries et façades",
  t="Verre pour fabricants de menuiseries et façadiers | Noxem Group",
  d="Verre feuilleté, trempé, Low-E, contrôle solaire et double vitrage sur plan pour fabricants de menuiseries et façadiers. Conteneur complet ou panaché.",
  h1="Verre pour fabricants de menuiseries et façadiers",
  intro="Fenêtres, portes, vérandas, murs-rideaux : Noxem Group, importateur et négociant de verre plat, fournit aux fabricants de menuiseries et aux façadiers les verres de sécurité, les verres à couche et les vitrages isolants dont ils ont besoin, en conteneur complet ou en livraison panachée.",
  blocs=[("Verres de sécurité", [("verre-feuillete","Verre feuilleté","PVB, SGP ou EVA ; 33.1, 44.2, 55.2…"),("verre-trempe","Verre trempé","Façonné sur plan, trempé HST sur demande")]),
         ("Performance thermique et solaire", [("verre-a-faible-emissivite","Verre Low-E","Couche faiblement émissive, EN 1096"),("verre-reflechissant","Verre réfléchissant","Contrôle solaire pour façades exposées"),("verre-colore","Verre teinté","Gris, bronze, vert, bleu")]),
         ("Vitrages isolants sur plan", [("double-vitrage","Double vitrage","Argon ou krypton, EN 1279"),("triple-vitrage","Triple vitrage","Haute performance thermique"),("verre-emaille-ou-imprime","Verre émaillé","Allèges et façades")])],
  faq=[("Pouvez-vous fournir des vitrages isolants à mes dimensions ?","Oui : doubles et triples vitrages sont réalisés sur plan, avec la composition que vous définissez."),
       ("Quelles normes ?","Selon le produit : EN 12150 (trempé), EN ISO 12543 et EN 14449 (feuilleté), EN 1096 (verre à couche), EN 1279 (vitrage isolant)."),
       ("Livrez-vous en France ?","Oui, sur votre site en France et en Belgique, et à l'export en conteneur.")],
  art=[("/murs-rideaux-les-elements-cruciaux-pour-reussir-son-projet/","Murs-rideaux : les éléments clés"),("/verre-feuillete-33-1-44-2-55-2-signification/","Feuilleté 33.1, 44.2, 55.2"),("/double-vitrage-ou-triple-vitrage-que-choisir-pour-vos-projets-residentiels-et-tertiaires/","Double ou triple vitrage")]),
 dict(slug="verre-miroiteries", nom="Miroiteries",
  t="Fournisseur de verre et miroirs pour miroiteries | Noxem Group",
  d="Miroirs argentés, sans cuivre, antiques, verres laqués, dépolis et extra-clairs pour miroiteries. Livraison panachée ou conteneur complet. Demandez un prix.",
  h1="Verre et miroirs pour les miroiteries",
  intro="Les miroiteries ont besoin de nombreuses références en quantités raisonnables. Noxem Group, importateur et négociant de verre plat, propose la livraison panachée (plusieurs références et épaisseurs dans un même transport) ou le conteneur complet pour les plus gros volumes.",
  blocs=[("Miroirs", [("miroirs-professionnels","Miroirs professionnels","Argenté, aluminium, de sécurité, coloré"),("miroir-sans-cuivre-ni-plomb","Miroir sans cuivre ni plomb","Résiste à l'humidité"),("miroir-antique","Miroir antique","Effet vieilli, chaque feuille unique")]),
         ("Verres décoratifs", [("verre-laque","Verre laqué","Teintes standards ou RAL / Pantone"),("verre-depoli","Verre dépoli","Acidé ou sablé"),("verre-a-motifs","Verre imprimé","Motifs classiques ou modernes")]),
         ("Verres de base", [("verre-float","Float clair et extra-clair","De 3 à 19 mm"),("verre-feuillete","Verre feuilleté","Pour les applications de sécurité")])],
  faq=[("Faut-il commander un conteneur complet ?","Non : la livraison panachée permet de regrouper plusieurs références dans un même transport."),
       ("Proposez-vous des teintes de laque sur mesure ?","Oui, sur demande, d'après une référence RAL ou Pantone."),
       ("Livrez-vous en France ?","Oui, sur votre site en France et en Belgique.")],
  art=[("/les-differents-types-de-miroirs-composition-proprietes-et-usages/","Les différents types de miroirs"),("/verre-float-clair-vs-verre-float-extra-clair-quelles-differences-guide-complet/","Float clair ou extra-clair")]),
 dict(slug="verre-transformateurs", nom="Transformateurs",
  t="Verre float et feuilleté pour transformateurs | Noxem Group",
  d="Float clair et extra-clair, feuilleté et verre trempable en plateaux pour transformateurs et trempeurs. Conteneur complet, livraison France, Belgique et export.",
  h1="Verre plat en plateaux pour transformateurs et trempeurs",
  intro="Pour alimenter vos lignes de découpe, de trempe, de feuilletage ou d'assemblage, Noxem Group fournit le verre de base en plateaux, en conteneur complet. Format standard 3210 × 2550 mm, autres dimensions sur demande.",
  blocs=[("Verres de base", [("verre-float","Float clair et extra-clair","3 à 19 mm, jusqu'à 3300 × 5100 mm"),("verre-colore","Verre teinté","Teinté dans la masse"),("verre-a-motifs","Verre imprimé","Pour portes et cloisons")]),
         ("Verres à transformer", [("verre-feuillete","Verre feuilleté","Pour découpe et assemblage"),("verre-a-faible-emissivite","Verre Low-E","Pour vitrages isolants"),("verre-reflechissant","Verre réfléchissant","Contrôle solaire")])],
  faq=[("Quel format de plateaux ?","Format standard 3210 × 2550 mm ; autres dimensions sur demande."),
       ("Combien de m² dans un conteneur ?","Cela dépend de l'épaisseur : voir notre tableau des m² par conteneur 20 et 40 pieds."),
       ("Comment le verre est-il conditionné ?","En caisses bois sécurisées, sanglées et calées, avec un intercalaire entre chaque feuille.")],
  art=[("/combien-m2-verre-conteneur-20-40-pieds/","Combien de m² de verre dans un conteneur ?"),("/cif-cfr-fob-incoterm-importer-verre-plat/","CIF, CFR ou FOB : quel Incoterm ?")]),
]

def page(m):
    blocs = "".join(f'<section class="nxp-sec{" nxp-alt" if i%2 else ""}"><div class="wrap"><h2>{titre}</h2>{cards(items)}</div></section>' for i, (titre, items) in enumerate(m["blocs"]))
    faq = "".join(f"<dt>{q}</dt><dd>{a}</dd>" for q, a in m["faq"])
    art = " · ".join(f'<a href="{u}">{t}</a>' for u, t in m["art"])
    faqld = ",".join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (__import__("json").dumps(q, ensure_ascii=False), __import__("json").dumps(a, ensure_ascii=False)) for q, a in m["faq"])
    body = f"""<div class="nxp-hero"><div class="wrap">
  <span class="eyebrow">Votre métier · {m["nom"]}</span>
  <h1>{m["h1"]}</h1>
  <p>{m["intro"]}</p>
  <div class="ctas"><a class="btn" href="#devis">Demander un prix <span class="arr">→</span></a> <a class="btn ghost" href="/produits/">Toute la gamme</a></div>
</div></div>
{blocs}
<section class="nxp-sec"><div class="wrap">
  <h2>Livraison</h2>
  <ul class="nxp-list"><li>Livraison sur votre site en France et en Belgique : <a href="/fournisseur-verre-plat-france/">notre offre France</a>.</li><li>Export en conteneur jusqu'à votre port : <a href="/livraison-monde/">livraison dans le monde</a>.</li><li>Logistique à Mollem (Belgique) : <a href="/logistique/">notre logistique</a>.</li></ul>
  <h2 style="margin-top:28px">Questions fréquentes</h2>
  <dl class="nxp-faq">{faq}</dl>
  <p style="margin-top:14px">À lire aussi : {art}</p>
</div></section>
"""
    out = prefix + body + suffix
    out = out.replace('"name":"Produits","item":"https://noxemgroup.com/produits/"', f'"name":"{m["nom"]}","item":"https://noxemgroup.com/{m["slug"]}/"')
    out = out.replace("<!-- /wp:html -->", '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + faqld + ']}</script>\n<!-- /wp:html -->')
    return out

with open(D / "metiers" / "index.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["slug", "titre_page", "titre_seo", "meta_description"])
    for m in M:
        (D / "metiers" / f'{m["slug"]}.html').write_text(page(m), encoding="utf-8")
        w.writerow([m["slug"], m["h1"], m["t"], m["d"]])
print(len(M), "pages métiers")
