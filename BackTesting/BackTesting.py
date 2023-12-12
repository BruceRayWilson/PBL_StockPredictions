import os
import pandas as pd
from tkinter import filedialog, Tk

class BackTesting:
    # Class to check stock market prediction results.

    @staticmethod
    def exec() -> None:
        '''Call the other methods to check the stock data prediction results.'''
        prediction_file = BackTesting.choose_file()
        prediction_df = BackTesting.read_file(prediction_file)
        sorted_df = BackTesting.sort_by_symbol(prediction_df)
        BackTesting.save_symbols(sorted_df)
        test_data_dir = BackTesting.choose_directory()
        combined_df = BackTesting.combine_data(sorted_df, test_data_dir)
        BackTesting.save_combined_data(combined_df)
        BackTesting.calculate_accuracy(combined_df)

    @staticmethod
    def choose_file() -> str:
        '''Allow the user to choose a file starting with 'predictions_output'.'''
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                               title="Select file",
                                               filetypes=(("CSV files", "predictions_output*.csv"),))
        root.destroy()
        return file_path

    @staticmethod
    def read_file(file_path: str) -> pd.DataFrame:
        '''Read the file into a pandas dataframe.'''
        return pd.read_csv(file_path)

    @staticmethod
    def sort_by_symbol(df: pd.DataFrame) -> pd.DataFrame:
        '''Sort the dataframe by 'Symbol'.'''
        return df.sort_values(by='Symbol')

    @staticmethod
    def save_symbols(df: pd.DataFrame) -> None:
        '''Save the 'Symbol' column to a CSV file.'''
        df[['Symbol']].to_csv('predicted_symbols_back_testing.csv', index=False)

    @staticmethod
    def choose_directory() -> str:
        '''Allow the user to choose a directory starting with 'test_data_'.'''
        root = Tk()
        root.withdraw()
        directory_path = filedialog.askdirectory(initialdir=os.getcwd(),
                                                 title="Select directory")
        root.destroy()
        return directory_path

    @staticmethod
    def combine_data(prediction_df: pd.DataFrame, test_data_dir: str) -> pd.DataFrame:
        '''Combine data from the prediction and test data files.'''
        combined_data = pd.DataFrame()
        for symbol in prediction_df['Symbol']:
            file_path = os.path.join(test_data_dir, f"{symbol}.csv")
            if os.path.exists(file_path):
                test_data_df = pd.read_csv(file_path)
                merged_df = prediction_df[prediction_df['Symbol'] == symbol].merge(test_data_df, on='Date')
                merged_df['Gain'] = merged_df['Gain'].astype(int)
                combined_data = pd.concat([combined_data, merged_df[['Date', 'Symbol', 'Date', 'Gain', 'PredictedClass']]])
        return combined_data

    @staticmethod
    def save_combined_data(df: pd.DataFrame) -> None:
        '''Save the combined dataframe to a CSV file.'''
        df.to_csv('combined_back_testing_results.csv', index=False)

    @staticmethod
    def calculate_accuracy(df: pd.DataFrame) -> None:
        '''Calculate and print the accuracy of the predictions.'''
        accuracy = (df['PredictedClass'] == df['Gain']).mean() * 100
        print(f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    BackTesting.exec()