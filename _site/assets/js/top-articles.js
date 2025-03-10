document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".top-articles-placeholder").forEach(placeholder => {
        const articles = JSON.parse(placeholder.getAttribute("data-articles") || "[]");

        if (articles.length > 0) {
            placeholder.innerHTML = articles.map((article, index) => `
                <a href="${article.link}" class="top-article">
                    <div class="rank">#${index + 1}</div>
                    <img src="${article.image}" alt="${article.title}">
                    <div class="text">
                        <div class="title">${article.title}</div>
                        <div class="link">${article.link}</div>
                    </div>
                    <div class="note">${article.note || "N/A"}/20</div>
                </a>
            `).join("");
        }
    });
});



