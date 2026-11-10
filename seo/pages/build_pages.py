"""Construit les pages légères /produits/, /qui-sommes-nous/, /contact/ et /fournisseur-verre-plat-france/.
Source du gabarit : la sauvegarde seo/backups/page-9827-produits-avant.html (styles, pied de page).
Usage : python3 seo/pages/build_pages.py  -> écrit seo/pages/*.html (contenu d'un bloc wp:html)."""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
src = (ROOT / "backups/page-9827-produits-avant.html").read_text(encoding="utf-8")

font = re.search(r'<link href="https://fonts.googleapis.com[^>]+>', src).group(0)
styles = re.findall(r"<style>.*?</style>", src, re.S)
base_css = styles[0]                                   # charte du site
footer_css = next(s for s in styles if ".nxf{" in s)   # pied de page
footer_html = re.search(r'<footer class="nxf".*?</footer>', src, re.S).group(0)
footer_js = re.search(r"<script>\s*/\* Pied de page.*?</script>", src, re.S).group(0)
ld_org = re.search(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"Organization".*?</script>', src, re.S).group(0)
form_html = re.search(r'<div class="quoteform" id="devis">.*?</form>\s*</div>\s*</div>', src, re.S).group(0)
# textes du formulaire figés en français (le script de traduction n'est plus chargé)
form_html = re.sub(r'\sdata-t="[^"]*"', "", form_html)
form_html = form_html.replace('<p class="sub">Envoyez vos références et votre lieu de livraison. Réponse sous 24 h.</p>',
                              '<p class="sub">Envoyez vos références, épaisseurs, quantités et votre lieu de livraison. Réservé aux professionnels.</p>')
wa_svg = re.search(r'<svg viewBox="0 0 32 32".*?</svg>', form_html, re.S).group(0)

PAGE_CSS = """<style>
/* Pages légères Noxem : neutralise le thème et ajoute les cartes produits */
html body{overflow:visible;overflow-x:clip}
.nxp-hero{padding:56px 0 36px;background:#f6f5f2;border-bottom:1px solid #e3e6ea}
.nxp-hero h1{font-size:clamp(28px,4vw,44px);line-height:1.15;font-weight:800;margin:10px 0 14px}
.nxp-hero p{max-width:760px;font-size:18px;line-height:1.6}
.nxp-sec{padding:44px 0}
.nxp-sec h2{font-size:clamp(22px,3vw,30px);font-weight:800;margin:0 0 16px}
.nxp-sec p,.nxp-sec li{font-size:16px;line-height:1.7}
.nxp-sec ul.nxp-list{list-style:disc;padding-left:22px;margin:8px 0 0}
.nxp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;margin-top:8px}
.nxp-card{display:block;border:1px solid #e3e6ea;border-radius:10px;padding:18px;background:#fff;text-decoration:none;color:inherit;transition:border-color .2s}
.nxp-card:hover{border-color:#141b25}
.nxp-card b{display:block;font-size:17px;margin-bottom:6px}
.nxp-card span{font-size:14.5px;line-height:1.5;color:#55606d}
.nxp-tbl{width:100%;border-collapse:collapse;margin-top:8px;font-size:15px}
.nxp-tbl th,.nxp-tbl td{border:1px solid #e3e6ea;padding:10px 12px;text-align:left;vertical-align:top}
.nxp-tbl th{background:#f6f5f2;width:32%}
.nxp-alt{background:#f6f5f2}
.nxp-nav{display:flex;flex-wrap:wrap;gap:18px}
.nxp-nav a{text-decoration:none;color:inherit;font-weight:600;font-size:15px}
.nxp-faq dt{font-weight:700;margin-top:14px}
.nxp-faq dd{margin:4px 0 0}
.nxp-sec p a,.nxp-sec li a,.nxp-sec dd a,.nxp-tbl a{color:#b3262d;text-decoration:underline;text-underline-offset:2px}
.nxp-hero .btn.ghost{color:#141b25;border-color:#141b25;background:transparent}
@media (max-width:860px){.nxp-nav{display:none}}
</style>"""

HEADER = """<header>
  <div class="wrap">
    <a href="/"><img decoding="async" src="https://noxemgroup.com/wp-content/uploads/2023/09/LOGO-1.png" alt="Noxem Group"></a>
    <nav class="nxp-nav" aria-label="Navigation principale"><a href="/produits/">Produits</a><a href="/fournisseur-verre-plat-france/">Livraison France</a><a href="/livraison-monde/">Export</a><a href="/logistique/">Logistique</a><a href="/guides-importateurs-verre-plat/">Guides</a><a href="/qui-sommes-nous/">Qui sommes-nous</a></nav>
    <div class="hdr-r"><a class="btn" href="/contact/">Demander un prix</a></div>
  </div>
</header>"""

FORM_JS = """<script>
(function(){
  var f = document.getElementById('qf'); if (!f) return;
  var CF7 = 9313;
  f.addEventListener('submit', function(e){
    e.preventDefault();
    var msg = document.getElementById('fmsg'), btn = f.querySelector('button');
    var v = function(n){ return f.elements[n].value.trim(); };
    if (!v('nom') || !v('email') || !v('produits')) { msg.className = 'msg err'; msg.textContent = 'Merci de renseigner votre nom, votre e-mail et les produits recherchés.'; return; }
    var fd = new FormData();
    fd.append('_wpcf7', CF7); fd.append('_wpcf7_version', '6.1.7'); fd.append('_wpcf7_locale', 'fr_FR');
    fd.append('_wpcf7_unit_tag', 'wpcf7-f' + CF7 + '-o1'); fd.append('_wpcf7_container_post', '0');
    ['nom','societe','email','tel','pays','produits'].forEach(function(n){ fd.append(n, v(n)); });
    fd.append('langue', 'Français (page ' + location.pathname + ')');
    btn.disabled = true; msg.className = 'msg'; msg.textContent = 'Envoi…';
    fetch('/wp-json/contact-form-7/v1/contact-forms/' + CF7 + '/feedback', {method:'POST', body:fd})
      .then(function(r){ return r.json(); })
      .then(function(j){
        if (j.status === 'mail_sent') { msg.className = 'msg ok'; msg.textContent = 'Merci, votre demande est envoyée. Nous revenons vers vous rapidement.'; f.reset();
          if (window.dataLayer) window.dataLayer.push({event:'generate_lead_form', page: location.pathname}); }
        else if (j.status === 'validation_failed') { msg.className = 'msg err'; msg.textContent = 'Merci de vérifier les champs obligatoires.'; }
        else { msg.className = 'msg err'; msg.textContent = 'L’envoi a échoué. Écrivez-nous à contact@noxemgroup.com ou par WhatsApp.'; }
      })
      .catch(function(){ msg.className = 'msg err'; msg.textContent = 'L’envoi a échoué. Écrivez-nous à contact@noxemgroup.com ou par WhatsApp.'; })
      .then(function(){ btn.disabled = false; });
  });
})();
</script>"""

WA_FLOAT = ('<a class="wa-float" id="waFloat" target="_blank" rel="noopener" aria-label="WhatsApp" '
            'href="https://wa.me/33686131271?text=Bonjour%2C%20je%20souhaite%20un%20prix%20pour%20du%20verre%20plat.">'
            + wa_svg + '</a>')

def mini(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    return re.sub(r"\s*([{};:,>])\s*", r"\1", css).replace("<style>", "<style>").strip()

def page(body, breadcrumb_name, path):
    crumbs = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
              '{"@type":"ListItem","position":1,"name":"Accueil","item":"https://noxemgroup.com/"},'
              '{"@type":"ListItem","position":2,"name":"%s","item":"https://noxemgroup.com%s"}]}</script>' % (breadcrumb_name, path))
    parts = ["<!-- wp:html -->", font, mini(base_css), mini(footer_css), mini(PAGE_CSS), HEADER, body, form_html,
             footer_html, ld_org, crumbs, WA_FLOAT, FORM_JS, "<!-- /wp:html -->"]
    return "\n".join(parts)

def cards(items):
    return '<div class="nxp-grid">' + "".join(
        f'<a class="nxp-card" href="{u}"><b>{t}</b><span>{d}</span></a>' for u, t, d in items) + "</div>"

# ---------------- /produits/ ----------------
produits = f"""
<div class="nxp-hero"><div class="wrap">
  <span class="eyebrow">Importateur &amp; négociant de verre plat</span>
  <h1>Verre plat en gros pour les professionnels</h1>
  <p>Float, feuilleté, trempé, miroirs, verres à couche et vitrages transformés : Noxem Group fournit les transformateurs, miroiteries, fabricants de menuiseries et façadiers, en conteneur complet ou en livraison panachée, en France, en Belgique et à l'export.</p>
  <div class="ctas"><a class="btn" href="#devis">Demander un prix <span class="arr">→</span></a> <a class="btn ghost" href="https://noxemgroup.com/wp-content/uploads/2026/09/NOXEM-GROUP-Catalogue-2026-FR.pdf" target="_blank" rel="noopener">Catalogue 2026 (PDF)</a></div>
</div></div>

<section class="nxp-sec"><div class="wrap">
  <h2>Verres de base</h2>
  {cards([("/service/verre-float/","Verre float clair et extra-clair","De 3 à 19 mm, plateaux jusqu'à 3300 × 5100 mm, norme EN 572."),
          ("/service/verre-colore/","Verre teinté","Gris, bronze, vert, bleu, teinté dans la masse."),
          ("/service/verre-a-motifs/","Verre imprimé à motifs","Pour portes, cloisons, douches et menuiseries."),
          ("/service/verre-depoli/","Verre dépoli","Verre acidé pour cloisons et agencement intérieur.")])}
</div></section>

<section class="nxp-sec nxp-alt"><div class="wrap">
  <h2>Verres de sécurité</h2>
  {cards([("/service/verre-feuillete/","Verre feuilleté","Feuilleté PVB (33.1, 44.2, 55.2…), normes EN ISO 12543 et EN 14449."),
          ("/service/verre-trempe/","Verre trempé","Trempé et trempé HST façonné sur plan, norme EN 12150."),
          ("/service/vitrages-techniques/","Vitrages techniques","Sécurité, acoustique, coupe-feu, contrôle solaire, sur plan.")])}
</div></section>

<section class="nxp-sec"><div class="wrap">
  <h2>Verres à couche et vitrages isolants</h2>
  {cards([("/service/verre-a-faible-emissivite/","Verre Low-E","Verre à faible émissivité, norme EN 1096."),
          ("/service/verre-reflechissant/","Verre réfléchissant","Contrôle solaire pour façades et climats chauds."),
          ("/service/double-vitrage/","Double vitrage","Fabriqué sur plan, norme EN 1279."),
          ("/service/triple-vitrage/","Triple vitrage","Pour menuiseries et façades à haute performance thermique."),
          ("/service/verre-photovoltaique/","Verre photovoltaïque","Verre extra-clair pour applications solaires.")])}
</div></section>

<section class="nxp-sec nxp-alt"><div class="wrap">
  <h2>Miroirs et verres décoratifs</h2>
  {cards([("/service/miroirs-professionnels/","Miroirs professionnels","Miroir argenté en plateaux pour miroiteries et agenceurs."),
          ("/service/miroir-sans-cuivre-ni-plomb/","Miroir sans cuivre ni plomb","Pour miroiteries et agencement intérieur."),
          ("/service/miroir-antique/","Miroir antique","Effet vieilli pour agenceurs et décorateurs."),
          ("/service/verre-laque/","Verre laqué","Teintes selon nuancier, pour cuisines et agencement."),
          ("/service/verre-emaille-ou-imprime/","Verre émaillé ou imprimé","Réalisé sur plan pour façades et allèges.")])}
</div></section>

<section class="nxp-sec"><div class="wrap">
  <h2>Formats, épaisseurs et normes</h2>
  <table class="nxp-tbl">
    <tr><th>Format standard</th><td>3210 × 2550 mm ; autres dimensions sur demande</td></tr>
    <tr><th>Verre float</th><td>3 – 4 – 5 – 5,5 – 6 – 8 – 10 – 12 – 15 – 19 mm ; plateaux jusqu'à 3300 × 5100 mm</td></tr>
    <tr><th>Normes</th><td>EN 572 (float), EN 1096 (verre à couche), EN 12150 (trempé), EN 12600, EN ISO 12543 et EN 14449 (feuilleté), EN 1279 (vitrage isolant)</td></tr>
    <tr><th>Conditionnement</th><td>Caisses bois sécurisées, sanglage, cales et papier intercalaire entre chaque feuille</td></tr>
  </table>
  <p style="margin-top:14px">Une référence ne figure pas dans la liste ? Nous la recherchons pour vous auprès de nos verriers.</p>
</div></section>

<section class="nxp-sec nxp-alt"><div class="wrap">
  <h2>Comment commander</h2>
  <ul class="nxp-list">
    <li><b>Conteneur complet</b> : pour les transformateurs, négociants et stockistes qui achètent en volume. Pour estimer la quantité : <a href="/combien-m2-verre-conteneur-20-40-pieds/">combien de m² de verre dans un conteneur 20 et 40 pieds</a>.</li>
    <li><b>Livraison panachée</b> : plusieurs références et épaisseurs dans un même transport, pour les miroiteries et les petits et moyens transformateurs.</li>
    <li>Envoyez votre liste (une feuille Excel suffit) avec le lieu de livraison : nous vous adressons un devis détaillé.</li>
  </ul>
  <p style="margin-top:14px">À lire aussi : <a href="/verre-feuillete-33-1-44-2-55-2-signification/">verre feuilleté 33.1, 44.2, 55.2 : que signifient ces chiffres</a> · <a href="/verre-float-clair-vs-verre-float-extra-clair-quelles-differences-guide-complet/">float clair ou extra-clair</a> · <a href="/low-e-ou-verre-reflechissant-climat-chaud/">Low-E ou verre réfléchissant</a>.</p>
</div></section>
"""

# ---------------- /qui-sommes-nous/ ----------------
qui = """
<div class="nxp-hero"><div class="wrap">
  <span class="eyebrow">Qui sommes-nous</span>
  <h1>Noxem Group, importateur et négociant de verre plat</h1>
  <p>Noxem Group fournit du verre plat en volume aux professionnels : transformateurs, miroiteries, fabricants de menuiseries, façadiers et constructeurs de serres. Nous ne sommes pas un verrier : nous sélectionnons les verres auprès de verriers, nous organisons l'achat, le contrôle, l'emballage et le transport, et vous avez un seul interlocuteur.</p>
</div></div>

<section class="nxp-sec"><div class="wrap">
  <h2>Notre métier</h2>
  <ul class="nxp-list">
    <li><b>Achat en volume</b> : conteneur complet ou livraison panachée, selon vos quantités.</li>
    <li><b>Contrôle et emballage</b> : verres mis en caisses bois, sanglés et calés, avec photos et vidéos avant le départ.</li>
    <li><b>Transport</b> : livraison sur votre site en France et en Belgique, et export en conteneur jusqu'à votre port.</li>
  </ul>
  <p style="margin-top:14px">Voir <a href="/produits/">notre gamme de verre plat</a> et <a href="/nos-realisations/">nos chargements en photos</a>.</p>
</div></section>

<section class="nxp-sec nxp-alt"><div class="wrap">
  <h2>Notre organisation</h2>
  <p>Noxem Group (NOXEM GROUP SAS, RCS Lyon 945 290 310) a son siège à Dardilly, près de Lyon. Notre plateforme logistique de Mollem, en Belgique, reçoit, stocke et réexpédie le verre en grand volume : <a href="/logistique/">découvrir notre logistique</a>.</p>
  <p>Noxem Group est une filiale de MONTAUGEM : <a href="/noxem-group-filiale-montaugem/">lire l'article</a>.</p>
</div></section>

<section class="nxp-sec"><div class="wrap">
  <h2>Pour qui nous travaillons</h2>
  <ul class="nxp-list">
    <li><b>Transformateurs et trempeurs</b> : float et feuilleté en plateaux pour alimenter vos lignes.</li>
    <li><b>Miroiteries</b> : miroirs, verres laqués et décoratifs, en conteneur ou panachés.</li>
    <li><b>Fabricants de menuiseries et façadiers</b> : feuilleté, Low-E, contrôle solaire, vitrages sur plan.</li>
    <li><b>Constructeurs de serres</b> : verre en grands volumes, livré en conteneur.</li>
    <li><b>Négociants et importateurs</b> : une chaîne d'achat et de transport coordonnée.</li>
  </ul>
  <p style="margin-top:14px">Nous travaillons uniquement avec des professionnels.</p>
</div></section>

<section class="nxp-sec nxp-alt"><div class="wrap">
  <h2>Le mot du dirigeant</h2>
  <p>Aaron Harfi, président de Noxem Group, présente la vision de l'entreprise dans <a href="/edito/">l'édito du PDG</a>.</p>
  <h2 style="margin-top:28px">La filière verre</h2>
  <p>Noxem Group travaille aux côtés des organisations professionnelles du verre plat : <a href="/partenaires/">voir nos partenaires</a>. Pour suivre nos annonces : <a href="/actualites/">actualités</a> et <a href="/presse/">espace presse</a>.</p>
</div></section>
"""

# ---------------- /contact/ ----------------
contact = """
<div class="nxp-hero"><div class="wrap">
  <span class="eyebrow">Contact</span>
  <h1>Demander un prix de verre plat</h1>
  <p>Indiquez les produits, les épaisseurs, les quantités (ou le nombre de conteneurs) et le lieu de livraison : nous vous adressons un devis détaillé. Noxem Group vend uniquement aux professionnels.</p>
</div></div>

<section class="nxp-sec"><div class="wrap">
  <h2>Nous joindre</h2>
  <table class="nxp-tbl">
    <tr><th>Téléphone</th><td><a href="tel:+33259508459">+33 (0)2 59 50 84 59</a>, du lundi au vendredi, 9 h – 18 h</td></tr>
    <tr><th>WhatsApp</th><td><a href="https://wa.me/33686131271" target="_blank" rel="noopener">+33 6 86 13 12 71</a></td></tr>
    <tr><th>E-mail</th><td><a href="mailto:contact@noxemgroup.com">contact@noxemgroup.com</a></td></tr>
    <tr><th>Siège</th><td>NOXEM GROUP SAS, 5 chemin du Jubin, 69570 Dardilly, France</td></tr>
    <tr><th>Logistique</th><td>Mollem, Belgique : <a href="/logistique/">notre logistique</a></td></tr>
  </table>
</div></section>

<section class="nxp-sec nxp-alt"><div class="wrap">
  <h2>Avant de nous écrire</h2>
  <dl class="nxp-faq">
    <dt>Vendez-vous aux particuliers ?</dt><dd>Non. Nous fournissons les professionnels : transformateurs, miroiteries, fabricants de menuiseries, façadiers, constructeurs de serres, négociants.</dd>
    <dt>Comment achetez-vous : conteneur ou petites quantités ?</dt><dd>En conteneur complet pour les gros volumes, ou en livraison panachée (plusieurs références dans un même transport).</dd>
    <dt>Que faut-il envoyer pour obtenir un prix ?</dt><dd>Références, épaisseurs, dimensions, quantités et lieu de livraison. Une liste Excel suffit. Voir <a href="/produits/">la gamme</a>.</dd>
    <dt>Livrez-vous hors de France ?</dt><dd>Oui, en Belgique et à l'export en conteneur jusqu'à votre port : <a href="/livraison-monde/">livraison dans le monde</a>.</dd>
  </dl>
</div></section>
"""

# ---------------- /fournisseur-verre-plat-france/ ----------------
france = """
<div class="nxp-hero"><div class="wrap">
  <span class="eyebrow">Livraison France et Belgique</span>
  <h1>Fournisseur de verre plat en France pour les professionnels du verre</h1>
  <p>Noxem Group est un importateur et négociant de verre plat. Nous achetons auprès de verriers sélectionnés et nous livrons les professionnels en France et en Belgique : en conteneur complet pour les gros volumes, ou en livraison panachée quand vous avez besoin de plusieurs références sans remplir un conteneur.</p>
  <div class="ctas"><a class="btn" href="#devis">Demander un prix <span class="arr">→</span></a></div>
</div></div>

<section class="nxp-sec"><div class="wrap">
  <h2>Ce que nous livrons</h2>
  <ul class="nxp-list">
    <li><a href="/service/verre-float/">Verre float</a> clair, extra-clair et teinté, en plateaux</li>
    <li><a href="/service/verre-feuillete/">Verre feuilleté</a> de sécurité</li>
    <li><a href="/service/verre-trempe/">Verre trempé</a> et vitrages transformés sur plan</li>
    <li><a href="/service/miroirs-professionnels/">Miroirs</a> et verres décoratifs</li>
    <li><a href="/service/verre-a-faible-emissivite/">Verres à couche Low-E</a> et <a href="/service/verre-reflechissant/">contrôle solaire</a></li>
  </ul>
  <p style="margin-top:14px">Voir <a href="/produits/">toute la gamme</a>.</p>
</div></section>

<section class="nxp-sec nxp-alt"><div class="wrap">
  <h2>Deux façons d'acheter</h2>
  <ul class="nxp-list">
    <li><b>Conteneur complet</b> : pour les transformateurs, négociants et stockistes qui achètent en volume ; une ou plusieurs références en caisses bois, livrées sur votre site. Pour estimer la quantité : <a href="/combien-m2-verre-conteneur-20-40-pieds/">combien de m² de verre dans un conteneur 20 et 40 pieds</a>.</li>
    <li><b>Livraison panachée</b> : pour les miroiteries et les petits et moyens transformateurs, plusieurs références et épaisseurs dans un même transport.</li>
  </ul>
</div></section>

<section class="nxp-sec"><div class="wrap">
  <h2>Pour qui</h2>
  <ul class="nxp-list">
    <li><b>Transformateurs et trempeurs</b> : float et feuilleté en grands formats pour vos lignes.</li>
    <li><b>Miroiteries</b> : miroirs et verres décoratifs, complets ou panachés.</li>
    <li><b>Fabricants de menuiseries et façadiers</b> : feuilleté, Low-E, contrôle solaire, double vitrage sur plan.</li>
    <li><b>Constructeurs de serres</b> : verre en grands volumes, livré en conteneur.</li>
  </ul>
</div></section>

<section class="nxp-sec nxp-alt"><div class="wrap">
  <h2>Une logistique en Belgique, proche du marché français</h2>
  <p>Notre plateforme de Mollem (Belgique) reçoit, stocke et réexpédie le verre en grand volume : <a href="/logistique/">voir notre logistique</a>.</p>
  <h2 style="margin-top:28px">Normes</h2>
  <p>EN 572 (verre float), EN 12150 (verre trempé), EN ISO 12543 et EN 14449 (verre feuilleté), EN 1096 (verre à couche), EN 1279 (vitrage isolant).</p>
</div></section>

<section class="nxp-sec"><div class="wrap">
  <h2>Comment se passe une commande</h2>
  <ol class="nxp-list" style="list-style:decimal">
    <li>Vous envoyez vos références, épaisseurs, quantités et lieu de livraison (une liste Excel suffit).</li>
    <li>Nous vous adressons un devis détaillé, rendu chez vous.</li>
    <li>La commande est confirmée par écrit, puis contrôlée et mise en caisses.</li>
    <li>Nous vous envoyons les photos du chargement avant le départ.</li>
    <li>Le verre est livré sur votre site.</li>
  </ol>
  <dl class="nxp-faq" style="margin-top:20px">
    <dt>Vendez-vous à l'unité ?</dt><dd>Non. Nous fournissons des professionnels, en conteneur complet ou en livraison panachée.</dd>
    <dt>Pouvez-vous fournir une référence absente du catalogue ?</dt><dd>Oui, sur demande : nous la recherchons auprès de nos verriers.</dd>
  </dl>
</div></section>
"""

def prune(html):
    """Retire les règles CSS dont les classes ou id n'existent pas dans la page."""
    body = re.sub(r"<style>.*?</style>", "", html, flags=re.S)
    classes = set(c for cl in re.findall(r'class="([^"]+)"', body) for c in cl.split())
    ids = set(re.findall(r'id="([^"]+)"', body))
    def keep_sel(sel):
        for c in re.findall(r"\.([A-Za-z0-9_-]+)", sel):
            if c not in classes: return False
        for i in re.findall(r"#([A-Za-z0-9_-]+)", sel):
            if i not in ids: return False
        return True
    def rules(css):
        out, i = [], 0
        while i < len(css):
            j = css.find("{", i)
            if j < 0: break
            sel = css[i:j].strip()
            if sel.startswith("@"):
                depth, k = 1, j + 1
                while depth and k < len(css):
                    depth += {"{":1, "}":-1}.get(css[k], 0); k += 1
                if sel.startswith("@media") or sel.startswith("@supports"):
                    inner = rules(css[j+1:k-1])
                    if inner: out.append(sel + "{" + inner + "}")
                else:
                    out.append(css[i:k].strip())
                i = k; continue
            k = css.find("}", j)
            decl = css[j+1:k]
            if sel.startswith("@") or any(keep_sel(x) for x in sel.split(",")):
                out.append(sel + "{" + decl + "}")
            i = k + 1
        return "".join(out)
    return re.sub(r"<style>(.*?)</style>", lambda m: "<style>" + rules(m.group(1)) + "</style>", html, flags=re.S)

OUT = ROOT / "pages"
for name, body, crumb, path in [("produits", produits, "Produits", "/produits/"),
                                ("qui-sommes-nous", qui, "Qui sommes-nous", "/qui-sommes-nous/"),
                                ("contact", contact, "Contact", "/contact/"),
                                ("fournisseur-verre-plat-france", france, "Fournisseur de verre plat en France", "/fournisseur-verre-plat-france/")]:
    html = prune(page(body, crumb, path))
    (OUT / f"{name}.html").write_text(html, encoding="utf-8")
    print(name, len(html.encode()), "octets")
