window.onload = function() {
    var sensorChart;
    var sensorData = {
        'ina219dc': [],
        'ads1115': [],
        'acs758lcb': [],
        'max31856': [],
    };
    var timestamps = [];

function updateSensorData() {
    fetch('/api/sensor_data')
        .then(response => response.json())
        .then(data => {
            // Add new sensor readings to the sensorData arrays
            Object.keys(sensorData).forEach(key => {
                sensorData[key].push(data[key]);
                // Remove the oldest reading if the array is too long
                if (sensorData[key].length > 10) {
                    sensorData[key].shift();
                }
            });
            // Add the current time to the timestamps array
            timestamps.push(new Date().toLocaleTimeString());
            // Remove the oldest timestamp if the array is too long
            if (timestamps.length > 10) {
                timestamps.shift();
            }
            updateChart();
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

    function updateDeviceState() {
        fetch('/api/device_state')
            .then(response => response.json())
            .then(data => {
                document.getElementById('buttonState').innerText = `Button State: ${data.button_state}`;
                document.getElementById('relayState').innerText = `Relay State: ${data.relay_state}`;
                document.getElementById('ledColor').innerText = `LED Color: ${data.led_color}`;
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
    }

function updateChart() {
    var ctx = document.getElementById('sensorChart').getContext('2d');
    if (sensorChart) {
        sensorChart.data.labels = timestamps;
        sensorChart.data.datasets.forEach((dataset, i) => {
            dataset.data = sensorData[Object.keys(sensorData)[i]];
        });
        sensorChart.update();
    } else {
        sensorChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: timestamps,
                datasets: [
                    {
                        label: 'INA219DC Readings',
                        data: sensorData['ina219dc'],
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    },
                    {
                        label: 'ADS1115 Readings',
                        data: sensorData['ads1115'],
                        fill: false,
                        borderColor: 'rgb(192, 75, 75)',
                        tension: 0.1
                    },
                    {
                        label: 'ACS758LCB Readings',
                        data: sensorData['acs758lcb'],
                        fill: false,
                        borderColor: 'rgb(75, 75, 192)',
                        tension: 0.1
                    },
                    {
                        label: 'MAX31856 Readings',
                        data: sensorData['max31856'],
                        fill: false,
                        borderColor: 'rgb(192, 192, 75)',
                        tension: 0.1
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

    document.getElementById('toggleButton').addEventListener('click', function() {
        fetch('/toggle', {method: 'POST'})
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
    });

    setInterval(function() {
        updateSensorData();
        updateDeviceState();
    }, 1000);
}
