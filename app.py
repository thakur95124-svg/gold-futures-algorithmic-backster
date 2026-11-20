
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from indicators import calculate_rsi
from stratergies import generate_signals
from backtester import run_backtest
from performance import calculate_performance
from trade_analysis import analyze_trades


# Dashboard configuration
st.set_page_config(
    page_title="Gold Futures Strategy Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("Gold Futures Trading Strategy Analyzer")
st.caption("Technical Analysis | Algorithmic Trading | Strategy Backtesting")

# Load historical data
@st.cache_data
def load_data():
    df = pd.read_csv(
        "gold_futures.csv",
        index_col=0,
        parse_dates=True
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df

data = load_data()


# Strategy Configuration
st.sidebar.header("Strategy Configuration")

short_sma = st.sidebar.slider(
    "Short SMA Period",
    min_value=5,
    max_value=40,
    value=20
)

long_sma = st.sidebar.slider(
    "Long SMA Period",
    min_value=20,
    max_value=100,
    value=50
)

rsi_period = st.sidebar.slider(
    "RSI Period",
    min_value=5,
    max_value=30,
    value=14
)

if short_sma >= long_sma:
    st.error("Short SMA must be smaller than Long SMA.")
    st.stop()


# Calculate indicators

data["SMA_20"] = data["Close"].rolling(
    window=short_sma
).mean()

data["SMA_50"] = data["Close"].rolling(
    window=long_sma
).mean()

data = calculate_rsi(data, period=rsi_period)

data = generate_signals(data)
data = run_backtest(data)


# RSI-Based Trading Strategy
rsi_data = data.copy()

rsi_data["Signal"] = 0

# Buy when RSI falls below 30
rsi_data.loc[rsi_data["RSI"] < 30, "Signal"] = 1

# Sell when RSI rises above 70
rsi_data.loc[rsi_data["RSI"] > 70, "Signal"] = -1

# Run RSI strategy backtest
rsi_data = run_backtest(rsi_data)


# RSI-Based Trading Strategy
rsi_data = data.copy()

rsi_data["Signal"] = 0

# Buy when RSI falls below 30
rsi_data.loc[rsi_data["RSI"] < 30, "Signal"] = 1

# Sell when RSI rises above 70
rsi_data.loc[rsi_data["RSI"] > 70, "Signal"] = -1

# Run RSI strategy backtest
rsi_data = run_backtest(rsi_data)


# Performance calculations

# Sidebar date filter
st.sidebar.header("Analysis Settings")

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=(
        data.index.min().date(),
        data.index.max().date()
    ),
    min_value=data.index.min().date(),
    max_value=data.index.max().date()
)

if start_date > end_date:
    st.error("Start date must be before end date.")
    st.stop()

# Filter data after calculating indicators and signals
filtered_data = data.loc[
    (data.index.date >= start_date) &
    (data.index.date <= end_date)
].copy()

if filtered_data.empty:
    st.warning("No data available for this date range.")
    st.stop()

# Recalculate equity curve for selected period
filtered_data["Equity_Curve"] = (
    1 + filtered_data["Strategy_Return"]
).cumprod()

filtered_data["Buy_Hold_Equity"] = (
    filtered_data["Close"] / filtered_data["Close"].iloc[0]
)


# Filter RSI strategy using the same date range
filtered_rsi = rsi_data.loc[
    (rsi_data.index.date >= start_date) &
    (rsi_data.index.date <= end_date)
].copy()

# Reset both equity curves to 1 for the selected period
filtered_rsi["Equity_Curve"] = (
    1 + filtered_rsi["Strategy_Return"]
).cumprod()


# Calculate performance for selected period
metrics = calculate_performance(filtered_data)

# Analyze completed trades over the selected period
trades = analyze_trades(data)

if trades is not None:
    trades["Exit Date"] = pd.to_datetime(trades["Exit Date"])
    trades = trades[
        (trades["Exit Date"].dt.date >= start_date) &
        (trades["Exit Date"].dt.date <= end_date)
    ].copy()


# Main metrics
st.subheader("Strategy Performance")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Return",
    f"{metrics['Total Return (%)']}%"
)

col2.metric(
    "Sharpe Ratio",
    metrics["Sharpe Ratio"]
)

col3.metric(
    "Maximum Drawdown",
    f"{metrics['Maximum Drawdown (%)']}%"
)

col4, col5, col6 = st.columns(3)

col4.metric(
    "Win Rate",
    f"{round((trades['Net Return (%)'] > 0).mean() * 100, 2) if trades is not None and len(trades) else 0}%"
)

col5.metric(
    "Total Trades",
    len(trades) if trades is not None else 0
)

col6.metric(
    "Annualized Return",
    f"{metrics['Annualized Return (%)']}%"
)

# Gold price chart

