/* Tengu Motion & Drone — comportements du site.
   Sans dépendance. Le site reste entièrement utilisable si ce fichier ne charge pas.

   Ce script est unique pour les trois langues : tous les textes affichés
   proviennent d'attributs data-* posés sur le formulaire par le générateur. */
(function () {
  "use strict";

  /* ── Menu mobile ──────────────────────────────────────────────────── */
  var toggle = document.querySelector(".nav__toggle");
  var links = document.getElementById("nav-links");

  if (toggle && links) {
    var opened = toggle.getAttribute("data-label-close") || toggle.textContent;
    var closed = toggle.textContent;

    function setMenu(open) {
      links.setAttribute("data-open", String(open));
      toggle.setAttribute("aria-expanded", String(open));
      toggle.textContent = open ? opened : closed;
    }

    toggle.addEventListener("click", function () {
      setMenu(links.getAttribute("data-open") !== "true");
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && links.getAttribute("data-open") === "true") {
        setMenu(false);
        toggle.focus();
      }
    });
  }

  /* ── Année du copyright ───────────────────────────────────────────── */
  var y = document.querySelectorAll("[data-year]");
  for (var i = 0; i < y.length; i++) { y[i].textContent = String(new Date().getFullYear()); }

  /* ── Formulaire de devis ──────────────────────────────────────────────
     Le formulaire poste vers le service défini dans son attribut action
     (Formspree par défaut — voir README). Tant que l'endpoint n'est pas
     configuré, on bascule sur un mailto pour ne jamais perdre une demande. */
  var form = document.getElementById("devis-form");
  if (!form) { return; }

  var status = document.getElementById("form-status");
  var action = form.getAttribute("action") || "";
  var configured = action.indexOf("VOTRE_ID") === -1 && action.indexOf("http") === 0;
  function msg(name) { return form.getAttribute("data-" + name) || ""; }

  function say(text, tone) {
    if (!status) { return; }
    status.textContent = text;
    status.style.color = tone === "error" ? "#9B2226" : "#2D2D2D";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var d = new FormData(form);

    // Endpoint non configuré : on compose un email plutôt que d'échouer en silence.
    if (!configured) {
      var body = [
        msg("l-name") + " : " + (d.get("nom") || ""),
        msg("l-email") + " : " + (d.get("email") || ""),
        msg("l-phone") + " : " + (d.get("telephone") || ""),
        msg("l-type") + " : " + (d.get("prestation") || ""),
        msg("l-deliverable") + " : " + (d.get("livrable") || ""),
        "",
        d.get("message") || ""
      ].join("\n");
      window.location.href = "mailto:" + (msg("to") || "video@tengumotion.com")
        + "?subject=" + encodeURIComponent(msg("subject") + " — " + (d.get("nom") || "web"))
        + "&body=" + encodeURIComponent(body);
      say(msg("msg-mailto"));
      return;
    }

    // Endpoint configuré : envoi en arrière-plan, sans quitter la page.
    say(msg("msg-sending"));
    fetch(action, {
      method: "POST",
      body: d,
      headers: { Accept: "application/json" }
    }).then(function (r) {
      if (!r.ok) { throw new Error("http " + r.status); }
      form.reset();
      say(msg("msg-ok"));
    }).catch(function () {
      say(msg("msg-error"), "error");
    });
  });
})();
