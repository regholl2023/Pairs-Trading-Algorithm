import os
import sys

from Analysis.statistical_methods import collect_metrics_for_pair
from Executors.cli_controller import main_menu
from Analysis.visualisation import spread_visualisation, zscored_spread, visualise_returns

# Get the directory of the current script
# If the script is not in the root directory, navigate to the root directory
# Append the root directory to sys.path so that modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from Analysis.errors import NoSuitablePairsError
from Analysis.stock_data import StockData
from AidanUtils.formatting_and_logs import green_bold_print, blue_bold_print, red_bold_print
from AidanUtils.formatting_and_logs import CustomFormatter
import logging

# Set up logging with custom formatter
logging.basicConfig(level=logging.INFO)
formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.handlers = [handler]


def read_tickers_from_file(path):
    try:
        with open(path, 'r') as file:
            return [ticker.strip() for ticker in file.read().split(',') if len(ticker.strip()) > 1]
    except FileNotFoundError:
        logging.error("File not found. Please try again.")
        return None


def process_stock_data(symbols_list):
    try:
        stock_data = StockData(asset_list=symbols_list, bypass_adf_test=False)
        red_bold_print("Most Suitable Pair: " + stock_data.most_suitable_pair)
        return stock_data.most_suitable_pair
    except NoSuitablePairsError:
        logging.warning("No suitable pairs found in the given list of tickers. Please try again.")
        logging.warning("Would you like to bypass the adf_test requirement? (y/n)")
        choice = input()
        if choice.lower() == 'y':
            stock_data = StockData(asset_list=symbols_list, bypass_adf_test=True)
            red_bold_print("Most Suitable Pair: " + str(stock_data.most_suitable_pair))
            return stock_data.most_suitable_pair
        else:
            main_menu()
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def run_analysis():
    while True:
        blue_bold_print("Ticker symbols list must be in a csv file.")
        blue_bold_print("Please enter a path to a csv file containing a list of ticker symbols or enter b to go back:")
        path = input()
        if path == 'b':
            main_menu()
        symbols_list = read_tickers_from_file(path)

        if symbols_list is not None:
            logging.info("Tickers to analyse: " + str(symbols_list))
            most_suitable_pair = process_stock_data(symbols_list)
            strategy_info = collect_metrics_for_pair(most_suitable_pair[0], most_suitable_pair[1])
            print(strategy_info)
            break


def backtest_strategy():
    def backtest_menu():
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
