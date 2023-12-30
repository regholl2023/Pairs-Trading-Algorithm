import os
import sys

from AidanUtils.formatting_and_logs import blue_bold_print

# Get the directory of the current script
# If the script is not in the root directory, navigate to the root directory
# Append the root directory to sys.path so that modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from Trading.alpaca_functions import Alpaca


def live_position_menu(alpaca: Alpaca):
    try:
        blue_bold_print("Current Positions - Live Portfolio")
        alpaca.use_live_tp_sl(5, 5)
    except Exception as e:
        print(e)


def manual_trade_menu(alpaca: Alpaca):
    try:
        blue_bold_print("Manual Trade Selected")
        blue_bold_print("To place a trade, please enter the following information:")
        symbol = input("Symbol: ")
        qty = input("Quantity: ")

        if qty.isnumeric():
            qty = float(qty)

        side = input("Side (buy/sell): ")
        order_type = input("Type (market/limit): ")

        if order_type == "limit":
            while True:
                limit_price = input("Limit Price: ")
                if limit_price.isnumeric():
                    limit_price = float(limit_price)
                    alpaca.send_limit_order(symbol, qty, side, limit_price)
                    break
        elif order_type == "market":
            alpaca.send_market_order(symbol, qty, side)

    except Exception as e:
        print(e)


def enter_new_hedge_position_menu(alpaca: Alpaca):
    try:
        blue_bold_print("Enter New Hedge Position Selected")
        blue_bold_print("Please enter the pair you would like to trade as: stock_1, stock_2 ")
        pair_input = input()
        pair_list = pair_input.split(',')
        hr = input("Please enter the hedge ratio: ")
        leverage = input("Please enter the leverage: ")
        alpaca.enter_hedge_position(pair_list[0], pair_list[1], side="buy", hr=hr, leverage=leverage)
    except Exception as e:
        print(e)
