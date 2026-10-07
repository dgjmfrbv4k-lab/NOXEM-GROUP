// Décors 3D (three.js) : usine de fenêtres + maison. Tout est piloté par le temps t
// (aucune horloge), pour un rendu image par image déterministe.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const P = (t, s, d) => clamp((t - s) / d);
const eo = x => 1 - Math.pow(1 - x, 3);
const eio = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const eback = x => { const c1 = 1.4, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const lerp = (a, b, x) => a + (b - a) * x;

export function createWorld(canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(1920, 1080, false);
  renderer.toneMapping = THREE.NeutralToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const pmrem = new THREE.PMREMGenerator(renderer);
  const envTex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  const camera = new THREE.PerspectiveCamera(38, 1920 / 1080, 0.1, 300);

  // ---------- matériaux ----------
  const M = {
    pvc: new THREE.MeshStandardMaterial({ color: 0xf4f4f2, roughness: .35, metalness: 0 }),
    alu: new THREE.MeshStandardMaterial({ color: 0x3a3f46, roughness: .35, metalness: .6 }),
    glass: new THREE.MeshStandardMaterial({ color: 0x9fd0cc, roughness: .05, metalness: .9, transparent: true, opacity: .45 }),
    dark: new THREE.MeshStandardMaterial({ color: 0x23272e, roughness: .7 }),
    steel: new THREE.MeshStandardMaterial({ color: 0x8a9099, roughness: .3, metalness: .8 }),
    orange: new THREE.MeshStandardMaterial({ color: 0xd0853c, roughness: .5 }),
    red: new THREE.MeshStandardMaterial({ color: 0xc0242f, roughness: .45 }),
    yellow: new THREE.MeshStandardMaterial({ color: 0xe8b23a, roughness: .5 }),
    skin: new THREE.MeshStandardMaterial({ color: 0xc8956d, roughness: .7 }),
    navy: new THREE.MeshStandardMaterial({ color: 0x1e2430, roughness: .8 }),
    lamp: new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xfff1d8, emissiveIntensity: 2.5 }),
  };

  // ---------- éléments réutilisables ----------
  function windowModel(w, h, frameMat = M.pvc, depth = .08, mull = false) {
    const g = new THREE.Group();
    const f = .08;
    const box = (sx, sy, x, y, mat = frameMat) => { const m = new THREE.Mesh(new THREE.BoxGeometry(sx, sy, depth), mat); m.position.set(x, y, 0); m.castShadow = true; g.add(m); return m; };
    box(w, f, 0, h / 2 - f / 2); box(w, f, 0, -h / 2 + f / 2); box(f, h, -w / 2 + f / 2, 0); box(f, h, w / 2 - f / 2, 0);
    if (mull) box(f, h, 0, 0);
    const glass = new THREE.Mesh(new THREE.PlaneGeometry(w - f * 2, h - f * 2), M.glass);
    g.add(glass); g.userData.glass = glass;
    return g;
  }

  function person(vestMat = M.orange, helmet = true) {
    const g = new THREE.Group();
    const cap = (r, l, mat) => { const m = new THREE.Mesh(new THREE.CapsuleGeometry(r, l, 6, 12), mat); m.castShadow = true; return m; };
    const hip = new THREE.Group(); hip.position.y = .95; g.add(hip);
    const torso = cap(.2, .42, vestMat); torso.position.y = .38; hip.add(torso);
    const head = new THREE.Mesh(new THREE.SphereGeometry(.13, 20, 16), M.skin); head.position.y = .9; hip.add(head);
    if (helmet) { const hm = new THREE.Mesh(new THREE.SphereGeometry(.15, 20, 12, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xf5f5f5, roughness: .3 })); hm.position.y = .93; hip.add(hm); }
    const limb = (x, y, len, r, mat) => { const p = new THREE.Group(); p.position.set(x, y, 0); const c = cap(r, len, mat); c.position.y = -len / 2 - r; p.add(c); hip.add(p); return p; };
    const legL = limb(-.1, 0, .72, .085, M.navy), legR = limb(.1, 0, .72, .085, M.navy);
    const armL = limb(-.27, .62, .5, .06, vestMat), armR = limb(.27, .62, .5, .06, vestMat);
    g.userData = { legL, legR, armL, armR, hip };
    return g;
  }
  function walk(p, phase, amp = .38) {
    const s = Math.sin(phase), u = p.userData;
    u.legL.rotation.x = s * amp; u.legR.rotation.x = -s * amp;
    u.armL.rotation.x = -s * amp * .8; u.armR.rotation.x = s * amp * .8;
    u.hip.position.y = .95 + Math.abs(Math.cos(phase)) * .03;
  }

  // =====================================================================
  // USINE
  // =====================================================================
  const factory = new THREE.Group();
  {
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(120, 60), new THREE.MeshStandardMaterial({ color: 0x3a3f47, roughness: .35, metalness: .3 }));
    floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; factory.add(floor);
    // marquage au sol
    for (const z of [-2.2, 2.2]) { const l = new THREE.Mesh(new THREE.PlaneGeometry(120, .12), M.yellow); l.rotation.x = -Math.PI / 2; l.position.set(0, .005, z); factory.add(l); }
    // murs + poteaux + poutres + lampes
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(120, 14), new THREE.MeshStandardMaterial({ color: 0x2b3038, roughness: .9 }));
    wall.position.set(0, 7, -14); factory.add(wall);
    for (let x = -50; x <= 50; x += 7) {
      const col = new THREE.Mesh(new THREE.BoxGeometry(.5, 12, .5), M.dark); col.position.set(x, 6, -12); col.castShadow = true; factory.add(col);
      const beam = new THREE.Mesh(new THREE.BoxGeometry(.3, .6, 30), M.dark); beam.position.set(x, 11, 0); factory.add(beam);
      for (const z of [-6, 0, 6]) {
        const lamp = new THREE.Mesh(new THREE.CylinderGeometry(.5, .5, .08, 24), M.lamp); lamp.position.set(x + 3.5, 9, z); factory.add(lamp);
      }
      // fenêtres hautes du mur (bandeau lumineux)
      const win = new THREE.Mesh(new THREE.PlaneGeometry(5.5, 2.2), new THREE.MeshStandardMaterial({ color: 0xbfd6e6, emissive: 0x9fbfd6, emissiveIntensity: .9 }));
      win.position.set(x + 3.5, 9.5, -13.95); factory.add(win);
    }
    // ligne de convoyage
    const base = new THREE.Mesh(new THREE.BoxGeometry(60, .7, 2.2), M.dark); base.position.set(0, .35, 0); base.castShadow = base.receiveShadow = true; factory.add(base);
    const belt = new THREE.Mesh(new THREE.BoxGeometry(60, .05, 2), new THREE.MeshStandardMaterial({ color: 0x15181d, roughness: .6 })); belt.position.set(0, .73, 0); belt.receiveShadow = true; factory.add(belt);
    for (let x = -29.5; x <= 29.5; x += .9) { const r = new THREE.Mesh(new THREE.CylinderGeometry(.06, .06, 2.15, 10), M.steel); r.rotation.x = Math.PI / 2; r.position.set(x, .68, 0); factory.add(r); }
    // portique de pose du vitrage
    const gantry = new THREE.Group(); factory.add(gantry);
    for (const z of [-1.5, 1.5]) { const leg = new THREE.Mesh(new THREE.BoxGeometry(.25, 3.6, .25), M.orange); leg.position.set(0, 1.8, z); leg.castShadow = true; gantry.add(leg); }
    const top = new THREE.Mesh(new THREE.BoxGeometry(.5, .4, 3.4), M.orange); top.position.set(0, 3.6, 0); gantry.add(top);
    const head = new THREE.Group(); gantry.add(head);
    const rod = new THREE.Mesh(new THREE.CylinderGeometry(.06, .06, 1.6, 10), M.steel); rod.position.y = .8; head.add(rod);
    const plate = new THREE.Mesh(new THREE.BoxGeometry(.9, .06, .9), M.dark); head.add(plate);
    for (const [x, z] of [[-.3, -.3], [.3, -.3], [-.3, .3], [.3, .3]]) { const cup = new THREE.Mesh(new THREE.CylinderGeometry(.09, .09, .05, 16), M.red); cup.position.set(x, -.05, z); head.add(cup); }
    const heldGlass = new THREE.Mesh(new THREE.BoxGeometry(1.25, .02, 1.55), M.glass); heldGlass.position.y = -.1; head.add(heldGlass);
    factory.userData.head = head; factory.userData.heldGlass = heldGlass;
    // cadres qui défilent (posés à plat)
    const frames = [];
    for (let i = 0; i < 14; i++) {
      const w = windowModel(1.4, 1.7); w.rotation.x = -Math.PI / 2; w.position.y = .8; factory.add(w); frames.push(w);
    }
    factory.userData.frames = frames;
    // bras robot
    const robot = new THREE.Group(); robot.position.set(3.4, 0, -2.4); factory.add(robot);
    const rb = new THREE.Mesh(new THREE.CylinderGeometry(.45, .55, .5, 24), M.orange); rb.position.y = .25; robot.add(rb);
    const turret = new THREE.Group(); turret.position.y = .5; robot.add(turret);
    const a1 = new THREE.Group(); a1.position.y = .3; turret.add(a1);
    const s1 = new THREE.Mesh(new THREE.BoxGeometry(.3, 1.6, .3), M.orange); s1.position.y = .8; a1.add(s1);
    const a2 = new THREE.Group(); a2.position.y = 1.6; a1.add(a2);
    const s2 = new THREE.Mesh(new THREE.BoxGeometry(.25, 1.3, .25), M.orange); s2.position.y = .65; a2.add(s2);
    const tool = new THREE.Mesh(new THREE.CylinderGeometry(.08, .12, .3, 12), M.steel); tool.position.y = 1.35; a2.add(tool);
    Object.assign(factory.userData, { turret, a1, a2 });
    // racks de fenêtres finies (chevalets en A)
    for (let k = 0; k < 4; k++) {
      const rack = new THREE.Group(); rack.position.set(-12 + k * 6.5, 0, -7); factory.add(rack);
      for (let j = 0; j < 7; j++) {
        const w = windowModel(1.4, 1.9); w.position.set(-1.2 + j * .38, 1.05, 0); w.rotation.set(0, Math.PI / 2, -.12); rack.add(w);
      }
      const frameA = new THREE.Mesh(new THREE.BoxGeometry(3.2, .12, 1.2), M.steel); frameA.position.y = .06; rack.add(frameA);
    }
    // ouvriers
    const worker = person(M.orange); worker.position.set(-8, 0, 3.2); worker.rotation.y = Math.PI / 2; factory.add(worker);
    const worker2 = person(M.yellow); worker2.position.set(4.5, 0, -2.6); worker2.rotation.y = -.4; factory.add(worker2);
    Object.assign(factory.userData, { worker, worker2 });

    const hemi = new THREE.HemisphereLight(0xdfe8f5, 0x2a2622, .9); factory.add(hemi);
    const sun = new THREE.DirectionalLight(0xfff0dc, 2.2); sun.position.set(8, 16, 10); sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -20, right: 20, top: 20, bottom: -20, near: 1, far: 60 });
    factory.add(sun);
    const warm = new THREE.PointLight(0xffc98a, 30, 18, 1.6); warm.position.set(0, 5, 2); factory.add(warm);
  }

  function updateFactory(t) {
    const u = factory.userData;
    const speed = .9, gap = 2.4;
    u.frames.forEach((f, i) => {
      let x = ((i * gap + t * speed) % (14 * gap)) - 7 * gap * 1.0;
      f.position.x = x;
      // vitrage : posé quand le cadre passe sous le portique (x = 0)
      const k = clamp((x + .05) / .05);
      f.userData.glass.visible = x > 0;
    });
    // tête du portique : descend quand un cadre arrive sous elle
    const phase = ((t * speed) % gap) / gap; // 0..1 entre deux cadres
    const down = Math.sin(Math.PI * clamp((phase - .62) / .38));
    u.head.position.set(0, lerp(3.2, 1.0, down), 0);
    u.heldGlass.visible = phase > .25 && phase < .99;
    // bras robot
    u.turret.rotation.y = Math.sin(t * 1.1) * .9;
    u.a1.rotation.z = -.4 + Math.sin(t * 1.3) * .25;
    u.a2.rotation.z = .9 + Math.sin(t * 1.7 + 1) * .35;
    // ouvrier qui marche le long de la ligne
    u.worker.position.x = -9 + t * 1.25;
    walk(u.worker, t * 6.2, .38);
    walk(u.worker2, 0, 0); u.worker2.userData.armR.rotation.x = -1.0 + Math.sin(t * 2) * .1;
  }

  // =====================================================================
  // MAISON
  // =====================================================================
  const house = new THREE.Group();
  const sky = new THREE.Color(0xdde7ee), dusk = new THREE.Color(0x1b2436);
  {
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), new THREE.MeshStandardMaterial({ color: 0x7d9a62, roughness: 1 }));
    ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; house.add(ground);
    const terrace = new THREE.Mesh(new THREE.BoxGeometry(12, .15, 4), new THREE.MeshStandardMaterial({ color: 0x9a7552, roughness: .8 }));
    terrace.position.set(-1, .07, 5.6); terrace.receiveShadow = true; house.add(terrace);
    const path = new THREE.Mesh(new THREE.BoxGeometry(2, .06, 8), new THREE.MeshStandardMaterial({ color: 0xc9c4b8, roughness: .9 }));
    path.position.set(7.2, .03, 7); house.add(path);
    // volumes
    const clad = new THREE.MeshStandardMaterial({ color: 0x2e3238, roughness: .75 });
    const wood = new THREE.MeshStandardMaterial({ color: 0xa47b53, roughness: .7 });
    const main = new THREE.Mesh(new THREE.BoxGeometry(14, 3.4, 7), clad); main.position.set(0, 1.7, 0); main.castShadow = main.receiveShadow = true; house.add(main);
    const shape = new THREE.Shape(); shape.moveTo(-3.7, 0); shape.lineTo(0, 2.6); shape.lineTo(3.7, 0); shape.lineTo(-3.7, 0);
    const roof = new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth: 14.4, bevelEnabled: false }), new THREE.MeshStandardMaterial({ color: 0x24282e, roughness: .4, metalness: .4 }));
    roof.rotation.y = Math.PI / 2; roof.position.set(-7.2, 3.4, 0); roof.castShadow = true; house.add(roof);
    const wing = new THREE.Mesh(new THREE.BoxGeometry(4, 3, 5), wood); wing.position.set(9, 1.5, -.6); wing.castShadow = wing.receiveShadow = true; house.add(wing);
    const wingRoof = new THREE.Mesh(new THREE.BoxGeometry(4.3, .2, 5.3), M.dark); wingRoof.position.set(9, 3.1, -.6); house.add(wingRoof);

    // intérieurs éclairés (visibles derrière les vitrages au crépuscule)
    const interior = new THREE.MeshStandardMaterial({ color: 0x3a3530, emissive: 0xffb35c, emissiveIntensity: 0 });
    house.userData.interior = interior;
    const opening = (w, h, x, y, z, ry = 0) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), interior); m.position.set(x, y, z); m.rotation.y = ry; house.add(m); return m; };

    // ouvertures + menuiseries à poser
    const items = [];
    const add = (model, x, y, z, ry, from) => { model.position.set(x, y, z); model.rotation.y = ry; house.add(model); items.push({ model, x, y, z, ry, from }); return model; };
    // baie coulissante (alu anthracite, 2 vantaux)
    opening(5.2, 2.5, -2.2, 1.3, 3.51);
    const bay = add(windowModel(5.2, 2.5, M.alu, .12, true), -2.2, 1.3, 3.56, 0, [0, 1.5, 6]);
    // fenêtres
    opening(1.6, 1.4, 3.6, 1.9, 3.51); add(windowModel(1.6, 1.4, M.alu, .1), 3.6, 1.9, 3.56, 0, [0, 2, 6]);
    opening(1.6, 1.4, -6, 1.9, 3.51); add(windowModel(1.6, 1.4, M.alu, .1), -6, 1.9, 3.56, 0, [0, 2, 6]);
    // porte d'entrée (aile bois)
    const doorG = new THREE.Group();
    const door = new THREE.Mesh(new THREE.BoxGeometry(1.1, 2.3, .1), new THREE.MeshStandardMaterial({ color: 0x2b2f35, roughness: .4, metalness: .3 })); doorG.add(door);
    const handle = new THREE.Mesh(new THREE.BoxGeometry(.05, 1.4, .06), M.steel); handle.position.set(.4, 0, .08); doorG.add(handle);
    const strip = new THREE.Mesh(new THREE.PlaneGeometry(.18, 1.6), new THREE.MeshStandardMaterial({ color: 0xffe2b0, emissive: 0xffc27a, emissiveIntensity: 0 })); strip.position.set(-.2, 0, .056); doorG.add(strip);
    house.userData.doorStrip = strip.material;
    add(doorG, 9, 1.15, 1.92, 0, [0, 1, 6]);
    // volets roulants : coffre + tablier au-dessus des fenêtres
    const shutters = [];
    for (const [x, w] of [[3.6, 1.6], [-6, 1.6]]) {
      const box = new THREE.Mesh(new THREE.BoxGeometry(w + .1, .25, .3), M.alu); box.position.set(x, 2.75, 3.62); house.add(box);
      const slat = new THREE.Mesh(new THREE.BoxGeometry(w, 1, .04), new THREE.MeshStandardMaterial({ color: 0x4a5059, roughness: .5, metalness: .4 }));
      slat.position.set(x, 2.6, 3.7); house.add(slat); shutters.push(slat);
    }
    house.userData.items = items; house.userData.shutters = shutters; house.userData.bay = bay;
    // arbres stylisés
    for (const [x, z, s] of [[-11, 2, 1.2], [-13, -4, 1.5], [13, 5, 1], [15, -3, 1.4], [-9, 9, .9]]) {
      const tr = new THREE.Mesh(new THREE.CylinderGeometry(.12, .16, 1.6, 8), new THREE.MeshStandardMaterial({ color: 0x5b4632 })); tr.position.set(x, .8 * s, z); house.add(tr);
      const cr = new THREE.Mesh(new THREE.IcosahedronGeometry(1.1 * s, 1), new THREE.MeshStandardMaterial({ color: 0x4f6e3f, roughness: .9, flatShading: true })); cr.position.set(x, 2.2 * s, z); cr.castShadow = true; house.add(cr);
    }
    // poseurs
    const p1 = person(M.orange), p2 = person(M.red, false);
    p1.position.set(1.2, 0, 5.2); p2.position.set(-5.2, 0, 5.4); house.add(p1, p2);
    house.userData.p1 = p1; house.userData.p2 = p2;

    const hemi = new THREE.HemisphereLight(0xe6f0ff, 0x5a5040, 1.1); house.add(hemi);
    const sun = new THREE.DirectionalLight(0xfff2de, 2.6); sun.position.set(-12, 18, 14); sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -22, right: 22, top: 22, bottom: -22, near: 1, far: 70 });
    house.add(sun); house.userData.sun = sun; house.userData.hemi = hemi;
    const porch = new THREE.PointLight(0xffb86b, 0, 10, 1.5); porch.position.set(9, 2.8, 3); house.add(porch); house.userData.porch = porch;
  }

  // tInstall : temps local de la pose ; night : 0 jour -> 1 crépuscule
  function updateHouse(tInstall, night, tPeople) {
    const u = house.userData;
    u.items.forEach((it, i) => {
      const k = eback(P(tInstall, .2 + i * .45, .8)), o = P(tInstall, .2 + i * .45, .15);
      const [fx, fy, fz] = it.from;
      it.model.position.set(it.x + fx * (1 - k), it.y + fy * (1 - k), it.z + fz * (1 - k));
      it.model.rotation.y = it.ry + (1 - k) * .6;
      it.model.visible = o > 0;
    });
    // volets : descendent à mi-hauteur puis remontent
    u.shutters.forEach((s, i) => {
      const d = Math.sin(Math.PI * P(tInstall, 2.6 + i * .2, 2.2)) * .7 + night * .55;
      s.scale.y = Math.max(.01, d); s.position.y = 2.62 - d / 2;
    });
    // poseurs : marchent vers la maison puis restent
    const w1 = P(tPeople, 0, 3);
    u.p1.position.x = lerp(4.5, 1.2, w1); u.p1.rotation.y = w1 < 1 ? -Math.PI / 2 : Math.PI * .1;
    walk(u.p1, tPeople * 6, w1 < 1 ? .5 : 0);
    walk(u.p2, 0, 0); u.p2.userData.armR.rotation.x = -1.2 + Math.sin(tPeople * 3) * .15; u.p2.rotation.y = Math.PI * .9;
    // jour -> crépuscule
    u.sun.intensity = lerp(2.6, .25, night); u.hemi.intensity = lerp(1.1, .35, night);
    u.interior.emissiveIntensity = lerp(0, 3.2, night); M.glass.opacity = lerp(.45, .18, night); u.doorStrip.emissiveIntensity = lerp(0, 2, night);
    u.porch.intensity = lerp(0, 25, night);
  }

  const scene = new THREE.Scene();
  scene.environment = envTex;
  scene.add(factory, house);

  // shot : { set:'factory'|'house', ... }
  function render(shot) {
    factory.visible = shot.set === 'factory';
    house.visible = shot.set === 'house';
    if (shot.set === 'factory') {
      scene.background = new THREE.Color(0x1d2128);
      scene.fog = new THREE.Fog(0x1d2128, 14, 60);
      renderer.toneMappingExposure = 1.0; scene.environmentIntensity = .8; M.glass.opacity = .45;
      updateFactory(shot.t);
    } else {
      const c = sky.clone().lerp(dusk, shot.night || 0);
      scene.background = c; scene.fog = new THREE.Fog(c, 30, 110);
      renderer.toneMappingExposure = 1.0; scene.environmentIntensity = lerp(1, .12, shot.night || 0);
      updateHouse(shot.install, shot.night || 0, shot.people || 0);
    }
    camera.position.set(...shot.cam); camera.lookAt(...shot.look); camera.fov = shot.fov || 38; camera.updateProjectionMatrix();
    renderer.render(scene, camera);
  }
  return { render };
}
