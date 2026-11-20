import yfinance as yf
import pandas as pd

# Download Gold Futures historical data
ticker = "GC=F"

data = yf.download(
    ticker,
    period="2y",
    interval="1d",
    auto_adjust=False,
    progress=False
)

# Handle multi-level columns if returned
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Remove rows with missing values
data = data.dropna(subset=["Open", "High", "Low", "Close"])

data.to_csv("gold_futures.csv")

# Display the dataset
print(data.head())

print("\nDataset Information:")
print(data.info())

# Save dataset
data.to_csv("gold_futures.csv")

print("\nData downloaded successfully!")


# Calculate Simple Moving Averages

data["SMA_20"] = data["Close"].rolling(window=20).mean()

data["SMA_50"] = data["Close"].rolling(window=50).mean()


# Display the latest results

print("\nTechnical Indicators:")
print(data[["Close", "SMA_20", "SMA_50"]].tail(10))


# Save updated dataset

data.to_csv("gold_futures.csv")

print("\nSMA calculations completed!")


import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))

plt.plot(data.index, data["Close"],
         label="Gold Closing Price", alpha=0.6)

plt.plot(data.index, data["SMA_20"],
         label="20-Day SMA")

plt.plot(data.index, data["SMA_50"],
         label="50-Day SMA")

plt.title("Gold Futures - Moving Average Analysis")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()


from indicators import calculate_rsi

# Calculate RSI
data = calculate_rsi(data)

print("\nLatest Technical Indicators:")

print(data[["Close", "SMA_20", "SMA_50", "RSI"]].tail(10))



import matplotlib.pyplot as plt

plt.figure(figsize=(14, 5))

plt.plot(data.index, data["RSI"], label="RSI")

plt.axhline(70, color="red", linestyle="--",
            label="Overbought (70)")

plt.axhline(30, color="green", linestyle="--",
            label="Oversold (30)")

plt.axhline(50, color="gray", linestyle=":")

plt.title("Gold Futures - RSI Analysis")
plt.xlabel("Date")
plt.ylabel("RSI")
plt.ylim(0, 100)

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

from stratergies import generate_signals

data = generate_signals(data)

print("\nTrading Signals:")
print(data[data["Signal"] != 0][
    ["Close", "SMA_20", "SMA_50", "RSI", "Signal"]
])


from backtester import run_backtest
from performance import calculate_performance

# Run backtesting
data = run_backtest(data)

# Calculate performance
results = calculate_performance(data)

print("\n========== BACKTEST RESULTS ==========")

for metric, value in results.items():
    print(f"{metric}: {value}")

# Save backtesting results
data.to_csv("backtest_results.csv")

print("\nBacktesting completed!")

# Equity Curve Visualization
import matplotlib.pyplot as plt

# Calculate Buy and Hold returns
data["Buy_Hold_Equity"] = (
    data["Close"] / data["Close"].iloc[0]
)

# Create comparison graph
plt.figure(figsize=(14, 7))

plt.plot(
    data.index,
    data["Equity_Curve"],
    label="Trading Strategy",
    linewidth=2,
    color="blue"
)

plt.plot(
    data.index,
    data["Buy_Hold_Equity"],
    label="Buy & Hold",
    linewidth=2,
    color="orange"
)

plt.title(
    "Trading Strategy vs Buy & Hold",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Date")
plt.ylabel("Portfolio Growth (Initial = 1)")

plt.legend()
plt.grid(alpha=0.25, linestyle="--")

plt.tight_layout()

plt.savefig("equity_curve.png", dpi=300)
plt.show()

from trade_analysis import analyze_trades

trades = analyze_trades(data)

# visualize trades on the price chart
import matplotlib.pyplot as plt

plt.figure(figsize=(15, 7))

plt.plot(
    data.index,
    data["Close"],
    label="Gold Futures Price",
    linewidth=1.5
)

plt.scatter(
    trades["Entry Date"],
    trades["Entry Price"],
    color="green",
    marker="^",
    s=120,
    label="BUY",
    zorder=5
)

plt.scatter(
    trades["Exit Date"],
    trades["Exit Price"],
    color="red",
    marker="v",
    s=120,
    label="SELL",
    zorder=5
)

plt.title("Gold Futures - Trading Signals", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Gold Price (USD)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("trade_signals.png", dpi=300)
plt.show()
