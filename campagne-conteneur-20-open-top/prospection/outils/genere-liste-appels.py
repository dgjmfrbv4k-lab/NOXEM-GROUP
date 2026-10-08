import io
# Octobre 2026 : Paris = UTC+2 (CEST jusqu'au 25/10). Fenetre locale visee 9h-17h.
# Heure de Paris = (11 - offset) a (19 - offset)
OFF = {
 'États-Unis':-4,'Canada':-4,'Mexique':-6,'Guatemala':-6,'Honduras':-6,'Salvador':-6,'Nicaragua':-6,
 'Costa Rica':-6,'Belize':-6,'Panama':-5,'Colombie':-5,'Pérou':-5,'Équateur':-5,'Jamaïque':-5,
 'Îles Caïmans':-5,'Cuba':-4,'Bahamas':-4,'Bermudes':-3,'Haïti':-4,'République dominicaine':-4,
 'Porto Rico':-4,'Barbade':-4,'Sainte-Lucie':-4,'Trinité-et-Tobago':-4,'Guyana':-4,'Suriname':-3,
 'Aruba':-4,'Curaçao':-4,'Bolivie':-4,'Venezuela':-4,'Martinique':-4,'Guadeloupe':-4,
 'Îles Turques-et-Caïques':-4,'Îles Vierges américaines':-4,'Antigua-et-Barbuda':-4,'Grenade':-4,
 'Saint-Vincent-et-les-Grenadines':-4,'Sint Maarten':-4,'Saint-Martin':-4,'Belize ':-6,
 'Brésil':-3,'Argentine':-3,'Uruguay':-3,'Paraguay':-3,'Chili':-3,
 'Cap-Vert':-1,'Royaume-Uni':1,'Irlande':1,'Portugal':1,
 'Maroc':1,'Ghana':0,'Liberia':0,'Sierra Leone':0,'Gambie':0,'Sénégal':0,'Mali':0,'Burkina Faso':0,
 "Côte d'Ivoire":0,'Togo':0,'Bénin':1,'Nigéria':1,'Niger':1,'Cameroun':1,'Gabon':1,'Tchad':1,
 'Congo (RDC)':1,'Angola':1,'Tunisie':1,'Algérie':1,'Libye':2,'Égypte':3,
 'Afrique du Sud':2,'Namibie':2,'Botswana':2,'Zimbabwe':2,'Zambie':2,'Malawi':2,'Mozambique':2,
 'Eswatini':2,'Lesotho':2,'Rwanda':2,'Burundi':2,'Soudan du Sud':2,
 'Kenya':3,'Ouganda':3,'Tanzanie':3,'Éthiopie':3,'Somalie':3,'Madagascar':3,'Maurice':4,
 'Seychelles':4,'Mayotte':3,'La Réunion':4,'Comores':3,
 'Espagne':2,'France':2,'Belgique':2,'Pays-Bas':2,'Allemagne':2,'Autriche':2,'Suisse':2,'Italie':2,
 'Malte':2,'Albanie':2,'Monténégro':2,'Serbie':2,'Croatie':2,'Bosnie-Herzégovine':2,'Slovaquie':2,
 'Hongrie':2,'Pologne':2,'Roumanie':3,'Bulgarie':3,'Grèce':3,'Chypre':3,'Lettonie':3,'Lituanie':3,
 'Estonie':3,'Finlande':3,'Danemark':2,'Norvège':2,'Suède':2,
 'Géorgie':4,'Arménie':4,'Azerbaïdjan':4,'Kazakhstan':5,'Ouzbékistan':5,
 'Liban':3,'Jordanie':3,'Irak':3,'Yémen':3,'Arabie saoudite':3,'Koweït':3,'Bahreïn':3,'Qatar':3,
 'Oman':4,'Émirats arabes unis':4,
 'Pakistan':5,'Inde':5.5,'Népal':5.75,'Bangladesh':6,'Sri Lanka':5.5,'Maldives':5,
 'Birmanie':6.5,'Thaïlande':7,'Cambodge':7,'Vietnam':7,'Indonésie':7,'Malaisie':8,'Singapour':8,
 'Brunei':8,'Philippines':8,
 'Australie':11,'Nouvelle-Zelande':13,'Fidji':12,'Papouasie-Nouvelle-Guinée':10,'Samoa':13,
 'Tonga':13,'Vanuatu':11,'Îles Salomon':11,'Nouvelle-Calédonie':11,'Polynésie française':-10,
}
def fenetre(pays, tel=''):
    if pays not in OFF: return 'a verifier'
    o=OFF[pays]
    # L'Australie couvre trois decalages : Perth UTC+8, Brisbane UTC+10 sans heure d'ete,
    # cote est UTC+11 en octobre. L'indicatif regional les distingue.
    if pays=='Australie':
        t=tel.replace(' ','')
        if t.startswith('+6189'): o=8          # Perth, Australie-Occidentale
        elif t.startswith(('+6187','+6188')): o=10.5  # Adelaide, Australie-Meridionale
        elif t.startswith('+617'): o=10         # Brisbane, pas d'heure d'ete
        else: o=11                              # Sydney Melbourne, heure d'ete
    def f(h):
        h=(h)%24
        return '%02dh%02d' % (int(h), int(round((h-int(h))*60)))
    return '%s - %s' % (f(11-o), f(19-o))

