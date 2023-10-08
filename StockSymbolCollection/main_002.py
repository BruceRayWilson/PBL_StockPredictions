import yfinance as yf
import csv
import requests
from bs4 import BeautifulSoup

class StockSymbolCollection:
    """
    A collection of stock symbols with utilities to fetch their data and details.

    Attributes:
        tickers (List[str]): A list of stock ticker symbols.
        stock_data (Dict[str, Dict[str, Any]]): A dictionary holding stock data, indexed by ticker symbol.
    """

    def __init__(self, csv_filename: str = None):
        """
        Initializes the StockSymbolCollection with tickers from a CSV file or an empty list.

        Args:
            csv_filename (str, optional): Path to a CSV file containing stock tickers. Defaults to None.
        """
        if csv_filename:
            self.tickers = self._load_tickers_from_csv(csv_filename)
        else:
            self.tickers = []
        self.stock_data = {}

    def _load_tickers_from_csv(self, csv_filename: str) -> list:
        """
        Loads ticker symbols from a CSV file.

        Args:
            csv_filename (str): Path to the CSV file.

        Returns:
            list: A list of ticker symbols.
        """
        tickers = []
        with open(csv_filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                tickers.append(row[0])
        return tickers

    def fetch_nasdaq_100_tickers(self) -> None:
        """
        Fetches NASDAQ-100 tickers from Wikipedia and updates the tickers attribute.

        Returns:
            None
        """
        URL = "https://en.wikipedia.org/wiki/NASDAQ-100"
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []

        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[1].text.strip()
            tickers.append(ticker)

        self.tickers = tickers

    def fetch_beta_values(self) -> None:
        """
        Fetches the beta values for the tickers in the tickers attribute and stores them in the stock_data attribute.

        Returns:
            None
        """
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            beta = stock.info.get("beta", None)
            self.stock_data[ticker] = {
                "Beta": beta
            }

    def display_beta_values(self) -> None:
        """
        Displays the beta values of the stocks in the stock_data attribute.

        Returns:
            None
        """
        for ticker, data in self.stock_data.items():
            print(f"{ticker}: Beta = {data['Beta']}")



if __name__ == "__main__":
    # Using CSV:
    # csv_filename = 'path_to_your_file.csv'
    # collection = StockSymbolCollection(csv_filename)

    # Using NASDAQ-100 scraping:
    collection = StockSymbolCollection()
    collection.fetch_nasdaq_100_tickers()

    collection.fetch_beta_values()
    collection.display_beta_values()