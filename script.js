/* ==========================================================================
   Aurelis — Comptoir d'Or

   ▸ POUR METTRE À JOUR LES PRIX : modifiez uniquement l'objet TARIFS
     ci-dessous. La grille de rachat affichée sur le site et le simulateur
     d'estimation s'appuient tous les deux sur ces valeurs.
   ▸ POUR CHANGER LE NOM DE LA MARQUE : voir index.html (balise <title>,
     les deux blocs .logo et le pied de page).
   ========================================================================== */

const TARIFS = {
  // Date affichée sous la grille de rachat.
  miseAJour: '16 septembre 2026',

  // Prix de rachat des bijoux et débris, en euros par gramme.
  alliages: [
    { id: '999', label: 'Or 24 carats — 999 ‰', exemple: 'Or fin, lingots, lingotins', prix: 100 },
    { id: '916', label: 'Or 22 carats — 916 ‰', exemple: 'Bijoux anciens, pièces d’or', prix: 91 },
    { id: '750', label: 'Or 18 carats — 750 ‰', exemple: 'Bijouterie française courante', prix: 74 },
    { id: '585', label: 'Or 14 carats — 585 ‰', exemple: 'Alliances, bijoux d’import', prix: 57 },
    { id: '375', label: 'Or 9 carats — 375 ‰', exemple: 'Bijoux fantaisie en or massif', prix: 36 },
  ],

  // Prix de rachat à l'unité des pièces et lingots, en euros.
  pieces: [
    { id: 'nap20', label: 'Napoléon 20 francs', detail: '5,81 g — 900 ‰', prix: 545 },
    { id: 'nap10', label: 'Napoléon 10 francs', detail: '3,22 g — 900 ‰', prix: 270 },
    { id: 'souverain', label: 'Souverain britannique', detail: '7,99 g — 917 ‰', prix: 765 },
    { id: 'suisse20', label: '20 francs suisses (Vreneli)', detail: '6,45 g — 900 ‰', prix: 600 },
    { id: 'krug', label: 'Krugerrand 1 once', detail: '33,93 g — 917 ‰', prix: 3250 },
    { id: 'pesos50', label: '50 pesos mexicains', detail: '41,67 g — 900 ‰', prix: 3900 },
    { id: 'lingotin100', label: 'Lingotin 100 g', detail: 'Or fin 999,9 ‰', prix: 10500 },
    { id: 'lingot1k', label: 'Lingot 1 kg', detail: 'Or fin 999,9 ‰ avec bulletin', prix: 105000 },
  ],
};

const euros = new Intl.NumberFormat('fr-FR', {
  style: 'currency',
  currency: 'EUR',
  maximumFractionDigits: 0,
});

const eurosPrecis = new Intl.NumberFormat('fr-FR', {
  style: 'currency',
  currency: 'EUR',
  maximumFractionDigits: 2,
});

// État de l'en-tête au défilement
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 10);
});

// Menu mobile
const burger = document.getElementById('burger');
const nav = document.getElementById('nav');
burger.addEventListener('click', () => {
  const ouvert = nav.classList.toggle('open');
  burger.setAttribute('aria-expanded', String(ouvert));
});
nav.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    nav.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
  });
});

// Grille de rachat
const corpsAlliages = document.getElementById('table-alliages');
TARIFS.alliages.forEach((a) => {
  const tr = document.createElement('tr');
  tr.innerHTML =
    `<td>${a.label}</td><td>${a.exemple}</td>` +
    `<td class="prix">${euros.format(a.prix)} <small>/ g</small></td>`;
  corpsAlliages.appendChild(tr);
});

const corpsPieces = document.getElementById('table-pieces');
TARIFS.pieces.forEach((p) => {
  const tr = document.createElement('tr');
  tr.innerHTML =
    `<td>${p.label}</td><td>${p.detail}</td>` +
    `<td class="prix">${euros.format(p.prix)} <small>/ unité</small></td>`;
  corpsPieces.appendChild(tr);
});

