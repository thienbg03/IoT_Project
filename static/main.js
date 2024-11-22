
// Declare global variables for chart instances
let temperatureChart, growthChart, lightIntensityChart;
let intensityArray = [];
let timeArray = [];
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

function updateFanUI(){
    fetch('/return_status')
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
                let fan_status = data.fan_state
                console.log("FAN: " + fan_status);
                if(fan_status == "ON"){
                    document.getElementById('fanStatus').innerHTML = "ON";
                    document.getElementById('fanButton').innerHTML = "Turn Off";
                    document.getElementById('fanImg').src = "/static/assets/img/fan.gif";
                    }else{
                    document.getElementById('fanStatus').innerHTML = "OFF";
                    document.getElementById('fanButton').innerHTML = "Turn On";
                    document.getElementById('fanImg').src = "/static/assets/img/fan.jpg";
                }
            }
        })
        .catch((error) => console.error("Error fetching sensor data:", error));
}

function toggleFan(){
    var isFanOn = document.getElementById('fanStatus').innerHTML;
    $.ajax({
        url: '/toggle_fan',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ state: isFanOn }),
        success: function (response) {
            document.getElementById('fanStatus').innerHTML = response.fan_state;
        },
        error: function (error) {
            console.log('Error:', error);
        }
    });
    updateFanUI();
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

function updateLightIntensity() {
  fetch('/return_status')  // Assuming /get_light_data returns a single light intensity value
    .then((response) => response.json())  // Parse the JSON response
    .then((data) => {
      // Assuming data has the light intensity value in `data.intensity`
      const newIntensityValue = data.light_intensity;
      console.log(newIntensityValue)
      document.getElementById("lightIntensity").textContent = newIntensityValue;
      // Get the current time and format it as you need for the x-axis
      const date = new Date();
      const hour = date.getHours();
      const min = date.getMinutes();
      const secs = date.getSeconds();
      const time = `${hour}:${min}:${secs}`;  // Example: '14:30'

      // Add the new value to your existing intensity array
      intensityArray.push(newIntensityValue);  // Add new intensity value
      timeArray.push(time);  // Add new time value

      // Optionally, if the array gets too large, remove the oldest data point to keep the chart manageable
      if (intensityArray.length > 7) {  // Keep only the last 7 values
        intensityArray.shift();  // Remove the oldest intensity value
        timeArray.shift();  // Remove the oldest time value
      }

      // Update the chart with the new series and categories (time values)
      if (lightIntensityChart) {
        lightIntensityChart.updateSeries([{
          data: intensityArray  // Update the data in the series
        }]);

        lightIntensityChart.updateOptions({
          xaxis: {
            categories: timeArray  // Update the x-axis with the new time values
          }
        });
      }
    })
    .catch((error) => console.error("Error fetching light intensity data:", error));
}


function updateLED(){
  fetch('/return_status')
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
                let led_status = data.led_state
                let email_status = data.email_status
                console.log("LED STATUS: " + led_status);
                if(led_status == "ON"){
                    document.getElementById('light-img').src = "../static/assets/img/icons/unicons/lightOn.jpg";
                    document.getElementById('led-status').textContent = led_status;
                    document.getElementById('emailStatus').textContent = email_status;
                    document.getElementById('led-switch').checked = true;
                  }else{
                    document.getElementById('light-img').src = "../static/assets/img/icons/unicons/lightOff.jpg";
                    document.getElementById('led-status').textContent = led_status;
                    document.getElementById('emailStatus').textContent = email_status;
                    document.getElementById('led-switch').checked = false;
                }
            }
        })
        .catch((error) => console.error("Error fetching sensor data:", error));
}

// On Page Load Create the Temperature and Humidity Charts
document.addEventListener('DOMContentLoaded', function () {
  // Ensure all elements are loaded before initializing the charts
  const temperatureChartEl = document.querySelector('#temperatureChart');
  const growthChartEl = document.querySelector('#growthChart');
  const lightChartEl = document.querySelector('#lightChart');
  // Define chart options
  const cardColor = config.colors.cardColor;
  const headingColor = config.colors.headingColor;
  const legendColor = config.colors.bodyColor;
  const shadeColor = config.colors.cardColor;
  const borderColor = config.colors.borderColor;
  const labelColor = config.colors.textMuted;
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

// Temperature Chart - Radial Bar Chart
  const lightIntensityConfig = {
    series: [
      {
        data: intensityArray
      }
    ],
    chart: {
      height: 285,
      parentHeightOffset: 0,
      parentWidthOffset: 0,
      toolbar: {
        show: false
      },
      type: 'area'
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      width: 3,
      curve: 'smooth'
    },
    legend: {
      show: false
    },
    markers: {
      size: 6,
      colors: 'transparent',
      strokeColors: 'transparent',
      strokeWidth: 4,
      discrete: [
        {
          fillColor: config.colors.white,
          seriesIndex: 0,
          dataPointIndex: 6,
          strokeColor: config.colors.primary,
          strokeWidth: 2,
          size: 6,
          radius: 8
        }
      ],
      hover: {
        size: 7
      }
    },
    colors: [config.colors.primary],
    fill: {
      type: 'gradient',
      gradient: {
        shade: shadeColor,
        shadeIntensity: 0.6,
        opacityFrom: 0.5,
        opacityTo: 0.25,
        stops: [0, 95, 100]
      }
    },
    grid: {
      borderColor: borderColor,
      strokeDashArray: 8,
      padding: {
        top: -20,
        bottom: -8,
        left: 0,
        right: 8
      }
    },
    xaxis: {
      categories: timeArray,
      axisBorder: {
        show: false
      },
      axisTicks: {
        show: true
      },
      labels: {
        show: true,
        style: {
          fontSize: '12px',
          colors: labelColor
        }
      },
      title: {
        text: 'Time',
        style: {
          fontSize: '14px',
          fontWeight: 'bold',
          color: labelColor,
          marginBottom: 5  // Ensure enough space for the card
        }
      }
    },
    yaxis: {
      labels: {
        show: true
      },
      min: 0,
      max: 4500,
      tickAmount: 4,
      title: {
        text: 'Intensity',  // Add title for Y-axis
        style: {
          fontSize: '14px',
          fontWeight: 'bold',
          color: labelColor,
        }
      }
    }
  };

  if (lightChartEl) {
    lightIntensityChart = new ApexCharts(lightChartEl, lightIntensityConfig);
    lightIntensityChart.render();
  }
  // displayTemp();
  // setInterval(displayTemp, 1000);
  // setInterval(updateFanUI, 1000);
  setInterval(updateLightIntensity, 3000);
  setInterval(updateLED, 3000);
});

