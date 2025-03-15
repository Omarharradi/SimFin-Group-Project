import pandas as pd
import logging
import os

# Ensure required directories exist
log_dir = "./logging"
output_dir = "./output"
os.makedirs(log_dir, exist_ok=True)  # Creates logging directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)  # Creates output directory if it doesn't exist

# Configure logging
log_file = os.path.join(log_dir, "etl.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def process_stock_data():
    logging.info("Starting stock data processing.")

    try:
        # Stock data downloaded:
        logging.info("Loading stock data from ZIP file.")
        prices_df = pd.read_csv("../data/us-shareprices-daily.zip", delimiter=";")
        logging.info(f"Stock data loaded successfully with {prices_df.shape[0]} rows and {prices_df.shape[1]} columns.")

        # Filter tickers
        selected_tickers = ["AAPL", "MSFT", "BRO", "FAST", "ODFL"]
        logging.info(f"Filtering data for tickers: {selected_tickers}.")
        tickers_df = prices_df[prices_df["Ticker"].isin(selected_tickers)]
        logging.info(f"Filtered data contains {tickers_df.shape[0]} rows.")

        tickers_df.drop(columns=['Dividend', 'SimFinId'], inplace=True)
        logging.info("Dropped unnecessary columns: Dividend, SimFinId.")

        tickers_df = tickers_df.sort_values(by=["Ticker", "Date"])
        logging.info("Sorted data by Ticker and Date.")

        # Remove last 30 rows per Ticker
        logging.info("Removing last 30 rows per Ticker.")
        df_cleaned = tickers_df.groupby('Ticker').apply(lambda x: x.iloc[:-30]).reset_index(drop=True)
        logging.info(f"Cleaned data contains {df_cleaned.shape[0]} rows after removing last 30 rows per ticker.")

        # Pivot table
        logging.info("Creating pivot table.")
        pivoted_df = df_cleaned.pivot(index="Date", columns="Ticker", values=["Open", "High", "Low", "Close", "Adj. Close", "Volume"])
        logging.info(f"Pivot table created with {pivoted_df.shape[0]} rows and {pivoted_df.shape[1]} columns.")

        # Flatten column names
        pivoted_df.columns = [f"{col[0]}_{col[1]}" for col in pivoted_df.columns]
        pivoted_df.reset_index(inplace=True)
        logging.info("Flattened column names in pivot table.")

        # Merge pivoted data with original data
        logging.info("Merging pivoted data with original data.")
        merged_df = df_cleaned.merge(pivoted_df, on="Date", how="left")
        logging.info(f"Merged data contains {merged_df.shape[0]} rows and {merged_df.shape[1]} columns.")

        # Drop unnecessary columns
        cols_to_drop = ["Open", "High", "Low", "Close", "Adj. Close", "Volume"]
        merged_df.drop(columns=cols_to_drop, inplace=True)
        logging.info(f"Dropped columns: {cols_to_drop}.")

        # Initialize shifted close column
        merged_df['Close_Ticker_Shifted'] = None
        logging.info("Initialized Close_Ticker_Shifted column.")

        # Process each ticker separately
        for ticker in merged_df['Ticker'].unique():
            close_col = f"Close_{ticker}"
            if close_col in merged_df.columns:
                logging.info(f"Processing ticker {ticker}.")
                shifted_values = merged_df.loc[merged_df['Ticker'] == ticker, close_col].shift(-1)

                # Assign to new column
                merged_df.loc[merged_df['Ticker'] == ticker, 'Close_Ticker_Shifted'] = shifted_values
                merged_df.loc[merged_df['Ticker'] == ticker, 'Target'] = (
                    merged_df.loc[merged_df['Ticker'] == ticker, 'Close_Ticker_Shifted'] >
                    merged_df.loc[merged_df['Ticker'] == ticker, close_col]
                ).astype(int)
                logging.info(f"Computed Target column for ticker {ticker}.")

        # Convert shifted close prices to numeric type
        merged_df['Close_Ticker_Shifted'] = pd.to_numeric(merged_df['Close_Ticker_Shifted'])
        logging.info("Converted Close_Ticker_Shifted column to numeric type.")

        logging.info("Stock data processing completed successfully.")
        return merged_df

    except Exception as e:
        logging.error(f"Error during stock data processing: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        logging.info("Script execution started.")
        final_df = process_stock_data()
        
        # Save processed data in ./output/
        output_file = os.path.join(output_dir, "processed_stock_data.csv")
        final_df.to_csv(output_file, index=False)
        logging.info(f"Processed stock data saved successfully at {output_file}.")

    except Exception as e:
        logging.critical("Script execution failed.", exc_info=True)
    
    print(f"Processed stock data saved successfully at {output_file}.")
