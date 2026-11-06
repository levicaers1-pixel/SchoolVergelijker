import json,csv,re,math,collections,datetime
from pyproj import Transformer
U='../bron/'
T=Transformer.from_crs(31370,4326,always_xy=True)
VANDAAG=datetime.date(2026,11,5)
hand=json.load(open('scholen.json')); hs=json.load(open('scores.json')); M=json.load(open('meta.json'))
csvr=list(csv.DictReader(open(U+'basisscholen.csv',encoding='utf-8-sig',errors='replace'),delimiter=';'))
PC='2000 2018 2020 2030 2040 2050 2060 2100 2140 2170 2180 2600 2610 2660'.split()
C={x['schoolnummer']:x for x in csvr}
J=json.load(open(U+'stad-antwerpen-scholen.json'))['features']
K=json.load(open(U+'stad-antwerpen-kaart.json'))
ZN={2000:'Antwerpen',2018:'Antwerpen',2020:'Antwerpen',2030:'Antwerpen',2040:'Berendrecht',2050:'Linkeroever',2060:'Antwerpen',2100:'Deurne',2140:'Borgerhout',2170:'Merksem',2180:'Ekeren',2600:'Berchem',2610:'Wilrijk',2660:'Hoboken'}
# zones en straten
def inring(x,y,r):
    c=False;j=len(r)-1
    for i in range(len(r)):
        xi,yi=r[i];xj,yj=r[j]
        if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi)+xi: c=not c
        j=i
    return c
zones=[]
for f in K['zones']['features']:
    a=f['attributes'];zones.append(dict(postcode=int(a['postcode']),district=a['district'],naam=a['naam'],rings=f['geometry']['rings']))
def zone(lat,lon):
    for z in zones:
        if sum(inring(lon,lat,r) for r in z['rings'])%2: return z['postcode']
    return None
per=collections.defaultdict(list)
for n,la,lo in K['streets']:
    n=n.strip()
    if not n: continue
    p=zone(la,lo)
    if p: per[(n,p)].append((la,lo))
straten=[dict(n=n,p=p,la=round(sum(a for a,_ in v)/len(v),4),lo=round(sum(b for _,b in v)/len(v),4)) for (n,p),v in sorted(per.items())]
ptn=[[a,b] for (n,p),v in per.items() for a,b in v]
print('straten',len(straten),'punten',len(ptn))
stidx=collections.defaultdict(list)
for s in straten: stidx[(re.sub(r'\W','',s['n'].lower()))].append(s)
def afst(a,b,c,d):
    return math.hypot((b-d)*111320*math.cos(math.radians(51.2)),(a-c)*111320)
# vestigingen uit stad, gecontroleerd tegen csv en straten
vest=collections.defaultdict(list); nvast=0
for f in J:
    a=f['attributes'];g=f.get('geometry') or {}
    if a.get('SUBTYPE')!='Gewoon Onderwijs': continue
    nr=str(a['SCHOOLNR']);la,lo=g.get('y'),g.get('x')
    if la is None: continue
    st=(a['STRAAT'] or '').strip()
    adres=f"{st} {a['HUISNUMMER'] or ''}".strip()+f", {a['POSTCODE']} {ZN.get(int(a['POSTCODE']),'Antwerpen')}"
    m=[s for s in stidx.get(re.sub(r'\W','',st.lower()),[])]
    bron='stad'
    if m:
        d=min(afst(la,lo,s['la'],s['lo']) for s in m)
        if d>900:
            b=min(m,key=lambda s:(str(s['p'])!=str(a['POSTCODE']),afst(la,lo,s['la'],s['lo'])));la,lo=b['la'],b['lo'];bron='straat';nvast+=1
    vest[nr].append(dict(nr=nr,adres=adres,la=round(la,5),lo=round(lo,5),b=bron))
print('verplaatst naar straat',nvast)
def csvpt(x):
    lo,la=T.transform(float(x['lx'].replace(',','.')),float(x['ly'].replace(',','.')));return round(la,5),round(lo,5)
