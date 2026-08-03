// ==============================
// SERT Office Monitor Dashboard
// ==============================

let chart;
let lastUpdateTime = null;

const dateElement = document.getElementById("date");
const timeElement = document.getElementById("time");
const nextUpdateElement = document.getElementById("nextUpdate");
const tempCard = document.getElementById("tempCard");
const humidityCard = document.getElementById("humidityCard");

lastUpdateTime = new Date(`${dateElement.innerText} ${timeElement.innerText}`);

// ------------------------------
// Countdown
// ------------------------------

function updateCountdown() {

    if (!lastUpdateTime) {
        nextUpdateElement.innerHTML = "--";
        return;
    }

    const nextUpdate = new Date(lastUpdateTime.getTime() + 5 * 60 * 1000);
    const diff = nextUpdate - new Date();

    if (diff <= 0) {
        nextUpdateElement.innerHTML = "Checking for new reading...";
        return;
    }

    const minutes = Math.floor(diff / 60000);
    const seconds = Math.floor((diff % 60000) / 1000);

    nextUpdateElement.innerHTML = `${minutes}m ${seconds}s`;
}

setInterval(updateCountdown, 1000);
updateCountdown();

// ------------------------------
// Check for new data every 5 seconds
// ------------------------------

setInterval(refreshDashboard, 5000);

function updateTemperatureColor(temp) {

    tempCard.className = "card shadow-lg";

    if (temp < 67) {

        tempCard.classList.add("bg-primary", "text-white");

    }
    else if (temp <= 74) {

        tempCard.classList.add("bg-success", "text-white");

    }
    else if (temp < 78) {

        tempCard.classList.add("bg-warning", "text-dark");

    }
    else {

        tempCard.classList.add("bg-danger", "text-white");

    }

}


function updateHumidityColor(humidity) {

    humidityCard.className = "card shadow-lg";

    if (humidity < 20) {

        humidityCard.classList.add("bg-primary", "text-white");

    }
    else if (humidity <= 40) {

        humidityCard.classList.add("bg-success", "text-white");

    }
    else if (humidity < 60) {

        humidityCard.classList.add("bg-warning", "text-dark");

    }
    else {

        humidityCard.classList.add("bg-danger", "text-white");

    }

}

// ------------------------------
// History Chart
// ------------------------------

async function loadHistory() {

    const response = await fetch("/api/history");
    const history = await response.json();

    if (history.length > 0) {

        const latest = history[history.length - 1];

        updateTemperatureColor(latest.temperature);
        updateHumidityColor(latest.humidity);

    }   

    const temperature = history.map(r => [
        r.timestamp,
        r.temperature
    ]);

    const humidity = history.map(r => [
        r.timestamp,
        r.humidity
    ]);

    chart = echarts.init(
        document.getElementById("historyChart")
    );

    chart.setOption({

        backgroundColor: "transparent",

        tooltip: {
            trigger: "axis"
        },

        legend: {

            top: 10,

            left: "center",

            textStyle: {

                color: "#ffffff",

                fontSize: 14

            },

            itemWidth: 18,

            itemHeight: 10,

            data: [
                "Temperature",
                "Humidity"
            ]

            },

        grid: {
            left: 60,
            right: 60,
            top: 50,
            bottom: 60
        },

        xAxis: {

            type: "time",

            axisLabel: {
                color: "#ffffff"
            },

            axisLine: {
                lineStyle: {
                    color: "#888"
                }
            }

        },

        yAxis: [

            {

                type: "value",

                name: "Temperature (°F)",

                nameLocation: "middle",

                nameGap: 45,

                nameTextStyle: {

                    color: "#ffffff",

                    fontSize: 14,

                    fontWeight: "bold"

                },

                min: 65,

                max: 90,

                interval: 5,

                axisLabel: {
                    color: "#ffffff"
                },

                splitLine: {
                    lineStyle: {
                        color: "#444"
                    }
                }

            },

            {

                type: "value",

                name: "Humidity (%)",

                nameLocation: "middle",

                nameGap: 45,

                nameTextStyle: {

                    color: "#ffffff",

                    fontSize: 14,

                    fontWeight: "bold"

                },

                min: 0,
                
                max: 100,

                position: "right",

                axisLabel: {
                    color: "#ffffff"
                },

                splitLine: {
                    show: false
                }

            }

        ],

        dataZoom: [

            {
                type: "inside"
            },

        ],

        series: [

            {

                name: "Temperature",

                type: "line",

                smooth: true,

                showSymbol: false,

                data: temperature

            },

            {

                name: "Humidity",

                type: "line",

                smooth: true,

                showSymbol: false,

                yAxisIndex: 1,

                data: humidity

            }

        ]

    });

}

loadHistory();

async function refreshDashboard() {

    const response = await fetch("/api/latest");
    const latest = await response.json();

    const newTime = new Date(`${latest.date} ${latest.time}`);

    // Nothing new? Just leave.
    if (lastUpdateTime &&
        newTime.getTime() === lastUpdateTime.getTime()) {
        return;
    }

    // New reading!
    lastUpdateTime = newTime;

    document.getElementById("date").innerText = latest.date;
    document.getElementById("time").innerText = latest.time;

    document.querySelector("#tempCard .value").innerHTML =
        `${latest.temperature}°`;

    document.querySelector("#humidityCard .value").innerHTML =
        `${latest.humidity}%`;

    document.querySelector("#batteryCard .value").innerHTML =
        `🔋 ${latest.battery}`;

    if (chart) {
        chart.dispose();
    }

    await loadHistory();
}


window.addEventListener("resize", () => {

    if (chart) {

        chart.resize();

    }

});