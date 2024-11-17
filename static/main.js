
// Declare global variables for chart instances
let temperatureChart, growthChart, lightIntensityChart;
let intensityArray = [100, 200, 300, 350, 450, 460, 500];
let timeArray = ['New2', 'New2', 'New3', 'New4', 'New5', 'New6', 'New7'];
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
  const date = new Date();
  const hour = date.getHours();
  const min = date.getMinutes();
  const time = hour + ":" + min;
    if (lightIntensityChart){
      lightIntensityChart.updateSeries([{
        data: intensityArray
      }]);
      lightIntensityChart.updateOptions({
        xaxis: {
          categories: timeArray // New dynamic values
        }
      });
    }
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
                console.log("LED STATUS: " + led_status);
                if(led_status == "ON"){
                    document.getElementById('light-img').src = "../static/assets/img/icons/unicons/lightOn.jpg";
                    document.getElementById('led-status').textContent = led_status;
                  }else{
                    document.getElementById('light-img').src = "../static/assets/img/icons/unicons/lightOff.jpg";
                    document.getElementById('led-status').textContent = led_status;
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
          data: [21, 30, 22, 42, 26, 35, 29]
        }
      ],
      chart: {
        height: 232,
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
        categories: ['oi', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'mate'],
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        },
        labels: {
          show: true,
          style: {
            fontSize: '13px',
            colors: labelColor
          }
        }
      },
      yaxis: {
        labels: {
          show: true
        },
        min: 0,
        max: 500,
        tickAmount: 4
      }
    };
  if (lightChartEl) {
    lightIntensityChart = new ApexCharts(lightChartEl, lightIntensityConfig);
    lightIntensityChart.render();
  }
  // displayTemp();
  // setInterval(displayTemp, 1000);
  // setInterval(updateFanUI, 1000);
});

