# Gold Futures Algorithmic Trading Backtester

A Python-based algorithmic trading and backtesting project that analyzes historical Gold Futures market data, generates automated trading signals, evaluates trading strategies, and visualizes performance through an interactive Streamlit dashboard.

## Project Overview

This project implements and compares two technical trading strategies: Simple Moving Average (SMA) Crossover and Relative Strength Index (RSI).

It uses historical Gold Futures data obtained from Yahoo Finance to simulate trading decisions and evaluate strategy performance using financial and statistical metrics.

## Key Features

- **Historical Market Data:** Fetches Gold Futures data using Yahoo Finance (`GC=F`).
- **Technical Indicators:** Calculates SMA (20, 50) and RSI.
- **Automated Trading Signals:** Generates BUY and SELL signals based on technical indicators.
- **Strategy Backtesting:** Simulates trades using historical price movements.
- **Transaction Costs:** Incorporates estimated transaction costs into strategy returns.
- **Performance Evaluation:** Calculates total return, annualized return, Sharpe ratio, volatility, win rate and profit factor.
- **Risk Analysis:** Evaluates maximum drawdown and rolling volatility.
- **Strategy Comparison:** Compares SMA Crossover and RSI-based strategies.
- **Interactive Dashboard:** Displays charts, performance metrics and strategy configurations using Streamlit.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical calculations |
| yfinance | Historical market data |
| Matplotlib | Financial data visualization |
| Streamlit | Interactive dashboard |

## Project Structure

```text
Algorithmic Trading Backtester/
│
├── main.py
├── app.py
├── indicators.py
├── strategies.py
├── backtester.py
├── performance.py
├── trade_analysis.py
├── gold_futures.csv
└── README.md
```

## Trading Strategies

### 1. SMA Crossover Strategy
- Uses short-term and long-term Simple Moving Averages.
- Generates a BUY signal when the short-term SMA crosses above the long-term SMA.
- Generates a SELL signal when the short-term SMA crosses below the long-term SMA.
- Uses RSI as an additional signal filter.

### 2. RSI-Based Strategy
- Uses the Relative Strength Index to identify potential market conditions.
- BUY signal when RSI falls below 30.
- SELL signal when RSI rises above 70.

## Performance Metrics

The backtesting engine evaluates strategies using:

- Total Return
- Annualized Return
- Annualized Volatility
- Sharpe Ratio
- Maximum Drawdown
- Win Rate
- Average Trade Return
- Profit Factor

The interactive dashboard provides:

- Gold Futures price visualization.
- SMA and RSI technical indicators.
- Automated BUY/SELL markers.
- Strategy versus Buy & Hold comparison.
- Portfolio drawdown visualization.
- Rolling volatility analysis.
- Adjustable trading strategy parameters.
- Quantitative performance comparison.

  App Link:
  https://gold-futures-algorithmic-backster-gtcoh62h93gkopuac8sgww.streamlit.app/

**Author:** Shubham Thakur
