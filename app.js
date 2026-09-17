/* =========================================================
   NOXEM GROUP FRANCE — logique du site
   Aucune dépendance externe.
   ========================================================= */
(function () {
  "use strict";

  var MAIL = "aaron.harfi@noxemgroup.com";
  var WHATSAPP = "33769725892";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var T = window.NOXEM_I18N;
  var lang = "en";

  /* =======================================================
     1. NUANCIER — les 30 teintes du nuancier physique
     Pour modifier une teinte : changer hex. metal = effet métallisé.
     ======================================================= */
  var COLORS = [
    { ref: "NX-01", en: "Bright Silver",  fr: "Argent brillant",   hex: "#C6CACD", metal: 1 },
    { ref: "NX-02", en: "Pure White",     fr: "Blanc pur",         hex: "#F2F4F6" },
    { ref: "NX-03", en: "Mint Green",     fr: "Vert menthe",       hex: "#A9D9C2" },
    { ref: "NX-04", en: "Lemon Yellow",   fr: "Jaune citron",      hex: "#E6D144" },
    { ref: "NX-05", en: "Pink",           fr: "Rose",              hex: "#E88CB2" },
    { ref: "NX-06", en: "Bordeaux Red",   fr: "Rouge bordeaux",    hex: "#6A1B30" },

    { ref: "NX-07", en: "Silver",         fr: "Argent",            hex: "#C2C7CB", metal: 1 },
    { ref: "NX-08", en: "Off White",      fr: "Blanc cassé",       hex: "#E3E2D7" },
    { ref: "NX-09", en: "Jade Green",     fr: "Vert jade",         hex: "#9FC3BF", metal: 1 },
    { ref: "NX-10", en: "Sign Yellow",    fr: "Jaune publicitaire",hex: "#F0C31C" },
    { ref: "NX-11", en: "Fuchsia Pink",   fr: "Rose fuchsia",      hex: "#CD1F5C" },
    { ref: "NX-12", en: "Wine Red",       fr: "Rouge vin",         hex: "#8D1516" },

    { ref: "NX-13", en: "Pearl White",    fr: "Blanc nacré",       hex: "#E7E8E5", metal: 1 },
    { ref: "NX-14", en: "Ivory",          fr: "Ivoire",            hex: "#D9DCD7" },
    { ref: "NX-15", en: "Blue Grey",      fr: "Bleu gris",         hex: "#A9C5DB" },
    { ref: "NX-16", en: "Bright Yellow",  fr: "Jaune vif",         hex: "#F2B32B" },
    { ref: "NX-17", en: "Orange Red",     fr: "Rouge orangé",      hex: "#E64C1B" },
    { ref: "NX-18", en: "Maroon Red",     fr: "Rouge marron",      hex: "#4B1519" },

    { ref: "NX-19", en: "Champagne Gold", fr: "Or champagne",      hex: "#DFC667", metal: 1 },
    { ref: "NX-20", en: "Cream",          fr: "Crème",             hex: "#DEE0D3" },
    { ref: "NX-21", en: "Rose Beige",     fr: "Beige rosé",        hex: "#D9BAA7" },
    { ref: "NX-22", en: "Saffron Yellow", fr: "Jaune safran",      hex: "#ECA527" },
    { ref: "NX-23", en: "Chinese Red",    fr: "Rouge chinois",     hex: "#D5211D" },
    { ref: "NX-24", en: "Black",          fr: "Noir",              hex: "#151515" },

    { ref: "NX-25", en: "Copper",         fr: "Cuivre",            hex: "#D8A46D", metal: 1 },
    { ref: "NX-26", en: "Milky White",    fr: "Blanc laiteux",     hex: "#EDE6BF" },
    { ref: "NX-27", en: "Salmon Pink",    fr: "Rose saumon",       hex: "#E08979" },
    { ref: "NX-28", en: "Orange",         fr: "Orange",            hex: "#E98C1F" },
    { ref: "NX-29", en: "Carmine Red",    fr: "Rouge carmin",      hex: "#B2202B" },
    { ref: "NX-30", en: "Deep Black",     fr: "Noir profond",      hex: "#1E1E1E" }
  ];

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* =======================================================
     2. LANGUES
     ======================================================= */
  function detectLang() {
    /* page pré-générée (/fr/, /ar/…) : sa langue prime */
    if (window.NOXEM_LANG && T[window.NOXEM_LANG]) return window.NOXEM_LANG;
    var saved;
    try { saved = localStorage.getItem("noxem-lang"); } catch (e) {}
    if (saved && T[saved]) return saved;
    var nav = (navigator.language || "en").slice(0, 2).toLowerCase();
    return T[nav] ? nav : "en";
  }

  function applyLang(code) {
    if (!T[code]) code = "en";
    lang = code;
    var d = T[code];

    document.documentElement.lang = code;
    document.documentElement.dir = d._dir;
    document.title = d.meta_title;

    $$("[data-i18n]").forEach(function (el) {
      var v = d[el.getAttribute("data-i18n")];
      if (typeof v === "string") el.textContent = v;
    });

    buildMarquee(d.mq);
    paintPick();
    try { localStorage.setItem("noxem-lang", code); } catch (e) {}

    var cur = $("#lang-current");
    if (cur) cur.textContent = d._name;

    /* lien WhatsApp : message pré-rempli dans la langue affichée */
    var wa = $("#wa-float");
    if (wa) wa.href = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(d.wa_msg);
    $$("#lang-menu button").forEach(function (b) {
      b.setAttribute("aria-selected", b.getAttribute("data-lang") === code ? "true" : "false");
    });
  }

  /* menu déroulant des langues */
  function initLangMenu() {
    var box = $("#lang"), btn = $("#lang-btn");
    if (!box || !btn) return;

    function close() {
      box.classList.remove("is-open");
      btn.setAttribute("aria-expanded", "false");
    }

    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = box.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });

    $$("#lang-menu button").forEach(function (b) {
      b.addEventListener("click", function () {
        applyLang(b.getAttribute("data-lang"));
        close();
      });
    });

    document.addEventListener("click", function (e) {
      if (!box.contains(e.target)) close();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  function buildMarquee(items) {
    var track = $("#marquee-track");
    if (!track || !items) return;
    var html = "";
    for (var pass = 0; pass < 2; pass++) {
      items.forEach(function (t) { html += "<span>" + t + "</span><i>◆</i>"; });
    }
    track.innerHTML = html;
  }

  /* =======================================================
     3. STUDIO 3D — nuancier interactif
     ======================================================= */
  var current = COLORS[0];
  var stage = $("#stage");

  function buildSwatches() {
    var wrap = $("#swatches");
    var grid = $("#chartgrid");
    if (!wrap) return;

    COLORS.forEach(function (c, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "sw" + (c.metal ? " sw--metal" : "") + (i === 0 ? " is-active" : "");
      b.style.setProperty("--sw", c.hex);
      b.title = c.ref + " · " + c.en;
      b.setAttribute("aria-label", c.en);
      b.addEventListener("click", function () {
        $$(".sw", wrap).forEach(function (x) { x.classList.remove("is-active"); });
        b.classList.add("is-active");
        pick(c);
      });
      wrap.appendChild(b);

      if (grid) {
        var cell = document.createElement("div");
        cell.className = "chartcell" + (c.metal ? " chartcell--metal" : "");
        cell.style.setProperty("--sw", c.hex);
        cell.innerHTML = "<span class='chartcell__chip'></span><b>" + c.en + "</b><em>" + c.ref + " · " + c.fr + "</em>";
        grid.appendChild(cell);
      }
    });

    addCustomSwatch(wrap);
  }

  /* tuile finale : toute autre teinte RAL ou sur mesure */
  function addCustomSwatch(wrap) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "sw sw--custom";
    b.textContent = "RAL";
    b.title = "RAL / custom";
    b.setAttribute("aria-label", "RAL / custom colour");
    b.addEventListener("click", function () { fillQuote("RAL / custom — reference to be specified"); });
    wrap.appendChild(b);
  }

  function pick(c) {
    current = c;
    if (stage) {
      stage.style.setProperty("--c", c.hex);
      stage.classList.toggle("is-metal", !!c.metal);
    }
    paintPick();
  }

  function paintPick() {
    var dot = $("#pick-dot"), name = $("#pick-name"), sub = $("#pick-sub");
    if (dot) dot.style.background = current.hex;
    if (name) name.textContent = lang === "fr" ? current.fr : current.en;
    if (sub) sub.textContent = current.ref + " · " + (lang === "fr" ? current.en : current.fr);
  }

  /* épaisseur du panneau -> épaisseur des tranches dans la pile 3D */
  function applyThickness() {
    var sel = $("#cfg-thickness");
    if (!sel || !stage) return;
    var mm = parseFloat(sel.value) || 4;
    stage.style.setProperty("--edge", (4.4 + mm * 1.9).toFixed(1) + "px");
  }

  /* rotation à la souris / au doigt */
  function enableDrag() {
    var room = $("#room");
    if (!room || !stage) return;
    var ry = -26, rx = -18, down = false, px = 0, py = 0, zoom = 0.74;

    function fit() {
      zoom = Math.max(0.40, Math.min(0.80, stage.clientWidth / 880));
      set();
    }
    function set() {
      room.style.transform = "scale(" + zoom.toFixed(3) + ") rotateX(" + rx + "deg) rotateY(" + ry + "deg)";
    }
    fit();
    window.addEventListener("resize", fit);

    stage.addEventListener("pointerdown", function (e) {
      down = true; px = e.clientX; py = e.clientY;
      stage.setPointerCapture(e.pointerId);
      stage.classList.add("is-dragging");
    });
    stage.addEventListener("pointermove", function (e) {
      if (!down) return;
      ry += (e.clientX - px) * 0.35;
      rx -= (e.clientY - py) * 0.22;
      rx = Math.max(-44, Math.min(6, rx));
      ry = Math.max(-72, Math.min(18, ry));
      px = e.clientX; py = e.clientY;
      set();
    });
    ["pointerup", "pointercancel", "pointerleave"].forEach(function (ev) {
      stage.addEventListener(ev, function () { down = false; stage.classList.remove("is-dragging"); });
    });
  }

  /* =======================================================
     4. FORMULAIRE
     ======================================================= */
  function fillQuote(forcedColour) {
    var g = function (id) { var e = $(id); return e ? e.value : ""; };
    var set = function (id, v) { var e = $(id); if (e) e.value = v; };

    set("#f-colour", forcedColour || (current.ref + " " + current.en + " (" + current.fr + ")"));
    set("#f-thickness", g("#cfg-thickness"));
    set("#f-skin", g("#cfg-skin"));
    set("#f-core", g("#cfg-core"));

    var msg = $("#f-msg");
    if (msg && !msg.value.trim()) {
      msg.value = T[lang].col_lbl_coating + ": " + g("#cfg-coating") + "\n";
    }
    var target = $("#quote");
    if (target) target.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
    setTimeout(function () { var n = $("#f-name"); if (n) n.focus({ preventScroll: true }); }, reduced ? 0 : 600);
  }

  function initForm() {
    var form = $("#quote-form"), status = $("#form-status");
    if (!form) return;

    form.addEventListener("input", function (e) {
      if (e.target.classList) e.target.classList.remove("is-error");
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var d = T[lang];
      var val = function (id) { var el = $(id); return el && el.value.trim() ? el.value.trim() : "—"; };
      var bad = false;

      [["#f-name", 0], ["#f-email", 1], ["#f-msg", 0]].forEach(function (p) {
        var el = $(p[0]); if (!el) return;
        var empty = !el.value.trim();
        var badMail = p[1] && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim());
        el.classList.toggle("is-error", empty || badMail);
        if (empty || badMail) bad = true;
      });

      if (bad) {
        if (status) { status.textContent = d.f_err; status.className = "form__status is-error"; }
        return;
      }

      var lines = [
        d.f_name + ": " + val("#f-name"),
        d.f_company + ": " + val("#f-company"),
        d.f_email + ": " + val("#f-email"),
        d.f_phone + ": " + val("#f-phone"),
        d.f_country + ": " + val("#f-country"),
        d.f_port + ": " + val("#f-port"),
        "",
        d.f_colour + ": " + val("#f-colour"),
        d.f_thickness + ": " + val("#f-thickness"),
        d.f_skin + ": " + val("#f-skin"),
        d.f_core + ": " + val("#f-core"),
        d.f_size + ": " + val("#f-size"),
        d.f_qty + ": " + val("#f-qty"),
        "",
        d.f_msg + ":",
        val("#f-msg"),
        "",
        "— noxemgroup.com (" + T[lang]._name + ")"
      ].join("\n");

      var subject = d.f_subject + " — " + val("#f-name") + " — " + val("#f-country");
      window.location.href = "mailto:" + MAIL +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(lines);

      if (status) { status.textContent = d.f_ok; status.className = "form__status is-ok"; }
    });
  }

  /* =======================================================
     5. INTERFACE — header, menu, apparitions, compteurs
     ======================================================= */
  function initChrome() {
    var y = $("#year"); if (y) y.textContent = new Date().getFullYear();

    var header = $("#header"), fab = $("#fab");
    function onScroll() {
      var s = window.scrollY;
      if (header) header.classList.toggle("is-stuck", s > 40);
      if (fab) fab.classList.toggle("is-visible", s > 800);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    var burger = $("#burger"), nav = $("#nav");
    if (burger && nav) {
      burger.addEventListener("click", function () {
        var open = nav.classList.toggle("is-open");
        burger.classList.toggle("is-open", open);
        burger.setAttribute("aria-expanded", open ? "true" : "false");
      });
      nav.addEventListener("click", function (e) {
        if (e.target.tagName === "A") {
          nav.classList.remove("is-open");
          burger.classList.remove("is-open");
          burger.setAttribute("aria-expanded", "false");
        }
      });
    }

    var rev = $$(".reveal");
    if (reduced || !("IntersectionObserver" in window)) {
      rev.forEach(function (el) { el.classList.add("is-visible"); });
    } else {
      var ro = new IntersectionObserver(function (entries) {
        entries.forEach(function (en, i) {
          if (!en.isIntersecting) return;
          var el = en.target;
          setTimeout(function () { el.classList.add("is-visible"); }, Math.min(i * 80, 320));
          ro.unobserve(el);
        });
      }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });
      rev.forEach(function (el) { ro.observe(el); });
    }

    var counters = $$("[data-count]");
    function run(el) {
      var target = parseFloat(el.getAttribute("data-count")) || 0;
      var suffix = el.getAttribute("data-suffix") || "";
      if (reduced) { el.textContent = target + suffix; return; }
      var t0 = null;
      requestAnimationFrame(function step(ts) {
        if (t0 === null) t0 = ts;
        var p = Math.min((ts - t0) / 1300, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix;
        if (p < 1) requestAnimationFrame(step);
      });
    }
    if ("IntersectionObserver" in window) {
      var co = new IntersectionObserver(function (es) {
        es.forEach(function (en) { if (en.isIntersecting) { run(en.target); co.unobserve(en.target); } });
      }, { threshold: 0.5 });
      counters.forEach(function (el) { co.observe(el); });
    } else { counters.forEach(run); }

    /* photos : on n'affiche l'image que si le fichier existe réellement */
    $$(".shot__img").forEach(function (img) {
      var fig = img.closest(".shot");
      if (!fig) return;
      if (img.complete && img.naturalWidth > 0) fig.classList.add("has-photo");
      img.addEventListener("load", function () {
        if (img.naturalWidth > 0) fig.classList.add("has-photo");
      });
    });
  }

  /* =======================================================
     6. DÉMARRAGE
     ======================================================= */
  buildSwatches();
  pick(COLORS[0]);
  applyThickness();
  enableDrag();
  initForm();
  initChrome();
  initLangMenu();
  applyLang(detectLang());

  var th = $("#cfg-thickness");
  if (th) th.addEventListener("change", applyThickness);

  var cta = $("#to-quote");
  if (cta) cta.addEventListener("click", function () { fillQuote(); });

})();
