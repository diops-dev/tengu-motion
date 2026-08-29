/* Tengu Motion & Drone — comportements du site.
   Sans dépendance. Le site reste entièrement utilisable si ce fichier ne charge pas. */
(function () {
  "use strict";

  /* ── Menu mobile ──────────────────────────────────────────────────── */
  var toggle = document.querySelector(".nav__toggle");
  var links = document.getElementById("nav-links");

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.getAttribute("data-open") === "true";
      links.setAttribute("data-open", String(!open));
      toggle.setAttribute("aria-expanded", String(!open));
      toggle.textContent = open ? "Menu" : "Fermer";
    });

    // Referme le menu à l'échappement, puis rend le focus au bouton.
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && links.getAttribute("data-open") === "true") {
        links.setAttribute("data-open", "false");
        toggle.setAttribute("aria-expanded", "false");
        toggle.textContent = "Menu";
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

  function say(msg, tone) {
    if (!status) { return; }
    status.textContent = msg;
    status.style.color = tone === "error" ? "#9B2226" : "#2D2D2D";
  }

  form.addEventListener("submit", function (e) {
    // Endpoint non configuré : on compose un email plutôt que d'échouer en silence.
    if (!configured) {
      e.preventDefault();
      var d = new FormData(form);
      var corps = [
        "Nom / société : " + (d.get("nom") || ""),
        "Email : " + (d.get("email") || ""),
        "Téléphone : " + (d.get("telephone") || ""),
        "Prestation : " + (d.get("prestation") || ""),
        "Livrable : " + (d.get("livrable") || ""),
        "",
        d.get("message") || ""
      ].join("\n");
      window.location.href = "mailto:video@tengumotion.com"
        + "?subject=" + encodeURIComponent("Demande de devis — " + (d.get("nom") || "site web"))
        + "&body=" + encodeURIComponent(corps);
      say("Votre logiciel de messagerie s'ouvre avec la demande pré-remplie.");
      return;
    }

    // Endpoint configuré : envoi en arrière-plan, sans quitter la page.
    e.preventDefault();
    say("Envoi en cours…");
    fetch(action, {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "application/json" }
    }).then(function (r) {
      if (!r.ok) { throw new Error("http " + r.status); }
      form.reset();
      say("Demande reçue. Devis personnalisé sous 24 h, avec plan de vol et fenêtres de tournage.");
    }).catch(function () {
      say("L'envoi a échoué. Écrivez-nous à video@tengumotion.com ou appelez le +33 6 33 59 87 74.", "error");
    });
  });
})();
