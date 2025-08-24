from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__, static_folder='../frontend')
CORS(app)

DATA_DIR = '../data'

def get_latest_csv():
    """Finds the most recent CSV file in the data directory."""
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    if not files:
        return None
    # Sort files by date in filename
    files.sort(key=lambda x: datetime.strptime(x.split('_')[-1].replace('.csv', ''), '%Y-%m-%d'), reverse=True)
    return os.path.join(DATA_DIR, files[0])

@app.route('/api/stocks')
def get_stocks():
    """API endpoint to get the latest stock data."""
    latest_csv = get_latest_csv()
    if not latest_csv:
        return jsonify({"error": "No data available"}), 404
    
    df = pd.read_csv(latest_csv)
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/stocks/chart/<ticker>')
def get_stock_chart(ticker):
    """API endpoint to generate and return a simple price chart for a ticker."""
    latest_csv = get_latest_csv()
    if not latest_csv:
        return jsonify({"error": "No data available"}), 404
        
    df = pd.read_csv(latest_csv)
    stock_data = df[df['Ticker'] == ticker]

    if stock_data.empty:
        return jsonify({"error": "Ticker not found"}), 404

    # For simplicity, we'll plot the price from the single available data point.
    # A real application would have historical data to plot a meaningful chart.
    plt.figure(figsize=(10, 5))
    
    # Convert price to numeric, coercing errors
    prices = pd.to_numeric(stock_data['Price'], errors='coerce').dropna()
    
    if prices.empty:
        return jsonify({"error": "Price data is not available or invalid for this ticker"}), 404

    plt.plot([datetime.now().strftime('%Y-%m-%d')], prices, marker='o', linestyle='-')
    plt.title(f'{ticker} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Encode image to base64
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
