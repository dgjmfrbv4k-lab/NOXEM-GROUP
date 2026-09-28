# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)
from reportlab.lib.enums import TA_LEFT

NAVY  = colors.HexColor('#1C2430')
RED   = colors.HexColor('#C1272D')
CREAM = colors.HexColor('#F9F7F3')
LINE  = colors.HexColor('#E3DCD1')
GREY  = colors.HexColor('#5B6472')
DARK  = colors.HexColor('#2A323D')

OUT = '/home/user/NOXEM-GROUP/campagne-conteneur-20-open-top/achats/NOXEM-RFQ-2026-09-28-Namibia.pdf'

def P(name, size=9.5, leading=14, color=DARK, font='Helvetica', space=0):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading,
                          textColor=color, alignment=TA_LEFT, spaceAfter=space)

body   = P('body', 9.0, 12.4, DARK, space=3)
bodyb  = P('bodyb', 9.8, 14.5, DARK, 'Helvetica-Bold', space=5)
h2     = P('h2', 10.5, 13, NAVY, 'Helvetica-Bold', space=3)
small  = P('small', 8.2, 11.5, GREY)
cell   = P('cell', 8.7, 11.8, DARK)
cellb  = P('cellb', 8.7, 11.8, DARK, 'Helvetica-Bold')
cellh  = P('cellh', 8.4, 11.5, colors.white, 'Helvetica-Bold')
bullet = P('bullet', 8.9, 12.0, DARK, space=0)

def header_footer(canv, doc):
    w, h = A4
    canv.saveState()
    # bandeau haut
    canv.setFillColor(NAVY); canv.rect(0, h-30*mm, w, 30*mm, stroke=0, fill=1)
    canv.setFillColor(colors.white); canv.setFont('Helvetica-Bold', 19)
    canv.drawString(20*mm, h-17*mm, 'NOXEM')
    nw = canv.stringWidth('NOXEM ', 'Helvetica-Bold', 19)
    canv.setFillColor(RED); canv.drawString(20*mm+nw, h-17*mm, 'GROUP')
    canv.setFillColor(colors.HexColor('#9AA4B2')); canv.setFont('Helvetica', 7.5)
    canv.drawString(20*mm, h-22.5*mm, 'FLAT GLASS  ·  FULL CONTAINER EXPORT')
    canv.setFillColor(colors.white); canv.setFont('Helvetica-Bold', 12)
    canv.drawRightString(w-20*mm, h-16*mm, 'REQUEST FOR QUOTATION')
    canv.setFillColor(colors.HexColor('#9AA4B2')); canv.setFont('Helvetica', 8)
    canv.drawRightString(w-20*mm, h-21.5*mm, 'Ref. NX-RFQ-2609-NAM   ·   28 September 2026')
    # bandeau bas
    canv.setFillColor(NAVY); canv.rect(0, 0, w, 15*mm, stroke=0, fill=1)
    canv.setFillColor(colors.HexColor('#9AA4B2')); canv.setFont('Helvetica', 7.2)
    canv.drawString(20*mm, 8.6*mm, 'NOXEM GROUP  —  subsidiary of MONTAUGEM  —  share capital EUR 5,177,000  —  5 chemin du Jubin, 69570 Dardilly, France  —  RCS Lyon 945 290 310')
    canv.drawString(20*mm, 5.2*mm, 'Aaron Harfi  —  aaron.harfi@noxemgroup.com  —  Tel / WhatsApp +33 7 69 72 58 92  —  noxemgroup.com')
    canv.drawRightString(w-20*mm, 5.2*mm, 'Page %d' % doc.page)
    canv.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                      topMargin=34*mm, bottomMargin=17*mm,
                      title='NOXEM GROUP - Request for Quotation - Namibia',
                      author='Aaron Harfi - NOXEM GROUP')
frame = Frame(doc.leftMargin, doc.bottomMargin,
              doc.width, doc.height, id='f', leftPadding=0, rightPadding=0,
              topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=header_footer)])

S = []

# --- bloc destinataire ---
info = Table([[Paragraph('<b>To</b>', cell),  Paragraph('Ramon', cell),
               Paragraph('<b>From</b>', cell), Paragraph('Aaron Harfi — NOXEM GROUP', cell)],
              [Paragraph('<b>Subject</b>', cell),
               Paragraph('New enquiry — 4 full 20′ containers, delivered Walvis Bay, Namibia', cell),
               Paragraph('<b>Reply by</b>', cell),
               Paragraph('As soon as you can — the customer is selecting now', cell)]],
             colWidths=[22*mm, 68*mm, 22*mm, 58*mm])
info.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1), CREAM),
    ('BOX',(0,0),(-1,-1), 0.6, LINE),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('TOPPADDING',(0,0),(-1,-1),4), ('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),8), ('RIGHTPADDING',(0,0),(-1,-1),8),
]))
S += [info, Spacer(1, 4*mm)]

S.append(Paragraph('Ramon,', body))
S.append(Paragraph(
    'I have just received a new enquiry and I want you to price it with me.', body))
S.append(Paragraph(
    'The customer is a <b>major glass distribution and installation group in Southern Africa</b>, with a network of '
    'branches across several countries. They run their own float plant in the region, but they buy laminated glass '
    'from outside — and they are <b>selecting their suppliers right now</b>. They have asked me for a price '
    '<b>CIF Walvis Bay, Namibia</b>, with the freight shown on a separate line. They have confirmed <b>standard closed 20\u2032 containers</b> \u2014 no Open Top.', body))
