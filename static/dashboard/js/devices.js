/* Devices page: list <-> detail view, driven by the URL hash (#DW-01). */
(() => {
  const list = document.getElementById('list');
  const detail = document.getElementById('detail');
  const cards = [...document.querySelectorAll('.dv-link')];
  const stage = detail.querySelector('.dv-stage');
  const $ = (id) => document.getElementById(id);
  let view = null;

  // Optional fields: show the row only when a value exists.
  const optional = (id, value, suffix = '') => {
    $(id).textContent = value ? value + suffix : '';
    $(id).parentElement.hidden = !value;
  };

  const render = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    const card = cards.find((c) => c.dataset.id === id);
    list.hidden = !!card;
    detail.hidden = !card;
    if (!card) return;

    const d = card.dataset;
    $('d-name').textContent = d.name;
    $('d-id').textContent = d.id;
    $('d-type').textContent = d.type;
    optional('d-location', d.location);
    optional('d-rated', d.rated, ' W');
    optional('d-plug', d.plug);
    $('d-power').textContent = d.power;
    $('d-voltage').textContent = d.voltage;
    $('d-current').textContent = d.current;
    const chip = $('d-status');
    chip.textContent = d.statusLabel;
    chip.className = 'dv-chip dv-' + d.status;

    view = view || Appliance3D.mount(stage);
    view.setKind(d.kind, d.status);
    view.resize();
    scrollTo(0, 0);
  };

  addEventListener('hashchange', render);
  render();
})();