document.getElementById('maj-date').textContent = TARIFS.miseAJour;

// Simulateur d'estimation
const selectAlliage = document.getElementById('sim-alliage');
const selectPiece = document.getElementById('sim-piece');
const champPoids = document.getElementById('sim-poids');
const champQuantite = document.getElementById('sim-quantite');
const resultat = document.getElementById('sim-result');
const detail = document.getElementById('sim-detail');

TARIFS.alliages.forEach((a) => {
  selectAlliage.add(new Option(`${a.label} — ${euros.format(a.prix)} / g`, a.id));
});
selectAlliage.value = '750'; // le cas le plus fréquent en France

TARIFS.pieces.forEach((p) => {
  selectPiece.add(new Option(`${p.label} — ${euros.format(p.prix)}`, p.id));
});

let modeActif = 'bijoux';

function calculer() {
  if (modeActif === 'bijoux') {
    const alliage = TARIFS.alliages.find((a) => a.id === selectAlliage.value);
    const poids = Math.max(0, parseFloat(champPoids.value) || 0);
    const total = alliage.prix * poids;
    resultat.textContent = eurosPrecis.format(total);
    detail.textContent = poids
      ? `${poids.toLocaleString('fr-FR')} g d\u2019${alliage.label.toLowerCase()} à ${euros.format(alliage.prix)} le gramme.`
      : 'Indiquez le poids de vos bijoux pour obtenir une estimation.';
  } else {
    const piece = TARIFS.pieces.find((p) => p.id === selectPiece.value);
    const quantite = Math.max(0, parseInt(champQuantite.value, 10) || 0);
    const total = piece.prix * quantite;
    resultat.textContent = eurosPrecis.format(total);
    detail.textContent = quantite
      ? `${quantite} × ${piece.label} à ${euros.format(piece.prix)} l'unité.`
      : 'Indiquez une quantité pour obtenir une estimation.';
  }
}

[selectAlliage, champPoids, selectPiece, champQuantite].forEach((el) => {
  el.addEventListener('input', calculer);
});

document.querySelectorAll('.tab').forEach((tab) => {
  tab.addEventListener('click', () => {
    modeActif = tab.dataset.panel;
    document.querySelectorAll('.tab').forEach((t) => {
      const actif = t === tab;
      t.classList.toggle('is-active', actif);
      t.setAttribute('aria-selected', String(actif));
    });
    document.querySelectorAll('.simulator__panel').forEach((panel) => {
      const visible = panel.id === `panel-${modeActif}`;
      panel.classList.toggle('is-hidden', !visible);
      panel.hidden = !visible;
    });
    calculer();
  });
});

calculer();

// Apparition au défilement
const revealEls = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15 }
);
revealEls.forEach((el) => observer.observe(el));

// Compteurs animés
const counters = document.querySelectorAll('[data-count]');
const counterObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const cible = parseInt(el.dataset.count, 10);
      const suffixe = el.dataset.suffix || '';
      const duree = 1200;
      const depart = performance.now();
      function tick(now) {
        const progression = Math.min((now - depart) / duree, 1);
        el.textContent = Math.floor(progression * cible) + suffixe;
        if (progression < 1) requestAnimationFrame(tick);
        else el.textContent = cible + suffixe;
      }
      requestAnimationFrame(tick);
      counterObserver.unobserve(el);
    });
  },
  { threshold: 0.5 }
);
counters.forEach((el) => counterObserver.observe(el));

// Formulaire de contact (démonstration front-end uniquement)
const form = document.getElementById('contact-form');
const status = document.getElementById('form-status');
form.addEventListener('submit', (e) => {
  e.preventDefault();
  status.textContent = 'Merci ! Votre demande est enregistrée, nous vous répondons sous 24 h ouvrées.';
  form.reset();
});

// Année du pied de page
document.getElementById('year').textContent = new Date().getFullYear();
