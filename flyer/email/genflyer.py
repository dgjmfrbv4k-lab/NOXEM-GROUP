"""Génère la file au format flyer HTML (texte réel + 6 photos en ligne cid:att0..att5)."""
import json, sys, html, glob, re

FL = '/tmp/claude-0/-home-user-NOXEM-GROUP/c5c42a75-7aa2-5443-ad79-20ab18526fff/scratchpad/flyer/'
TPL = open(FL + 'email_flyer.html').read()
ATT = [
 ("30baa7ed31a4fafc101ba75c21edf9d26000f3561529af2b836780850fd2c6ee", "logo.png", "image/png"),
 ("2ff6a3a407ad31ad4770f6f367cd43db413bebd06e51149fb1d80ec764f80d8b", "hero.jpg", "image/jpeg"),
 ("3236cda0a94153be265a8e6ff90d5add89e056574b4ba72e97705925a36d369c", "load.jpg", "image/jpeg"),
 ("55380cdf8a8ebc93859e443cf7567f7feb1e3da35ba5df8f5f03e04f5cafd5e4", "ship.jpg", "image/jpeg"),
 ("e7543d779b6e26b849452d8f6aea398607d17071bc3cfba73e6c80d1507fdfd2", "flat.jpg", "image/jpeg"),
 ("215f7122198812973576281b04bacff9ab0e24ec246a0726510917e1904e0514", "igu.jpg", "image/jpeg"),
]
ATTACH = [{"content": f"sha256:{h}:{FL}em/{n}", "filename": n, "mimeType": m, "inline": True} for h, n, m in ATT]

SEG = {
 'en': {'menuiserie': ('window and door manufacturing', 'insulated glass units (4/16/4, Low-E, argon) and glass louvre blades'),
        'miroiterie': ('glass processing and glazing', 'clear and extra-clear float glass, tempered and laminated glass, cut to size'),
        'negoce': ('building materials distribution', 'float glass, insulated glass units and louvre blades for resale'),
        'btp': ('construction projects', 'flat glass and insulated glass units for your building sites')},
 'pt': {'menuiserie': ('a fabricação de janelas e portas', 'vidros insulados (4/16/4, Low-E, argônio) e lâminas de vidro para venezianas'),
        'miroiterie': ('o beneficiamento e a instalação de vidros', 'vidro float incolor e extraclaro, vidro temperado e laminado, cortado sob medida'),
        'negoce': ('a distribuição de materiais de construção', 'vidro float, vidros insulados e lâminas para revenda'),
        'btp': ('as suas obras', 'vidro plano e vidros insulados para as suas obras')},
 'es': {'menuiserie': ('la fabricación de ventanas y puertas', 'vidrio insulado (4/16/4, Low-E, argón) y lamas de vidrio para persianas'),
        'miroiterie': ('el procesamiento e instalación de vidrio', 'vidrio float claro y extraclaro, templado y laminado, cortado a medida'),
        'negoce': ('la distribución de materiales de construcción', 'vidrio float, vidrio insulado y lamas para reventa'),
        'btp': ('sus proyectos de construcción', 'vidrio plano y vidrio insulado para sus obras')},
}

