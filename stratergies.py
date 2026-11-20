
def generate_signals(data):

    data = data.copy()

    # Previous day's moving averages
    data["Previous_SMA_20"] = data["SMA_20"].shift(1)
    data["Previous_SMA_50"] = data["SMA_50"].shift(1)

    # BUY condition: Golden Cross
    buy_condition = (
        (data["Previous_SMA_20"] <= data["Previous_SMA_50"]) &
        (data["SMA_20"] > data["SMA_50"]) &
        (data["RSI"] < 70)
    )

    # SELL condition: Death Cross
    sell_condition = (
        (data["Previous_SMA_20"] >= data["Previous_SMA_50"]) &
        (data["SMA_20"] < data["SMA_50"]) &
        (data["RSI"] > 30)
    )

    data["Signal"] = 0

    data.loc[buy_condition, "Signal"] = 1
    data.loc[sell_condition, "Signal"] = -1

    return data
