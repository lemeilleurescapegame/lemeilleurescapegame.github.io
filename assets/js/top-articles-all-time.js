document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".blackgold-top-data").forEach(placeholder => {
    const articles = JSON.parse(placeholder.getAttribute("data-articles") || "[]");

    if (articles.length > 0) {
      placeholder.innerHTML = articles.map((article, index) => `
        <a href="${article.link}" class="blackgold-article-card">
          <div class="blackgold-article-rank">
            👑<span>#${index + 1}</span>
          </div>

          <div class="blackgold-article-main">
            <div class="blackgold-article-image-wrapper">
              <img src="${article.image}" alt="${article.title}">
            </div>
            <div class="blackgold-article-content">
              <div class="blackgold-article-title">${article.title}</div>
              <div class="blackgold-article-enseigne">${article.enseigne}</div>
            </div>
          </div>

          ${article.note ? `
             <div class="blackgold-note-wrapper">
               <button class="blackgold-note-button">Notre avis</button>
             </div>` : ""}
        </a>
      `).join("");
    }
  });
});