document.addEventListener('DOMContentLoaded', () => {
    const placeholder = document.querySelector('.featured-articles-placeholder');
    if (!placeholder) return;
  
    let articles = [];
  
    try {
      articles = JSON.parse(placeholder.dataset.featured);
    } catch (e) {
      console.error("Failed to parse featured articles JSON:", e);
      return;
    }
  
    placeholder.innerHTML = ''; // Clear placeholder
  
    articles.forEach(article => {
      const card = document.createElement('a');
      card.className = 'featured-article';
      card.href = article.link;
  
      card.innerHTML = `
        <span class="bullet">•</span>
        <img src="${article.image}" alt="${article.title}">
        <div class="text">
          <div class="title">${article.title}</div>
          <div class="theme">${article.enseigne}</div>
        </div>
        <button class="info-btn">More Info</button>
      `;
  
      const button = card.querySelector('.info-btn');
      button.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        window.location.href = article.link;
      });
  
      placeholder.appendChild(card);
    });
  });
  