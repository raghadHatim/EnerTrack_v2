(() => {
  const stage = document.querySelector('.dv-stage[data-manual]');
  const view = Appliance3D.mount(stage);
  const idInput = document.getElementById('f-id');
  const idChip = document.getElementById('idChip');
  const custom = document.getElementById('customType');
  const typeInput = document.getElementById('f-type');
  const prefix = { dishwasher: 'DW', fridge: 'FR', washer: 'WM', ac: 'AC', other: 'DV' };

  // Suggested id; the server must still confirm it is unique before saving.
  const newId = (kind) => `${prefix[kind]}-${Math.floor(100 + Math.random() * 900)}`;

  const update = (radio) => {
    const kind = radio.value;
    const isOther = kind === 'other';
    view.setKind(kind);
    idInput.value = idChip.textContent = newId(kind);
    custom.hidden = !isOther;
    typeInput.required = isOther;
    typeInput.value = isOther ? '' : radio.dataset.label;
    if (isOther) typeInput.focus();
  };

  const radios = document.querySelectorAll('input[name="kind"]');
  radios.forEach((r) => r.addEventListener('change', () => update(r)));
  update(document.querySelector('input[name="kind"]:checked'));
})();