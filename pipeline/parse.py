import re,subprocess,html,collections
G={'':0,'':1,'':2,'':3,'◼':0,'◆':1,'⚫':2}
def words(pdf):
    x=subprocess.run(['pdftotext','-bbox',pdf,'-'],capture_output=True,text=True).stdout
    pages=[]
    for pg in re.findall(r'<page[^>]*>(.*?)</page>',x,re.S):
        w=[(float(a),float(b),float(c),float(d),html.unescape(t)) for a,b,c,d,t in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',pg)]
        pages.append(w)
    return pages
def rowkey(l):
    t=l.lower()
    for k,v in [('afstemming van het aanbod','Afstemming op doelenkader'),('afstemming van de begeleiding','Begeleiding op de beeldvorming'),('onderwijs en begeleiding','Onderwijs en begeleiding op maat'),('klimaat','Leef- en leerklimaat'),('ontwikkelingsgericht','Leer- en ontwikkelingsgerichte aanpak'),('feedback','Effectieve feedback'),('materi','Materiële leeromgeving'),('evaluatie','Leerlingenevaluatie'),('leereffect','Leereffecten'),('curriculum','Curriculum')]:
        if k in t: return v
    return None
QK=[('visie','Visie en strategisch beleid'),('organisatiebeleid','Organisatiebeleid'),('onderwijskundig','Onderwijskundig beleid'),('betrouwbare','Betrouwbare evaluatie'),('cyclische','Cyclische evaluatie'),('systematische','Cyclische evaluatie'),('borgen','Borgen en bijsturen')]
def parse(pdf):
    pages=words(pdf); res=[]; sec=None; started=False
    for w in pages:
        gl=[x for x in w if len(x[4])==1 and x[4] in G]
        up=[x for x in w if not(len(x[4])==1 and x[4] in G)]
        # lijnen
        lines=collections.defaultdict(list)
        for x in up:
            if (x[3]-x[1])>2.5*(x[2]-x[0]) and len(x[4])>3: continue
            lines[round(x[1]/2.5)].append(x)
        ln=sorted([(min(i[1] for i in v),' '.join(i[4] for i in sorted(v))) for v in lines.values()])
        ev=[(t,0,s) for t,s in ln]+[(g[1],1,g) for g in gl]
        ev.sort(key=lambda e:(e[0],e[1]))
        rot=[x for x in w if (x[3]-x[1])>1.5*(x[2]-x[0]) and len(x[4])>2]
        for t,k,v in ev:
            if k==0:
                s=v.lower()
                if re.search(r'legend',s): started=True; sec=None
                if not started: continue
                if re.match(r'^\s*\d?\s*advies betreffende|^\d+\s+advies',s): return res
                if re.search(r'ontwikkelt de (kleuter|lagere |basis)?school haar eigen kwaliteit',s) and 'bijzondere' not in s and re.match(r'^\s*\d',s): sec='kwaliteit'
                elif re.match(r'^\s*\d(\.\d)*\s+.*omgaan met diversiteit',s): sec='diversiteit'
                elif re.match(r'^\s*\d(\.\d)+',s):
                    if 'bewoonbaarheid' in s or 'voert de school een doeltreffend' in s: sec='veiligheid'
                    elif 'onderwijsleerpraktijk' in s: sec='prak'
                    elif 'begeleiding' in s or 'personeel' in s: sec='zorg'
                    elif 'verstrekt' in s: sec=None
            elif started and sec:
                g=v
                if abs(g[2]-g[0])>30: continue
                nb=[l for l in ln if abs(l[0]-g[1])<9]
                # label: tekstwoorden links van glyph op zelfde hoogte; bij afbreking ook vorige/volgende regel
                lw=[x for x in up if x[2]<g[0]+1 and abs(x[1]-g[1])<7 and not (x[3]-x[1])>1.5*(x[2]-x[0])]
                lab=' '.join(i[4] for i in sorted(lw))
                if '=' in lab: continue
                if not lab.strip() or rowkey(lab) is None and sec=='prak':
                    lw=[x for x in up if x[2]<g[0]+1 and abs((x[1]+x[3])/2-(g[1]+g[3])/2)<16 and not (x[3]-x[1])>1.5*(x[2]-x[0])]
                    lab=' '.join(i[4] for i in sorted(lw,key=lambda i:(round(i[1]),i[0])))
                col=''
                if sec=='prak':
                    cw=[x for x in rot if abs((x[0]+x[2])/2-(g[0]+g[2])/2)<24]
                    cw.sort(key=lambda i:(round(i[0]/3),-i[1]))
                    col=' '.join(i[4] for i in cw)
                res.append(dict(sec=sec,lab=lab.strip(),col=col,score=G[g[4]]))
    return res
def norm(rows):
    o=[]
    for r in rows:
        if r['sec']=='kwaliteit':
            n=next((v for k,v in QK if k in r['lab'].lower()),r['lab'])
            o.append(('kwaliteit',n,r['score']))
        elif r['sec']=='prak':
            c=r['col'].lower()
            d='kleuter' if 'kleuter' in c else None
            if not d:
                for k,v in [('nederlands','Nederlands'),('wiskunde','Wiskunde'),('mens','Mens en maatschappij'),('wetenschap','Wetenschappen en techniek'),('lichamelijke','Lichamelijke opvoeding'),('muzisch','Muzische vorming'),('frans','Frans'),('ict','ICT'),('levens','Levensbeschouwing')]:
                    if k in c: d=v;break
            o.append((d or '?'+c[:30],rowkey(r['lab']) or r['lab'],r['score']))
        else:
            o.append((r['sec'],r['lab'],r['score']))
    return o
if __name__=='__main__':
    import sys,json,glob,collections
    sc=json.load(open('scores.json'))
    t={'kolibrie':'10223','fonkelpad':'10249','kring':'118703','fruithof':'10256','avontuur':'128868','boomhut':'10231','knikkerbaan':'130153','pulhof-kleuter':'10348','pulhof-lager':'10306','kleinestan':'10322'}
    for i,n in t.items():
        f=[x for x in glob.glob('../verslagen/*/*.pdf') if f'-{n}-' in x and 'DL3' not in x and 'OV' not in x][0]
        got=norm(parse(f))
        a=collections.Counter((d if not d in('Nederlands','Wiskunde','Mens en maatschappij','Lichamelijke opvoeding') else 'lager',s) for d,_,s in got)
        b=collections.Counter(('lager' if r['deel']=='lager2' else r['deel'],r['score']) for r in sc if r['id']==i)
        # LO zit niet in mijn data
        print(i,len(got),'OK' if a==b else 'VERSCHIL',sorted(set(a.items())^set(b.items()))[:6], [x for x in got if x[0].startswith('?')][:2])
