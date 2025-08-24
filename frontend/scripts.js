document.addEventListener('DOMContentLoaded', function() {
    const stockDataDiv = document.getElementById('stock-data');
    const tickerSelect = document.getElementById('ticker-select');
    const chartDiv = document.getElementById('chart');

    const API_URL = 'http://127.0.0.1:5000/api';

    // Fetch and display stock data
    fetch(`${API_URL}/stocks`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                stockDataDiv.innerHTML = `<p>${data.error}</p>`;
                return;
            }
            
            stockDataDiv.innerHTML = ''; // Clear loading...
            data.forEach(stock => {
                const stockCard = document.createElement('div');
                stockCard.className = 'stock-card';
                stockCard.innerHTML = `
                    <h3>${stock.Ticker}</h3>
                    <p><strong>Price:</strong> ${stock.Price}</p>
                    <p><strong>Previous Close:</strong> ${stock['Previous Close']}</p>
                    <p><strong>Open:</strong> ${stock.Open}</p>
                    <p><strong>Volume:</strong> ${stock.Volume}</p>
                    <p><strong>Market Cap:</strong> ${stock['Market Cap']}</p>
                `;
                stockDataDiv.appendChild(stockCard);

                // Populate ticker select for chart
                const option = document.createElement('option');
                option.value = stock.Ticker;
                option.textContent = stock.Ticker;
                tickerSelect.appendChild(option);
            });

            // Load chart for the first ticker by default
            if (data.length > 0) {
                loadChart(data[0].Ticker);
            }
        })
        .catch(error => {
            console.error('Error fetching stock data:', error);
            stockDataDiv.innerHTML = '<p>Error loading data. Is the backend server running?</p>';
        });

    // Event listener for ticker selection change
    tickerSelect.addEventListener('change', (event) => {
        loadChart(event.target.value);
    });

    function loadChart(ticker) {
        chartDiv.innerHTML = '<p>Loading chart...</p>';
        fetch(`${API_URL}/stocks/chart/${ticker}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    chartDiv.innerHTML = `<p>${data.error}</p>`;
                    return;
                }
                chartDiv.innerHTML = `<img src="data:image/png;base64,${data.chart}" alt="${ticker} Chart">`;
            })
            .catch(error => {
                console.error('Error fetching chart data:', error);
                chartDiv.innerHTML = '<p>Error loading chart.</p>';
            });
    }
});