T = {
 'en': dict(
  subj='Flat glass by the full container – CIF {port} – NOXEM GROUP',
  bold='Flat glass, insulated glass &amp; louvre blades – delivered CIF {port}, full container, 0% deposit',
  hello='Hello,',
  p1='I came across {co} in {city} and your work in {seg}, and I believe our glass could be a good fit for you.',
  p2='NOXEM GROUP, based in Lyon, France, supplies flat glass, insulated glass units and glass louvre blades made to order, by full container, delivered CIF {port}. We work with 54 partner factories, ship more than 100 containers every month, and offer payment on delivery or at 30 days (subject to our credit insurer\'s approval). For you: {focus}.',
  p3='Our presentation is below.',
  q='Just one question: which products and volumes do you need for your next orders?',
  cat='Full catalogue', regards='Best regards,', pres='President',
  unsub='One-time B2B trade message. If you would prefer not to receive further communications from us, simply reply "UNSUBSCRIBE" and we will remove you from our list.',
  f=None),
 'pt': dict(
  subj='Vidro plano por contêiner completo – CIF {port} – NOXEM GROUP',
  bold='Vidro plano, vidro insulado e lâminas para venezianas – entregues CIF {port}, contêiner completo, 0% de entrada',
  hello='Bom dia,',
  p1='Conheci a empresa {co}, em {city}, e o seu trabalho com {seg}, e acredito que o nosso vidro pode interessar a vocês.',
  p2='A NOXEM GROUP, sediada em Lyon, França, fornece vidro plano, vidros insulados e lâminas de vidro sob encomenda, por contêiner completo, entregues CIF {port}. Trabalhamos com 54 fábricas parceiras, embarcamos mais de 100 contêineres por mês e oferecemos pagamento na entrega ou em 30 dias (sujeito à aprovação da nossa seguradora de crédito). Para vocês: {focus}.',
  p3='A nossa apresentação está logo abaixo.',
  q='Uma única pergunta: quais produtos e volumes vocês precisam para os próximos pedidos?',
  cat='Catálogo completo', regards='Atenciosamente,', pres='Presidente',
  unsub='Mensagem comercial B2B pontual. Se preferir não receber mais comunicações nossas, basta responder "REMOVER" e retiraremos o seu endereço da nossa lista.',
  f=[('NOXEM GROUP · FLAT GLASS', 'NOXEM GROUP · VIDRO PLANO'), ('BY THE FULL CONTAINER · CIF YOUR PORT', 'POR CONTÊINER COMPLETO · CIF NO SEU PORTO'),
     ('DIRECT FROM 54 PARTNER FACTORIES', 'DIRETO DE 54 FÁBRICAS PARCEIRAS'), ('Your glass, made to order,', 'O seu vidro, sob encomenda,'),
     ('delivered to your port.', 'entregue no seu porto.'), ('Float, tempered, laminated, insulated glass and louvre blades — by full container.', 'Vidro float, temperado, laminado, insulado e lâminas para venezianas — por contêiner completo.'),
     ('partner<br>factories', 'fábricas<br>parceiras'), ('containers<br>every month', 'contêineres<br>por mês'), ('delivered<br>to your port', 'entregue<br>no seu porto'),
     ('deposit –<br>pay at 30 days*', 'de entrada –<br>pague em 30 dias*'), ('Loading at the factory', 'Carregamento na fábrica'), ('Shipped CIF to your port', 'Embarque CIF até o seu porto'),
     ('>Flat glass<', '>Vidro plano<'), ('FLOAT · TEMPERED · LAMINATED', 'FLOAT · TEMPERADO · LAMINADO'), ('Clear &amp; extra-clear, 3–19 mm', 'Incolor e extraclaro, 3–19 mm'),
     ('Tinted, reflective, mirror', 'Colorido, refletivo, espelho'), ('Cut to size, edges ground', 'Cortado sob medida, bordas lapidadas'), ('Jumbo or custom sheets', 'Chapas jumbo ou sob medida'),
     ('Insulated glass &amp; louvres', 'Vidro insulado e lâminas'), ('DOUBLE GLAZING · LOUVRE BLADES', 'VIDRO DUPLO · LÂMINAS PARA VENEZIANAS'), ('4/16/4 and custom builds', '4/16/4 e composições sob medida'),
     ('Argon filling, Low-E coating', 'Gás argônio, revestimento Low-E'), ('Louvre blades: clear, frosted', 'Lâminas: incolor, jateado'), ('All lengths, ready to fit', 'Todos os comprimentos, prontas para instalar'),
     ('>Glaziers<', '>Vidraçarias<'), ('Window &amp; door makers', 'Esquadrias'), ('Façade contractors', 'Fachadas'), ('>Greenhouses<', '>Estufas<'), ('>Distributors<', '>Distribuidores<'), ('Building projects', 'Construtoras'),
     ('Free quote<br>for your project', 'Orçamento grátis<br>para o seu projeto'), ('Products, quantities, destination port: we reply fast.', 'Produtos, quantidades, porto de destino: respondemos rápido.'),
     ("*Payment terms subject to our credit insurer's approval of your company. Indicative price, full container. NOXEM GROUP SAS, Lyon, France.", '*Condições de pagamento sujeitas à aprovação da sua empresa pela nossa seguradora de crédito. Contêiner completo. NOXEM GROUP SAS, Lyon, França.'),
     ('alt="Loading at the factory"', 'alt="Carregamento"'), ('alt="Shipped CIF to your port"', 'alt="Embarque"')]),
 'es': dict(
  subj='Vidrio plano por contenedor completo – CIF {port} – NOXEM GROUP',
  bold='Vidrio plano, vidrio insulado y lamas para persianas – entregados CIF {port}, contenedor completo, 0% de anticipo',
  hello='Buenos días,',
  p1='Conocí la empresa {co}, en {city}, y su trabajo en {seg}, y creo que nuestro vidrio puede interesarles.',
  p2='NOXEM GROUP, con sede en Lyon, Francia, suministra vidrio plano, vidrio insulado y lamas de vidrio fabricados a pedido, por contenedor completo, entregados CIF {port}. Trabajamos con 54 fábricas asociadas, despachamos más de 100 contenedores al mes y ofrecemos pago a la entrega o a 30 días (sujeto a la aprobación de nuestra aseguradora de crédito). Para ustedes: {focus}.',
  p3='Nuestra presentación está aquí abajo.',
  q='Una sola pregunta: ¿qué productos y volúmenes necesitan para sus próximos pedidos?',
  cat='Catálogo completo', regards='Saludos cordiales,', pres='Presidente',
  unsub='Mensaje comercial B2B puntual. Si prefiere no recibir más comunicaciones nuestras, simplemente responda "BAJA" y le retiraremos de nuestra lista.',
  f=[('NOXEM GROUP · FLAT GLASS', 'NOXEM GROUP · VIDRIO PLANO'), ('BY THE FULL CONTAINER · CIF YOUR PORT', 'POR CONTENEDOR COMPLETO · CIF SU PUERTO'),
     ('DIRECT FROM 54 PARTNER FACTORIES', 'DIRECTO DE 54 FÁBRICAS ASOCIADAS'), ('Your glass, made to order,', 'Su vidrio, a pedido,'),
     ('delivered to your port.', 'entregado en su puerto.'), ('Float, tempered, laminated, insulated glass and louvre blades — by full container.', 'Vidrio float, templado, laminado, insulado y lamas para persianas — por contenedor completo.'),
     ('partner<br>factories', 'fábricas<br>asociadas'), ('containers<br>every month', 'contenedores<br>al mes'), ('delivered<br>to your port', 'entregado<br>en su puerto'),
     ('deposit –<br>pay at 30 days*', 'de anticipo –<br>pago a 30 días*'), ('Loading at the factory', 'Carga en fábrica'), ('Shipped CIF to your port', 'Envío CIF a su puerto'),
     ('>Flat glass<', '>Vidrio plano<'), ('FLOAT · TEMPERED · LAMINATED', 'FLOAT · TEMPLADO · LAMINADO'), ('Clear &amp; extra-clear, 3–19 mm', 'Claro y extraclaro, 3–19 mm'),
     ('Tinted, reflective, mirror', 'Color, reflectivo, espejo'), ('Cut to size, edges ground', 'Cortado a medida, cantos pulidos'), ('Jumbo or custom sheets', 'Hojas jumbo o a medida'),
     ('Insulated glass &amp; louvres', 'Vidrio insulado y lamas'), ('DOUBLE GLAZING · LOUVRE BLADES', 'DOBLE VIDRIO · LAMAS PARA PERSIANAS'), ('4/16/4 and custom builds', '4/16/4 y composiciones a medida'),
     ('Argon filling, Low-E coating', 'Gas argón, capa Low-E'), ('Louvre blades: clear, frosted', 'Lamas: claras, esmeriladas'), ('All lengths, ready to fit', 'Todos los largos, listas para instalar'),
     ('>Glaziers<', '>Vidrierías<'), ('Window &amp; door makers', 'Ventanas y puertas'), ('Façade contractors', 'Fachadas'), ('>Greenhouses<', '>Invernaderos<'), ('>Distributors<', '>Distribuidores<'), ('Building projects', 'Constructoras'),
     ('Free quote<br>for your project', 'Cotización gratis<br>para su proyecto'), ('Products, quantities, destination port: we reply fast.', 'Productos, cantidades, puerto de destino: respondemos rápido.'),
     ("*Payment terms subject to our credit insurer's approval of your company. Indicative price, full container. NOXEM GROUP SAS, Lyon, France.", '*Condiciones de pago sujetas a la aprobación de su empresa por nuestra aseguradora de crédito. Contenedor completo. NOXEM GROUP SAS, Lyon, Francia.'),
     ('alt="Loading at the factory"', 'alt="Carga"'), ('alt="Shipped CIF to your port"', 'alt="Envío"')]),
}
PRICE_EN = ('<td style="padding:14px 18px"><div style="font-size:12px;color:#6b7785">Clear float glass, from</div><div style="font-size:28px;font-weight:900;color:#c1272d">€{PRICE} / m²</div></td>\n<td align="right" style="padding:14px 18px;font-size:13px;font-weight:bold;color:#2b3e55;line-height:1.5">CIF your port<br>full container</td>')
PRICE_BOX = {'en': ('Your best price, delivered', 'Ask for your quote<br>full container · 0% deposit'),
             'pt': ('O seu melhor preço, entregue', 'Peça o seu orçamento<br>contêiner completo · 0% de entrada'),
             'es': ('Su mejor precio, entregado', 'Pida su cotización<br>contenedor completo · 0% de anticipo')}

