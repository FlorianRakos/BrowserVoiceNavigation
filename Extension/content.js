// content.js

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    // Perform actions on the webpage based on the message received
    var buttonText = request.text;

    // Find the button with the specified text
    var buttons = document.querySelectorAll('button');
    for (var i = 0; i < buttons.length; i++) {
      if (buttons[i].innerText === buttonText) {
        // Click the button
        buttons[i].click();
        break; // Stop searching after the first matching button is found
      }
    }
  });
