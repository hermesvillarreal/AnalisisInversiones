from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__, static_folder='../frontend')
CORS(app)

DB_PATH = os.path.join('../data', 'stocks.db')

@app.route('/api/stocks')
def get_stocks():
    """API endpoint to get the latest stock data for each ticker."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Get the latest record for each ticker
    c.execute('''SELECT Ticker, Price, Previous_Close, Open, Volume, Market_Cap, Timestamp FROM stock_data WHERE id IN (
        SELECT MAX(id) FROM stock_data GROUP BY Ticker
    )''')
    rows = c.fetchall()
    conn.close()
    columns = ['Ticker', 'Price', 'Previous Close', 'Open', 'Volume', 'Market Cap', 'Timestamp']
    data = [dict(zip(columns, row)) for row in rows]
    return jsonify(data)

@app.route('/api/stocks/chart/<ticker>')
def get_stock_chart(ticker):
    """API endpoint to generate and return a price chart for a ticker using historical data."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT Timestamp, Price FROM stock_data WHERE Ticker = ? ORDER BY Timestamp ASC''', (ticker,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        return jsonify({"error": "Ticker not found or no data available"}), 404
    dates = [datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S') for row in rows]
    prices = [row[1] for row in rows]
    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices, marker='o', linestyle='-')
    plt.title(f'{ticker} Stock Price History')
    plt.xlabel('Fecha')
    plt.ylabel('Precio (USD)')
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return jsonify({'chart': image_base64})

# Serve frontend
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
