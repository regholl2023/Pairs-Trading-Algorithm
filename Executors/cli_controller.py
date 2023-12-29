import Executors.analysis_executor
from Trading.alpaca_functions import Alpaca
from AidanUtils.formatting_and_logs import green_bold_print
from Executors import analysis_executor
from Executors import alpaca_executor


while True:
    try:
        green_bold_print("1: Run Analysis")
        green_bold_print("2: Current Positions - Live Portfolio")
        green_bold_print("3: Enter New Hedge Position")
        choice = input("Please select an option: ")
        if choice not in ["1", "2", "3"]:
            raise ValueError
        elif choice == "1":
            analysis_executor.run()
        elif choice == "2":
            green_bold_print("Current Positions - Live Portfolio")
            alpaca_executor.execute_algo(tp=5, sl=5)
        elif choice == "3":
            green_bold_print("Enter New Hedge Position Selected")
            alpaca = Alpaca()
            green_bold_print("Please enter the pair you would like to trade as: stock_1, stock_2 ")
            pair_input = input()
            pair_list = pair_input.split(',')
            hr = input("Please enter the hedge ratio: ")
            leverage = input("Please enter the leverage: ")
            alpaca.enter_hedge_position(pair_list[0], pair_list[1], side="buy", hr=hr, leverage=leverage)
    except ValueError:
        green_bold_print("Invalid input")
        continue
    except Exception as e:
        print(e)