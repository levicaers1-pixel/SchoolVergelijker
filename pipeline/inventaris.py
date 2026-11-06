import glob,re,subprocess,os,json
os.makedirs('v',exist_ok=True)
out=[]
for f in sorted(glob.glob('../verslagen/auto/*.pdf')):
    b=os.path.basename(f)[:-4]
    t='v/'+re.sub(r'\W+','_',b)+'.txt'
    subprocess.run(['pdftotext','-layout',f,t])
    s=open(t,encoding='utf8',errors='replace').read()
    c=re.sub(r'[ \t]+',' ',s)
    nr=re.search(r'Instellingsnummer\s+(?:\d+ - )?(\d+)',c)
    inst=re.search(r'Instelling\s+(.+)',c)
    adv=re.findall(r'(ONGUNSTIG ADVIES|GUNSTIG ADVIES waarbij|GUNSTIG ADVIES|BEPERKT GUNSTIG|\nONGUNSTIG\n|\nGUNSTIG\n)',c)
    date=re.search(r'(?:Start- en einddatum doorlichting|Einddatum van het (?:doorlichtingsbezoek|opvolgingsbezoek)|Dagen van het doorlichtingsbezoek|Doorlichtingsdagen|Data van het doorlichtingsbezoek)\s+(.+)',c)
    out.append(dict(file=b,txt=t,nr=nr and nr.group(1),inst=inst and inst.group(1).strip(),adv=adv[:2],date=date and date.group(1)[:50],n=len(s)))
    print(b[:46].ljust(47),out[-1]['nr'],'|',(out[-1]['inst'] or '')[:38],'|',out[-1]['adv'],'|',out[-1]['date'])
json.dump(out,open('inv.json','w'),indent=0)