ncheck=[]
def adr(x): return x['adres'].split(',')[0]+f", {x['postcode']} {ZN[int(x['postcode'])]}"
for nr,x in C.items():
    if x['postcode'] not in PC or not x['lx']: continue
    la,lo=csvpt(x)
    if nr not in vest:
        vest[nr].append(dict(nr=nr,adres=adr(x),la=la,lo=lo,b='csv'))
    else:
        d=min(afst(la,lo,v['la'],v['lo']) for v in vest[nr])
        if d>300: ncheck.append((nr,x['adres'],round(d)));vest[nr].insert(0,dict(nr=nr,adres=adr(x),la=la,lo=lo,b='csv'))
print('hoofdzetel ver van stadspunten (toegevoegd):',ncheck[:12],len(ncheck))
# dubbele punten per school wegwerken
for nr in vest:
    u={}
    for v in vest[nr]: u.setdefault(re.sub(r'\W','',v['adres'].split(',')[0].lower()),v)
    vest[nr]=list(u.values())
def naamk(x):
    n=x['naam'].strip()
    n2=re.sub(r'^(Vrije Basisschool|Vrije basisschool|Vrije Kleuterschool|Vrije Lagere School|Stedelijke Basisschool|Stedelijke Kleuterschool|Stedelijke Lagere School|Gemeentelijke Basisschool|Gemeentelijke Kleuterschool|Gesubsidieerde Vrije Basisschool|VBS|SBS|SKS|GO! Basisschool|GO! basisschool|GO! Kleuterschool|Vrije Basis­school)\s*[-:]?\s*','',n).strip()
    n2=re.sub(r'^(GVBS|GVKS)\s+','',n2)
    n2=re.sub(r'\s+(Merksem|Antwerpen|Ekeren)$','',n2)
    n2=n2[0].upper()+n2[1:] if n2 else n2
    n2=re.sub(r'^De (\w)',lambda m:'De '+m.group(1).upper(),n2)
    if n2.startswith('3hoek') : n2='3Hoek'
    return n2 if len(n2)>2 else f"{n} ({x['straat'].strip()})"
def net(x):
    n=x['net']
    if n.startswith('Gemeen'): return 'GO!'
    if n.startswith('Vrij'): return 'Vrij'
    t=(x['naam']+x.get('beheerder(s)','')+x.get('website','')+x.get('bestuur','')).lower()
    return 'Stedelijk' if ('stedelijk' in t or 'stad antwerpen' in t) else 'Officieel'
def site(x):
    w=(x.get('website') or '').strip()
    if not w or w.lower() in('none','null'): return ''
    return w if w.startswith('http') else 'https://'+w
def afd(x):
    t=x['instellingstype']
    return ('ja' if 'lagere' not in t else 'nee','ja' if 'kleuter' not in t else 'nee')