# Gold Price, Moving Averages and Trading Signals
st.subheader("Gold Futures Price & Trading Signals")

fig, ax = plt.subplots(figsize=(14, 6))

# Gold price
ax.plot(
    filtered_data.index,
    filtered_data["Close"],
    label="Gold Price",
    linewidth=1.5
)

# Moving averages
ax.plot(
    filtered_data.index,
    filtered_data["SMA_20"],
    label=f"SMA {short_sma}",
    alpha=0.8
)

ax.plot(
    filtered_data.index,
    filtered_data["SMA_50"],
    label=f"SMA {long_sma}",
    alpha=0.8
)

# BUY and SELL markers
if trades is not None and not trades.empty:

    ax.scatter(
        trades["Entry Date"],
        trades["Entry Price"],
        marker="^",
        color="green",
        s=120,
        label="BUY",
        zorder=5
    )

    ax.scatter(
        trades["Exit Date"],
        trades["Exit Price"],
        marker="v",
        color="red",
        s=120,
        label="SELL",
        zorder=5
    )

ax.set_xlabel("Date")
ax.set_ylabel("Gold Price (USD)")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)


# RSI chart
st.subheader("Relative Strength Index")

fig, ax = plt.subplots(figsize=(14, 3))

ax.plot(data.index, data["RSI"], label="RSI")
ax.axhline(70, linestyle="--", label="Overbought")
ax.axhline(30, linestyle="--", label="Oversold")

ax.set_ylabel("RSI")
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)
plt.close(fig)


# Strategy vs Buy and Hold
st.subheader("Strategy vs Buy & Hold")

fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(
    filtered_data.index,
    filtered_data["Equity_Curve"],
    label="Trading Strategy",
    linewidth=2
)

ax.plot(
    filtered_data.index,
    filtered_data["Buy_Hold_Equity"],
    label="Buy & Hold",
    linewidth=2
)

ax.set_xlabel("Date")
ax.set_ylabel("Portfolio Growth")
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)
plt.close(fig)


# Multiple Strategy Comparison
st.subheader("Trading Strategy Comparison")

fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(
    filtered_data.index,
    filtered_data["Equity_Curve"],
    label="SMA Crossover Strategy",
    linewidth=2
)

ax.plot(
    filtered_rsi.index,
    filtered_rsi["Equity_Curve"],
    label="RSI Strategy",
    linewidth=2
)

ax.set_title("SMA vs RSI Strategy Performance")
ax.set_xlabel("Date")
ax.set_ylabel("Portfolio Growth (Initial = 1)")
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)
plt.close(fig)


# Strategy Performance Comparison
st.subheader("Strategy Performance Comparison")

sma_metrics = calculate_performance(filtered_data)
rsi_metrics = calculate_performance(filtered_rsi)

comparison = pd.DataFrame({
    "Metric": list(sma_metrics.keys()),
    "SMA Strategy": list(sma_metrics.values()),
    "RSI Strategy": list(rsi_metrics.values())
})

st.dataframe(
    comparison,
    hide_index=True,
    use_container_width=True
)


# Trade history
st.subheader("Trade History")

if trades is not None and len(trades):
    st.dataframe(trades, use_container_width=True)
else:
    st.info("No completed trades found.")

st.caption(
    "Educational backtest using historical Gold Futures data. "
    "Results are simulated and do not represent guaranteed future performance."
)


# Drawdown Analysis
st.subheader("Portfolio Drawdown Analysis")

# Calculate drawdown
filtered_data["Drawdown"] = (
    filtered_data["Equity_Curve"] /
    filtered_data["Equity_Curve"].cummax()
    - 1
) * 100

fig, ax = plt.subplots(figsize=(14, 4))

ax.fill_between(
    filtered_data.index,
    filtered_data["Drawdown"],
    0,
    alpha=0.3,
    color="red"
)

ax.plot(
    filtered_data.index,
    filtered_data["Drawdown"],
    color="red",
    linewidth=1.5,
    label="Drawdown"
)

ax.set_title("Strategy Drawdown Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Drawdown (%)")
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)
plt.close(fig)


# Rolling Volatility Analysis
st.subheader("Rolling 20-Day Strategy Volatility")

filtered_data["Rolling_Volatility"] = (
    filtered_data["Strategy_Return"]
    .rolling(window=20)
    .std()
    * (252 ** 0.5)
    * 100
)

fig, ax = plt.subplots(figsize=(14, 4))

ax.plot(
    filtered_data.index,
    filtered_data["Rolling_Volatility"],
    label="20-Day Annualized Volatility",
    linewidth=1.5
)

ax.set_title("Rolling Strategy Volatility")
ax.set_xlabel("Date")
ax.set_ylabel("Volatility (%)")
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)
plt.close(fig)
