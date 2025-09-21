(function () {
  const KEY = "theme";
  const root = document.documentElement;
  const btn = document.getElementById("themeToggle");

  const saved = localStorage.getItem(KEY);
  const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  const initial = saved || (prefersDark ? "dark" : "light");
  setTheme(initial);

  btn?.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    setTheme(next);
  });

  function setTheme(mode) {
    root.setAttribute("data-theme", mode);
    localStorage.setItem(KEY, mode);
    if (btn) {
      btn.textContent = mode === "dark" ? "Light" : "Dark";
      btn.setAttribute("aria-pressed", mode === "dark" ? "true" : "false");
      btn.setAttribute("title", mode === "dark" ? "Switch to light mode" : "Switch to dark mode");
    }
  }

  const navToggle = document.getElementById("navToggle");
  const navMenu = document.getElementById("navMenu");

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", (e) => {
      e.stopPropagation();
      const expanded = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!expanded));
      if (navMenu.hasAttribute("hidden")) navMenu.removeAttribute("hidden");
      navMenu.classList.toggle("open", !expanded);

      if (expanded) {
        const onEnd = () => {
          if (!navMenu.classList.contains("open")) navMenu.setAttribute("hidden", "");
          navMenu.removeEventListener("transitionend", onEnd);
        };
        navMenu.addEventListener("transitionend", onEnd);
      }
    });

    document.addEventListener("click", (e) => {
      if (!navMenu.classList.contains("open")) return;
      if (navMenu.contains(e.target) || navToggle.contains(e.target)) return;
      navToggle.setAttribute("aria-expanded", "false");
      navMenu.classList.remove("open");
      const onEnd = () => {
        if (!navMenu.classList.contains("open")) navMenu.setAttribute("hidden", "");
        navMenu.removeEventListener("transitionend", onEnd);
      };
      navMenu.addEventListener("transitionend", onEnd);
    });

    navMenu.querySelectorAll("a").forEach(a => {
      a.addEventListener("click", () => {
        navToggle.setAttribute("aria-expanded", "false");
        navMenu.classList.remove("open");
        const onEnd = () => {
          if (!navMenu.classList.contains("open")) navMenu.setAttribute("hidden", "");
          navMenu.removeEventListener("transitionend", onEnd);
        };
        navMenu.addEventListener("transitionend", onEnd);
      });
    });
  }
})();