def methode(n): return 'Freinet' if 'freinet' in n.lower() else 'Andere'
def schoon(z):
    z=z.strip().rstrip('.').strip().rstrip('.')
    e=' (voorwaarde voor erkenning)' if 'erkenningsvoorwaarde' in z else ''
    z=re.sub(r'\.?\s*\(erkenningsvoorwaarde\)','',z).strip().rstrip('.')
    z=re.sub(r'^de onderwijsleerpraktijk voor de onderwijsleerpraktijk in de kleuterafdeling$','de kleuterafdeling',z,flags=re.I)
    z=re.sub(r'^de onderwijsleerpraktijk voor de kleuterafdeling$','de kleuterafdeling',z,flags=re.I)
    z=re.sub(r'^de onderwijsleerpraktijk voor De onderwijsleerpraktijk in de kleuterafdeling$','de kleuterafdeling',z)
    z=re.sub(r'^de onderwijsleerpraktijk in (de kleuterafdeling|het kleuteronderwijs)$','de kleuterafdeling',z)
    m=re.match(r'^de onderwijsleerpraktijk (?:voor )?(.+?) in (?:de lagere afdeling|het lager onderwijs|lager onderwijs|lagere afdeling)$',z,re.I)
    if m:
        v=m.group(1); v='Nederlands' if v.lower()=='nederlands' else v
        z=v+' in het lager'
    z=re.sub(r'^de onderwijsleerpraktijk voor (.+?) in de kleuterafdeling$',lambda m:m.group(1)[0].upper()+m.group(1)[1:]+' in de kleuterafdeling' if m.group(1).lower()=='nederlands' else m.group(1).lower()+' in de kleuterafdeling',z)
    z=re.sub(r'^(het voeren van een doeltreffend beleid op het vlak van )?(de )?bewoonbaarheid, veiligheid en hygiëne$','gebouwen, veiligheid en hygiëne',z)
    z=re.sub(r'^kleuter- (of|en/of) leerlingenevaluatie$','de evaluatie van kinderen',z)
    z=z.replace('de kleuter- en/of leerlingenevaluatie','de evaluatie van kinderen').replace('de leerlingbegeleiding','de leerlingenbegeleiding')
    z=z.replace('de kwaliteitsontwikkeling','de eigen kwaliteitszorg')
    m=re.match(r'^(Mens en Maatschappij en Wetenschappen en Techniek|Lichamelijke Opvoeding)(.*)$',z)
    if m: z=m.group(1).lower()+m.group(2)
    return z+e
def opsom(l):
    return l[0] if len(l)==1 else ', '.join(l[:-1])+' en '+l[-1]
def recs(m):
    o=dict(b=[],k=[],t=[])
    for r in m['recs']:
        for key,p in (('b','De kwaliteit borgen van '),('k','De ontwikkelkansen benutten met betrekking tot '),('t','De tekorten wegwerken met betrekking tot ')):
            if r.startswith(p):
                z=schoon(r[len(p):])
                if z not in o[key]: o[key].append(z)
    return o
MD={1:'januari',2:'februari',3:'maart',4:'april',5:'mei',6:'juni',7:'juli',8:'augustus',9:'september',10:'oktober',11:'november',12:'december'}
def datum(m):
    d=m['date']
    if not d:
        d=re.search(r'Einde doorlichting\s+(\S+)|Data doorlichtingsbezoek\s+(\S+)',open(m['txt'],encoding='utf8').read())
        d=d and (d.group(1) or d.group(2))
    x=re.findall(r'(\d{2})[-/](\d{2})[-/](\d{4})',d)
    a=x[-1];return f'{a[2]}-{a[1]}-{a[0]}'
def opgelost_vakken(m):
    t=open(m['txt'],encoding='utf8').read()
    h=list(re.finditer(r'^\s*2\s+TE REMEDI\w+ TEKORT\(EN\)\s*$',t,re.M))
    if not h: return []
    r=t[h[-1].end():]; r=r[:re.search(r'^\s*3\s+',r,re.M).start()]
    out=[];afd_=''
    for l in r.split('\n'):
        s=l.strip()
        if not s: continue
        if re.match(r'^(Kleuteronderwijs|Lager onderwijs)',s): afd_='kleuter' if s.startswith('Kleuter') else 'lager'; continue
        s2=re.sub(r"^[^\w']+",'',s)
        if 'erkenningsvoorwaarde' in s2: continue
        if 'regelgeving' in s2.lower():
            if 'de regelgeving' not in out: out.append('de regelgeving')
            continue
        s2=s2.replace(' & ',' en ')
        out.append(s2+(' in de '+('kleuterafdeling' if afd_=='kleuter' else 'lagere afdeling') if afd_ else ''))
    return out
