import os
import sys
import threading
import time

from AidanUtils.formatting_and_logs import green_bold_print

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# If the script is not in the root directory, navigate to the root directory
root_dir = os.path.dirname(current_dir)
# Append the root directory to sys.path so that modules can be imported
sys.path.append(root_dir)

import pandas as pd
from alpaca.trading import OrderSide, TimeInForce, PositionSide, Position
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.stream import TradingStream
from AidanUtils.MyTimer import timeit

os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'


def connect_to_trading_stream():
    """
    Connects to the Alpaca Trading Stream using predefined API credentials.
    Returns a TradingStream object if successful, else prints an error message.
    """
    try:
        return TradingStream("PKNWSWFGL7X6F50PJ8UH", "1qpcAmhEmzxONh3Im0V6lzgqtVOX2xD3k7mViYLX", paper=True)
    except Exception:
        print("Error getting trade stream")


def pause_algo(seconds):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r" + "Paused Algorithm: {:2d} seconds remaining.".format(remaining))
        time.sleep(1)


class Alpaca:

    """
    Alpaca class to manage trading activities.
    It handles connection to Alpaca API, managing positions, entering hedge positions,
    retrieving and displaying position data, profit calculation, and order management.
    """

    def __init__(self):
        """
        Constructor for Alpaca class.
        Initializes connection to Alpaca API, retrieves current positions,
        and sets up trading stream.
        """
        self.connected = False
        self.account = None
        self.client = self.connect_to_alpaca("PKNWSWFGL7X6F50PJ8UH", "1qpcAmhEmzxONh3Im0V6lzgqtVOX2xD3k7mViYLX",
                                             paper=True)
        self.in_position = bool(self.client.get_all_positions())
        self.positions = self.client.get_all_positions()

    @timeit
    def connect_to_alpaca(self, api_key: str, api_secret: str, paper: bool) -> TradingClient:
        """
        Establishes a connection to the Alpaca trading service using API credentials.
        If successful, prints the connection status and available buying power.
        Returns a TradingClient object.

        Args:
        api_key (str): Alpaca API key.
        api_secret (str): Alpaca API secret.
        paper (bool): Flag for paper trading (True for paper trading, False for live trading).

        Returns:
        TradingClient: A client object to interact with Alpaca's trading services.
        """
        try:
            trading_client = TradingClient(api_key, api_secret, paper=paper)
            self.account = trading_client.get_account()
            print('Connected to Alpaca, buying power is: ' + self.account.buying_power)
            self.connected = True
            return trading_client

        except Exception:
            print("Error connecting to Alpaca")

    def send_market_order(self, symbol: str, qty: int | float, side: OrderSide | str):
        """
        Sends a market order to the Alpaca API.

        Args:
        symbol (str): Symbol of the stock to trade.
        qty (int): Quantity of the stock to trade.
        side (OrderSide | str): Side of the order, either 'buy' or 'sell'.
        """
        try:
            self.client.submit_order(
                order_data=MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=side,
                ))
            green_bold_print("Market order executed for {} shares of {}".format(qty, symbol))
        except Exception:
            print("Error sending order")

    def send_limit_order(self, symbol: str, qty: int | float, side: OrderSide | str, limit_price: float, **kwargs):
        """
        Sends a limit order to the Alpaca API.

        Args:
        symbol (str): Symbol of the stock to trade.
        qty (int): Quantity of the stock to trade.
        side (OrderSide): Side of the order, either 'buy' or 'sell'.
        limit_price (float): Limit price of the order.
        **kwargs:
            Optional arguments for take profit. Must specify take_profit=TP_PRICE.
            Optional arguments for stop loss. Must specify stop_loss=SL_PRICE.

        """
        try:
            self.client.submit_order(
                order_data=LimitOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=side,
                    limit_price=limit_price,
                    take_profit=kwargs.get('take_profit', None),
                    stop_loss=kwargs.get('stop_loss', None),
                ))
            green_bold_print("Limit order placed for {} shares of {} at {}".format(qty, symbol, limit_price))

        except Exception:
            print("Error sending order")

    def enter_hedge_position(self, stock_1, stock_2, side, leverage, hr):
        """
        Enters a hedge position by placing market orders on two stocks.
        A hedge position involves buying one stock and selling another.

        Args:
        stock_1 (str): Symbol of the first stock.
        stock_2 (str): Symbol of the second stock.
        side (str): 'buy' or 'sell', indicating the direction of the hedge.
        leverage (float): Leverage factor to apply to the order quantity.
        hr (float): Hedge ratio to calculate the quantity of the second stock.
        """
        if side == "buy":
            stock_2_side = OrderSide.SELL
        elif side == "sell":
            stock_2_side = OrderSide.BUY

        try:
            # Placing market orders for both stocks
            self.client.submit_order(
                order_data=MarketOrderRequest(
                    symbol=stock_1,
                    qty=1 * leverage,
                    side=side,
                    time_in_force=TimeInForce.DAY
                ))
            print(stock_1 + ' ' + side + ' order executed')

            self.client.submit_order(
                order_data=MarketOrderRequest(
                    symbol=stock_2,
                    qty=round(hr * leverage),
                    side=stock_2_side,
                    time_in_force=TimeInForce.DAY
                ))
            print(stock_2 + ' ' + stock_2_side + ' order executed')

        except Exception:
            print("Error entering hedge position")

    def get_positions_dict(self):
        if self.in_position:
            return self.client.get_all_positions()

    def get_open_position_for_symbol(self, symbol_or_asset_id) -> Position:
        """
        Get the open position for a symbol or asset ID.

        Args:
            symbol_or_asset_id: The symbol or asset ID to get the open position for.

        Returns:
            The open position for the symbol or asset ID.
        """
        return self.client.get_open_position(symbol_or_asset_id=symbol_or_asset_id)

    def close_position_for_symbol(self, symbol_or_asset_id):
        """
        Close a position for a symbol or asset ID.

        Args:
            symbol_or_asset_id: The symbol or asset ID to close the position for.

        Returns:
            The closed position for the symbol or asset ID.
        """
        return self.client.close_position(symbol_or_asset_id=symbol_or_asset_id)

    def get_positions_df(self):
        """
        Retrieves and formats the current positions into a DataFrame.
        Converts specific string columns to float for numerical analysis.
        Returns a DataFrame of the current positions.

        Returns:
        pandas.DataFrame: DataFrame containing details of current positions.
        """
        assets = pd.DataFrame()
        if self.in_position:
            for n in range(len(self.client.get_all_positions())):
                pos = dict(self.client.get_all_positions()[n])
                pos = pd.DataFrame.from_dict(pos, orient='index').T
                assets = pd.concat([assets, pos])

                # Changing columns from str to float type
                columns_to_convert = ['unrealized_pl', 'cost_basis', 'market_value',
                                      'avg_entry_price', 'qty', 'unrealized_plpc']
                for column in columns_to_convert:
                    assets[column] = assets[column].astype(float)
        return assets

    def print_positions(self):
        """
        Prints the details of the current positions held.
        Includes the side (Long/Short), quantity, purchase price, and unrealized profit percentage.
        """
        portfolio = self.client.get_all_positions()
        side_map = {PositionSide.SHORT: "Short", PositionSide.LONG: "Long"}
        print("Current Positions:")
        if portfolio:
            for position in portfolio:
                print("{} {} shares of {} purchased for {} current unrealised profit_pc is {}%"
                      .format(side_map[position.side],
                              position.qty.replace("-", ""),
                              position.symbol,
                              abs(float(position.cost_basis)),
                              self.get_unrealised_profit_pc()))
        else:
            print("No positions")

    def get_unrealised_profit_pc(self):
        """
        Calculates the percentage of unrealized profit or loss across all positions.
        Returns the percentage value rounded to three decimal places.

        Returns:
        float: The percentage of unrealized profit or loss.
        """
        try:
            portfolio = self.client.get_all_positions()
            profit = sum([position.unrealized_pl for position in portfolio])
            cost_basis = sum([position.cost_basis for position in portfolio])

            if cost_basis == 0:
                return 0

            return round((profit * 100 / cost_basis), 3)

        except Exception:
            pass

    def check_and_take_profit(self, tp):
        """
        Executes orders to take profit if the unrealized profit percentage exceeds the specified threshold.

        Args:
        tp (float): The profit threshold percentage to trigger selling.
        """
        assert tp > 0, "Stop loss must be a positive value"

        if self.get_unrealised_profit_pc() > tp:
            print("Executing orders to take profit...")
            if self.close_all_positions():
                print("Took profit")

    def check_and_stop_loss(self, sl):
        """
        Executes stop loss orders if the unrealized loss exceeds the specified threshold.

        Args:
        sl (float): The loss threshold percentage to trigger selling.
        """
        sl = abs(sl) * -1
        assert sl <= 0, "Stop loss must be a negative value"
        if self.get_unrealised_profit_pc() < sl:
            print("Executing orders to stop loss")
            if self.close_all_positions():
                print("Stopped Loss")

    def close_all_positions(self):
        # This needs to be fixed and we should split this into other methods that limit orders and market orders
        """
        Closes all positions by submitting market or limit orders.
        If unable to submit a market order, it submits a limit order at the current price.
        Returns True if all orders are filled, False otherwise.

        Returns:
        bool: True if all positions are closed successfully, False otherwise.
        """
        close_info = self.client.close_all_positions(cancel_orders=True)
        for order in close_info:
            order = order.body
            side_map = {OrderSide.BUY: "buy", OrderSide.SELL: "sell"}
            print(
                f"Attempted to {side_map[order.side]} {order.qty} shares of {order.symbol}. {order.filled_qty} orders filled for {order.filled_avg_price}")
            if order.filled_qty == order.qty:
                return True
            else:
                return False

    def use_live_tp_sl(self, tp: int | float, sl: int | float):
        """
        Continuously monitors the portfolio for take profit (tp) or stop loss (sl) conditions.
        Prints the current unrealized profit percentage and executes orders if conditions are met.

        Args:
        tp (float): Take profit threshold percentage.
        sl (float): Stop loss threshold percentage.
        """

        def exit_monitor():
            """
            Monitors for the user input to pause the algorithm.
            """
            while True:
                user_input = input()  # Wait for user input
                if user_input.lower() == 'exit':
                    print("\nPausing algorithm...")
                    pause_algo(60)  # Call the pause_algo method
                    break

        self.print_positions()

        # Start the thread for monitoring pause input
        pause_thread = threading.Thread(target=exit_monitor)
        pause_thread.start()

        count = 0
        while pause_thread.is_alive():  # Continue while the pause thread is running
            output = f'{count} Current Profit: {self.get_unrealised_profit_pc()} %' + ' | Type "pause" to pause for 60s:'
            self.check_and_stop_loss(sl)
            self.check_and_take_profit(tp)
            sys.stdout.write("\r" + output)  # Overwrite the line with padding
            time.sleep(5)
            sys.stdout.flush()
            count += 1

        # Optional: Wait for the pause thread to finish if needed
        pause_thread.join()
