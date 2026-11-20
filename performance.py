
import numpy as np


def calculate_performance(data):

    returns = data["Strategy_Return"]

    total_return = (
        data["Equity_Curve"].iloc[-1] - 1
    ) * 100

    annual_return = (
        data["Equity_Curve"].iloc[-1]
        ** (252 / len(data)) - 1
    ) * 100

    volatility = returns.std() * np.sqrt(252) * 100

    sharpe_ratio = (
        (returns.mean() / returns.std()) * np.sqrt(252)
        if returns.std() != 0 else 0
    )

    drawdown = (
        data["Equity_Curve"]
        / data["Equity_Curve"].cummax()
    ) - 1

    max_drawdown = drawdown.min() * 100

    positive_days = (
        returns[returns != 0] > 0
    ).mean() * 100 if (returns != 0).any() else 0

    return {
        "Total Return (%)": round(total_return, 2),
        "Annualized Return (%)": round(annual_return, 2),
        "Annualized Volatility (%)": round(volatility, 2),
        "Sharpe Ratio": round(sharpe_ratio, 2),
        "Maximum Drawdown (%)": round(max_drawdown, 2),
        "Positive Trading Days (%)": round(positive_days, 2)
    }
