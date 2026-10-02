# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT

NAVY  = colors.HexColor('#1C2430'); RED = colors.HexColor('#C1272D')
CREAM = colors.HexColor('#F9F7F3'); LINE = colors.HexColor('#E3DCD1')
GREY  = colors.HexColor('#5B6472'); DARK = colors.HexColor('#2A323D')
GREEN = colors.HexColor('#1E7A4B')

OUT='/home/user/NOXEM-GROUP/destockage-verre-plat/devis/NOXEM-devis-VIT-destockage.pdf'

def P(n,s=9,l=12,c=DARK,f='Helvetica',sp=0,a=TA_LEFT):
    return ParagraphStyle(n,fontName=f,fontSize=s,leading=l,textColor=c,spaceAfter=sp,alignment=a)
body=P('b',8.7,11.6,DARK,sp=2); h2=P('h2',10.5,13,NAVY,'Helvetica-Bold',sp=3)
cell=P('c',8.4,10.9); cellb=P('cb',8.4,10.9,DARK,'Helvetica-Bold')
cellr=P('cr',8.4,10.9,DARK,'Helvetica',a=TA_RIGHT); cellrb=P('crb',8.4,10.9,DARK,'Helvetica-Bold',a=TA_RIGHT)
cellh=P('ch',8,10.5,colors.white,'Helvetica-Bold'); cellhr=P('chr',8,10.5,colors.white,'Helvetica-Bold',a=TA_RIGHT)
old=P('o',8.2,10.9,GREY,'Helvetica',a=TA_RIGHT); small=P('s',7.8,10.5,GREY)

def eur(v): return format(v,',.2f').replace(',','\u00a0').replace('.',',') + '\u00a0\u20ac'
def m2(v):  return format(v,',.2f').replace(',','\u00a0').replace('.',',')

def hf(canv,doc):
    w,h=A4; canv.saveState()
    canv.setFillColor(NAVY); canv.rect(0,h-30*mm,w,30*mm,stroke=0,fill=1)
    canv.setFillColor(colors.white); canv.setFont('Helvetica-Bold',19)
    canv.drawString(20*mm,h-17*mm,'NOXEM')
    nw=canv.stringWidth('NOXEM ','Helvetica-Bold',19)
    canv.setFillColor(RED); canv.drawString(20*mm+nw,h-17*mm,'GROUP')
    canv.setFillColor(colors.HexColor('#9AA4B2')); canv.setFont('Helvetica',7.5)
    canv.drawString(20*mm,h-22.5*mm,'VERRE PLAT  ·  DÉSTOCKAGE COMPLET')
    canv.setFillColor(colors.white); canv.setFont('Helvetica-Bold',13)
    canv.drawRightString(w-20*mm,h-15.5*mm,'DEVIS')
    canv.setFillColor(colors.HexColor('#9AA4B2')); canv.setFont('Helvetica',8)
    canv.drawRightString(w-20*mm,h-20.5*mm,'N° D-2026-DEST-VIT-01')
    canv.drawRightString(w-20*mm,h-24.5*mm,'2 octobre 2026')
    canv.setFillColor(NAVY); canv.rect(0,0,w,15*mm,stroke=0,fill=1)
    canv.setFillColor(colors.HexColor('#9AA4B2')); canv.setFont('Helvetica',6.8)
    canv.drawString(20*mm,9.2*mm,'NOXEM GROUP SAS — capital social 100 000 € — filiale de MONTAUGEM, capital social 5 177 000 €')
    canv.drawString(20*mm,6.3*mm,'5 chemin du Jubin, 69570 Dardilly, France — RCS Lyon 945 290 310 — TVA FR88945290310 — APE 46.73A')
    canv.drawString(20*mm,3.4*mm,'aaron.harfi@noxemgroup.com — Tél. / WhatsApp +33 7 69 72 58 92 — noxemgroup.com')
    canv.drawRightString(w-20*mm,3.4*mm,'Page %d'%doc.page)
    canv.restoreState()

doc=BaseDocTemplate(OUT,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,
    topMargin=33*mm,bottomMargin=17*mm,title='NOXEM GROUP - Devis destockage verre plat - VIT',
    author='Aaron Harfi - NOXEM GROUP')