def score(act, note):
    t=(act+' '+note).lower(); s=0
    if 'importateur' in t or 'import ' in t or 'importation' in t: s+=5
    if 'prioritaire' in t or 'meilleure fiche' in t or 'tres bonne cible' in t: s+=5
    if 'grossiste' in t or 'distributeur' in t or 'distribution' in t or 'negoce' in t or 'negociant' in t: s+=4
    if 'gros :' in t or 'gros:' in t or 'tres grosse' in t or 'major' in t or 'plus gros' in t or 'premier ' in t: s+=4
    if 'trempe' in t or 'feuillet' in t or 'transformat' in t or 'usine' in t or 'fabricant' in t: s+=2
    if 'detail' in t or 'petite structure' in t or 'poseur' in t or 'priorite basse' in t: s-=5
    if 'automobile' in t or 'pare-brise' in t: s-=8
    return s

rows=[]
for l in io.open('liste-prospects.csv',encoding='utf-8').read().split('\n')[1:]:
    if not l.strip(): continue
    c=l.rstrip('\r').split(';')
    if len(c)<10: continue
    if c[7].strip()=='' or c[-1] not in ('A APPELER','A QUALIFIER'): continue
    rows.append((score(c[4],c[8]), c[0], c[3], c[7], c[8], c[-1]))
rows.sort(key=lambda r: (-r[0], r[1]))

EU={'Espagne','France','Belgique','Pays-Bas','Allemagne','Autriche','Suisse','Italie','Malte','Albanie',
 'Monténégro','Serbie','Croatie','Bosnie-Herzégovine','Slovaquie','Hongrie','Pologne','Roumanie',
 'Bulgarie','Grèce','Chypre','Lettonie','Lituanie','Estonie','Finlande','Danemark','Norvège','Suède',
 'Royaume-Uni','Irlande','Portugal'}
hors=[r for r in rows if r[1] not in EU]
eur=[r for r in rows if r[1] in EU]

def tab(rs):
    o=['| Pays | Societe | Telephone | Appeler entre (heure de Paris) | Statut | Pourquoi elle compte |',
       '|---|---|---|---|---|---|']
    for s,pays,soc,tel,note,st in rs:
        n=note.replace('|','/').strip()
        if len(n)>230: n=n[:227]+'...'
        o.append('| %s | **%s** | `%s` | %s | %s | %s |' % (pays,soc,tel,fenetre(pays,tel),st,n))
    return '\n'.join(o)

