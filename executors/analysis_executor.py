import os
import sys
from typing import List, Tuple, Optional
# Get the directory of the current script
# If the script is not in the root directory, navigate to the root directory
# Append the root directory to sys.path so that modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from analysis.statistical_methods import collect_metrics_for_pair
from executors.cli_controller import main_menu
from analysis.visualisation import spread_visualisation, zscored_spread, visualise_returns
from analysis.errors import NoSuitablePairsError
from analysis.stock_data import StockData
from utils.formatting_and_logs import green_bold_print, blue_bold_print, red_bold_print
from utils.formatting_and_logs import CustomFormatter
import logging

from trading.alpaca_functions import Alpaca

# Configure logging with a custom formatter
logging.basicConfig(level=logging.INFO)
formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.handlers = [handler]


def read_tickers_from_file(path: str) -> Optional[List[str]]:
    """
    Reads ticker symbols from a file and returns them as a list.
    Args:
    path (str): File path to read ticker symbols.
    Returns:
    Optional[List[str]]: List of ticker symbols, or None if file not found.
    """
    try:
        with open(path, 'r') as file:
            return [ticker.strip() for ticker in file.read().split(',') if len(ticker.strip()) > 1]
    except FileNotFoundError:
        logging.error("File not found. Please try again.")
        return None


def process_stock_data(symbols_list: List[str]) -> Optional[Tuple[str, str]]:
    """
    Processes stock symbols to find the most suitable pair for analysis.
    Args:
    symbols_list (List[str]): List of stock ticker symbols.
    Returns:
    Optional[Tuple[str, str]]: Most suitable pair of stocks, or None if no suitable pair is found.
    """
    try:
        stock_data = StockData(asset_list=symbols_list, bypass_adf_test=False)
        red_bold_print("Most Suitable Pair: " + stock_data.most_suitable_pair)
        return stock_data.most_suitable_pair
    except NoSuitablePairsError:
        logging.warning("No suitable pairs found. Option to bypass adf_test is available but not recommended (y/n): ")
        bypass_adf_test = input()
        if bypass_adf_test.lower() == 'y':
            stock_data = StockData(asset_list=symbols_list, bypass_adf_test=True)
            red_bold_print("Most Suitable Pair: {}, {}".format(stock_data.most_suitable_pair[0], stock_data.most_suitable_pair[1]))
            return stock_data.most_suitable_pair
        else:
            return None




    except Exception as e:
        logging.error(f"An error occurred: {e}")


def run_analysis() -> None:
    """
    Initiates the stock analysis process by reading ticker symbols and processing them.
    """
    while True:
        try:
            blue_bold_print("Ticker symbols list must be in a csv file.")
            blue_bold_print("Please enter a path to a csv file containing a list of ticker symbols or enter b to go "
                            "back:")
            path = input()
            if path == 'b':
                main_menu(alpaca=Alpaca())
            symbols_list = read_tickers_from_file(path)

            if symbols_list is not None:
                logging.info("Tickers to analyse: " + str(symbols_list))
                most_suitable_pair = process_stock_data(symbols_list)
                strategy_info = collect_metrics_for_pair(most_suitable_pair[0], most_suitable_pair[1])
                print(strategy_info)
                hedge_ratio = strategy_info['hedge_ratio'].iloc[0]
                print("Hedge Ratio: " + str(hedge_ratio))
                red_bold_print("Would you like to enter a hedge position using this pair? (y/n)")
                choice = input()
                if choice.lower() == "y":
                    try:
                        alpaca = Alpaca()
                        leverage = float(input("Please enter the leverage: "))
                        tp_sl = input("Please enter the take profit and stop loss percentage in the format 0.05, 0.05: ")
                        tp, sl = tp_sl.split(',')
                        tp, sl = float(tp.strip()), float(sl.strip())
                        alpaca.enter_hedge_position(most_suitable_pair[0], most_suitable_pair[1],
                                                    side="buy", hr=hedge_ratio, leverage=leverage)
                        logging.info("Hedge position entered.")
                        alpaca.use_live_tp_sl(tp, sl)
                        break
                    except Exception as e:
                        print(e)
                else:
                    break
            break
        except Exception as e:
            print(e)


def backtest_strategy() -> None:
    """
    Backtests a trading strategy based on user choices and stock pairs.
    """

    def backtest_menu() -> str:
        """
        Shows backtest options and returns user choice.
        Returns:
        str: User's menu choice.
        """
        blue_bold_print("1: Visualise Spread")
        blue_bold_print("2: Visualise Z-Scored Spread")
        blue_bold_print("3: Visualise Returns")
        return input("Please select an option or type 'b' to return to the main menu: ")

    blue_bold_print("Please enter the stock ticker you would like to backtest in the format stock_1, stock_2:")
    pair_input = input()
    pair_list = [pair.strip() for pair in pair_input.split(',')]
    strategy_info = collect_metrics_for_pair(pair_list[0], pair_list[1])

    while True:
        try:
            choice = backtest_menu()
            if choice not in ["1", "2", "3", "b"]:
                raise ValueError
            elif choice == "1":
                blue_bold_print("You have selected to visualise the spread.")
                spread_visualisation(strategy_info)
            elif choice == "2":
                blue_bold_print("You have selected to visualise the Z-scored spread.")
                zscored_spread(strategy_info)
            elif choice == "3":
                blue_bold_print("You have selected to visualise the returns.")
                blue_bold_print("Specify a take profit and stop loss percentage in the format 0.05, 0.05:")
                tp_sl = input()
                tp, sl = tp_sl.split(',')
                tp, sl = float(tp.strip()), float(sl.strip())
                visualise_returns(strategy_info, tp, sl)
            elif choice == 'b':
                break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    run_analysis()
