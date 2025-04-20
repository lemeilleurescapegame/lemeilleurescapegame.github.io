document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".top-articles-placeholder").forEach(placeholder => {
        const articles = JSON.parse(placeholder.getAttribute("data-articles") || "[]");
        
        console.log("Loaded articles:", articles); // Debugging

        if (articles.length > 0) {
            placeholder.innerHTML = articles.map((article, index) => `
                <a href="${article.link}" class="top-article">
                    <div class="rank">#${index + 1}</div>
                    <img src="${article.image}" alt="${article.title}">
                    <div class="text">
                        <div class="title">${article.title}</div>
                        <div class="link">${article.enseigne}</div>
                    </div>
                    ${article.note ? `<div class="note">${article.note}/20</div>` : ""}
                </a>
            `).join("");

            console.log("Rendered HTML:", placeholder.innerHTML); // Debugging
        }
    });
});




