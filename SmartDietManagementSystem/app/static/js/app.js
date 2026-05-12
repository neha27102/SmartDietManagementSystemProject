const root = document.documentElement;
const savedTheme = localStorage.getItem("fitness-pro-theme");
if (savedTheme) root.dataset.theme = savedTheme;

document.getElementById("themeToggle")?.addEventListener("click", () => {
  root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
  localStorage.setItem("fitness-pro-theme", root.dataset.theme);
});

window.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) lucide.createIcons();
});
