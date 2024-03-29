function create_dashboard(period) {
    const apiUrl = `http://localhost:3000/api/expense/${period}/summary/`;

    const title2 = document.getElementsByTagName('h2');

    // Get the table body element
    const tableBody = document.getElementById("table-body");

    const colors = [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(75, 192, 192, 0.5)',
        'rgba(153, 102, 255, 0.5)',
        'rgba(255, 159, 64, 0.5)',
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
        'rgba(75, 192, 192, 0.5)',
        'rgba(153, 102, 255, 0.5)',
        'rgba(255, 159, 64, 0.5)',
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
    ];


    // Fetch JSON data from the API
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            title2[0].innerHTML = data.total
            // Iterate through each content item and add a row to the table
            data.content.forEach(item => {
                var row = tableBody.insertRow();
                var periodCell = row.insertCell(0);
                var accountCell = row.insertCell(1);
                var totalAmountCell = row.insertCell(2);

                periodCell.innerHTML = item.period;
                accountCell.innerHTML = item.account;
                totalAmountCell.innerHTML = item.total_amount;
            });


            // Extract labels and data from JSON
            const labels = data.content.map(item => item.account);
            const values = data.content.map(item => item.total_amount);

            // Create the chart
            const ctx = document.getElementById('myChart').getContext('2d');
            const myChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Total Amount',
                        data: values,
                        backgroundColor: colors,
                        borderColor: 'rgba(0, 0, 0, 0.5)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    tooltips: {
                        callbacks: {
                            label: function (tooltipItem, data) {
                                let label = data.labels[tooltipItem.index] || '';
                                let value = data.datasets[0].data[tooltipItem.index];
                                let percentage = ((value / data.datasets[0].data.reduce((a, b) => a + b, 0)) * 100).toFixed(2);
                                return label + ': ' + value + ' (' + percentage + '%)';
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}

document.addEventListener("DOMContentLoaded", function() {
    // Your code here
    create_dashboard();
  });