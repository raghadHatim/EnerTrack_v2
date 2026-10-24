(() => {
  const stage = document.querySelector('.dv-stage[data-manual]');
  const view = Appliance3D.mount(stage);
  const idInput = document.getElementById('f-id');
  const idChip = document.getElementById('idChip');
  const prefix = { dishwasher: 'DW', fridge: 'FR', washer: 'WM', ac: 'AC', other: 'DV' };

  // معرّف مقترح؛ السيرفر هو اللي يتأكد لاحقاً أنه غير مكرر قبل الحفظ
  const newId = (kind) => `${prefix[kind]}-${Math.floor(100 + Math.random() * 900)}`;

  const update = (kind) => {
    view.setKind(kind);
    idInput.value = idChip.textContent = newId(kind);
  };

  document.querySelectorAll('input[name="kind"]').forEach((radio) =>
    radio.addEventListener('change', () => update(radio.value))
  );
  update(document.querySelector('input[name="kind"]:checked').value);
})();