S.append(Spacer(1, 2*mm))

S.append(Paragraph('WHAT THEY ARE ASKING FOR', h2))
S.append(Paragraph('<b>One full 20′ container per product</b>, cut to the finished sizes below.', body))
S.append(Spacer(1, 2*mm))

rows = [[Paragraph('#', cellh), Paragraph('PRODUCT', cellh), Paragraph('MAKE-UP', cellh),
         Paragraph('FINISHED SIZE', cellh), Paragraph('QUANTITY', cellh)],
        [Paragraph('1', cellb), Paragraph('Clear Float', cell), Paragraph('4 mm, Grade A', cell),
         Paragraph('1830 × 2440 mm', cellb), Paragraph('1 × 20′ full', cell)],
        [Paragraph('2', cellb), Paragraph('Clear Laminated', cell), Paragraph('6.38 — 3 + 3 + 0.38 clear PVB', cell),
         Paragraph('2440 × 2000 mm', cellb), Paragraph('1 × 20′ full', cell)],
        [Paragraph('3', cellb), Paragraph('Grey Tinted Laminated', cell), Paragraph('6.38 — see note below', cell),
         Paragraph('2440 × 2000 mm', cellb), Paragraph('1 × 20′ full', cell)],
        [Paragraph('4', cellb), Paragraph('White Translucent Laminated', cell),
         Paragraph('6.38 — white translucent PVB', cell),
         Paragraph('2440 × 2000 mm', cellb), Paragraph('1 × 20′ full', cell)]]
t = Table(rows, colWidths=[9*mm, 42*mm, 53*mm, 33*mm, 33*mm], repeatRows=1)
t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), NAVY),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, CREAM]),
    ('BOX',(0,0),(-1,-1), 0.6, LINE),
    ('INNERGRID',(0,0),(-1,-1), 0.4, LINE),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),4), ('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),7), ('RIGHTPADDING',(0,0),(-1,-1),7),
]))
S += [t, Spacer(1, 4*mm)]

S.append(Paragraph('WHAT I NEED FROM YOU, LINE BY LINE', h2))
for txt in [
    '<b>FOB price per m²</b> and the <b>total per 20′ container</b>',
    '<b>CIF Walvis Bay, Namibia</b> — with the <b>freight on a separate line</b> (the customer asked for this explicitly)',
    'How many <b>m²</b> and how many <b>sheets</b> you load per 20′',
    '<b>Production lead time</b> and your earliest loading slot',
    '<b>Payment terms</b>, and how long the price stays valid',
    'Confirm the crates go in through the <b>doors of a standard closed 20\u2032</b> (2.34 \u00d7 2.28 m opening)',
    'Which <b>certificates</b> come with the goods',
]:
    S.append(Paragraph('<font color="#C1272D">▪</font>&nbsp;&nbsp;' + txt, bullet))
S.append(Spacer(1, 3*mm))

note_txt = (
    '<b>1. Cut to size, not jumbo.</b> Please quote these as <b>finished sizes produced to measure</b>. '
    'Cutting 2440 × 2000 out of a 3210 × 2550 jumbo wastes about 40 % of the sheet and the price would '
    'be out of the market before we start.<br/><br/>'
    '<b>2. The grey tinted is ambiguous.</b> Is it <b>body-tinted grey float</b> (3 mm grey + 3 mm clear), or a '
    '<b>grey PVB interlayer</b> between two clear? <b>Please quote both</b> — I will confirm with the customer '
    'which one they mean.<br/><br/>'
    '<b>3. The white must be translucent</b>, not opaque. White / opal translucent PVB, 0.38 mm.')
note = Table([[Paragraph('TECHNICAL POINTS — PLEASE READ BEFORE QUOTING', cellh)],
              [Paragraph(note_txt, cell)]], colWidths=[170*mm])
note.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(0,0), RED),
    ('BACKGROUND',(0,1),(0,1), CREAM),
    ('BOX',(0,0),(-1,-1), 0.6, LINE),
    ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),6),
    ('LEFTPADDING',(0,0),(-1,-1),9), ('RIGHTPADDING',(0,0),(-1,-1),9),
]))
S += [KeepTogether(note), Spacer(1, 4*mm)]

S.append(Paragraph('AND ONE THING, RAMON', h2))
S.append(Paragraph(
    '<b>Give me your very best price on this one.</b> These are serious, well established companies — not a '
    'one-off buyer. They move volume every month, they are picking their suppliers for the coming period, and if we '
    'win this first order the repeat business follows behind it.', body))
S.append(Paragraph(
    'I would rather come back to them with a sharp number straight away than negotiate three times. '
    'Price it as if the whole account depends on it, because it does.', body))
S.append(Spacer(1, 2.5*mm))
S.append(Paragraph('Thank you — and please come back to me quickly.', body))
S.append(Spacer(1, 1.5*mm))
S.append(Paragraph('<b>Aaron Harfi</b> \u2014 NOXEM GROUP, subsidiary of MONTAUGEM, share capital EUR 5,177,000<br/>'
                   'Tel / WhatsApp +33 7 69 72 58 92 \u00b7 aaron.harfi@noxemgroup.com', body))

doc.build(S)
print('OK', OUT)
