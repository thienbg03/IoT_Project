
// Declare global variables for chart instances
let temperatureChart, growthChart;
// Function to toggle the LED state based on the switch
function toggleLED() {
    const isOn = document.getElementById('led-switch').checked ? 'ON' : 'OFF';
    //console.log(data);
    $.ajax({
        url: '/toggle_led',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ state: isOn }),
        success: function (response) {
            document.getElementById('led-status').textContent = response.led_state;
        },
        error: function (error) {
            console.log('Error:', error);
        }
    });
    // Update light bulb image based on LED state
    document.getElementById('light-img').src = isOn === "ON"
        ? "../static/assets/img/icons/unicons/lightOn.jpg"
        : "../static/assets/img/icons/unicons/lightOff.jpg";


}

function displayTemp() {
    fetch('/sensor_data')
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            if (data.error) {
                console.error('Error:', data.error);
            } else {
                updateTemperature(data.temperature);
                updateHumidity(data.humidity);
            }
        })
        .catch((error) => console.error("Error fetching sensor data:", error));
}


function toggleFan(){
    var isOn = document.getElementById('fanStatus').innerHTML;
    if(isOn == "OFF"){
      document.getElementById('fanImg').src = "/static/assets/img/fan.gif";
      document.getElementById('fanStatus').innerHTML = "ON";
      document.getElementById('fanButton').innerHTML = "Turn Off";
    }else{
      document.getElementById('fanImg').src = "/static/assets/img/fan.jpg";
      document.getElementById('fanStatus').innerHTML = "OFF";
      document.getElementById('fanButton').innerHTML = "Turn On";
    }
}
// Function to update the temperature chart value
function updateTemperature(value) {
    if (temperatureChart) {
        temperatureChart.updateSeries([value]); // Update the temperature value
    }
}

// Function to update the humidity chart value
function updateHumidity(value) {
    if (growthChart) {
        growthChart.updateSeries([value]); // Update the humidity value
    }
}




// On Page Load Create the Temperature and Humidity Charts
document.addEventListener('DOMContentLoaded', function () {
  // Ensure all elements are loaded before initializing the charts
  const temperatureChartEl = document.querySelector('#temperatureChart');
  const growthChartEl = document.querySelector('#growthChart');

  // Define chart options
  const cardColor = config.colors.cardColor;
  const headingColor = config.colors.headingColor;
  const legendColor = config.colors.bodyColor;

  // Growth Chart - Radial Bar Chart
  const growthChartOptions = {
      series: [40],
      labels: ['Humidity'],
      chart: {
          height: 240,
          type: 'radialBar'
      },
      plotOptions: {
          radialBar: {
              size: 150,
              offsetY: 10,
              startAngle: -150,
              endAngle: 150,
              hollow: { size: '55%' },
              track: { background: cardColor, strokeWidth: '100%' },
              dataLabels: {
                  name: { offsetY: 15, color: legendColor, fontSize: '15px', fontWeight: '500', fontFamily: 'Public Sans' },
                  value: { offsetY: -25, color: headingColor, fontSize: '22px', fontWeight: '500', fontFamily: 'Public Sans' }
              }
          }
      },
      colors: [config.colors.primary],
      fill: {
          type: 'gradient',
          gradient: { shade: 'dark', shadeIntensity: 0.5, gradientToColors: [config.colors.primary], inverseColors: true, opacityFrom: 1, opacityTo: 0.6, stops: [30, 70, 100] }
      },
      stroke: { dashArray: 5 },
      grid: { padding: { top: -35, bottom: -10 } }
  };

  // Initialize Growth Chart
  if (growthChartEl) {
      growthChart = new ApexCharts(growthChartEl, growthChartOptions);
      growthChart.render();
  }

  // Temperature Chart - Radial Bar Chart
  const temperatureChartOptions = {
      series: [24],
      labels: ['Temperature'],
      chart: { height: 240, type: 'radialBar' },
      plotOptions: {
          radialBar: {
              size: 150,
              offsetY: 10,
              startAngle: -150,
              endAngle: 150,
              hollow: { size: '55%' },
              track: { background: cardColor, strokeWidth: '100%' },
              dataLabels: {
                  name: { offsetY: 15, color: legendColor, fontSize: '15px', fontWeight: '500', fontFamily: 'Public Sans' },
                  value: {
                      offsetY: -25,
                      color: headingColor,
                      fontSize: '22px',
                      fontWeight: '500',
                      fontFamily: 'Public Sans',
                      formatter: function (val) { return val + ' °C'; }
                  }
              }
          }
      },
      colors: [config.colors.warning],
      fill: {
          type: 'gradient',
          gradient: { shade: 'dark', shadeIntensity: 0.5, gradientToColors: [config.colors.primary], inverseColors: true, opacityFrom: 1, opacityTo: 0.6, stops: [30, 70, 100] }
      },
      stroke: { dashArray: 5 },
      grid: { padding: { top: -35, bottom: -10 } }
  };

  // Initialize Temperature Chart
  if (temperatureChartEl) {
      temperatureChart = new ApexCharts(temperatureChartEl, temperatureChartOptions);
      temperatureChart.render();
  }
  displayTemp();

  setInterval(displayTemp, 5000);
});

