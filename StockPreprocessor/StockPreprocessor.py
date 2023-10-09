import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class StockPreprocessor:
    # Class to preprocess collected stock market data

    @staticmethod
    def exec() -> None:
        '''The method ...'''
        print("Preprocessing data...")

        # Create 'preprocessed_data' directory if it does not exist
        if not os.path.exists('preprocessed_data'):
            os.makedirs('preprocessed_data')

        # Get list of CSV files in 'data' directory
        files = [f for f in os.listdir('data') if f.endswith('.csv')]

        for file in files:
            # Read CSV file
            df = pd.read_csv(os.path.join('data', file))

            # Keep only the necessary fields
            df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

            # Divide data into 42-day chunks
            chunks = [df[i:i+42] for i in range(0, df.shape[0], 42)]

            for chunk in chunks:
                # Normalize the fields Open, High, Low, Close, and Volume
                scaler = MinMaxScaler()
                chunk.loc[:, ['Open', 'High', 'Low', 'Close', 'Volume']] = scaler.fit_transform(chunk[['Open', 'High', 'Low', 'Close', 'Volume']])

                # Save the preprocessed chunk to a new CSV file
                chunk.to_csv(os.path.join('preprocessed_data', file), index=False)

        print("Preprocessing completed.")
