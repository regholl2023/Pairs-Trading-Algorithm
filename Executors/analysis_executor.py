import os
import sys

from Executors.cli_controller import main_menu

# Get the directory of the current script
# If the script is not in the root directory, navigate to the root directory
# Append the root directory to sys.path so that modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from Analysis.errors import NoSuitablePairsError
from Analysis.stock_data import StockData
from AidanUtils.formatting_and_logs import green_bold_print, blue_bold_print
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
            return [ticker.strip() for ticker in file.read().split(',')]
    except FileNotFoundError:
        logging.error("File not found. Please try again.")
        return None


def process_stock_data(symbols_list):
    try:
        stock_data = StockData(asset_list=symbols_list)
        green_bold_print("Most Suitable Pair: " + stock_data.most_suitable_pair)
    except NoSuitablePairsError:
        logging.warning("No suitable pairs found in the given list of tickers. Please try again.")
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
            process_stock_data(symbols_list)
            break


if __name__ == '__main__':
    run_analysis()
