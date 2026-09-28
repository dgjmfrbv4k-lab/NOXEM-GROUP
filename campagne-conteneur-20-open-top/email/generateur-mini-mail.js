// Generateur de mini-mail NOXEM GROUP : 5-8 lignes, langue locale, banniere cliquable
const MAIL='aaron.harfi@noxemgroup.com';
const TEL='+33 7 69 72 58 92';
const WA='https://wa.me/33769725892';
const SITE='https://noxemgroup.com';
const CAT='https://raw.githubusercontent.com/dgjmfrbv4k-lab/NOXEM-GROUP/claude/campagne-conteneur-20-open-fl0382/campagne-conteneur-20-open-top/catalogue/NOXEM-GROUP-catalogue-EN.pdf';

// o = {objet, salut, lignes:[], cta, ctaSub, waTxt, labels:{tel,wa,mail,site,cat}, signature}
function build(o){
  const mailto='mailto:'+MAIL+'?subject='+encodeURIComponent(o.objet);
  const wa=WA+'?text='+encodeURIComponent(o.waTxt||o.objet);
  const L=Object.assign({filiale:'share capital EUR 100,000',capital:'subsidiary of MONTAUGEM, share capital EUR 5,177,000'},o.labels);
  const plain=s=>s.replace(/<[^>]+>/g,'').replace(/&#8242;/g,"'").replace(/&#215;/g,'x').replace(/&#178;/g,'2').replace(/&#8212;/g,'-').replace(/&#8217;/g,"'").replace(/&#233;/g,'e').replace(/&#232;/g,'e').replace(/&#234;/g,'e').replace(/&#224;/g,'a').replace(/&#231;/g,'c').replace(/&#244;/g,'o').replace(/&#249;/g,'u').replace(/&#238;/g,'i').replace(/&#9654;/g,'').replace(/&#183;/g,'-').replace(/&amp;/g,'&').replace(/&nbsp;/g,' ').replace(/&#\d+;/g,'').replace(/&euro;/g,'EUR').replace(/&eacute;|&egrave;|&ecirc;/g,'e').replace(/&agrave;|&acirc;/g,'a').replace(/&ccedil;/g,'c').replace(/&ocirc;/g,'o').replace(/&ugrave;/g,'u').replace(/&icirc;|&iuml;/g,'i').replace(/&[a-zA-Z]+;/g,'');
  const txt=[plain(o.salut),'',...o.lignes.map(plain),'',
    '>>> '+plain(o.cta)+' : '+mailto,
    '',
    plain(L.tel)+' : '+TEL,
    'WhatsApp : '+WA,
    plain(L.mail)+' : '+MAIL,
    plain(L.site)+' : '+SITE,
    plain(L.cat)+' : '+CAT,
    '',plain(o.signature),'Aaron Harfi','NOXEM GROUP - '+plain(L.filiale)+' - '+plain(L.capital),'5 chemin du Jubin, 69570 Dardilly, France - RCS Lyon 945 290 310'].join('\n');

  const html=`<!DOCTYPE html><html><body style="margin:0;padding:0;background-color:#F4F2EE;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#F4F2EE" style="background-color:#F4F2EE;"><tr><td align="center" style="padding:24px 12px;">
<table width="580" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" style="background-color:#FFFFFF;max-width:580px;border:1px solid #E3DCD1;">

<tr><td bgcolor="#1C2430" style="background-color:#1C2430;padding:18px 28px;font-family:Helvetica,Arial,sans-serif;">
<span style="color:#FFFFFF;font-size:21px;font-weight:bold;letter-spacing:3px;">NOXEM</span>
<span style="color:#C1272D;font-size:21px;font-weight:bold;letter-spacing:3px;"> GROUP</span><br>
<span style="color:#9AA4B2;font-size:11px;letter-spacing:1.5px;">${o.baseline}</span>
</td></tr>

<tr><td style="padding:26px 28px 6px;font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.65;color:#2A323D;">
${o.salut}
</td></tr>

<tr><td style="padding:0 28px;font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.7;color:#2A323D;">
${o.lignes.map(l=>'<p style="margin:10px 0;">'+l+'</p>').join('\n')}
</td></tr>

<tr><td align="center" style="padding:22px 28px 6px;">
<table cellpadding="0" cellspacing="0" border="0" width="100%"><tr>
<td align="center" bgcolor="#C1272D" style="background-color:#C1272D;padding:0;">
<a href="${mailto}" style="display:block;padding:15px 20px;font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:bold;color:#FFFFFF;text-decoration:none;letter-spacing:0.5px;">${o.cta} &#9654;</a>
</td></tr></table>
<div style="font-family:Helvetica,Arial,sans-serif;font-size:12px;color:#7A828E;padding-top:7px;">${o.ctaSub}</div>
</td></tr>

<tr><td style="padding:18px 28px 4px;font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:1.6;color:#2A323D;">
${o.signature}<br><strong>Aaron Harfi</strong> &#8212; NOXEM GROUP
</td></tr>

<tr><td style="padding:12px 28px 24px;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#F9F7F3" style="background-color:#F9F7F3;border:1px solid #E6DFD4;">
<tr><td style="padding:14px 18px;font-family:Helvetica,Arial,sans-serif;font-size:13px;line-height:1.85;color:#2A323D;">
<strong style="color:#C1272D;">${L.tel}</strong> <a href="tel:+33769725892" style="color:#2A323D;text-decoration:none;">${TEL}</a><br>
<strong style="color:#25D366;">WhatsApp</strong> <a href="${wa}" style="color:#2A323D;text-decoration:none;">${TEL}</a><br>
<strong style="color:#C1272D;">${L.mail}</strong> <a href="mailto:${MAIL}" style="color:#2A323D;text-decoration:none;">${MAIL}</a><br>
<strong style="color:#C1272D;">${L.site}</strong> <a href="${SITE}" style="color:#2A323D;text-decoration:none;">noxemgroup.com</a><br>
<strong style="color:#C1272D;">${L.cat}</strong> <a href="${CAT}" style="color:#C1272D;text-decoration:none;font-weight:bold;">PDF</a>
</td></tr></table>
</td></tr>

<tr><td bgcolor="#1C2430" style="background-color:#1C2430;padding:11px 28px;font-family:Helvetica,Arial,sans-serif;font-size:11px;color:#9AA4B2;">
NOXEM GROUP &#8212; ${L.filiale} &#8212; ${L.capital}<br>5 chemin du Jubin, 69570 Dardilly, France &#8212; RCS Lyon 945 290 310
</td></tr>

</table></td></tr></table></body></html>`;
  return {txt,html};
}
module.exports={build};
