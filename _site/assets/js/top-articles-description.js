document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".top-articles-placeholder-description").forEach(placeholder => {
        // Safely parse JSON
        let articles = [];
        try {
            articles = JSON.parse(placeholder.getAttribute("data-articles") || "[]");
        } catch (error) {
            console.error("❌ JSON parsing error:", error);
            return;
        }

        console.log("✅ Loaded articles:", articles); // Debugging

        if (articles.length > 0) {
            placeholder.innerHTML = ""; // Clear content before adding new elements

            articles.forEach((article, index) => {
                // Create elements
                const articleElement = document.createElement("div");
                articleElement.classList.add("top-article-description");
                articleElement.setAttribute("data-article", JSON.stringify(article));

                const linkElement = document.createElement("a");
                linkElement.href = article.link;
                linkElement.classList.add("top-article-description-link");

                const imageContainer = document.createElement("div");
                imageContainer.classList.add("top-article-description-image");

                const rankSpan = document.createElement("span");
                rankSpan.classList.add("article-rank-description");
                rankSpan.textContent = article.rank;

                const imageElement = document.createElement("img");
                imageElement.src = article.image;
                imageElement.alt = article.title;

                const overlayDiv = document.createElement("div");
                overlayDiv.classList.add("overlay");

                const titleElement = document.createElement("h2");
                titleElement.classList.add("article-description-title");
                titleElement.textContent = article.title; // SAFE: No HTML parsing issues

                const enseigneSpan = document.createElement("span");
                enseigneSpan.classList.add("article-description-enseigne");
                enseigneSpan.textContent = article.enseigne;

                const infoDiv = document.createElement("div");
                infoDiv.classList.add("top-article-description-info");
                infoDiv.innerHTML = article.info_top.replace(/\n/g, "<br>"); // HTML allowed for line breaks

                // Build the structure
                overlayDiv.appendChild(titleElement);
                overlayDiv.appendChild(enseigneSpan);

                imageContainer.appendChild(rankSpan);
                imageContainer.appendChild(imageElement);
                imageContainer.appendChild(overlayDiv);

                linkElement.appendChild(imageContainer);
                linkElement.appendChild(infoDiv);

                articleElement.appendChild(linkElement);
                placeholder.appendChild(articleElement);
            });

            console.log("✅ Articles rendered successfully");
        } else {
            console.warn("⚠️ No articles found.");
        }
    });
});
