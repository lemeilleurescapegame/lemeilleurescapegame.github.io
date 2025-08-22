document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".top-articles-placeholder-child").forEach(placeholder => {
        const articles = JSON.parse(placeholder.getAttribute("data-articles") || "[]");

        if (articles.length > 0) {
            placeholder.innerHTML = articles.map((article, index) => {
                // Check if the closed property has any non-empty value
                const isClosed = article.closed && article.closed.trim() !== "";

                return `
                    <a href="${article.link}" class="child-escape-card ${isClosed ? 'closed' : ''}">
                        <div class="child-rank">•</div>
                        <img class="child-image" src="${article.image}" alt="${article.title}">
                        <div class="child-info">
                            <div class="child-title">${article.title}</div>
                            <div class="child-enseigne">${article.enseigne}</div>
                            <div class="child-details">
                                <span class="child-age">👶 Age: ${article.age || "N/A"}</span>
                                <span class="child-accompagnant">👨‍👩‍👧 Accompagnant: ${article.accompagnant || "N/A"}</span>
                            </div>
                            ${isClosed ? `<div class="child-status">❌ Fermé</div>` : ""}
                        </div>
                    </a>
                `;
            }).join("");
        }
    });
});
