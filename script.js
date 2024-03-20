document.getElementById('predict-btn').addEventListener('click', function() {
    const formData = new FormData(document.getElementById('upload-form'));
    
    axios.post('/predict', formData)
        .then(function(response) {
            const data = response.data;
            const ctx = document.getElementById('plot').getContext('2d');
            if (window.myChart) {
                window.myChart.destroy();
            }
            window.myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'Original Data',
                        data: data.original_data.map(item => ({ x: item[0], y: item[1] })),
                        borderWidth: 1,
                        fill: false,
                        borderColor: 'blue'
                    }, {
                        label: 'Predicted Data',
                        data: data.future_data.map(item => ({ x: item[0], y: item[1] })),
                        borderWidth: 1,
                        fill: false,
                        borderColor: 'red'
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day'
                            }
                        },
                        y: {
                            beginAtZero: false
                        }
                    }
                }
            });
        })
        .catch(function(error) {
            console.error('Error:', error);
        });
});
