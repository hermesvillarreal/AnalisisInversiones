import yfinance as yf
import pandas as pd
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
            'Price': info.get('regularMarketPrice', 'N/A'),
            'Previous Close': info.get('previousClose', 'N/A'),
            'Open': info.get('open', 'N/A'),
            'Volume': info.get('volume', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A')
        }
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker} using yfinance: {e}")
        return None

def save_to_csv(data_list):
    """
    Saves a list of stock data to a CSV file.
    """
    if not data_list:
        return

    # Create data directory if it doesn't exist
    if not os.path.exists('../data'):
        os.makedirs('../data')

    # Use the current date for the filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"../data/stock_data_{date_str}.csv"
    
    df = pd.DataFrame(data_list)
    
    # If file exists, append without header, otherwise create new
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


if __name__ == '__main__':
    # List of tickers to scrape
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    
    all_data = []
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        stock_data = get_stock_data(ticker)
        if stock_data:
            all_data.append(stock_data)
    
    save_to_csv(all_data)