SEG['fr'] = {'menuiserie': ('la fabrication de fenêtres et de portes', 'double vitrage (4/16/4, Low-E, argon) et lames de verre pour persiennes'),
             'miroiterie': ('la transformation et la pose de vitrages', 'verre float clair et extra-clair, verre trempé et feuilleté, coupé sur mesure'),
             'negoce': ('la distribution de matériaux de construction', 'verre float, double vitrage et lames pour la revente'),
             'btp': ('le bâtiment et les travaux publics', 'verre plat et double vitrage pour vos chantiers')}
T['fr'] = dict(
  subj='Verre plat par conteneur complet – CIF {port} – NOXEM GROUP',
  bold='Verre plat, double vitrage et lames de persiennes – livrés CIF {port}, conteneur complet, 0 % d\'acompte',
  hello='Bonjour,',
  p1='J\'ai découvert {co}, à {city}, et votre activité dans {seg}, et je pense que notre verre peut vous intéresser.',
  p2='NOXEM GROUP, basée à Lyon, fournit du verre plat, du double vitrage et des lames de verre pour persiennes fabriqués sur commande, par conteneur complet, livrés CIF {port}. Nous travaillons avec 54 usines partenaires, expédions plus de 100 conteneurs chaque mois et proposons le paiement à la livraison ou à 30 jours (sous réserve de l\'accord de notre assureur-crédit). Pour vous : {focus}.',
  p3='Notre présentation est ci-dessous.',
  q='Une seule question : quels produits et quels volumes vous faut-il pour vos prochaines commandes ?',
  cat='Catalogue complet', regards='Cordialement,', pres='Président',
  unsub='Message professionnel ponctuel. Si vous ne souhaitez plus recevoir nos communications, répondez simplement « STOP » et nous vous retirerons de notre liste.',
  f=[('NOXEM GROUP · FLAT GLASS', 'NOXEM GROUP · VERRE PLAT'), ('BY THE FULL CONTAINER · CIF YOUR PORT', 'PAR CONTENEUR COMPLET · CIF VOTRE PORT'),
     ('DIRECT FROM 54 PARTNER FACTORIES', 'EN DIRECT DE 54 USINES PARTENAIRES'), ('Your glass, made to order,', 'Votre verre, sur commande,'),
     ('delivered to your port.', 'livré à votre port.'), ('Float, tempered, laminated, insulated glass and louvre blades — by full container.', 'Verre float, trempé, feuilleté, double vitrage et lames de persiennes — par conteneur complet.'),
     ('partner<br>factories', 'usines<br>partenaires'), ('containers<br>every month', 'conteneurs<br>par mois'), ('delivered<br>to your port', 'livré<br>à votre port'),
     ('deposit –<br>pay at 30 days*', 'd\'acompte –<br>paiement à 30 jours*'), ('Loading at the factory', 'Chargement à l\'usine'), ('Shipped CIF to your port', 'Expédié CIF à votre port'),
     ('>Flat glass<', '>Verre plat<'), ('FLOAT · TEMPERED · LAMINATED', 'FLOAT · TREMPÉ · FEUILLETÉ'), ('Clear &amp; extra-clear, 3–19 mm', 'Clair et extra-clair, 3–19 mm'),
     ('Tinted, reflective, mirror', 'Teinté, réfléchissant, miroir'), ('Cut to size, edges ground', 'Coupé sur mesure, bords façonnés'), ('Jumbo or custom sheets', 'Plateaux jumbo ou sur mesure'),
     ('Insulated glass &amp; louvres', 'Double vitrage et lames'), ('DOUBLE GLAZING · LOUVRE BLADES', 'DOUBLE VITRAGE · LAMES DE PERSIENNES'), ('4/16/4 and custom builds', '4/16/4 et compositions sur mesure'),
     ('Argon filling, Low-E coating', 'Gaz argon, couche Low-E'), ('Louvre blades: clear, frosted', 'Lames : claires, dépolies'), ('All lengths, ready to fit', 'Toutes longueurs, prêtes à poser'),
     ('>Glaziers<', '>Miroitiers<'), ('Window &amp; door makers', 'Menuisiers'), ('Façade contractors', 'Façadiers'), ('>Greenhouses<', '>Serres<'), ('>Distributors<', '>Négociants<'), ('Building projects', 'Entreprises du BTP'),
     ('Free quote<br>for your project', 'Devis gratuit<br>pour votre projet'), ('Products, quantities, destination port: we reply fast.', 'Produits, quantités, port de destination : on vous répond vite.'),
     ("*Payment terms subject to our credit insurer's approval of your company. Indicative price, full container. NOXEM GROUP SAS, Lyon, France.", '*Conditions de paiement sous réserve de l\'accord de notre assureur-crédit sur votre société. Conteneur complet. NOXEM GROUP SAS, Lyon, France.')])
