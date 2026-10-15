/* ============================================================================
   Versal — Bewegung
   Faehrt, was CSS nicht kann. Alle Dauern und Kurven stehen im Stylesheet,
   damit es genau eine Quelle fuer die Werte gibt. Siehe DESIGN.md 4.

   Die Vorlage animiert ueberwiegend per JavaScript (GSAP und ScrollTrigger
   sind dort geladen, 86 Elemente tragen eingebettete Transformationen).
   Hier wird stattdessen die gemessene CSS-Grammatik benutzt — eine
   Schriftgiesserei laedt keine 70 kB Animationsbibliothek fuer ein paar
   Blenden. Begruendung in DESIGN.md 4.5.
   ========================================================================== */
(() => {
  "use strict";
  const sparsam = matchMedia("(prefers-reduced-motion: reduce)");

  /* -- Einblenden beim Scrollen ------------------------------------------
     Gemessen: 700 ms easeOutQuint auf Opazitaet und Versatz. */
  const einblenden = () => {
    const stuecke = document.querySelectorAll("[data-ein]");
    if (!stuecke.length) return;
    if (sparsam.matches) { stuecke.forEach(e => e.classList.add("da")); return; }

    const beobachter = new IntersectionObserver((eintraege) => {
      for (const e of eintraege) {
        if (!e.isIntersecting) continue;
        e.target.classList.add("da");
        beobachter.unobserve(e.target);
      }
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0 });
    stuecke.forEach(e => beobachter.observe(e));

    /* Zwei Netze darunter. Die ganze Seitenschrift startet auf Opazitaet 0 —
       loest der Beobachter nicht aus, bleibt die Seite leer. Das darf nicht
       an einem einzigen Ausloeser haengen.
         Netz 1: Was beim Laden im Bild steht, wird sofort gezeigt.
         Netz 2: Nach 2,5 s ohne jede Reaktion faellt alles sichtbar. */
    const zeigeSichtbare = () => {
      for (const el of stuecke) {
        if (el.classList.contains("da")) continue;
        const r = el.getBoundingClientRect();
        if (r.top < innerHeight && r.bottom > 0) {
          el.classList.add("da");
          beobachter.unobserve(el);
        }
      }
    };
    requestAnimationFrame(zeigeSichtbare);
    setTimeout(() => {
      if ([...stuecke].some(el => el.classList.contains("da"))) return;
      stuecke.forEach(el => { el.classList.add("da"); beobachter.unobserve(el); });
    }, 2500);
  };

  /* -- Handymenue --------------------------------------------------------
     visibility mit Verzug, damit es sichtbar bleibt, solange es ausblendet.
     Gemessen an der Vorlage. */
  const menue = () => {
    const brenner = document.querySelector(".brenner");
    const tafel = document.querySelector(".menue");
    if (!brenner || !tafel) return;

    const setze = (auf) => {
      tafel.dataset.auf = auf ? "ja" : "nein";
      brenner.setAttribute("aria-expanded", String(auf));
      document.documentElement.style.overflow = auf ? "hidden" : "";
    };
    setze(false);
    brenner.addEventListener("click", () => setze(tafel.dataset.auf !== "ja"));
    tafel.querySelectorAll("a").forEach(a => a.addEventListener("click", () => setze(false)));
    addEventListener("keydown", (ev) => { if (ev.key === "Escape") setze(false); });
    matchMedia("(min-width:1000px)").addEventListener("change", (m) => {
      if (m.matches) setze(false);
    });
  };

  const los = () => { einblenden(); menue(); };
  if (document.readyState === "loading") addEventListener("DOMContentLoaded", los);
  else los();
})();