# hand-rijen aanvullen
S=[];R=[]
for h in hand:
    h=dict(h);nr=str(h['nr']);x=C.get(nr)
    h['nr']=nr;h['auto']=False;h['inb_lijst']=''
    if h['groep']==6: h['groep_naam']='Alleen een opvolgingsverslag'
    if h['groep']==5: h['groep_naam']='Alleen gebouwen en veiligheid onderzocht'
    h.pop('kw_ok',None);h.pop('kw_tot',None)
    vak={'lager':h.pop('lager_vak',''),'lager2':h.pop('lager_vak2','')}
    for r in hs:
        if r['id']==h['id']:
            d=vak.get(r['deel'],r['deel'])
            R.append(dict(id=h['id'],deel=d or 'Lager',onderdeel=r['onderdeel'],score=r['score']))
    S.append(h)
# automatische rijen
GN={1:'Gunstig advies, recent verslag',2:'Gunstig advies, oud verslag',3:'Gunstig advies, met tekorten',4:'Ongunstig advies',5:'Alleen gebouwen en veiligheid onderzocht',6:'Alleen een opvolgingsverslag'}
log=[]
for m in M:
    nr=m['nr'];x=C[nr];d=datum(m);dd=datetime.date.fromisoformat(d);jaar=(VANDAAG-dd).days/365.25
    if nr=='128876':
        t=open(m['txt'],encoding='utf8').read();m['recs']=[re.sub(r'\s+',' ',z).strip() for z in re.findall(r'•\s*(De kwaliteit borgen[^•]*?)(?=\n\s*•|\n\s*\n)',t,re.S)]
    k,l=afd(x);r=recs(m);naam=naamk(x);typ=m['typ']
    s=dict(id=nr,naam=naam,net=net(x),methode=methode(x['naam']),adres=adr(x),kleuter=k,lager=l,datum=d,nr=nr,site=site(x),auto=True,historiek='',opschorting='',llb=(m['llb'] or '').capitalize(),gok=(m['gok'] or '').capitalize(),inbreuken=len(m['inb']),inb_lijst=' | '.join(i.rstrip('.') for i in m['inb']))
    o=opgelost_vakken(m) if typ=='OV' else []
    if nr=='6072': o=['wereldoriëntatie in de lagere afdeling','lichamelijke opvoeding in de lagere afdeling']
    if typ=='OV':
        s.update(groep=6,advies='Gunstig, alleen opvolging',advies_key='opvolging',inbreuken='n.v.t.')
        if nr=='6635':
            s.update(advies='Geen nieuw advies',sterk='Geen oordeel over het onderwijs in dit verslag.',letop='In november 2018 kon de inspectie geen nieuw advies geven, omdat de vestiging Van Peenestraat niet in gebruik was. Het ongunstig advies van 9 december 2015 vervalt daarmee niet.',vraag='Is er een recentere volledige doorlichting, en hoe staat het met de vestiging Van Peenestraat?')
        elif nr=='128876':
            s.update(sterk='De elementen uit het eerdere ongunstige advies zijn weggewerkt. De inspectie vraagt om dit vast te houden: '+opsom(r['b'])+'.',letop='Dit verslag ging alleen over die elementen, niet over de hele school.',vraag='Is er een recentere volledige doorlichting, en waar kan ik die lezen?')
        else:
            s.update(sterk='De tekorten uit de vorige doorlichting zijn weggewerkt.',letop='Dit verslag ging alleen over '+opsom(o or ['de eerdere tekorten'])+', niet over de hele school.',vraag='Is er een recentere volledige doorlichting, en waar kan ik die lezen?')
    else:
        if typ=='BVH':
            lab={'gunstig':'Gunstig, alleen gebouwen en veiligheid','tekorten':'Gunstig met tekorten, alleen gebouwen en veiligheid','ongunstig':'Ongunstig, alleen gebouwen en veiligheid'}[m['adv']]
            s.update(groep=5,advies=lab,advies_key='veiligheid' if m['adv']=='ongunstig' else 'bvh')
        elif m['adv']=='gunstig':
            s.update(groep=1 if jaar<=5 else 2,advies='Gunstig',advies_key='gunstig')
        elif m['adv']=='tekorten':
            s.update(groep=3,advies='Gunstig, met tekorten',advies_key='tekorten')
        else:
            s.update(groep=4,advies='Ongunstig',advies_key='ongunstig')
        s['sterk']=('De inspectie vraagt om dit vast te houden, want het zit goed: '+opsom(r['b'])+'.') if r['b'] else 'De inspectie noemt geen onderdeel om vast te houden.'
        lo=[]
        if r['t']: lo.append('De school moet tekorten wegwerken bij '+opsom(r['t'])+'.')
        if r['k']: lo.append('Ze kan nog groeien bij '+opsom(r['k'])+'.')
        s['letop']=' '.join(lo) or 'De inspectie noemt geen tekorten of ontwikkelkansen.'
        if typ=='BVH': s['sterk']=s['sterk'].replace('De inspectie vraagt om dit vast te houden, want het zit goed: ','Bij gebouwen en veiligheid zit dit goed: ')
        if typ=='BVH': s['letop']=s['letop'].replace('tekorten wegwerken bij ','tekorten wegwerken bij het veiligheidsbeleid, namelijk ')+' De kwaliteit van het onderwijs werd niet onderzocht.'
        if r['t']: s['vraag']='Wat is er intussen opgelost aan '+re.sub(r' \(voorwaarde voor erkenning\)','',r['t'][0])+', en hoe volgt de school dat op?'
        elif r['k']: s['vraag']='Hoe werkt de school verder aan '+r['k'][0]+'?'
        else: s['vraag']='Wat is er veranderd sinds de doorlichting?'
        if m['ops']:
            mt=m['ops'].split();od=datetime.date(int(mt[2]),[k for k,v in MD.items() if v==mt[1]][0],int(mt[0]))
            s['opschorting']=f"Procedure tot intrekking van de erkenning opgeschort tot minstens {m['ops']}."+(' Die datum is voorbij: vraag naar de nieuwe doorlichting.' if od<VANDAAG else ' Daarna volgt een nieuwe doorlichting.')
        if jaar>5: s['vraag']='Is er een recentere doorlichting? '+s['vraag']
    s['groep_naam']=GN[s['groep']]
    S.append(s)
    for de,on,sc in m['rows']:
        R.append(dict(id=nr,deel=de,onderdeel=on,score=sc))
    log.append((nr,naam,s['net'],k,l,s['groep'],s['advies'],d,len(vest.get(nr,[])),s['site'][:30]))
