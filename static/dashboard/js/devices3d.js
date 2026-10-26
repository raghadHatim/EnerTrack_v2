/* Builds a small 3D appliance model inside each .dv-stage (Three.js r128). */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const LED = { running: 0x2ecc8f, idle: 0xf5a623, offline: 0x9a9ab0 };

  const mat = (c, o = {}) =>
    new THREE.MeshStandardMaterial(Object.assign({ color: c, roughness: 0.45, metalness: 0.2 }, o));
  const steel = mat(0xd5d8e4, { metalness: 0.5 });
  const white = mat(0xf7f7fb, { metalness: 0.05 });
  const dark = mat(0x23233a, { roughness: 0.85, metalness: 0 });
  const panelMat = mat(0x1b2f5b);

  const box = (w, h, d, m, x = 0, y = 0, z = 0) => {
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
    mesh.position.set(x, y, z);
    return mesh;
  };
  const led = (parent, st, x, y, z) => {
    const m = new THREE.Mesh(
      new THREE.SphereGeometry(0.06, 16, 16),
      new THREE.MeshBasicMaterial({ color: LED[st] || LED.offline })
    );
    m.position.set(x, y, z);
    parent.add(m);
    return m;
  };
  const hinge = (parent, x, y, z) => {
    const p = new THREE.Group();
    p.position.set(x, y, z);
    parent.add(p);
    return p;
  };

  // Each builder fills group g and returns the parts that animate.
  const builders = {
    dishwasher(g, st) {
      g.add(box(2, 2, 1.8, steel, 0, 1, 0));
      g.add(box(1.86, 1.62, 0.02, dark, 0, 0.95, 0.905));
      g.add(box(1.7, 0.05, 1.5, mat(0x9aa0b4), 0, 0.75, 0.15));
      g.add(box(1.7, 0.05, 1.5, mat(0x9aa0b4), 0, 1.3, 0.15));
      g.add(box(1.9, 0.2, 0.1, panelMat, 0, 1.9, 0.9));
      const door = hinge(g, 0, 0.12, 0.9);
      door.add(box(1.9, 1.72, 0.1, white, 0, 0.86, 0.05));
      door.add(box(1.2, 0.08, 0.1, steel, 0, 1.5, 0.13));
      return { pivot: door, axis: 'x', max: 1.3, led: led(g, st, 0.75, 1.9, 0.96) };
    },

    fridge(g, st) {
      g.add(box(1.5, 3, 1.4, steel, 0, 1.5, 0));
      g.add(box(1.4, 2.8, 0.02, dark, 0, 1.5, 0.705));
      const door = hinge(g, 0.75, 0, 0.7);
      door.add(box(1.5, 2.95, 0.1, white, -0.75, 1.5, 0.05));
      door.add(box(1.5, 0.03, 0.11, steel, -0.75, 2.1, 0.05));
      door.add(box(0.06, 1.1, 0.1, steel, -1.35, 1.2, 0.13));
      return { pivot: door, axis: 'y', max: 1.2, led: led(door, st, -1.25, 2.75, 0.12) };
    },

    washer(g, st) {
      g.add(box(1.8, 2.2, 1.7, white, 0, 1.1, 0));
      g.add(box(1.8, 0.35, 0.05, panelMat, 0, 2.0, 0.86));
      const ring = new THREE.Mesh(new THREE.TorusGeometry(0.55, 0.09, 16, 40), steel);
      ring.position.set(0, 1.0, 0.88);
      g.add(ring);
      const glass = new THREE.Mesh(
        new THREE.CircleGeometry(0.52, 40),
        mat(0x7fb4e8, { transparent: true, opacity: 0.6, metalness: 0.1 })
      );
      glass.position.set(0, 1.0, 0.89);
      g.add(glass);
      const drum = box(0.7, 0.08, 0.02, white, 0, 1.0, 0.9);
      g.add(drum);
      return { spin: drum, led: led(g, st, 0.7, 2.0, 0.9) };
    },

    ac(g, st) {
      g.add(box(3, 0.9, 0.8, white, 0, 1.7, 0));
      const flap = hinge(g, 0, 1.28, 0.4);
      flap.add(box(2.8, 0.05, 0.35, steel, 0, 0, 0.17));
      return { pivot: flap, axis: 'x', max: 0.8, led: led(g, st, 1.3, 1.85, 0.41) };
    },

    generic(g, st) {
      g.add(box(1.8, 1.6, 1.4, white, 0, 0.8, 0));
      g.add(box(1.8, 0.3, 0.05, panelMat, 0, 1.4, 0.71));
      return { led: led(g, st, 0.7, 1.4, 0.75) };
    },
  };

  function mount(stage) {
    const canvas = stage.querySelector('canvas');
    let status = stage.dataset.status;
    let running = status === 'running';

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));

    const scene = new THREE.Scene();
    const cam = new THREE.PerspectiveCamera(35, 1, 0.1, 50);
    cam.position.set(0, 3.4, 8.6);
    cam.lookAt(0, 1.4, 0);
    scene.add(new THREE.HemisphereLight(0xffffff, 0xb4c4e6, 0.95));
    const sun = new THREE.DirectionalLight(0xffffff, 0.8);
    sun.position.set(4, 6, 5);
    scene.add(sun);

    const floor = new THREE.Mesh(
      new THREE.CircleGeometry(2.4, 48),
      new THREE.MeshBasicMaterial({ color: 0xcdd9ee, transparent: true, opacity: 0.55 })
    );
    floor.rotation.x = -Math.PI / 2;
    scene.add(floor);

    const holder = new THREE.Group();
    const body = new THREE.Group();
    holder.add(body);
    scene.add(holder);
    holder.rotation.y = 0.6;
    let parts = {};
    const setKind = (kind, st) => {
      if (st) { status = st; running = st === 'running'; }
      while (body.children.length) body.remove(body.children[0]);
      open = 0;
      parts = (builders[kind] || builders.generic)(body, status);
    };

    const size = () => {
      const w = stage.clientWidth, h = stage.clientHeight;
      renderer.setSize(w, h, false);
      cam.aspect = w / h;
      cam.updateProjectionMatrix();
    };
    size();
    addEventListener('resize', size);

    let moved = false, drag = false, lastX = 0, hover = false, visible = true, open = 0, t = Math.random() * 6;
    setKind(stage.dataset.kind);

    canvas.addEventListener('pointerdown', (e) => {
      drag = true;
      moved = false;
      lastX = e.clientX;
      canvas.setPointerCapture(e.pointerId);
    });
    canvas.addEventListener('pointermove', (e) => {
      if (!drag) return;
      if (Math.abs(e.clientX - lastX) > 1) moved = true;
      holder.rotation.y += (e.clientX - lastX) * 0.01;
      lastX = e.clientX;
    });
    canvas.addEventListener('click', (e) => { if (moved) e.preventDefault(); });
    ['pointerup', 'pointercancel'].forEach((ev) => canvas.addEventListener(ev, () => (drag = false)));
    stage.addEventListener('pointerenter', () => (hover = true));
    stage.addEventListener('pointerleave', () => (hover = false));
    new IntersectionObserver(([e]) => (visible = e.isIntersecting)).observe(stage);

    (function tick() {
      requestAnimationFrame(tick);
      if (!visible) return;
      t += 0.016;
      if (!drag && !reduce) holder.rotation.y += hover ? 0.005 : 0.012;
      body.position.y = reduce ? 0 : Math.sin(t) * 0.05;
      if (parts.pivot) {
        open += ((hover ? parts.max : 0) - open) * 0.08;
        parts.pivot.rotation[parts.axis] = open;
      }
      if (parts.spin && (running || hover) && !reduce) parts.spin.rotation.z += 0.08;
      if (parts.led) parts.led.scale.setScalar(running && !reduce ? 1 + 0.35 * Math.sin(t * 4) : 1);
      renderer.render(scene, cam);
    })();
    return { setKind, resize: size };
  }

  document.querySelectorAll('.dv-stage:not([data-manual])').forEach(mount);
  window.Appliance3D = { mount };
})();