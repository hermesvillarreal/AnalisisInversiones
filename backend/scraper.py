import yfinance as yf
import sqlite3
import os
from datetime import datetime

def get_stock_data(ticker):
    """
    Gets stock data for a given ticker using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        data = {
            'Ticker': ticker,
            'Price': info.get('regularMarketPrice', None),
            'Previous_Close': info.get('previousClose', None),
            'Open': info.get('open', None),
            'Volume': info.get('volume', None),
            'Market_Cap': info.get('marketCap', None),
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker} using yfinance: {e}")
        return None

def save_to_sqlite(data_list):
    """
    Saves a list of stock data to a SQLite database.
    """
    if not data_list:
        return

    db_path = os.path.join('../data', 'stocks.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stock_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Ticker TEXT,
        Price REAL,
        Previous_Close REAL,
        Open REAL,
        Volume INTEGER,
        Market_Cap INTEGER,
        Timestamp TEXT
    )''')
    for data in data_list:
        c.execute('''INSERT INTO stock_data (Ticker, Price, Previous_Close, Open, Volume, Market_Cap, Timestamp)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (data['Ticker'], data['Price'], data['Previous_Close'], data['Open'], data['Volume'], data['Market_Cap'], data['Timestamp']))
    conn.commit()
    conn.close()
    print(f"Data saved to {db_path}")

if __name__ == '__main__':
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    all_data = []
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        stock_data = get_stock_data(ticker)
        if stock_data:
            all_data.append(stock_data)
    save_to_sqlite(all_data)
