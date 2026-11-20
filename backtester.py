
import pandas as pd
import numpy as np


def run_backtest(data, transaction_cost=0.0005):

    data = data.copy()

    # Track whether we are holding a position
    position = 0
    positions = []

    for signal in data["Signal"]:

        if signal == 1:
            position = 1

        elif signal == -1:
            position = 0

        positions.append(position)

    data["Target_Position"] = positions

    # Execute signals on the next trading bar
    data["Position"] = (
        data["Target_Position"].shift(1).fillna(0)
    )

    # Calculate daily market returns
    data["Market_Return"] = data["Close"].pct_change().fillna(0)

    # Calculate transaction costs
    data["Trades"] = data["Position"].diff().abs().fillna(0)

    data["Transaction_Cost"] = (
        data["Trades"] * transaction_cost
    )

    # Calculate strategy returns
    data["Strategy_Return"] = (
        data["Position"] * data["Market_Return"]
        - data["Transaction_Cost"]
    )

    # Calculate cumulative returns
    data["Equity_Curve"] = (
        1 + data["Strategy_Return"]
    ).cumprod()

    return data
