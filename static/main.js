// Function to toggle the LED state based on the switch
function toggleLED() {
    // Determine if the switch is on or off
    // const isOn = document.getElementById('led-switch').checked ? 'ON' : 'OFF';
    // // Send AJAX request to toggle the LED state
    // $.ajax({
    //     url: '/toggle_led',
    //     type: 'POST',
    //     contentType: 'application/json',
    //     data: JSON.stringify({ state: isOn }),
    //     success: function (response) {
    //         // Update the LED status text and lightbulb graphic based on the response
    //         document.getElementById('led-status').textContent = response.led_state;
    //         const lightbulb = document.getElementById('lightbulb');
    //         if (response.led_state === 'ON') {
    //             lightbulb.classList.remove('lightbulb-off');
    //             lightbulb.classList.add('lightbulb-on');
    //         } else {
    //             lightbulb.classList.add('lightbulb-off');
    //             lightbulb.classList.remove('lightbulb-on');
    //         }
    //     },
    //     error: function (error) {
    //         console.log('Error:', error); // Log any errors to the console
    //     }
    // });
    const isOn = document.getElementById('led-switch');
    const image = document.getElementById('light-img');
    isOn.innerHTML = "Turn Off";
    image.src = "../static/assets/img/icons/unicons/lightOn.jpg";
    console.log("Hello world!");
}

// Function to trigger GPIO cleanup
function cleanupGPIO() {
    // Send AJAX request to cleanup GPIO
    $.ajax({
        url: '/cleanup',
        type: 'GET',
        success: function (response) {
            alert(response);  // Display confirmation message after cleanup
        },
        error: function (error) {
            console.log('Error during cleanup:', error); // Log errors during cleanup
        }
    });
}