PRICE_BOX['fr'] = ('Votre meilleur prix, livré', 'Demandez votre devis<br>conteneur complet · 0 % d\'acompte')


def build(c, raw=False):
    l = c['lang'] if c['lang'] in T else 'en'
    t = T[l]
    e = lambda s: html.escape(s, quote=False)
    port, city, co = e(c['port']), e(c['city']), e(c['company'])
    seg, focus = SEG[l].get(c['segment'], SEG[l]['negoce'])
    if l == 'pt' and not re.search(r'(?i)^(a|o)\s', c['company']):
        pass
    h = TPL
    a, b = PRICE_BOX[l]
    newbox = (f'<td style="padding:14px 18px"><div style="font-size:12px;color:#6b7785">{a}</div><div style="font-size:28px;font-weight:900;color:#c1272d">CIF {port}</div></td>\n'
              f'<td align="right" style="padding:14px 18px;font-size:13px;font-weight:bold;color:#2b3e55;line-height:1.5">{b}</td>')
    assert PRICE_EN in h
    h = h.replace(PRICE_EN, newbox)
    # intro
    intro_old = h[h.index('<!-- intro text -->'):h.index('<!-- header -->')]
    intro = ('<!-- intro text -->\n<tr><td style="padding:8px 4px 6px;font-size:15px;line-height:1.55;color:#202124">\n'
             f'<p style="margin:0 0 14px"><b>{t["bold"].format(port=port)}</b></p>\n'
             f'<p style="margin:0 0 14px">{t["hello"]}</p>\n'
             f'<p style="margin:0 0 14px">{t["p1"].format(co=co, city=city, seg=seg)}</p>\n'
             f'<p style="margin:0 0 14px">{t["p2"].format(port=port, focus=focus)}</p>\n'
             f'<p style="margin:0 0 14px">{t["p3"]}</p>\n'
             f'<p style="margin:0 0 18px"><b>{t["q"]}</b></p>\n</td></tr>\n')
    h = h.replace(intro_old, intro)
    if t['f']:
        for o, n in t['f']:
            assert o in h or o.startswith("alt="), o
            h = h.replace(o, n)
    h = h.replace('👉 Full catalogue:', f'👉 {t["cat"]}' + (' :' if l == 'fr' else ':')).replace('Best regards,', t['regards']).replace('– President, NOXEM', f'– {t["pres"]}, NOXEM')
    h = h.replace('One-time B2B trade message. If you would prefer not to receive further communications from us, simply reply "UNSUBSCRIBE" and we will remove you from our list.', t['unsub'])
    if raw:
        return h
    h = re.sub(r'<!--.*?-->\n?', '', h)
    assert '{' not in h and 'PRICE' not in h, 'placeholder left'
    txt = re.sub(r'<br>', '\n', intro)
    body = (re.sub(r'<[^>]+>', '', re.sub(r'</p>', '\n\n', txt)).strip() + '\n\n'
            + f'{t["cat"]}' + (' :' if l == 'fr' else ':') + f' https://noxemgroup.com/en/catalog/\n\n{t["regards"]}\nAaron Harfi – {t["pres"]}, NOXEM GROUP SAS, Lyon, France\n+33 2 59 50 84 59 · WhatsApp +33 6 86 13 12 71\naaron.harfi@noxem-group.com\n\n{t["unsub"]}')
    body = re.sub(r'\n{3,}', '\n\n', html.unescape(body))
    return {"to": c['email'], "company": c['company'], "zone": c.get('zone'), "subject": html.unescape(t['subj'].format(port=c['port'])),
            "htmlBody": h, "body": body, "attachments": ATTACH}


