document.addEventListener('DOMContentLoaded', function() {
  var textInput = document.getElementById('textInput');
  var clickButton = document.getElementById('clickButton');

  clickButton.addEventListener('click', function() {
    // Make a request to the local server
    fetch('http://localhost:5000/get_text')
      .then(response => response.json())
      .then(data => {
        // Update the input field with the received text
        textInput.value = data.text;

        // Send a message to the content script to interact with the webpage
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.tabs.sendMessage(tabs[0].id, {text: data.text});
        });
      })
      .catch(error => console.error('Error:', error));
  });
});
