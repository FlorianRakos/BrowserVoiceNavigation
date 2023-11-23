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
                if (buttons[i].innerText.toLowerCase() === content) {
                    // Click the button
                    fetch('http://localhost:5000/reset')
                    buttons[i].click();
                    break; // Stop searching after the first matching button is found
                }
            }
            fetch('http://localhost:5000/reset')
        break;
        case "scroll":
            scroll(content)
        break;

    }

}

function scroll(content) {
    let viewportHeight = window.screen.height;
    let currentY = window.scrollY;
    console.log("vp: " + viewportHeight)
    switch (content) {
        case "up":
            console.log("scroll up window")
            window.scrollTo(0, currentY - Math.round(viewportHeight * 0.9))
            fetch('http://localhost:5000/reset')
            break;
        case "down":
            console.log("scroll down window")
            window.scrollTo(0,currentY + Math.round(viewportHeight * 0.9))
            fetch('http://localhost:5000/reset')
            break;

        case "top":
            window.scrollTo(0, 0)
            fetch('http://localhost:5000/reset')
            break;
        case "bottom":
            window.scrollTo(0, document.body.scrollHeight)
            fetch('http://localhost:5000/reset')
            break;
        default:
            fetch('http://localhost:5000/reset')

    }
}

setInterval(fetchData, 100);
