import yfinance as yf
import csv
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
import pandas as pd
import shutil

MAX_WORKERS = 5  # Global constant for max number of threads

class StockSymbolCollection:

    def __init__(self, csv_filename: str):
        """
        Initializes the StockSymbolCollection with tickers from the given CSV file.

        Args:
        csv_filename (str): Path to the CSV file containing stock tickers.

        Attributes:
        tickers (List[str]): List of stock tickers.
        stock_data (Dict[str, Dict[str, float]]): Dictionary holding data about the stocks.
        """
        self.tickers = self._load_tickers_from_csv(csv_filename)
        self.stock_data = {}

    def _load_tickers_from_csv(self, csv_filename: str) -> List[str]:
        """
        Loads tickers from the given CSV file using pandas.

        Args:
        csv_filename (str): Path to the CSV file containing stock tickers.

        Returns:
        List[str]: List of stock tickers.
        """
        df = pd.read_csv(csv_filename)
        
        # Assuming the tickers are in the first column.
        tickers = df.iloc[:, 0].tolist()
        
        return tickers


    def _is_valid_ticker(self, ticker: str) -> bool:
        """
        Checks if a ticker is valid by fetching its historical data.

        Args:
        ticker (str): The stock ticker to validate.

        Returns:
        bool: True if valid, False otherwise.
        """
        stock = yf.Ticker(ticker)

        rc = not stock.history(period='1d').empty
        print(f'Ticker {ticker} is valid: {rc}')
        return rc

    def _fetch_beta_for_ticker(self, ticker: str) -> Dict[str, float]:
        """
        Fetches the beta value for a given ticker and prints the result.

        Args:
        ticker (str): The stock ticker.

        Returns:
        Dict[str, float]: A dictionary with ticker as key and its beta value.
        """
        stock = yf.Ticker(ticker)
        beta = stock.info.get("beta", None)
        
        # Print the fetched beta value for the ticker
        print(f"Fetched {ticker}: Beta = {beta}")
        
        return {ticker: {"Beta": beta}}

    def validate_tickers(self) -> None:
        """
        Validates stock tickers and saves valid and invalid tickers to separate CSV files.
        Invalid tickers are then copied to 'train.csv'.
        Uses 10 threads for concurrent validation.
        """
        valid_tickers = []
        invalid_tickers = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            results = list(executor.map(self._is_valid_ticker, self.tickers))
        
        for ticker, is_valid in zip(self.tickers, results):
            if is_valid:
                valid_tickers.append(ticker)
            else:
                invalid_tickers.append(ticker)
        
        self._save_to_csv('valid_tickers.csv', valid_tickers)
        self._save_to_csv('invalid_tickers.csv', invalid_tickers)

        # Copy the contents of 'valid_tickers.csv' to 'train.csv'
        shutil.copy('valid_tickers.csv', 'train.csv')

        # Reinitialize self.tickers with the contents of 'train.csv'
        self.tickers = self._load_tickers_from_csv('valid_tickers.csv')


    def _save_to_csv(self, filename: str, tickers: List[str]) -> None:
        """
        Saves a list of tickers to a CSV file.

        Args:
        filename (str): The name of the CSV file.
        tickers (List[str]): The list of stock tickers.
        """
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for ticker in tickers:
                writer.writerow([ticker])

    def fetch_beta_values(self) -> None:
        """
        Fetches beta values for each stock ticker and updates stock_data dictionary.
        Uses MAX_WORKERS threads for concurrent fetching.
        """
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            results = list(executor.map(self._fetch_beta_for_ticker, self.tickers))
        
        # Update the stock_data with fetched beta values.
        for data in results:
            self.stock_data.update(data)


    def display_beta_values(self) -> None:
        """
        Displays beta values for each stock ticker. If Beta is None, it's set to 0.
        The results are sorted by Beta in descending order and saved to a CSV file.
        """
        # Sort the stock_data based on Beta values (set to 0 if None) in descending order
        sorted_stock_data = dict(sorted(self.stock_data.items(), 
                                        key=lambda item: item[1]['Beta'] if item[1]['Beta'] is not None else 0, 
                                        reverse=True))

        # Update Beta values in the sorted dictionary to 0 if they are None
        for ticker, data in sorted_stock_data.items():
            if data['Beta'] is None:
                data['Beta'] = 0

        # Print the sorted data
        for ticker, data in sorted_stock_data.items():
            print(f"{ticker}: Beta = {data['Beta']}")

        # Save the sorted data to a CSV file
        with open('sorted_beta_values.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Ticker", "Beta"])  # header row
            for ticker, data in sorted_stock_data.items():
                writer.writerow([ticker, data['Beta']])

    @classmethod
    def exec(cls, csv_filename: str) -> None:
        """
        Validates tickers, fetches their beta values, and displays the results.

        Args:
        csv_filename (str): Path to the CSV file containing stock tickers.
        """
        collection_instance = cls(csv_filename)
        collection_instance.validate_tickers()
        collection_instance.fetch_beta_values()
        collection_instance.display_beta_values()

if __name__ == "__main__":
    # Specify the path to your CSV file.
    csv_filename = 'train_base.csv'
    StockSymbolCollection.exec(csv_filename)