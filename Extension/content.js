// content.js

console.log("run content.js")



function fetchData () {
//console.log('in while')

    fetch('http://localhost:5000/get_text')
        .then(response => response.json())
        .then(data => {
            // Update the input field with the received text
            if (data.action != null) {
                //console.log(data.action)
                pressLink(data.action, data.element)
            }
        })
        .catch(error => console.error('Error:', error));
}

function pressLink (action, content) {
        // Find the button with the specified text
    switch (action) {
        case "click":
            console.log("Try click on: " + content)
            var buttons = document.querySelectorAll('a');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].innerText === content) {
                    // Click the button
                    buttons[i].click();
                    fetch('http://localhost:5000/reset')
                    break; // Stop searching after the first matching button is found
                }
            }
        break;
        case "scroll":
            console.log("scroll " + content)
        break;

    }

}

setInterval(fetchData, 1000);
