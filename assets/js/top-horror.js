document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".top-articles-placeholder-horreur").forEach(placeholder => {
    const articles = JSON.parse(placeholder.getAttribute("data-articles") || "[]");

    if (articles.length > 0) {
      placeholder.innerHTML = articles.map((article, index) => `
        <a href="${article.link}" class="horreur-article-card">
          <div class="horreur-article-rank">
            🩸<span>#${index + 1}</span>
          </div>

          <div class="horreur-article-main">
            <div class="horreur-article-image-wrapper">
              <img src="${article.image}" alt="${article.title}">
            </div>
            <div class="horreur-article-content">
              <div class="horreur-article-title">${article.title}</div>
              <div class="horreur-article-enseigne">${article.enseigne}</div>
            </div>
          </div>

          ${article.scaremeter ? `
            <div class="horreur-scaremeter">
            <div class="scaremeter-label">Scare Meter</div>
              <div class="scaremeter-thermo">
                <div class="scaremeter-fill" style="height: ${Math.min(100, (article.scaremeter/10)*100)}%"></div>
              </div>
              <span class="scaremeter-label">${article.scaremeter}/10</span>
            </div>
          ` : ""}
        </a>
      `).join("");
    }
  });
});
