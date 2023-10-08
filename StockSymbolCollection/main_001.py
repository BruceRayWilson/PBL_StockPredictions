import yfinance as yf
import csv

class StockSymbolCollection:
    def __init__(self, csv_filename):
        self.tickers = self._load_tickers_from_csv(csv_filename)
        self.stock_data = {}

    def _load_tickers_from_csv(self, csv_filename):
        tickers = []
        with open(csv_filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                tickers.append(row[0])
        return tickers

    def validate_tickers(self):
        valid_tickers = []
        invalid_tickers = []
        
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            if not stock.history(period='1d').empty:
                valid_tickers.append(ticker)
            else:
                invalid_tickers.append(ticker)
                
        self.tickers = valid_tickers  # Update tickers list to contain only valid tickers
        
        # Save valid tickers to valid_tickers.csv
        with open('valid_tickers.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for ticker in valid_tickers:
                writer.writerow([ticker])
        
        # Save invalid tickers to invalid_tickers.csv
        with open('invalid_tickers.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for ticker in invalid_tickers:
                writer.writerow([ticker])
                
        print(f"Saved {len(valid_tickers)} valid tickers to valid_tickers.csv")
        print(f"Saved {len(invalid_tickers)} invalid tickers to invalid_tickers.csv")

    def fetch_beta_values(self):
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            beta = stock.info.get("beta", None)
            self.stock_data[ticker] = {
                "Beta": beta
            }

    def display_beta_values(self):
        for ticker, data in self.stock_data.items():
            print(f"{ticker}: Beta = {data['Beta']}")

if __name__ == "__main__":
    # Specify the path to your CSV file
    csv_filename = 'rf_train.csv'

    collection = StockSymbolCollection(csv_filename)
    collection.validate_tickers()
    collection.fetch_beta_values()
    collection.display_beta_values()