out=f"""# Liste d'appel NOXEM GROUP — campagne conteneur

Regeneree le **08/10/2026** depuis le registre. **{len(rows)} societes** portent un telephone et
aucune adresse e-mail exploitable. L'e-mail ne peut pas les atteindre : seul le telephone les ouvre.

Tri par valeur commerciale decroissante, calculee sur les marqueurs de la fiche : importateur
declare, grossiste ou distributeur, gros volume, cible prioritaire. Un importateur qui achete
deja au conteneur n'a rien a apprendre, il compare un prix rendu : c'est la conversation la plus
courte et la plus rentable.

**Fenetres d'appel recalculees pour octobre 2026** (Paris = UTC+2 jusqu'au 25/10), pour tomber
entre 9h et 17h chez l'interlocuteur. Attention, deux zones ont change depuis la version du 06/10 :
l'**Australie** et le **Paraguay** sont passes a l'heure d'ete australe, leurs fenetres ont bouge.

## Pourquoi cette liste existe, et ce qui a change le 08/10 apres-midi

**Le diagnostic du matin etait trop pessimiste et il faut le corriger ici aussi.** J'ecrivais que
ces fiches ne s'ouvriraient qu'au telephone, parce que la lecture web est coupee et qu'un annuaire
ne satisfait pas la regle anti-rebond du paragraphe 5. Les deux premieres affirmations restent
vraies. La conclusion, non.

**Une methode de recherche trouvee l'apres-midi en a deverrouille 55 sur 88 testees, soit 62 %** :
recherche large sur le nom de la societe avec les annuaires et les courtiers bloques, pour faire
remonter son domaine propre, puis recherche restreinte a ce domaine pour l'adresse publiee. Trente-
cinq fiches sont ainsi sorties de cette liste dans la journee, et **54 attendent desormais un envoi**.

**Ce qui reste ici est donc un residu, mais un residu reel :** ces {len(rows)} societes ont ete
testees ou n'ont pas de domaine indexe. Deux cas se distinguent :
- celles dont le site n'expose qu'un **formulaire** ou une adresse **obfusquee** — Manna Glass,
  Dr Greiche, Glasshouse, Nawzad NIT, Glass Enterprises, Nassau Glass, Vidrio Centro. Elles
  existent, elles sont grosses, et seul le telephone les ouvre ;
- celles dont le **domaine n'est plus indexe du tout** — a requalifier avant d'y mettre un appel.

Le telephone garde donc sa valeur, mais il n'est plus le seul chemin : c'est **le chemin des
grosses maisons qui protegent leur adresse**, ce qui est precisement le haut de la liste.

## Quatre fiches camerounaises a NE PAS appeler avant verification

AFRICALU, ALUBAT-CAM, ETS Verrerie et METALUX portent une adresse e-mail et aucun rebond, tout en
etant en statut appel. Impossible de savoir si elles ont deja ete contactees : les envois de
septembre partaient de l'ancienne boite `harfiaaron0@gmail.com`, que la session ne lit pas.
**Aaron peut lever le doute en cherchant une de ces adresses dans l'ancienne boite.** D'ici la,
ne pas les appeler en se presentant comme un premier contact.

## Hors Europe — {len(hors)} societes

{tab(hors)}

## Europe — {len(eur)} societes

Rappel du paragraphe 6 : **pas de nouvelle prospection europeenne.** Ces fiches ne s'appellent que
s'il s'agit de relancer un dossier deja ouvert.

{tab(eur)}
"""
io.open('LISTE-APPELS.md','w',encoding='utf-8').write(out)
print('LISTE-APPELS.md regeneree :',len(rows),'fiches |',len(hors),'hors Europe |',len(eur),'Europe')
print('--- top 8 ---')
for r in rows[:8]: print('  %2d  %s | %s | %s' % (r[0],r[1],r[2],fenetre(r[1],r[3])))
