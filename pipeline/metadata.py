import re,glob,os,json,collections
from parse import parse,norm
inv=json.load(open('inv.json'))
out=[]
for r in inv:
    f='../verslagen/auto/'+r['file']+'.pdf'
    s=open(r['txt'],encoding='utf8').read()
    c=re.sub(r'[ \t]+',' ',s)
    typ='OV' if re.search(r'-OV-|-PC-',r['file']) else ('BVH' if '-BVH-' in r['file'] else 'DL')
    rows=norm(parse(f)) if 'OI2_0' in r['file'] or 'DL_VER' in r['file'] else []
    # advies
    m=None
    for m in re.finditer(r'een\s+(ONGUNSTIG|GUNSTIG)\s+ADVIES(\s+waarbij)?',c): pass
    adv=None
    if m: adv='ongunstig' if m.group(1)=='ONGUNSTIG' else ('tekorten' if m.group(2) else 'gunstig')
    if not adv:
        # opvolgings- en PC-verslagen: het advies staat als losse regel
        f=re.findall(r'^\s*(ONGUNSTIG|GUNSTIG|BEPERKT GUNSTIG)\s*$',c,re.M)
        if f: adv={'ONGUNSTIG':'ongunstig','GUNSTIG':'gunstig','BEPERKT GUNSTIG':'tekorten'}[f[-1]]
    llb=re.search(r'Uitspraak over de leerlingenbegeleiding:\s*([A-Za-z ]+?)(?:\.|\n)',c,re.I)
    gok=re.search(r'Uitspraak over het gelijkeonderwijskansenbeleid:\s*([A-Za-z ]+?)(?:\.|\n)',c,re.I)
    ops=re.search(r'opgeschort tot ten minste\s+(\d+\s+\w+\s*\d{4})',c.replace('\n',' '))
    inb=[]
    hs=list(re.finditer(r'^\s*\d+\s+Respecteert de .{0,20}regelgeving\?\s*$',c,re.M|re.I))
    if hs:
        rest=c[hs[-1].end():]
        e=re.search(r'^\s*\d+\s+(Samenvatting|Advies)',rest,re.M|re.I)
        rest=rest[:e.start()] if e else rest
        cur=None
        for l in rest.split('\n'):
            st=l.strip()
            mm=re.match('^[\u2022\uf0b7\uf0a1\uf0a7]\\s*(.+)',st)
            if mm:
                cur=mm.group(1); inb.append(cur)
            elif cur and st and not st.startswith('-') and not re.search(r'bao - |schooljaar|verslag',st,re.I) and not inb[-1].endswith('.'):
                inb[-1]+=' '+st
            elif st.startswith('-') or not st: cur=None if not st else cur
    recs=re.findall(r'[]\s*(De (?:kwaliteit borgen|ontwikkelkansen benutten|tekorten wegwerken)[^]*?)(?=\n\s*[]|\n\s*\n|\Z)',c[c.find('Advies betreffende de erkenning',3000) if 'Advies betreffende de erkenning' in c[3000:] else c.find('ADVIES BETREFFENDE',3000):],re.S)
    recs=[re.sub(r'\s+',' ',x).strip() for x in recs]
    out.append(dict(r,typ=typ,adv=adv,rows=rows,llb=llb and llb.group(1).strip(),gok=gok and gok.group(1).strip(),ops=ops and ops.group(1),inb=inb,recs=recs))
    d=collections.Counter(x[0] for x in rows)
    0 and print(r['file'][-36:].ljust(37),r['nr'],(r['inst'] or '')[:22].ljust(22),typ,adv,dict(d),'|',llb and llb.group(1)[:12],gok and gok.group(1)[:8],ops and ops.group(1),'inb',len(inb),'rec',len(recs))
json.dump(out,open('meta.json','w'),ensure_ascii=False)