doc.addPageTemplates([PageTemplate(id='m',frames=[Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,
    id='f',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=hf)])
S=[]

# --- bloc client ---
cli=Table([[Paragraph('CLIENT',cellh),Paragraph('LIVRAISON',cellh)],
 [Paragraph('<b>VITRAGE ISOLANT TECHNIQUE (VIT)</b><br/>'
            'M. Vincent Tallarico &#183; M. Michael Labrosse<br/>'
            'ZA de Hautefond &#8212; 233 route de Guichard<br/>71600 Paray-le-Monial, France<br/>'
            'SIRET 321 798 076 00022 &#183; TVA FR91321798076',cell),
  Paragraph('<b>Rendu votre entrep&#244;t</b>, ZA de Hautefond<br/>'
            '<b>5 camions inloader</b> &#8212; 10 piles par camion<br/>'
            'D&#233;chargement lat&#233;ral, pile par pile<br/>'
            '<b>D&#233;lai : 4 &#224; 5 jours</b> &#224; la date de votre choix<br/>'
            '<b>Transport inclus dans les prix</b>',cell)]],
 colWidths=[85*mm,85*mm])
cli.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),
 ('BACKGROUND',(0,1),(-1,1),CREAM),('BOX',(0,0),(-1,-1),0.6,LINE),('INNERGRID',(0,0),(-1,-1),0.4,LINE),
 ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),3.5),('BOTTOMPADDING',(0,0),(-1,-1),3.5),
 ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)]))
for i,c in enumerate(cli._cellvalues[0]):
    pass
S+=[cli,Spacer(1,3.5*mm)]

S.append(Paragraph('D&#201;STOCKAGE COMPLET &#8212; 8 230,66 m&#178; &#8212; FORMAT 2550 &#215; 3210 mm',h2))
S.append(Paragraph('Int&#233;gralit&#233; de notre stock de Mollem (Asse, Belgique). '
  '50 caisses, 6 r&#233;f&#233;rences. <b>Composition des piles au choix du client.</b>',body))
S.append(Spacer(1,1.5*mm))

DATA=[('Verre float Low-E','4 mm',9,2357.42,12.50,8.30),
      ('Miroir argent&#233;','4 mm',10,2373.80,9.84,7.20),
      ('Verre float clair','6 mm',10,1555.25,8.95,5.80),
      ('Verre float clair','8 mm',5,572.99,10.50,6.40),
      ('Verre float clair','10 mm',5,450.20,12.50,7.40),
      ('Verre feuillet&#233; 55.2','10,8 mm',11,921.00,15.50,10.50)]
rows=[[Paragraph('D&#201;SIGNATION',cellh),Paragraph('&#201;PAIS.',cellh),Paragraph('CAISSES',cellhr),
       Paragraph('SURFACE',cellhr),Paragraph('TARIF<br/>DE BASE',cellhr),Paragraph('VOTRE PRIX<br/>AU M&#178;',cellhr),
       Paragraph('REMISE',cellhr),Paragraph('TOTAL HT',cellhr)]]
tb=tp=tm=0; tc=0
for n,e,c,m,b,p in DATA:
    tb+=m*b; tp+=m*p; tm+=m; tc+=c
    rows.append([Paragraph(n,cell),Paragraph(e,cell),Paragraph(str(c),cellr),
        Paragraph(m2(m)+' m&#178;',cellr),Paragraph('<strike>'+('%.2f'%b).replace('.',',')+' €</strike>',old),
        Paragraph('<b>'+('%.2f'%p).replace('.',',')+' €</b>',cellrb),
        Paragraph('<font color="#1E7A4B"><b>'+('%.0f'%((p/b-1)*100))+' %</b></font>',cellr),
        Paragraph(eur(m*p),cellrb)])
t=Table(rows,colWidths=[38*mm,16*mm,16*mm,25*mm,22*mm,24*mm,16*mm,25*mm],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),
 ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,CREAM]),
 ('BOX',(0,0),(-1,-1),0.6,LINE),('INNERGRID',(0,0),(-1,-1),0.4,LINE),
 ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),3.5),('BOTTOMPADDING',(0,0),(-1,-1),3.5),
 ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)]))
S+=[t,Spacer(1,3.5*mm)]

TRANSP=7500.00
tva=tp*0.20; ttc=tp+tva
rec=[[Paragraph('Sous-total marchandise au tarif de base',cell),Paragraph('<strike>'+eur(tb)+'</strike>',old)],
     [Paragraph('Sous-total marchandise remis&#233;',cell),Paragraph(eur(tp),cellr)],
     [Paragraph('<b>Transport</b> &#8212; 5 camions inloader, rendu ZA de Hautefond',cell),
      Paragraph('<strike>'+eur(TRANSP)+'</strike>',cellr)],
     [Paragraph('<font color="#1E7A4B"><b>Remise exceptionnelle sur le transport</b></font>',cell),
      Paragraph('<font color="#1E7A4B"><b>- '+eur(TRANSP)+'</b></font>',cellr)],
     [Paragraph('<b>TOTAL HT &#8212; TRANSPORT INCLUS</b>',cellb),Paragraph('<b>'+eur(tp)+'</b>',cellrb)],
     [Paragraph('<font color="#1E7A4B"><b>Votre &#233;conomie totale</b></font>',cell),
      Paragraph('<font color="#1E7A4B"><b>'+eur(tb-tp+TRANSP)+'</b></font>',cellr)],
     [Paragraph('TVA 20 %',cell),Paragraph(eur(tva),cellr)],
     [Paragraph('<b>TOTAL TTC</b>',cellb),Paragraph('<b>'+eur(ttc)+'</b>',cellrb)]]
