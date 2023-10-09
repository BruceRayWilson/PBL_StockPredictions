from typing import List, Dict
import numpy as np

class StockData:
    """
    This is the StockData Class responsible for handling stock market data.
    """
    def __init__(self, ticker_symbol: str):
        """ 
        Initialize with the stock's ticker symbol.
        """
        self.ticker = ticker_symbol
    
    def get_data(self, start_date: str, end_date: str) -> Dict:
        """ 
        Method to retrieve stock data within a specified date range.  
        """
        pass

class Preprocessor:
    """
    This is the Preprocessor class responsible for preprocessing stock market data.
    """
    def __init__(self, data: Dict):
        """ 
        Initialize with the stock data. 
        """
        self.data = data
    
    def clean_data(self) -> Dict: 
        """ 
        Method to clean the raw stock data.
        """
        pass
    
    def split_data(self, test_size: float = 0.2) -> Dict: 
        """
        Method to split the data into a training set and a test set. 
        """
        pass

class LLM:
    """
    This is the LLM class which encapsulates the Linear Learning Model.
    """
    def __init__(self):
        """ 
        Initialize an empty model. 
        """
        self.model = None
    
    def train(self, x_train: np.ndarray, y_train: np.ndarray) -> None:
        """ 
        Method to train the LLM on the training data.
        """
        pass
    
    def predict(self, x_test: np.ndarray) -> np.ndarray:
        """ 
        Method to generate predictions on the test data.
        """
        pass

class StockPredictor:
    """
    This is the main class, StockPredictor, which uses the StockData, Preprocessor, and LLM classes to make predictions.
    """
    def __init__(self, ticker_symbol: str):
        """ 
        Initialize with the stock's ticker symbol.
        """
        self.ticker = ticker_symbol
        self.stock_data_class = StockData(self.ticker)
        self.preprocessor_class = Preprocessor({})
        self.LLM_class = LLM()
    
    def predict(self, start_date: str, end_date: str, test_size: float) -> np.ndarray:
        """ 
        Method to preprocess stock data and make predictions using the LLM.
        """
        pass
