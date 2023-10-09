import yfinance as yf
import pandas as pd
import os
from typing import List
from datetime import datetime
import csv

# import MeaningfulData

class StockData:
    data_dir = "data_stocks"

class StockData:
    def __init__(self, stock_symbols_path: str, start_time: datetime, end_time: datetime):
        """
        Initialize the StockData object.

        Args:
            stock_symbols_path (str): Path to the CSV file containing stock symbols.
            start_time (datetime): The start time for collecting data.
            end_time (datetime): The end time for collecting data.

        """
        self.start_time = start_time
        self.end_time = end_time

        # Read the stock symbols from the CSV file
        with open(stock_symbols_path, 'r') as file:
            reader = csv.reader(file)
            self.stock_symbols = [row[0] for row in reader]

        # Create the data directory if it doesn't exist
        self.data_dir = "data"  # Assuming the data directory name is 'data'
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)


    def _get_stock_data(self, symbol: str):
        """
        Collect stock data for a single stock symbol.

        Args:
            symbol (str): The stock symbol to collect data for.

        Returns:
            pd.DataFrame: A Pandas DataFrame containing the stock data.
        """
        filepath = os.path.join(self.data_dir, f"{symbol}.csv")
        if not os.path.exists(filepath):
            print(f'File {filepath} does not exist.  Gathering stock data now.')
            symbol_ticker = yf.Ticker(symbol)
            df_symbol = symbol_ticker.history(start=self.start_time, end=self.end_time)
            df_symbol.to_csv(filepath)

        # Read the data from the CSV file
        stock_data = pd.read_csv(filepath, index_col='Date', parse_dates=True)
        return stock_data

    @classmethod
    def exec(cls, stock_symbols_path: str, start_time: datetime, end_time: datetime):
        """
        Create a StockData object and fetch stock data for multiple symbols.

        Args:
            stock_symbols_path (str): Path to the CSV file containing stock symbols.
            start_time (datetime): The start time for collecting data.
            end_time (datetime): The end time for collecting data.

        Returns:
            bool: Always returns True (as in the original).
        """
        # # Read the stock symbols from the CSV file
        # with open(stock_symbols_path, 'r') as file:
        #     reader = csv.reader(file)
        #     stock_symbols = [row[0] for row in reader]

        stock_data_instance = cls(stock_symbols_path, start_time, end_time)
        for symbol in stock_data_instance.stock_symbols:
            df_stock_data = stock_data_instance._get_stock_data(symbol)
        
            # # Call the exec method of MeaningfulData with stock_data.
            # meaningful_data = MeaningfulData.exec(df_stock_data)

            # # Create a data pipeline.
            # success = MyPipeline.create(symbol, meaningful_data)

            # # Check if not successful.
            # if not success:
            #     print(f'Pipeline creation failed for {symbol}')

        return True

