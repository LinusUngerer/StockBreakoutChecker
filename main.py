import yfinance as yf
import pandas as pd
#from concurrent.futures import ThreadPoolExecutor, as_completed


## Define a list of tickers to analyze (currently using a subset of the S&P 500)
#sp500 = ["PLTR","AXON","AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "XEL","WELL"] ##Sample data
tickers = [
    'ACIC', 'ADBE', 'ADIL', 'AHT', 'ALKT', 'ALOT', 'ALRM', 'ALT', 'ALTI', 'AMRX',
    'APPN', 'ARL', 'ATHE', 'ATMU', 'BEN', 'BHLB', 'BNR', 'BRFS', 'BSTZ', 'BTI',
    'BUSE', 'BV', 'BWMN', 'BZFD', 'CART', 'CATY', 'CCRN', 'CDZIP', 'CFB', 'CHMG',
    'CMG', 'CSTE', 'CXM', 'CYCN', 'DAKT', 'DDOG', 'DIAX', 'DJTWW', 'DSGN', 'DSGX',
    'ECX', 'ELA', 'EOI', 'EPAM', 'ESPR', 'EVC', 'EW', 'FIHL', 'FLR', 'FROG', 'FTIIU',
    'FWONK', 'GDTC', 'GENC', 'GGR', 'GGT', 'GILD', 'GNTY', 'GRPN', 'HEAR', 'HIMX',
    'HIVE', 'HOFT', 'INDV', 'INOD', 'INTJ', 'IPX', 'JANX', 'LFMD', 'LITE', 'LPTX',
    'LTRN', 'MCHX', 'METC', 'METCB', 'MFC', 'MRVL', 'NCNO', 'NET', 'NFE', 'NIXX',
    'NOW', 'NVA', 'NWFL', 'ONIT', 'OOMA', 'PACB', 'PATH', 'PCOR', 'PCRX', 'PD', 'PRO',
    'PRPL', 'PSTG', 'PW', 'PWOD', 'PYPL', 'QCRH', 'QUAD', 'RDCM', 'RNAC', 'RNG', 'ROKU',
    'ROP', 'RPD', 'RR', 'SATL', 'SHBI', 'SOND', 'SOUN', 'SPT', 'STCN', 'STOK'
]


#Added in Variance vars
stock_price_percentage_jump = 1.03
stock_volume_percentage_jump = 2 #Adjust this percentage according to how much larger the volume must be.
candle_percentage_jump = 1.01     #Adjust this percentage according to how large you want the candlestick jump must be from previous close to todays open
candle_size_percentage_jump = 1.2 #Adjust this percentage according to how much larger the new candle must be than the old one.

#end_date = "2024-11-09" #datetime.now()
#start_date ="2024-01-01"


#cryptoStocks = ['GALAUSD','XRPUSD']
# Function to analyze stock data for a given ticker
def analyze_stock(ticker):
    try:
        # Download the last 3 months of daily stock data for the ticker
        stock_data = yf.download(ticker, period="3mo", interval="1d" )

        #Backtesting to known Breakout. Days must be larger than 3 months range for 50MA
       # stock_data = yf.download(ticker, start=start_date, end=end_date)
        
        # Calculate the 50-day moving average
        stock_data['50_MA'] = stock_data['Close'].rolling(window=50).mean()
        
        # Calculate the 10-day average volume
        stock_data['10_AVG_VOL'] = stock_data['Volume'].rolling(window=10).mean()
        
        # Get the latest row of data
        latest = stock_data.iloc[-1]
        yesterday = stock_data.iloc[-2]

        # Todays Open must be at least 3% larger than yesterdays close.
        price_open_is_greater_than_yesterday=latest['Open'][ticker]> candle_percentage_jump * yesterday['Close'][ticker]

        if price_open_is_greater_than_yesterday!=True:
            return None
        
        # Check if the stock price is above the 50-day moving average
        price_above_50_ma = latest['Close'][ticker] > stock_price_percentage_jump * stock_data.iloc[-1]['50_MA'].iloc[0]
        
        if price_above_50_ma!=True:
            return None
        
        # Check if the stock's volume is 50% higher than the 10-day average volume
        high_volume = latest['Volume'].iloc[0] > stock_volume_percentage_jump * latest['10_AVG_VOL'].iloc[0]

        if high_volume!=True:
            return None
        
         # Calculate the candle size for both today and yesterday
        yesterday_candle_size=yesterday['Close'][ticker]-yesterday['Open'][ticker]
        latest_candle_size=latest['Close'][ticker]-latest['Open'][ticker]

        # Check if today's candle size is at least 20% larger than yesterday's
        candlesize_larger=latest_candle_size>= candle_size_percentage_jump*yesterday_candle_size
        if candlesize_larger!=True:
            return None

        
        # If both conditions are met, return the stock data
        if price_above_50_ma and high_volume and price_open_is_greater_than_yesterday:
            return {
                "Ticker": ticker,
                "Price": latest['Close'][ticker],
                "Volume": latest['Volume'].iloc[0],
                "50_MA": stock_data.iloc[-1]['50_MA'].iloc[0]
            }
    except Exception as e:
        # Handle any errors that occur during analysis and print a message
        print(f"Error analyzing {ticker}: {e}")
    
    # Return None if the stock does not meet the breakout criteria
    return None

# Function to generate a watchlist of stocks meeting the breakout criteria
def generate_watchlist(tickers):
    watchlist = []
    # Loop through each ticker in the list
    counter = 0
    for ticker in tickers:
        counter += 1
        print(str(counter)+ f" - Processing {ticker}...")  # Print the ticker being processed
        result = analyze_stock(ticker)
        # If the stock meets the breakout criteria, add it to the watchlist
        if result:
            watchlist.append(result)
    return watchlist

# Function to display the stocks that meet the breakout criteria
def display_watchlist(watchlist):
    # If no stocks meet the criteria, print a message
    if not watchlist:
        print("No stocks meeting breakout criteria.\n")
        return
    # Print a separator line and header
    print("-" * 50)
    print("Stocks Meeting Breakout Criteria:\n")
    print("-" * 50)
    
    # Loop through each stock in the watchlist and display its details
    for stock in watchlist:
        print(f"Ticker: {stock['Ticker']}")
        print(f"Price: {stock['Price']}")
        print(f"Volume: {stock['Volume']}")
        print(f"50_MA: {stock['50_MA']}")
        print("-" * 50)  # Add a separator line for better readability

# Generate the watchlist of stocks that meet the breakout criteria
#sp500_cleaned = [item for item in sp500 if '^' not in item]
watchlist = generate_watchlist(tickers)

# Display the results
display_watchlist(watchlist)