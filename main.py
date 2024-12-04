import yfinance as yf
import pandas as pd

sp500 = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

def analyze_stock(ticker):
    try:
        stock_data = yf.download(ticker, period="6mo", interval="1d")
        stock_data['50_MA'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['10_AVG_VOL'] = stock_data['Volume'].rolling(window=10).mean()
        latest = stock_data.iloc[-1]
        price_above_50_ma = latest['Close'] > latest['50_MA']
        high_volume = latest['Volume'] > latest['10_AVG_VOL']
        if price_above_50_ma and high_volume:
            return {
                "Ticker": ticker,
                "Price": latest['Close'],
                "Volume": latest['Volume'],
                "50_MA": latest['50_MA']
            }
    except Exception as e:
        print(f"Error analyzing {ticker}: {e}")
    return None

def generate_watchlist(tickers):
    watchlist = []
    for ticker in tickers:
        result = analyze_stock(ticker)
        if result:
            watchlist.append(result)
    return watchlist

def display_watchlist(watchlist):
    if not watchlist:
        print("No stocks meeting breakout criteria.")
        return
    watchlist_df = pd.DataFrame(watchlist)
    print("Stocks Meeting Breakout Criteria:")
    print(watchlist_df)

watchlist = generate_watchlist(sp500)
display_watchlist(watchlist)
