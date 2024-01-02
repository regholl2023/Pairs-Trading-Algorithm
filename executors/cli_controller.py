import os
import sys
# Get the directory of the current script
# If the script is not in the root directory, navigate to the root directory
# Append the root directory to sys.path so that modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Get the directory of the current script
# If the script is not in the root directory, navigate to the root directory
# Append the root directory to sys.path so that modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from trading.alpaca_functions import Alpaca
from utils.formatting_and_logs import green_bold_print, blue_bold_print, red_bold_print, emphasis_bold_red_print
from executors import analysis_executor
from executors import alpaca_executor


def main_menu(alpaca: Alpaca):
    # new line
    sys.stdout.write("\n")
    emphasis_bold_red_print("Main Menu | " + "Alpaca Balance: $" + str(alpaca.account.buying_power))
    blue_bold_print("1: Run analysis - Find Suitable Pair")
    blue_bold_print("2: Current Positions - Live Portfolio")
    blue_bold_print("3: Enter New Hedge Position")
    blue_bold_print("4: Manual Trade")
    blue_bold_print("5: Backtest Strategy")
    choice = input("Please select an option: ")
    return choice


def main():
    alpaca_connection = Alpaca()
    while True:
        try:
            choice = main_menu(alpaca=alpaca_connection)
            if choice not in ["1", "2", "3", "4", "5"]:
                raise ValueError
            elif choice == "1":
                analysis_executor.run_analysis()
            elif choice == "2":
                alpaca_executor.live_position_menu(alpaca_connection)
            elif choice == "3":
                alpaca_executor.enter_new_hedge_position_menu(alpaca_connection)
            elif choice == "4":
                alpaca_executor.manual_trade_menu(alpaca_connection)
            elif choice == "5":
                analysis_executor.backtest_strategy()
        except ValueError:
            red_bold_print("Invalid input")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
