const ctx = document.getElementById('profitChart');

new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Trade 1', 'Trade 2', 'Trade 3'],
        datasets: [{
            label: 'Profit/Loss',
            data: [10, -5, 15],
            borderWidth: 2
        }]
    }
});
