# filename: stock_manager.py

import argparse
from datetime import datetime
import pandas as pd

class StockSymbolCollection:
    """Class to verify stock symbols"""

    @staticmethod
    def exec(csv_filename: str) -> None:
        '''Executes the StockSymbolCollection class. Reads CSV and prints content'''
        df = pd.read_csv(csv_filename)
        print(df)

class StockData:
    """Class to collect stock market data"""

    @staticmethod
    def exec(self, symbols_list: list, start_time: datetime, end_time: datetime) -> None:
        '''Executes the StockData class. Prints the symbols along with start and end time'''
        print(f"Collecting data for '{symbols_list}' from '{start_time}' to '{end_time}'")


class StockPreprocessor:
    """Class to preprocess collected stock market data"""

    @staticmethod
    def exec() -> None:
        '''The method just prints a success message as of now'''
        print("Preprocessing data...")

class LLM:
    """Class to manage Linear Level Models (LLM) for stock market data analysis"""

    @staticmethod
    def train() -> None:
        '''Trains LLM. Prints a success message as of now.'''
        print("LLM training...")

    @staticmethod
    def predict() -> None:
        '''Runs LLM prediction. Prints a success message as of now.'''
        print("LLM predicting...")


def add_args():
    """Function to add command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-csv", "--csv_filename", help="CSV filename for StockSymbolCollection")
    parser.add_argument("-sym", "--symbols", help="List of stock symbols for StockData")
    parser.add_argument("-st", "--start_time", help="Start time for StockData in the format YYYY-MM-DD")
    parser.add_argument("-et", "--end_time", help="End time for StockData in the format YYYY-MM-DD")
    parser.add_argument("-pp", "--preprocess", action='store_true', help="Execute StockPreprocessor")
    parser.add_argument("-train", action='store_true', help="Execute LLM training")
    parser.add_argument("-predict", action='store_true', help="Execute LLM prediction")


def main() -> None:
    """Main function to execute the script"""
    args = add_args()
    if args.csv_filename:
        StockSymbolCollection.exec(args.csv_filename)
    if args.symbols and args.start_time and args.end_time:
        symbols_list = args.symbols.split(',')
        start_time = datetime.strptime(args.start_time, '%Y-%m-%d')
        end_time = datetime.strptime(args.end_time, '%Y-%m-%d')
        StockData.exec(symbols_list, start_time, end_time)
    if args.preprocess:
        StockPreprocessor.exec()
    if args.train:
        LLM.train()
    if args.predict:
        LLM.predict()


def menu() -> None:
    """
    Displays a menu for users who run the script without CLI arguments
    """
    print("1. Stock Symbol Verification")
    print("2. Stock Data Collection")
    print("3. Stock Preprocessor")
    print("4. LLM")
    print("   4.1 LLM Training")
    print("   4.2 LLM Prediction")

    choice = input("Choose an option: ")
    if choice == '1':
        csv_filename = 'train_base.csv'
        StockSymbolCollection.exec(csv_filename)
    elif choice == '2':
        csv_filename = 'train.csv'
        df = pd.read_csv(csv_filename)
        symbols_list = df['Symbol'].tolist()
        start_time = input("Enter start time (YYYY-MM-DD): ")
        end_time = input("Enter end time (YYYY-MM-DD): ")
        start_time = datetime.strptime(start_time, '%Y-%m-%d')
        end_time = datetime.strptime(end_time, '%Y-%m-%d')
        StockData.exec(symbols_list, start_time, end_time)
    elif choice == '3':
        StockPreprocessor.exec()
    elif choice == '4':
        subchoice = input("   Choose an option (1 or 2): ")
        if subchoice == '1':
            LLM.train()
        elif subchoice == '2':
            LLM.predict()

if __name__ == "__main__":
    main()

"""
This script creates the necessary classes and methods. You can run the script from the 
command line using CLI arguments (Option A), or run the script and use the menu (Option B). 

Please note the current state of the methods `StockSymbolCollection.exec, StockData.exec(), 
StockPreprocessor.exec(), LLM.train() and LLM.predict()` are simple, meaning they just print 
out some information and do not perform actual operations. You would need to replace the 
print statements with your actual implementation.

You can execute option A by providing the proper arguments in the command line after the python command:

    python stock_manager.py --csv_filename train_base.csv --symbols AAPL,MSFT,GOOGL --start_time 2023-01-01 --end_time 2023-10-01

For Option B, the menu gets displayed and expects a user input:

    python stock_manager.py
    1. Stock Symbol Verification
    2. Stock Data Collection
    3. Stock Preprocessor
    4. LLM
       4.1 LLM Training
       4.2 LLM Prediction
    Choose an option: '1'
"""

