// Stratenkaart voor de website (GitHub Pages), met MapLibre en kaarten van OpenFreeMap.
// index.html gebruikt dit alleen als window.bsWebkaart bestaat. In het Claude-dashboard
// ontbreekt dit bestand en blijft de getekende kaart zonder netwerk gelden.
// Privacy: OpenFreeMap ziet welke kaartdelen geladen worden, niet wat iemand in het zoekveld typt.
(() => {
  const ML = window.maplibregl;
  if (!ML) return; // Bibliotheek niet geladen (offline): val terug op de getekende kaart.
  const donker = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const STIJL = 'https://tiles.openfreemap.org/styles/' + (donker ? 'dark' : 'liberty');
  const COS = Math.cos(51.2 * Math.PI / 180);
  const M_PER_GRAAD = 111320;

  const NS = 'http://www.w3.org/2000/svg';
  const vec = (tag, attrs) => {
    const e = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => e.setAttribute(k, v));
    return e;
  };
  const VORMEN = {
    gunstig: (hol) => ['circle', {r: hol ? 4.6 : 5.5}],
    tekorten: (hol) => ['path', {d: hol ? 'M0-5.6L5.6 0 0 5.6-5.6 0z' : 'M0-6.5L6.5 0 0 6.5-6.5 0z'}],
    ongunstig: () => ['rect', {x: -5, y: -5, width: 10, height: 10}],
    deel: () => ['circle', {r: 3.5}],
    geen: () => ['circle', {r: 2.5}],
  };
  const speld = (soort, hol, gekozen, ver, label) => {
    const knop = document.createElement('button');
    knop.type = 'button';
    knop.className = 'bs-pin bs-webpin' + (ver ? ' bs-ver' : '') + (gekozen ? ' bs-gekozen' : '');
    knop.setAttribute('aria-label', label);
    const svg = vec('svg', {width: 24, height: 24, viewBox: '-12 -12 24 24', 'aria-hidden': 'true'});
    const [tag, attrs] = VORMEN[soort](hol);
    svg.appendChild(vec(tag, {...attrs, class: 'bs-k-' + soort + (hol ? ' bs-hol' : '')}));
    if (gekozen) svg.appendChild(vec('circle', {r: 10, class: 'bs-sel'}));
    knop.appendChild(svg);
    return knop;
  };
  const thuisSpeld = () => {
    const d = document.createElement('div');
    d.className = 'bs-webthuis';
    const svg = vec('svg', {width: 26, height: 34, viewBox: '-13 -20 26 34', 'aria-hidden': 'true'});
    svg.appendChild(vec('path', {d: 'M0-19C-6.5-19-10.5-14-10.5-8.5c0 7 10.5 21 10.5 21s10.5-14 10.5-21C10.5-14 6.5-19 0-19z'}));
    svg.appendChild(vec('circle', {r: 3.8, cy: -8.5}));
    d.appendChild(svg);
    return d;
  };
  const vak = (la, lo, km) => {
    const dla = km * 1000 / M_PER_GRAAD;
    const dlo = dla / COS;
    return [[lo - dlo, la - dla], [lo + dlo, la + dla]];
  };
  const cirkel = (la, lo, km) => {
    const r = km * 1000 / M_PER_GRAAD;
    const ring = [];
    for (let i = 0; i <= 64; i++) {
      const a = (i / 64) * 2 * Math.PI;
      ring.push([lo + (r * Math.cos(a)) / COS, la + r * Math.sin(a)]);
    }
    return {type: 'Feature', geometry: {type: 'Polygon', coordinates: [ring]}, properties: {}};
  };
  const LEEG = {type: 'FeatureCollection', features: []};

  let kaart = null;
  let ctx = null;
  let wacht = null;
  let stadVak = null;
  let spelden = [];
  let thuis = null;
  let straal = LEEG;
  let klaar = false;
  const info = new ML.Popup({closeButton: false, closeOnClick: false, offset: 12, className: 'bs-webinfo'});

  const focus = (la, lo, km) => {
    if (!kaart) { wacht = [la, lo, km]; return; }
    kaart.fitBounds(vak(la, lo, km), {padding: 16, maxZoom: 17, duration: 600});
  };

  const zetStraal = () => {
    if (klaar && kaart.getSource('straal')) kaart.getSource('straal').setData(straal);
  };

  const maakKaart = (el) => {
    const doos = document.createElement('div');
    doos.className = 'bs-webkaart';
    el.replaceChildren(doos);
    const vest = dash.data('vestigingen').data;
    const la = vest.map((v) => v.la);
    const lo = vest.map((v) => v.lo);
    stadVak = [[Math.min(...lo) - 0.006, Math.min(...la) - 0.004], [Math.max(...lo) + 0.006, Math.max(...la) + 0.004]];
    kaart = new ML.Map({
      container: doos,
      style: STIJL,
      bounds: stadVak,
      fitBoundsOptions: {padding: 8},
      maxZoom: 18,
      dragRotate: false,
      pitchWithRotate: false,
      touchPitch: false,
      // Zoals een ingebedde Google-kaart: scrollen schuift de pagina, Ctrl + scrollen of twee vingers bewegen de kaart.
      cooperativeGestures: true,
      attributionControl: {compact: true},
      locale: {
        'CooperativeGesturesHandler.WindowsHelpText': 'Gebruik Ctrl + scrollen om in te zoomen',
        'CooperativeGesturesHandler.MacHelpText': 'Gebruik ⌘ + scrollen om in te zoomen',
        'CooperativeGesturesHandler.MobileHelpText': 'Gebruik twee vingers om de kaart te verplaatsen',
        'AttributionControl.ToggleAttribution': 'Bronnen van de kaart',
      },
    });
    kaart.touchZoomRotate.disableRotation();
    kaart.on('load', () => {
      kaart.addSource('straal', {type: 'geojson', data: straal});
      kaart.addLayer({id: 'straal-vlak', type: 'fill', source: 'straal', paint: {'fill-color': '#1a73e8', 'fill-opacity': 0.08}});
      kaart.addLayer({id: 'straal-rand', type: 'line', source: 'straal', paint: {'line-color': '#1a73e8', 'line-width': 1.5, 'line-dasharray': [3, 3]}});
      klaar = true;
    });
    kaart.on('click', (e) => {
      if (e.originalEvent && e.originalEvent.target.closest && e.originalEvent.target.closest('.bs-webpin')) return;
      const {lat, lng} = e.lngLat;
      const stra = dash.data('straten').data.reduce((b, r) => { const d = ctx.afstand(lat, lng, r.la, r.lo); return d < b.d ? {d, r} : b; }, {d: Infinity});
      ctx.zetThuis(lat, lng, stra.d < 400 ? 'Bij ' + stra.r.n : 'Punt op de kaart');
    });
    if (wacht) { focus(...wacht); wacht = null; }
  };

  const teken = (el, c) => {
    ctx = c;
    const {st} = c;
    if (!kaart || !el.contains(kaart.getContainer())) { kaart = null; klaar = false; maakKaart(el); }
    const doos = kaart.getContainer();
    const W = el.clientWidth || 720;
    const H = Math.round(Math.min(640, Math.max(400, W * 1.02)));
    if (doos.style.height !== H + 'px') doos.style.height = H + 'px';
    kaart.resize();

    info.remove();
    spelden.forEach((m) => m.remove());
    spelden = [];
    if (thuis) { thuis.remove(); thuis = null; }

    straal = st.thuis && st.straal ? {type: 'FeatureCollection', features: [cirkel(st.thuis.la, st.thuis.lo, st.straal)]} : LEEG;
    zetStraal();

    const per = c.perSchool();
    const ver = (nr) => !!(st.thuis && st.straal && !c.binnen(c.dichtst(nr)));
    const zet = (v, knop, titel, id) => {
      const tekst = document.createElement('span');
      tekst.textContent = titel;
      knop.addEventListener('mouseenter', () => info.setLngLat([v.lo, v.la]).setDOMContent(tekst).addTo(kaart));
      knop.addEventListener('mouseleave', () => info.remove());
      knop.addEventListener('click', (e) => { e.stopPropagation(); info.remove(); c.kies(id); });
      spelden.push(new ML.Marker({element: knop}).setLngLat([v.lo, v.la]).addTo(kaart));
      knop.setAttribute('aria-label', titel); // MapLibre zet hier standaard "Map marker".
    };
    if (st.grijs) {
      dash.data('andere').data.filter(c.pastFilter).forEach((s) => {
        const titel = s.naam + ', geen verslag in dit overzicht';
        (per[s.nr] || []).forEach((v) => zet(v, speld('geen', false, st.school === s.nr, ver(s.nr), titel), titel, s.nr));
      });
    }
    // Zelfde volgorde als de getekende kaart: wat later komt, ligt bovenop.
    dash.data('scholen').data.filter(c.pastFilter).sort((a, b) => Number(b.groep) - Number(a.groep)).forEach((s) => {
      const soort = c.soort(s.advies_key);
      const titel = s.naam + ': ' + s.advies + ', ' + c.maand.format(new Date(s.datum));
      (per[s.nr] || []).forEach((v) => zet(v, speld(soort, soort !== 'deel' && c.oud(s), st.school === s.id, ver(s.nr), titel), titel, s.id));
    });
    if (st.thuis) thuis = new ML.Marker({element: thuisSpeld(), anchor: 'bottom'}).setLngLat([st.thuis.lo, st.thuis.la]).addTo(kaart);
  };

  window.bsWebkaart = {
    teken,
    focus,
    zoom: (d) => { if (kaart) (d > 0 ? kaart.zoomIn() : kaart.zoomOut()); },
    stad: () => { if (kaart) kaart.fitBounds(stadVak, {padding: 8}); },
  };
})();
