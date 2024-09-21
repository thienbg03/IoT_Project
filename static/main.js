// Function to toggle the LED state based on the switch
function toggleLED() {
    //Determine if the switch is on or off
    const isOn = document.getElementById('led-switch').checked ? 'ON' : 'OFF';
    // Send AJAX request to toggle the LED state
    $.ajax({
        url: '/toggle_led',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ state: isOn}),
        success: function (response) {
            // Update the LED status text and lightbulb graphic based on the response
            document.getElementById('led-status').textContent = response.led_state;
        },
        error: function (error) {
            console.log('Error:', error); // Log any errors to the console
        }
    });  

    if(isOn == "ON"){
        document.getElementById('light-img').src = "../static/assets/img/icons/unicons/lightOn.jpg";
    }else{
        document.getElementById('light-img').src = "../static/assets/img/icons/unicons/lightOff.jpg";
    }
    
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
