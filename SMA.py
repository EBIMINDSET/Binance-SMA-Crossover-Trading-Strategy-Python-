from binance.client import Client
import pandas as pd

API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

SYMBOL = "BTCUSDT"
INTERVAL = Client.KLINE_INTERVAL_5MINUTE
LIMIT = 200

FAST_SMA = 10
SLOW_SMA = 50

client = Client(API_KEY, API_SECRET)

klines = client.get_klines(
    symbol=SYMBOL,
    interval=INTERVAL,
    limit=LIMIT
)

df = pd.DataFrame(klines, columns=[
    'time','open','high','low','close','volume',
    'close_time','qav','num_trades',
    'taker_base','taker_quote','ignore'
])

df['close'] = df['close'].astype(float)

df['SMA_FAST'] = df['close'].rolling(FAST_SMA).mean()
df['SMA_SLOW'] = df['close'].rolling(SLOW_SMA).mean()

df['signal'] = 0
df.loc[df['SMA_FAST'] > df['SMA_SLOW'], 'signal'] = 1
df.loc[df['SMA_FAST'] < df['SMA_SLOW'], 'signal'] = -1

df['trade'] = df['signal'].diff()

last_trade = df.iloc[-1]

if last_trade['trade'] == 2:
    print(" BUY SIGNAL (SMA Crossover)")
elif last_trade['trade'] == -2:
    print(" SELL SIGNAL (SMA Crossdown)")
else:
    print("⏳ No Trade Signal")

print(df.tail(5))