rt=Table(rec,colWidths=[110*mm,60*mm])
rt.setStyle(TableStyle([('BACKGROUND',(0,4),(-1,4),colors.HexColor('#FDF3F3')),
 ('BACKGROUND',(0,7),(-1,7),CREAM),('BOX',(0,0),(-1,-1),0.6,LINE),('INNERGRID',(0,0),(-1,-1),0.4,LINE),
 ('TOPPADDING',(0,0),(-1,-1),3.2),('BOTTOMPADDING',(0,0),(-1,-1),3.2),
 ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)]))
S+=[rt,Spacer(1,3.5*mm)]

cmp_txt=('Pour m&#233;moire, votre commande du 29 mai 2026 (devis D-20260000106) portait sur 2 701,22 m&#178; '
 'de feuillet&#233; 33.2 et 44.2 pour 25 453,15 &#8364; HT, soit une <b>moyenne de 9,42 &#8364; le m&#178;</b> &#8212; '
 'des prix que vous aviez vous-m&#234;me qualifi&#233;s de tr&#232;s bons.<br/><br/>'
 'La pr&#233;sente offre ressort &#224; une <b>moyenne de 7,58 &#8364; le m&#178;, transport compris</b>, '
 'soit <b>20 % en dessous</b> de cette r&#233;f&#233;rence.<br/><br/>'
 'En particulier : vous aviez pris du <b>feuillet&#233; 44.2 &#224; 10,55 &#8364;</b>. '
 'Nous vous proposons ici du <b>feuillet&#233; 55.2, plus &#233;pais, &#224; 10,50 &#8364;</b>.')
cb=Table([[Paragraph('COMPARAISON AVEC VOTRE COMMANDE DU 29 MAI 2026',cellh)],[Paragraph(cmp_txt,cell)]],
 colWidths=[170*mm])
cb.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),RED),('BACKGROUND',(0,1),(0,1),CREAM),
 ('BOX',(0,0),(-1,-1),0.6,LINE),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),7),
 ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9)]))
S+=[KeepTogether(cb),Spacer(1,3.5*mm)]

S.append(Paragraph('CONDITIONS',h2))
for x in ['<b>Transport offert</b> &#8212; valoris&#233; 7 500 &#8364;, int&#233;gralement remis. Livraison rendue ZA de Hautefond, 71600 Paray-le-Monial.',
 '<b>5 camions inloader</b>, 10 piles par camion, 50 piles au total. '
 'Composition de chaque pile d&#233;finie par le client.',
 '<b>D&#233;lai : 4 &#224; 5 jours</b> apr&#232;s accord, &#224; la date de votre convenance.',
 'R&#232;glement : <b>30 % &#224; la commande</b> ('+eur(ttc*0.30)+' TTC), '
 '<b>70 % &#224; la livraison</b> ('+eur(ttc*0.70)+' TTC).',
 'Escompte de 2 % pour paiement comptant du solde.',
 '<b>Validit&#233; : 10 jours.</b> Au-del&#224;, notre stock est transf&#233;r&#233; vers notre nouvel entrep&#244;t '
 'et cette offre ne pourra pas &#234;tre reconduite.']:
    S.append(Paragraph('<font color="#C1272D">&#9642;</font>&nbsp;&nbsp;'+x,body))
S.append(Spacer(1,2.5*mm))
S.append(Paragraph('Bon pour accord, le &nbsp;.....................&nbsp; &#8212; signature et cachet :',body))
S.append(Spacer(1,2*mm))
S.append(Paragraph('R&#233;serve de propri&#233;t&#233; : les marchandises demeurent notre propri&#233;t&#233; jusqu\'au paiement int&#233;gral du prix '
 '(loi n°80-335 du 12 mai 1980). Marchandise vendue en l\'&#233;tat, visible sur notre site de Mollem (Asse) avant enl&#232;vement.',small))

doc.build(S)
print('OK',OUT)
print('Total HT %.2f  TVA %.2f  TTC %.2f  base %.2f  eco %.2f  moy %.2f'%(tp,tva,ttc,tb,tb-tp,tp/tm))
