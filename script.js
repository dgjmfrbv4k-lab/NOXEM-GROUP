/* =========================================================
   NOXEM GROUP — interactions du site vitrine
   Aucune dépendance : tout tourne en local dans le navigateur.
   ========================================================= */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Année du copyright ---------- */
  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- Header collant + bouton flottant ---------- */
  var header = document.getElementById("header");
  var fab = document.getElementById("fab");

  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("is-stuck", y > 40);
    if (fab) fab.classList.toggle("is-visible", y > 700);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Menu mobile ---------- */
  var burger = document.getElementById("burger");
  var nav = document.getElementById("nav");

  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      burger.classList.toggle("is-open", open);
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      burger.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    });

    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("is-open");
        burger.classList.remove("is-open");
        burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------- Apparition au défilement ---------- */
  var revealables = document.querySelectorAll(".reveal");

  if (reduced || !("IntersectionObserver" in window)) {
    Array.prototype.forEach.call(revealables, function (el) { el.classList.add("is-visible"); });
  } else {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry, i) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        setTimeout(function () { el.classList.add("is-visible"); }, Math.min(i * 90, 360));
        revealObserver.unobserve(el);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -60px 0px" });

    Array.prototype.forEach.call(revealables, function (el) { revealObserver.observe(el); });
  }

  /* ---------- Compteurs du hero ---------- */
  var counters = document.querySelectorAll("[data-count]");

  function runCounter(el) {
    var target = parseFloat(el.getAttribute("data-count")) || 0;
    var suffix = el.getAttribute("data-suffix") || "";
    if (reduced) { el.textContent = target + suffix; return; }

    var duration = 1400;
    var start = null;

    function frame(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  if ("IntersectionObserver" in window) {
    var countObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        runCounter(entry.target);
        countObserver.unobserve(entry.target);
      });
    }, { threshold: 0.5 });
    Array.prototype.forEach.call(counters, function (el) { countObserver.observe(el); });
  } else {
    Array.prototype.forEach.call(counters, runCounter);
  }

  /* ---------- Sélecteur de finitions ---------- */
  var swatches = document.querySelectorAll(".swatch");
  var panel = document.getElementById("panel");
  var finishName = document.getElementById("finish-name");
  var finishRef = document.getElementById("finish-ref");

  Array.prototype.forEach.call(swatches, function (btn) {
    btn.addEventListener("click", function () {
      Array.prototype.forEach.call(swatches, function (b) { b.classList.remove("is-active"); });
      btn.classList.add("is-active");

      if (panel) panel.setAttribute("data-finish", btn.getAttribute("data-finish"));
      if (finishName) finishName.textContent = btn.getAttribute("data-name");
      if (finishRef) finishRef.textContent = btn.getAttribute("data-ref");
    });
  });

  /* ---------- Formulaire de devis (sans serveur : mailto) ---------- */
  var form = document.getElementById("quote-form");
  var status = document.getElementById("form-status");
  var DESTINATAIRE = "contact@noxem-group.com";

  function setStatus(msg, kind) {
    if (!status) return;
    status.textContent = msg;
    status.className = "form__status" + (kind ? " is-" + kind : "");
  }

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      var required = ["name", "email", "message"];
      var missing = false;

      required.forEach(function (id) {
        var input = document.getElementById(id);
        if (!input) return;
        var empty = !input.value.trim();
        var badMail = id === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim());
        input.classList.toggle("is-error", empty || badMail);
        if (empty || badMail) missing = true;
      });

      if (missing) {
        setStatus("Merci de renseigner votre nom, un email valide et la description du projet.", "error");
        return;
      }

      var get = function (id) {
        var el = document.getElementById(id);
        return el && el.value.trim() ? el.value.trim() : "—";
      };

      var subject = "Demande de devis — " + get("type") + " — " + get("name");
      var body = [
        "Nom : " + get("name"),
        "Société : " + get("company"),
        "Email : " + get("email"),
        "Téléphone : " + get("phone"),
        "Type de projet : " + get("type"),
        "Surface estimée : " + get("surface") + " m²",
        "",
        "Projet :",
        get("message"),
        "",
        "— Envoyé depuis le site NOXEM GROUP"
      ].join("\n");

      window.location.href =
        "mailto:" + DESTINATAIRE +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);

      setStatus("Votre messagerie s'ouvre avec la demande pré-remplie. Il ne reste qu'à l'envoyer.", "ok");
    });

    form.addEventListener("input", function (e) {
      if (e.target.classList) e.target.classList.remove("is-error");
    });
  }
})();
