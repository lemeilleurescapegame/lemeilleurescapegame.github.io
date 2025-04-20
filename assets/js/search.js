(function() {
    function displaySearchResults(results, store) {
      print('--   >')
      var searchResults = document.getElementById('search-results');
  
      if (results.length) { // Are there any results?
        var appendString = '';
  
        for (var i = 0; i < results.length; i++) {  // Iterate over the results
          var item = store[results[i].ref];
          appendString += '<li><a href="' + item.url + '"><h3>' + item.title + '</h3></a>';
          appendString += '<p>' + item.content.substring(0, 150) + '...</p></li>';
        }
  
        searchResults.innerHTML = appendString;
      } else {
        searchResults.innerHTML = '<li>No results found</li>';
      }
    }
  
    function getQueryVariable(variable) {
      var query = window.location.search.substring(1);
      var vars = query.split('&');
  
      for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
  
        if (pair[0] === variable) {
          return decodeURIComponent(pair[1].replace(/\+/g, '%20'));
        }
      }
    }
  
    var searchTerm = getQueryVariable('query');
    if (searchTerm) {
      document.getElementById('search-box').setAttribute("value", searchTerm);
  
      // Initalize lunr with the fields it will be searching on. I've given title
      // a boost of 10 to indicate matches on this field are more important.
    //   var idx = lunr(function () {
    //     this.field('id');
    //     this.field('title', { boost: 10 });
    //     this.field('enseigne');
    //   });
      
      var idx = lunr(function () {
        this.ref("id");
        this.field("title", { boost: 10 });
        this.field('enseigne');
        this.field('image');
      
        for (var key in window.store) {
          this.add({
            id : key,
            title: window.store[key].title,
            enseigne : window.store[key].enseigne,
            url: window.store[key].url,
            image : window.store[key].image
          });
        }
      });

    var results = idx.search(searchTerm);
    var $results = document.getElementById("search-results");

    if (results.length > 0) {
        results.forEach(function (result) {
        var item = window.store[result.ref];
        var li = document.createElement("li");
        li.innerHTML = `
            <a href="${item.url}" style="display: flex; align-items: center; gap: 1rem; text-decoration: none; color: inherit;">
                <img src="${item.image}" alt="${item.title}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px;">
                <div>
                <h3 style="margin: 0;">${item.title}</h3>
                <p style="margin: 0; font-size: 0.9em; color: gray;">${item.enseigne}</p>
                </div>
            </a>
            `;
        li.style.padding = "10px";
        li.style.borderBottom = "1px solid #ddd";
        li.style.width = "100%";
        li.style.maxWidth = "500px"; // or however wide you want the result cards
        li.style.listStyle = "disc"; // if you still want a bullet
        li.style.textAlign = "left"; // to keep text inside aligned properly

        $results.appendChild(li);
        });
    } else {
        $results.innerHTML = "<li>No results found</li>";
    }
    }
  })();