for l in log: print(l)
for s in S:
    if s['nr'] not in vest: print('GEEN PUNT',s['nr'],s['naam'])
tel=collections.Counter(s['naam'] for s in S)
for s in S:
    if tel[s['naam']]>1: s['naam']+=' ('+s['adres'].split(' ')[0]+')'
V=[v for s in S for v in vest.get(s['nr'],[])]
ids={s['nr'] for s in S}
A=[]
for nr,x in C.items():
    if nr in ids or x['postcode'] not in PC or 'buitengewoon' in x['instellingstype'] or nr not in vest: continue
    k,l=afd(x)
    A.append(dict(nr=nr,naam=naamk(x),net=net(x),methode=methode(x['naam']),adres=adr(x),kleuter=k,lager=l,site=site(x)))
    V+=vest[nr]
print(len(S),len(R),len(V),len(A))
Z=[dict(postcode=z['postcode'],district=z['district'],ringen=';'.join(' '.join(f'{a},{b}' for a,b in r) for r in z['rings'])) for z in zones]
for n,o in (('scholen',S),('scores',R),('vestigingen',[{k:v for k,v in x.items() if k!='b'} for x in V]),('andere',A),('zones',Z),('straten',straten),):
    json.dump(o,open(f'../data/{n}.json','w'),ensure_ascii=False,separators=(',',':'))
import os
print({f:os.path.getsize('../data/'+f)//1024 for f in os.listdir('../data')})