if __name__ == '__main__':
    out, inp = sys.argv[1], sys.argv[2]
    q = [build(c) for c in json.load(open(inp))]
    json.dump(q, open(out, 'w'), ensure_ascii=False, indent=1)
    print(len(q), 'emails')


# ===== Format validé : texte + UNE seule grande image flyer (dans la langue du prospect) =====
import hashlib as _h
def _sha(p):
    return _h.sha256(open(p, 'rb').read()).hexdigest()
FLYIMG = {l: FL + f'NOXEM_GROUP_Flyer_{l}.jpg' for l in ['en', 'es', 'pt', 'fr']}
ALT = {'en': 'NOXEM GROUP – flat glass by the full container, CIF your port', 'es': 'NOXEM GROUP – vidrio plano por contenedor completo, CIF su puerto',
       'pt': 'NOXEM GROUP – vidro plano por contêiner completo, CIF no seu porto', 'fr': 'NOXEM GROUP – verre plat par conteneur complet, CIF votre port'}


def build_single(c):
    l = c['lang'] if c['lang'] in T else 'en'
    full = build(c)
    h = full['htmlBody']
    a = h.index('<tr><td style="padding:10px 20px 14px;border-bottom:4px solid #c1272d">')
    b = h.index('<tr><td style="padding:22px 4px 0;font-size:15px;line-height:1.55;color:#202124">')
    img = (f'<tr><td style="padding:4px 0 6px"><img src="cid:att0" width="640" alt="{ALT[l]}" '
           'style="display:block;width:100%;max-width:640px;height:auto;border:0"></td></tr>\n')
    full['htmlBody'] = h[:a] + img + h[b:]
    p = FLYIMG[l]
    full['attachments'] = [{"content": f"sha256:{_sha(p)}:{p}", "filename": f"NOXEM_GROUP_Flyer.jpg", "mimeType": "image/jpeg", "inline": True}]
    return full


if __name__ == '__main__' and len(sys.argv) > 3 and sys.argv[3] == 'single':
    q = [build_single(c) for c in json.load(open(sys.argv[2]))]
    json.dump(q, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
    print(len(q), 'emails (single image)')
