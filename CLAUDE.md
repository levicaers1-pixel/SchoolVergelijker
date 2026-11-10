# Basisscholen Antwerpen

Zie README.md voor structuur, datamodel en beperkingen.

## Afspraken

- Alle tekst voor gebruikers is in het Nederlands (België).
- Gebruik nooit em dashes in tekst. Gebruik een punt, komma of dubbelpunt. In `app/index.html` is het teken wel de wachtwaarde van een drawing.
- Geen totaalscore en geen ranking. Toon per school de feiten: advies, datum, wat onderzocht werd, inbreuken, en een link naar de officiële fiche.
- Maak geen conclusies die niet in het verslag staan. Een deelverslag (gebouwen of opvolging) zegt niets over de hele school.
- Scholen zonder verslag krijgen geen negatieve lading.
- Haal geen verslagen automatisch op van data-onderwijs.vlaanderen.be. De site sluit dat uit. Verslagen komen handmatig in `verslagen/auto/`.
- Het zoekadres van een gebruiker wordt nergens bewaard of verstuurd.
- Uitzondering, alleen op de website: de stratenkaart laadt kaartbeelden van OpenFreeMap, die zo ziet welk deel van de kaart iemand bekijkt. De zoektekst zelf blijft in de browser. In het Claude-dashboard is er geen netwerk en blijft de getekende kaart.

## Commando's

- Preview: `python3 app/maak_preview.py`, open daarna `app/preview.html`.
- Data bouwen: `cd pipeline && ./bouw.sh`.
- Parser controleren: `cd pipeline && python3 parse.py`.
- Rooktest: `node tests/smoke.js`.

## De website

`python3 app/maak_preview.py --site _site` voegt `webkaart.js` en `webkaart.css` toe (MapLibre van unpkg, stijl `liberty` van OpenFreeMap). `index.html` gebruikt die kaart alleen als `window.bsWebkaart` bestaat, anders tekent ze de eigen kaart. De workflow `.github/workflows/pages.yml` publiceert bij elke push naar `main`.

## De pagina

`app/index.html` volgt de regels van het Claude-dashboard zolang je daarop blijft publiceren:

- De eerste regel is `<meta name="dash-one-writer">`.
- Datagedreven delen zijn `data-draw`-elementen met alleen `—`, gevuld via `dash.draw(naam, fn)`.
- Buiten drawings zetten scripts alleen class, style, hidden, disabled, checked, value en aria-attributen.
- Geen netwerk, opslag of modules. Data komt uit `dash.data(id)`. Toon waarden met `textContent`.
- Thema via tokens zoals `--color-fg`. Een bestand mag maximaal 256 KB zijn.

Stap je over op een eigen app, dan vervallen deze regels. De inhoudelijke afspraken hierboven blijven gelden.
