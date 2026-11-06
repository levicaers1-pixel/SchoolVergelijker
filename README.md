# Basisscholen Antwerpen

Overzicht voor ouders: zoek je straat, zie de basisscholen in de buurt en lees wat de onderwijsinspectie erover schreef. Bewust geen ranking of totaalscore.

Live versie (Claude-dashboard, privé tot je deelt): https://claude.ai/artifact/YPPx5FkQ6ho3nRHJbmwyWX

## Snel starten

```bash
python3 app/maak_preview.py     # maakt app/preview.html
# open app/preview.html in je browser
```

Data opnieuw bouwen (vraagt `pdftotext` van poppler-utils en `pip install -r pipeline/requirements.txt`):

```bash
cd pipeline && ./bouw.sh
```

Dit geeft exact de bestanden in `data/` terug. Rooktest: `npm i playwright && node tests/smoke.js`.

## Structuur

| Map | Inhoud |
|---|---|
| `app/` | `index.html` is de pagina zoals gepubliceerd. `dash-stub.js`, `tokens.css` en `maak_preview.py` laten ze lokaal draaien. |
| `data/` | De zes JSON-bestanden die de pagina gebruikt. |
| `pipeline/` | Van PDF naar JSON. `hand.py` bevat de teksten van de 14 handmatige scholen. |
| `bron/` | CSV van het Vlaams Ministerie van Onderwijs en Vorming, plus open data van Stad Antwerpen. |
| `verslagen/auto/` | 60 PDF's, automatisch verwerkt. |
| `verslagen/handmatig/` | 16 PDF's achter de 14 handmatige schoolrijen, inclusief oudere verslagen. |
| `tests/` | Rooktest met Playwright. |

## Data

**scholen.json**, 74 rijen, één per school: `id`, `nr` (instellingsnummer), `naam`, `net`, `methode`, `adres`, `kleuter`, `lager`, `datum`, `groep`, `groep_naam`, `advies`, `advies_key`, `inbreuken`, `inb_lijst`, `llb`, `gok`, `site`, `sterk`, `letop`, `vraag`, `opschorting`, `historiek`, `auto`.

`advies_key` is `gunstig`, `tekorten`, `ongunstig`, `veiligheid` (ongunstig, alleen gebouwen), `bvh` (gunstig of met tekorten, alleen gebouwen) of `opvolging`.

**scores.json**, 1025 rijen: `id`, `deel`, `onderdeel`, `score`. Score 0 is beneden, 1 benadert, 2 volgens en 3 overstijgt de verwachting. `deel` is `kwaliteit`, `kleuter`, `zorg`, `diversiteit`, `veiligheid` of de naam van een vak in het lager.

**vestigingen.json**, 234 rijen: `nr`, `adres`, `la`, `lo`. Koppelt via `nr` aan scholen en andere.

**andere.json**, 119 rijen: gewone basisscholen in Antwerpen zonder verslag in dit overzicht.

**zones.json**: postzones, `ringen` is tekst in de vorm `lon,lat lon,lat;...`.

**straten.json**, 3663 rijen: `n` naam, `p` postcode, `la`, `lo`. Zoeken werkt dus op straatniveau, zonder externe geocoder.

## Wat je moet weten

- Sterk en Let op zijn bij 60 scholen automatisch afgeleid uit de aanbevelingen. Veld `auto` is dan `true`. Alleen een steekproef is met de originele PDF vergeleken.
- De parser is gecontroleerd op 10 verslagen. `python3 parse.py` in `pipeline/` meldt één verwacht verschil: bij Pulhof lager staat de kolom lichamelijke opvoeding niet in de handmatige data.
- `VANDAAG` staat vast in `samenvoegen.py`. Pas die aan bij een herbouw, want ze bepaalt de groep recent of oud en of een opschorting voorbij is. De pagina zelf rekent met de echte datum.
- Scholen kunnen een recenter verslag hebben dat hier niet in zit. Het script controleert dat niet.
- Verslagen moeten handmatig gedownload worden. `data-onderwijs.vlaanderen.be` sluit automatische toegang uit via robots.txt.
- Het portaal van Stad Antwerpen vermeldt voor de kaartdata geen licentie. Kijk dat na voor een publieke release, net als de juistheid van de samenvattingen.

## Mogelijke volgende stappen

1. Verslagen toevoegen voor de 119 scholen zonder verslag.
2. Eigen app uit het Claude-dashboard halen: `dash-stub.js` toont welke functies je moet vervangen.
3. Het huisnummer meenemen via een geocoder.
4. Zoeken buiten de stad Antwerpen: `bron/basisscholen.csv` dekt heel Vlaanderen.

## Bronnen

Doorlichtingsverslagen: Onderwijsinspectie Vlaanderen. Schoolgegevens: Vlaams Ministerie van Onderwijs en Vorming. Kaart en vestigingen: Stad Antwerpen.
