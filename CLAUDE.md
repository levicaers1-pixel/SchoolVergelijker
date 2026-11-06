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

## Commando's

- Preview: `python3 app/maak_preview.py`, open daarna `app/preview.html`.
- Data bouwen: `cd pipeline && ./bouw.sh`.
- Parser controleren: `cd pipeline && python3 parse.py`.
- Rooktest: `node tests/smoke.js`.

## De pagina

`app/index.html` volgt de regels van het Claude-dashboard zolang je daarop blijft publiceren:

- De eerste regel is `<meta name="dash-one-writer">`.
- Datagedreven delen zijn `data-draw`-elementen met alleen `—`, gevuld via `dash.draw(naam, fn)`.
- Buiten drawings zetten scripts alleen class, style, hidden, disabled, checked, value en aria-attributen.
- Geen netwerk, opslag of modules. Data komt uit `dash.data(id)`. Toon waarden met `textContent`.
- Thema via tokens zoals `--color-fg`. Een bestand mag maximaal 256 KB zijn.

Stap je over op een eigen app, dan vervallen deze regels. De inhoudelijke afspraken hierboven blijven gelden.
