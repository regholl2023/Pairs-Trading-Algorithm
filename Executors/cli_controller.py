import Executors.analysis_executor
from Trading.alpaca_functions import Alpaca
from AidanUtils.formatting_and_logs import green_bold_print, blue_bold_print, red_bold_print
from Executors import analysis_executor
from Executors import alpaca_executor


def main_menu():
    blue_bold_print("1: Run Analysis")
    blue_bold_print("2: Current Positions - Live Portfolio")
    blue_bold_print("3: Enter New Hedge Position")
    blue_bold_print("4: Manual Trade")
    choice = input("Please select an option: ")
    return choice


def main():
    alpaca_connection = Alpaca()
    while True:
        try:
            choice = main_menu()
            if choice not in ["1", "2", "3", "4"]:
                raise ValueError
            elif choice == "1":
                analysis_executor.run_analysis()
            elif choice == "2":
                alpaca_executor.live_position_menu(alpaca_connection)
            elif choice == "3":
                alpaca_executor.enter_new_hedge_position_menu(alpaca_connection)
            elif choice == "4":
                alpaca_executor.manual_trade_menu(alpaca_connection)
        except ValueError:
            red_bold_print("Invalid input")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
