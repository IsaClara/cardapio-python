document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".comida_descricao").forEach((el) => {
    const fullText = el.dataset.fulltext;
    const LIMIT = 47;

    if (!fullText) return;

    if (fullText.length <= LIMIT) {
      el.textContent = fullText;
      return;
    }

    const shortText = fullText.slice(0, LIMIT);

    el.innerHTML = `
      ${shortText}...
      <span class="ver-mais">Ver mais</span>
    `;

    let expanded = false;

    el.addEventListener("click", (e) => {
      if (!e.target.classList.contains("ver-mais")) return;

      expanded = !expanded;

      el.innerHTML = expanded
        ? `${fullText} <span class="ver-mais">Ver menos</span>`
        : `${shortText}... <span class="ver-mais">Ver mais</span>`;
    });
  });
});
