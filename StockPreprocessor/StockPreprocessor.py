import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class StockPreprocessor:
    def __init__(self):
        self.input_directory = 'data'
        self.output_directory = 'preprocessed_data'
        self.chunk_size = 42

    def create_output_directory(self):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def load_csv_files(self):
        files = [f for f in os.listdir(self.input_directory) if f.endswith('.csv')]
        return files

    def preprocess_file(self, file):
        # Read CSV file
        df = pd.read_csv(os.path.join(self.input_directory, file))

        # Keep only the necessary fields
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

        # Divide data into chunks of the specified size in reverse order
        chunks = [df[i:i + self.chunk_size] for i in range(df.shape[0] - self.chunk_size, -1, -self.chunk_size)]

        # Initialize an empty DataFrame to store the concatenated chunks
        result_df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

        for chunk in chunks:
            # Normalize 'Open', 'High', 'Low', 'Close' as a group
            ohlc_data = chunk[['Open', 'High', 'Low', 'Close']]
            volume_data = chunk[['Volume']]

            ohlc_scaler = MinMaxScaler()
            volume_scaler = MinMaxScaler()

            chunk.loc[:, ['Open', 'High', 'Low', 'Close']] = ohlc_scaler.fit_transform(ohlc_data)
            chunk.loc[:, ['Volume']] = volume_scaler.fit_transform(volume_data)

            # Append the chunk to the result DataFrame
            result_df = pd.concat([result_df, chunk])

        # Sort the result DataFrame by 'Date'
        result_df.sort_values(by=['Date'], inplace=True)

        # Save the preprocessed data to a new CSV file
        result_df.to_csv(os.path.join(self.output_directory, file), index=False)

    def preprocess_data(self):
        print("Preprocessing data...")
        self.create_output_directory()
        files = self.load_csv_files()

        for file in files:
            self.preprocess_file(file)

        print("Preprocessing completed.")

    @classmethod
    def exec(cls):
        stock_preprocessor = cls()
        stock_preprocessor.preprocess_data()

if __name__ == "__main__":
    StockPreprocessor.exec()
