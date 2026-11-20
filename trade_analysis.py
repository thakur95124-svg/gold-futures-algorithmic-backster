
import pandas as pd


def analyze_trades(data):

    trades = []
    entry_date = None
    entry_price = None
    entry_index = None

    for i in range(1, len(data)):

        previous_position = data["Position"].iloc[i - 1]
        current_position = data["Position"].iloc[i]

        # Enter a trade
        if previous_position == 0 and current_position == 1:
            entry_index = i
            entry_date = data.index[i - 1]
            entry_price = data["Close"].iloc[i - 1]

        # Exit a trade
        elif previous_position == 1 and current_position == 0:

            exit_date = data.index[i - 1]
            exit_price = data["Close"].iloc[i - 1]

            trade_returns = data["Strategy_Return"].iloc[
                entry_index:i + 1
            ]

            net_return = ((1 + trade_returns).prod() - 1) * 100

            trades.append({
                "Entry Date": entry_date,
                "Exit Date": exit_date,
                "Entry Price": entry_price,
                "Exit Price": exit_price,
                "Net Return (%)": net_return
            })

            entry_date = None
            entry_price = None
            entry_index = None

    if not trades:
        print("No completed trades found.")
        return

    trades_df = pd.DataFrame(trades)

    winning = trades_df[trades_df["Net Return (%)"] > 0]
    losing = trades_df[trades_df["Net Return (%)"] < 0]

    win_rate = len(winning) / len(trades_df) * 100

    gross_profit = winning["Net Return (%)"].sum()
    gross_loss = abs(losing["Net Return (%)"].sum())

    profit_factor = (
        gross_profit / gross_loss if gross_loss != 0 else float("inf")
    )

    print("\nTRADE ANALYSIS")
    print("------------------------")
    print("Total Trades:", len(trades_df))
    print("Winning Trades:", len(winning))
    print("Losing Trades:", len(losing))
    print("Win Rate:", round(win_rate, 2), "%")
    print("Average Net Return:",
          round(trades_df["Net Return (%)"].mean(), 2), "%")
    print("Profit Factor:", round(profit_factor, 2))

    print("\nTRADE HISTORY")
    print(trades_df.to_string(index=False))

    return trades_df
