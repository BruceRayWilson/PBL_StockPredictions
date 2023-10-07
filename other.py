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
    parser.add_argument("-tb", "--train_base_filename", default='train_base.csv', help="CSV filename for StockSymbolCollection")
    parser.add_argument("-tf", "--train_filename", default='train.csv', help="CSV filename to get the list of stock symbols for StockData")
    parser.add_argument("-st", "--start_time", help="Start time for StockData in the format YYYY-MM-DD")
    parser.add_argument("-et", "--end_time", help="End time for StockData in the format YYYY-MM-DD")
    parser.add_argument("-pp", "--preprocess", action='store_true', help="Execute StockPreprocessor")
    parser.add_argument("-train", action='store_true', help="Execute LLM training")
    parser.add_argument("-predict", action='store_true', help="Execute LLM prediction")


def main() -> None:
    """Main function to execute the script"""
    args = add_args()

    if args.train_base_filename:
        StockSymbolCollection.exec(args.train_base_filename)

    if args.train_filename and args.start_time and args.end_time:
        df = pd.read_csv(args.train_filename)
        symbols_list = df['Symbol'].tolist()
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
Now, you can run the script with the provided default values or specify new file names with the `-tb` and `-tf` flags for train_base_filename and train_filename respectively:

    python stock_manager.py --start_time 2023-01-01 --end_time 2023-10-01

Or:

    python stock_manager.py --tb new_train_base.csv --tf new_train.csv --start_time 2023-01-01 --end_time 2023-10-01
"""


