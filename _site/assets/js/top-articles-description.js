document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".top-articles-placeholder").forEach(placeholder => {
        let articlesData = placeholder.getAttribute("data-articles").replace(/&quot;/g, '"');
        const articles = JSON.parse(articlesData || "[]");
        
        let isEnglish = false;

        function renderArticles() {
            placeholder.innerHTML = articles.map((article, index) => `
                <a href="${article.link}" class="top-article-description">
                    <img src="${article.image}" alt="${article.title}">
                    <div class="text">
                        <div class="title">${article.title}</div>
                        <div class="link">${article.enseigne}</div>
                        <div class="info">${isEnglish ? article.info_top_en : article.info_top}</div>
                    </div>
                </a>
            `).join("");
        }

        // Render articles initially
        renderArticles();

        // Add language toggle button
        const toggleButton = document.createElement("button");
        toggleButton.className = "language-button";
        toggleButton.innerText = "Switch to English";
        toggleButton.addEventListener("click", () => {
            isEnglish = !isEnglish;
            toggleButton.innerText = isEnglish ? "Passer en Français" : "Switch to English";
            renderArticles();
        });

        const buttonContainer = document.createElement("div");
        buttonContainer.className = "language-toggle";
        buttonContainer.appendChild(toggleButton);
        placeholder.parentNode.insertBefore(buttonContainer, placeholder.nextSibling);
    });
});

// document.addEventListener("DOMContentLoaded", function () {
//     const placeholder = document.querySelector(".top-articles-placeholder");
//     const articlesData = JSON.parse(placeholder.getAttribute("data-articles"));

//     // Clear placeholder content before inserting dynamically
//     placeholder.innerHTML = "";

//     articlesData.forEach((article) => {
//         // Create the article container
//         const articleElement = document.createElement("div");
//         articleElement.classList.add("top-article-description");

//         // Inject HTML structure for the article
//         articleElement.innerHTML = `
//             <div class="top-article-description-image">
//                 <span class="article-rank">${article.rank}</span>
//                 <img src="${article.image}" alt="${article.title}">
//                 <div class="overlay">
//                     <h2 class="article-description-title">${article.title}</h2>
//                     <span class="article-description-enseigne">${article.enseigne}</span>
//                 </div>
//             </div>
//             <div class="top-article-description-info">
//                 ${article.info_top}
//             </div>
//         `;

//         // Append the article to the placeholder
//         placeholder.appendChild(articleElement);
//     });
// });
