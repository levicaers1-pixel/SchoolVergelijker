#!/usr/bin/env bash
# Bouwt data/*.json opnieuw uit bron/ en verslagen/. Draai vanuit de map pipeline/.
set -euo pipefail
python3 hand.py          # 14 handmatig samengevatte scholen -> scholen.json, scores.json
python3 inventaris.py    # pdftotext -> v/*.txt en inv.json
python3 metadata.py      # advies, scores, inbreuken, aanbevelingen -> meta.json
python3 samenvoegen.py   # alles samen -> ../data/*.json
