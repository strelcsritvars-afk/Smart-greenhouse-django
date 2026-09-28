/* globals Chart:false, feather:false */

if (typeof feather!== "undefined")
  {
    feather.replace()
  }


var sensorDataElement = document.getElementById("sensor-data");
var sensorData = JSON.parse(sensorDataElement.textContent);

var myChart = new Chart(document.getElementById("myChart"), {
  type: "line",
  data: {
    labels: sensorData.map(function (reading) {
      return new Date(reading.timestamp).toLocaleString()
    }),
    datasets: [{
      label: "Air humidity (%)",
      data: sensorData.map(function (reading) {
        return reading.air_humidity
      }),
      borderColor: "#007bff",
      backgroundColor: "rgba(0, 123, 255, 0.15)",
      borderWidth: 2,
      fill: true
    }]
  }
})

document.getElementById("theme-toggle").addEventListener("click", function () {
    var html = document.documentElement
    var isDark = html.getAttribute("data-bs-theme") !== "dark"

    html.setAttribute("data-bs-theme", isDark ? "dark" : "light")
    document.body.classList.toggle("dark-mode", isDark)
    this.innerHTML = isDark 
    ? '<i class="bi bi-sun-fill" aria-hidden="true"></i>'
    :'<i class="bi bi-moon-fill" aria-hidden="true"></i>'
    this.setAttribute(
        "aria-label",
        isDark ? "Switch to light mode" : "Switch to dark mode"
    )
    this.setAttribute("aria-pressed", isDark)
})
