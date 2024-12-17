import ccxt
import pandas as pd
import matplotlib.pyplot as plt

# Set API keys
api_key = ""
secret_key = 
# Create exchange object
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': secret_key,
    'enableRateLimit': True,
})

# Set symbol
symbol = "BTC/USDT"

# Get historical data
data = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=1000)
df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Calculate moving averages
df['ma50'] = df['close'].rolling(window=50).mean()
df['ma200'] = df['close'].rolling(window=200).mean()

# Define trading strategy
def trade(df):
    position = 0
    for i in range(len(df)):
        if df['ma50'].iloc[i] > df['ma200'].iloc[i] and position == 0:
            print("Buy at", df['close'].iloc[i])
            position = 1
        elif df['ma50'].iloc[i] < df['ma200'].iloc[i] and position == 1:
            print("Sell at", df['close'].iloc[i])
            position = 0

# Trade
trade(df)