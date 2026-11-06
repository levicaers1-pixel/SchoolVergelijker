// Minimale nabootsing van de dash-runtime van het Claude-dashboard, alleen voor lokale preview.
(() => {
  const D = window.__DATA__;
  const F = {};
  const O = [];
  let P = {afdeling: 'alle', methode: 'alle'};
  const run = (n) => document.querySelectorAll('[data-draw="' + n + '"]').forEach((e) => F[n](e));
  window.dash = {
    data: (id) => ({status: D[id] ? 'ok' : 'missing', data: D[id] || []}),
    params: () => P,
    setParams: (p) => { P = {...P, ...p}; Object.keys(F).forEach(run); O.forEach((f) => f()); },
    onData: (f) => { O.push(f); f(); },
    draw: (n, fn) => { if (fn) F[n] = fn; run(n); },
  };
  window.addEventListener('resize', () => { Object.keys(F).forEach(run); O.forEach((f) => f()); });
})();
