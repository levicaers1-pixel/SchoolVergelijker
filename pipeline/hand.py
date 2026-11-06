import json,re,glob
V,B,L,O=2,1,0,3
Q6=["Visie en strategisch beleid","Organisatiebeleid","Onderwijskundig beleid","Cyclische evaluatie","Betrouwbare evaluatie","Borgen en bijsturen"]
Q5=[Q6[0]]+Q6[2:]
MAAT=["Onderwijs en begeleiding op maat","Leer- en ontwikkelingsgerichte aanpak","Materiële leeromgeving","Leerlingenevaluatie"]
KLIM=["Leef- en leerklimaat","Leer- en ontwikkelingsgerichte aanpak","Materiële leeromgeving","Leerlingenevaluatie"]
OUD=["Afstemming op doelenkader","Leer- en ontwikkelingsgericht aanbod","Leer- en leefklimaat","Materiële leeromgeving","Feedback","Evaluatie","Leereffecten"]
BRED=["Afstemming op doelenkader","Begeleiding op de beeldvorming","Positief en inclusief klimaat","Leer- en ontwikkelingsgerichte instructie","Effectieve feedback","Materiële leeromgeving","Leerlingenevaluatie","Leereffecten"]
S=[
dict(id="kolibrie",naam="De Kolibrie",net="Stedelijk",methode="Andere",adres="Sint-Hubertusstraat 13, 2600 Berchem en Markgravelei 149, 2018 Antwerpen",kleuter="ja",lager="ja",
 datum="2024-11-07",groep=1,groep_naam="Gunstig advies, recent verslag",advies="Gunstig",advies_key="gunstig",inbreuken=0,llb="Positief met werkpunten",gok="Positief",lager_vak="Wiskunde",nr=10223,site="https://www.stedelijkonderwijs.be/dekolibrie",
 sterk="De didactische aanpak is volgens verwachting, zowel in de kleuterklas als voor wiskunde in het lager. Leraren werken met een afgesproken instructiemodel.",
 letop="Kinderen met specifieke noden krijgen nog te weinig een planmatige aanpak met duidelijke doelen. De aanpak van begrijpend luisteren en lezen is niet schoolbreed gecoördineerd.",
 vraag="Op welke vestiging zou mijn kind starten, en hoe ziet een begeleidingsplan er concreet uit?",opschorting="",
 kw=[V,V,B,V,V,V],kl=(MAAT,[B,V,V,V]),la=(MAAT,[B,V,V,V]),zo=None),
dict(id="fonkelpad",naam="Het Fonkelpad",net="Stedelijk",methode="Andere",adres="Mellinetplein 13, 2600 Berchem",kleuter="ja",lager="ja",
 datum="2025-06-05",groep=1,groep_naam="Gunstig advies, recent verslag",advies="Gunstig",advies_key="gunstig",inbreuken=0,llb="Positief",gok="Positief",lager_vak="Nederlands",nr=10249,site="https://hetfonkelpad.stedelijkonderwijs.be",
 sterk="Nederlands in het lager scoort op alle vier de onderdelen volgens verwachting. De zorg is planmatig, en de school gebruikt data om bij te sturen.",
 letop="In de kleuterafdeling verschilt de aanpak sterk per klas. Didactiek en evaluatie zitten daar net onder de verwachting. Wiskunde werd niet onderzocht.",
 vraag="Hoe ver staan de gezamenlijke afspraken in de kleuterklassen intussen?",opschorting="",
 kw=[V,V,B,V,V,V],kl=(MAAT,[V,B,V,B]),la=(MAAT,[V,V,V,V]),zo=None),
dict(id="pulhof-kleuter",naam="OLV Pulhof kleuterschool",net="Katholiek",methode="Andere",adres="Floraliënlaan 370/2, 2600 Berchem",kleuter="ja",lager="nee",
 datum="2018-11-09",groep=2,groep_naam="Gunstig advies, oud verslag",advies="Gunstig",advies_key="gunstig",inbreuken=0,llb="",gok="",lager_vak="",nr=10348,site="https://www.pulhof-ks.be",
 sterk="Visie en leer- en leefklimaat overstijgen de verwachting. De speelleeromgeving geldt als voorbeeld van goede praktijk.",
 letop="De afstemming op het leerplan benaderde de verwachting. Teamleden meldden stroefheid in het beleid. Dit is de situatie van 2018.",
 vraag="Is er een recentere doorlichting, en wat is er sinds 2018 veranderd?",opschorting="",
 kw=[O,V,V,V,V,V],kl=(OUD,[B,V,O,V,V,V,V]),la=None,zo=(["Brede basiszorg","Passende begeleiding","Samenwerking met het CLB","Ondersteuning van de leraren"],[V,V,V,V]),ve=[V,V,V,V]),
dict(id="pulhof-lager",naam="OLV Pulhof lagere school",net="Katholiek",methode="Andere",adres="Grotesteenweg 489, 2600 Berchem",kleuter="nee",lager="ja",
 datum="2019-05-24",groep=2,groep_naam="Gunstig advies, oud verslag",advies="Gunstig",advies_key="gunstig",inbreuken=0,llb="",gok="",lager_vak="Nederlands",nr=10306,site="https://www.pulhof-ls.be",
 sterk="Nederlands scoort op alle onderdelen volgens verwachting. Ook lichamelijke opvoeding was sterk, op de evaluatie na.",
 letop="De draagkracht van het team stond onder druk door veel prioriteiten. Zelfstandig leren en probleemoplossend denken hadden groeikansen. Wiskunde werd niet onderzocht.",
 vraag="Is er een recentere doorlichting, en past de katholieke schoolcultuur met uniform bij jullie gezin?",opschorting="",
 kw=[V,V,V,V,B,V],kl=None,la=(OUD,[V,V,V,V,V,V,V]),zo=(["Selectie en aanwerving","Coaching en beoordeling","Professionalisering","Aanvangsbegeleiding"],[V,V,V,V]),ve=[V,V,V,V]),
dict(id="schatkist",naam="De Schatkist",net="Vrij",methode="Andere",adres="Ferdinand Coosemansstraat 15 en 17 en Grotesteenweg 106, 2600 Berchem",kleuter="ja",lager="ja",
 datum="2019-11-22",groep=2,groep_naam="Gunstig advies, oud verslag",advies="Gunstig",advies_key="gunstig",inbreuken=0,llb="",gok="",lager_vak="Wiskunde",lager_vak2="Mens en maatschappij",nr=10314,site="https://www.deschatkistberchem.be",
 sterk="Eigen kwaliteit scoort 6 op 6. Wiskunde in het lager en de leerlingenbegeleiding zijn volledig volgens verwachting. Kleuters zitten in leefgroepen met alle leeftijden samen.",
 letop="De kleuterafdeling had toen geen kindvolgsysteem, en de evaluatie benaderde de verwachting. Nederlands werd niet onderzocht. Dit is de situatie van 2019.",
 vraag="Is er een recentere doorlichting, en hoe volgt de school kleuters nu op?",opschorting="",historiek="",
 kw=[V,V,V,V,V,V],kl=(OUD,[V,V,V,V,V,B,V]),la=(OUD,[V,V,V,V,V,V,V]),la2=(OUD,[V,V,V,V,V,B,V]),zo=(["Brede basiszorg","Passende begeleiding","Samenwerking met het CLB","Ondersteuning van de leraren"],[V,V,V,V]),ve=[V,V,V,V]),
dict(id="kring",naam="De kRing",net="GO!",methode="Freinet",adres="Uitbreidingstraat 251, 2600 Berchem",kleuter="ja",lager="ja",
 datum="2026-05-21",groep=3,groep_naam="Gunstig advies, met tekorten",advies="Gunstig, met tekorten",advies_key="tekorten",inbreuken=1,llb="Positief met werkpunten",gok="Negatief",lager_vak="Wiskunde",nr=118703,site="https://www.de-kring.com",
 sterk="De freinetvisie is zichtbaar in de klas. Wiskunde in het lager scoort volgens verwachting op didactiek en evaluatie, met doorgaans hoge verwachtingen.",
 letop="Zelfsturing en doelgericht leren hangen deels af van de leraar. De school maakt minder expliciet welke minimale leerresultaten ze verwacht. Het tekort gaat over de inzet van SES-lestijden.",
 vraag="Hoe legt de school minimale leerresultaten vast, en hoe beperkt ze verschillen tussen leraren?",opschorting="",historiek="In mei 2015 bevestigde een opvolging dat het tekort voor muzische vorming uit 2012 was weggewerkt.",
 kw=[V,B,V,B,V],kw5=True,kl=(["Leer- en ontwikkelingsgerichte aanpak","Materiële leeromgeving","Leerlingenevaluatie"],[B,V,V]),la=(["Leer- en ontwikkelingsgerichte aanpak","Effectieve feedback","Leerlingenevaluatie"],[V,B,V]),zo=(["Begeleiding volgens het zorgcontinuüm","Professionalisering"],[B,V])),
dict(id="fruithof",naam="Fruithof",net="Stedelijk",methode="Andere",adres="Flor Alpaertsstraat 45, 2600 Berchem",kleuter="ja",lager="ja",
 datum="2025-09-18",groep=3,groep_naam="Gunstig advies, met tekorten",advies="Gunstig, met tekorten",advies_key="tekorten",inbreuken=4,llb="Positief met werkpunten",gok="Negatief",lager_vak="Wiskunde",nr=10256,site="https://fruithof.stedelijkonderwijs.be",
 sterk="Het klimaat is positief en de klasorganisatie goed, zowel in de kleuterklas als in het lager.",
 letop="Afspraken zijn te versnipperd en leraren passen ze verschillend toe. De didactiek zit net onder de verwachting, en hoge verwachtingen stellen is een werkpunt.",
 vraag="Hoe werkt de school aan de vier tekorten, en wat is er al veranderd?",opschorting="",
 kw=[B,V,B,B,V,B],kl=(KLIM,[V,B,V,V]),la=(KLIM,[V,B,V,V]),zo=(["Begeleiding volgens het zorgcontinuüm"],[B])),
dict(id="kleinestan",naam="Kleine Stan",net="Vrij",methode="Andere",adres="Gustaaf Garittestraat 1, 2600 Berchem en Groenenborgerlaan 212, 2610 Wilrijk",kleuter="ja",lager="ja",
 datum="2022-03-25",groep=3,groep_naam="Gunstig advies, met tekorten",advies="Gunstig, met tekorten",advies_key="tekorten",inbreuken=1,llb="",gok="",lager_vak="Nederlands",lager_vak2="Wiskunde",nr=10322,site="https://www.kleinestan.be",
 sterk="Het leef- en leerklimaat is positief en inclusief. Nederlands in het lager scoort sterk, en de leereffecten zijn in alle onderzochte onderdelen volgens verwachting.",
 letop="Begeleiding op maat en feedback zitten in alle onderzochte onderdelen net onder de verwachting. De instructie in de kleuterklas en voor wiskunde laat nog kansen liggen.",
 vraag="Zijn de brandveiligheid en de renovatie intussen in orde, en op welke vestiging zou mijn kind starten?",opschorting="Tekort op bewoonbaarheid, veiligheid en hygiëne: de brandveiligheid in de Gustaaf Garittestraat moest prioritair aangepakt worden, met knelpunten uit 2011 die in 2022 nog openstonden.",
 kw=[V,V,B,B,B,B],kl=(BRED,[V,B,V,B,B,V,B,V]),la=(BRED,[V,B,V,V,B,V,V,V]),la2=(BRED,[V,B,V,B,B,V,V,V]),zo=None,ve=[L,B,B,L]),
dict(id="avontuur",naam="Het Avontuur",net="GO!",methode="Freinet",adres="Filip Williotstraat 11, 2600 Berchem",kleuter="ja",lager="ja",
 datum="2025-02-14",groep=4,groep_naam="Ongunstig advies",advies="Ongunstig",advies_key="ongunstig",inbreuken=3,llb="Negatief",gok="Negatief",lager_vak="Nederlands",nr=128868,site="https://www.hetavontuur.be",
 sterk="Freinettechnieken zijn zichtbaar in de klas, en kleuters krijgen ruimte om te exploreren en problemen op te lossen.",
 letop="Voor heel wat leerlingen ontbrak effectieve remediëring voor lezen en spelling. Er was te weinig oefentijd, en geluidsoverlast beperkt het leren.",
 vraag="Wat is er sinds februari 2025 aantoonbaar verbeterd voor lezen en spelling?",opschorting="Procedure tot intrekking van de erkenning opgeschort tot minstens 14 februari 2028, met externe begeleiding. Daarna volgt een nieuwe doorlichting.",
 kw=[B,V,B,B,B,B],kl=(MAAT,[B,B,B,V]),la=(MAAT,[B,B,B,B]),zo=None),
dict(id="boomhut",naam="De Boomhut",net="Stedelijk",methode="Andere",adres="Ramskapellestraat 43, 2600 Berchem",kleuter="ja",lager="ja",
 datum="2024-11-21",groep=4,groep_naam="Ongunstig advies",advies="Ongunstig",advies_key="ongunstig",inbreuken=4,llb="Negatief",gok="Negatief",lager_vak="Nederlands",nr=10231,site="https://www.stedelijkonderwijs.be/deboomhut",
 sterk="Een groene, warme en laagdrempelige school. De leesdidactiek in het lager is degelijk, met ruime oefenkansen.",
 letop="In de meeste kleuterklassen bestaat het aanbod vooral uit repetitieve activiteiten met lage complexiteit. Alle vier de kleuteronderdelen zitten net onder de verwachting.",
 vraag="Hoe verandert het aanbod in de kleuterklassen, en wat is er al aantoonbaar verbeterd?",opschorting="Procedure tot intrekking van de erkenning opgeschort tot minstens 21 november 2027, met externe begeleiding. Daarna volgt een nieuwe doorlichting.",
 kw=[V,V,B,B,B,B],kl=(MAAT,[B,B,B,B]),la=(MAAT,[B,V,V,B]),zo=None),
dict(id="knikkerbaan",naam="De Knikkerbaan",net="Vrij",methode="Andere",adres="Frederik de Merodestraat 36, 2600 Berchem",kleuter="ja",lager="ja",
 datum="2026-05-21",groep=4,groep_naam="Ongunstig advies",advies="Ongunstig",advies_key="ongunstig",inbreuken=5,llb="Negatief",gok="Negatief",lager_vak="Wiskunde",nr=130153,site="https://www.deknikkerbaan.be",
 sterk="Het klimaat is positief, en de didactiek voor wiskunde in het lager is volgens verwachting.",
 letop="De kleuterevaluatie zit beneden de verwachting: er is geen systeem om de ontwikkeling op te volgen. Verschillende opmerkingen uit de doorlichting van 2016 werden niet aangepakt.",
 vraag="Hoe volgt de school de ontwikkeling van kleuters nu op, en wat is er sinds mei 2026 veranderd?",opschorting="Procedure tot intrekking van de erkenning opgeschort tot minstens 21 mei 2029, met externe begeleiding. Daarna volgt een nieuwe doorlichting.",historiek="In mei 2016 kreeg de school nog een gunstig advies, toen als jonge school in opstart.",
 kw=[B,B,B,L,B],kw5=True,kl=(["Leer- en ontwikkelingsgerichte aanpak","Effectieve feedback","Leerlingenevaluatie"],[B,B,L]),la=(["Leef- en leerklimaat","Leer- en ontwikkelingsgerichte aanpak","Leerlingenevaluatie"],[V,V,B]),zo=(["Begeleiding volgens het zorgcontinuüm","Professionalisering"],[B,B])),
dict(id="heilige-familie",naam="Heilige Familie",net="Vrij",methode="Andere",adres="Jan Moorkensstraat 95, 2600 Berchem",kleuter="ja",lager="ja",
 datum="2025-11-24",groep=5,groep_naam="Ongunstig advies over gebouwen en veiligheid, onderwijs niet onderzocht",advies="Ongunstig, alleen gebouwen en veiligheid",advies_key="veiligheid",inbreuken=1,llb="",gok="",lager_vak="",nr=10331,site="https://www.heilige-familie.be",
 sterk="De school heeft een ruim team eerstehulpverleners en heeft aandacht voor CO2-metingen in de klas.",
 letop="De inspectie noemt de toestand van de sporthal zorgwekkend. Risico's rond elektriciteit, liften en gebouwen keren al jaren terug. Dit verslag zegt niets over de kwaliteit van het onderwijs.",
 vraag="Wat is er sinds november 2025 opgelost aan de sporthal, de elektriciteit en de liften?",opschorting="Procedure tot intrekking van de erkenning opgeschort tot minstens 24 november 2027, met externe begeleiding. Daarna volgt een nieuwe doorlichting.",historiek="",
 kw=[],kl=None,la=None,zo=None,ve=[B,B,B,B]),
dict(id="hinkelpad",naam="Het Hinkelpad",net="Vrij",methode="Andere",adres="Geluwestraat 4, 2600 Berchem",kleuter="ja",lager="ja",
 datum="2026-01-22",groep=5,groep_naam="Ongunstig advies over gebouwen en veiligheid, onderwijs niet onderzocht",advies="Ongunstig, alleen gebouwen en veiligheid",advies_key="veiligheid",inbreuken=1,llb="",gok="",lager_vak="",nr=110569,site="https://www.hethinkelpad.be",
 sterk="De evaluatie van de veiligheid is volgens verwachting, en de school maakte recent een inhaalbeweging. De oplevering van een nieuwbouw is voorzien eind 2026.",
 letop="Verschillende geplande veiligheidsacties bleven jarenlang liggen. Zo was de toegang tot de wenteltrap in de kleuterafdeling en tot de kelder niet degelijk afgeschermd. Dit verslag zegt niets over de kwaliteit van het onderwijs.",
 vraag="Wat is er sinds januari 2026 opgelost, en wanneer is de nieuwbouw klaar?",opschorting="Procedure tot intrekking van de erkenning opgeschort tot minstens 22 januari 2029, met externe begeleiding. Daarna volgt een nieuwe doorlichting.",historiek="",
 kw=[],kl=None,la=None,zo=None,ve=[B,B,V,B]),
dict(id="klavertjevier",naam="Klavertjevier",net="Stedelijk",methode="Andere",adres="Jozef Balstraat 6, 2600 Berchem",kleuter="ja",lager="ja",
 datum="2015-10-01",groep=6,groep_naam="Alleen een oud opvolgingsverslag",advies="Gunstig, alleen opvolging",advies_key="opvolging",inbreuken="n.v.t.",llb="",gok="",lager_vak="",nr=10264,site="https://www.stedelijkonderwijs.be/klavertjevier",
 sterk="In 2015 waren de tekorten voor wereldoriëntatie weggewerkt, met een hernieuwd elan onder een nieuwe directeur.",
 letop="Dit is alleen een opvolging over wereldoriëntatie in het lager. Er is hier geen actueel beeld van Nederlands, wiskunde of de kleuterafdeling.",
 vraag="Is er een recentere volledige doorlichting, en waar kan ik die lezen?",opschorting="",historiek="",
 kw=[],kl=None,la=None,zo=None),
]
rows=[];sc=[]
for s in S:
    kw=s.pop('kw');kw5=s.pop('kw5',False);kl=s.pop('kl');la=s.pop('la');zo=s.pop('zo');la2=s.pop('la2',None);ve=s.pop('ve',None);s.setdefault('lager_vak2','');s.setdefault('historiek','')
    names=Q5 if kw5 else Q6
    assert not kw or len(names)==len(kw)
    for n,v in zip(names,kw): sc.append(dict(id=s['id'],deel="kwaliteit",onderdeel=n,score=v))
    if kl:
        assert len(kl[0])==len(kl[1])
        for n,v in zip(*kl): sc.append(dict(id=s['id'],deel="kleuter",onderdeel=n,score=v))
    if la:
        assert len(la[0])==len(la[1])
        for n,v in zip(*la): sc.append(dict(id=s['id'],deel="lager",onderdeel=n,score=v))
    if la2:
        for n,v in zip(*la2): sc.append(dict(id=s['id'],deel="lager2",onderdeel=n,score=v))
    if ve:
        for n,v in zip(['Planning en uitvoering','Ondersteuning','Cyclische en betrouwbare evaluatie','Borgen en bijsturen'],ve): sc.append(dict(id=s['id'],deel='veiligheid',onderdeel=n,score=v))
    if zo:
        for n,v in zip(*zo): sc.append(dict(id=s['id'],deel="zorg",onderdeel=n,score=v))
    s['kw_ok']=sum(1 for v in kw if v>=2);s['kw_tot']=len(kw)
    rows.append(s)
json.dump(rows,open('scholen.json','w'),ensure_ascii=False,indent=0)
json.dump(sc,open('scores.json','w'),ensure_ascii=False,indent=0)
print(len(rows),len(sc))
