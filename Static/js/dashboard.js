// ==============================
// SERT Office Monitor Dashboard
// ==============================

let chart;

const timestampElement = document.getElementById("timestamp");
const nextUpdateElement = document.getElementById("nextUpdate");
const tempCard = document.getElementById("tempCard");
const humidityCard = document.getElementById("humidityCard");

// ------------------------------
// Countdown
// ------------------------------

function updateCountdown() {

    const text = timestampElement.innerText.replace(/\n/g, " ");

    const lastUpdate = new Date(text);

    if (isNaN(lastUpdate)) {

        nextUpdateElement.innerHTML = "--";
        return;

    }

    const nextUpdate = new Date(lastUpdate.getTime() + (5 * 60 * 1000));

    const diff = nextUpdate - new Date();

    if (diff <= 0) {

        nextUpdateElement.innerHTML = "Updating...";
        return;

    }

    const minutes = Math.floor(diff / 60000);
    const seconds = Math.floor((diff % 60000) / 1000);

    nextUpdateElement.innerHTML =
        `${minutes}m ${seconds}s`;

}

setInterval(updateCountdown, 1000);

updateCountdown();

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

setInterval(async () => {

    if (chart) {
        chart.dispose();
    }

    await loadHistory();

}, 30000);

window.addEventListener("resize", () => {

    if (chart) {

        chart.resize();

    }

});