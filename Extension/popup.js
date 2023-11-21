document.addEventListener('DOMContentLoaded', function() {
    var textInput = document.getElementById('textInput');
    var clickButton = document.getElementById('clickButton');

    clickButton.addEventListener('click', function() {
      // Get the text from the input field
      var inputText = textInput.value;

      // Send a message to the content script to interact with the webpage
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {text: inputText});
      });
    });
  });
