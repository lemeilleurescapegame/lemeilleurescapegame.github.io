// document.addEventListener("DOMContentLoaded", function () {
//     const placeholder = document.querySelector(".top-articles-placeholder");
//     const articlesData = JSON.parse(placeholder.getAttribute("data-articles"));

//     placeholder.innerHTML = ""; // Clear placeholder content before inserting

//     articlesData.forEach((article) => {
//         const articleElement = document.createElement("div");
//         articleElement.classList.add("top-article-description");
//         articleElement.setAttribute("data-article", JSON.stringify(article)); // Store article data for easy access

//         // Wrap everything inside an anchor tag to make it clickable
//         articleElement.innerHTML = `
//             <a href="${article.link}" class="top-article-description-link">
//                 <div class="top-article-description-image">
//                     <span class="article-rank-description">${article.rank}</span>
//                     <img src="${article.image}" alt="${article.title}">
//                     <div class="overlay">
//                         <h2 class="article-description-title">${article.title}</h2>
//                         <span class="article-description-enseigne">${article.enseigne}</span>
//                     </div>
//                 </div>
//                 <div class="top-article-description-info">
//                     ${article.info_top.replace(/\n/g, "<br>")}
//                 </div>
//             </a>
//         `;

//         placeholder.appendChild(articleElement);
//     });
// });

document.addEventListener("DOMContentLoaded", function () {
    const placeholder = document.querySelector(".top-articles-placeholder");
    const articlesData = JSON.parse(placeholder.getAttribute("data-articles"));

    placeholder.innerHTML = ""; // Clear placeholder content before inserting

    articlesData.forEach((article) => {
        const articleElement = document.createElement("div");
        articleElement.classList.add("top-article-description");
        articleElement.setAttribute("data-article", JSON.stringify(article)); // Store article data for easy access

        // Wrap everything inside an anchor tag to make it clickable
        articleElement.innerHTML = `
            <a href="${article.link}" class="top-article-description-link">
                <div class="top-article-description-image">
                    <span class="article-rank-description">${article.rank}</span>
                    <img src="${article.image}" alt="${article.title}">
                    <div class="overlay">
                        <h2 class="article-description-title">${article.title.replace(/'/g, "&#39;")}</h2> <!-- Escape single quotes -->
                        <span class="article-description-enseigne">${article.enseigne}</span>
                    </div>
                </div>
                <div class="top-article-description-info">
                    ${article.info_top.replace(/\n/g, "<br>")}
                </div>
            </a>
        `;

        placeholder.appendChild(articleElement);
    });
});
