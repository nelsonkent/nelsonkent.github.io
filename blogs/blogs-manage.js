// Create a new link element
var linkElement = document.createElement('link');

// Set attributes for the link element
linkElement.rel = 'stylesheet';
linkElement.id = 'mesmerize-style-css';
linkElement.href = '/blogs/style.min.css';
linkElement.type = 'text/css';
linkElement.media = 'all';

// Append the link element to the <head> of the document
document.head.appendChild(linkElement);

// Create a new script element
var scriptElement = document.createElement('script');

// Set the src attribute to the path of the secondary JavaScript file
scriptElement.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js';

// Append the script element to the document's <head> or <body>
document.head.appendChild(scriptElement);
// or document.body.appendChild(scriptElement); // Choose the appropriate location
// Define a callback function to execute once the script (jQuery) has loaded
scriptElement.onload = function() {
  // jQuery is now loaded and ready to use
  $(document).ready(function () {
    const newElement = document.createElement('div');
    newElement.id = "headerContainer";
    document.body.insertBefore(newElement, document.body.firstChild);
    // Load header.html into #headerContainer
    $('#headerContainer').load('/blogs/header.html');
  });
};

// Function to include HTML content from a URL
function includeHTML(url) {
  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.text();
    })
    .then(html => {
      const tempContainer = document.createElement('div');
      tempContainer.innerHTML = html;

      // Append the contents of the temporary container to the body
      document.body.appendChild(tempContainer);
      // Execute scripts in the appended content
      const scripts = tempContainer.querySelectorAll('script');
      scripts.forEach(script => {
        const newScript = document.createElement('script');
        newScript.text = script.text;
        document.body.appendChild(newScript);
      });

    })
    .catch(error => {
      console.error('Error fetching HTML:', error);
    });
}

// Call the function to include HTML content from an external URL
includeHTML('/blogs/comment.html');