import yfinance as yf # Where we will be scraping the data from
from datetime import datetime, timedelta # For the rolling time window
from pathlib import Path # Import Path for working with file paths in a cross-platform way

# List of assets to analyze; kept centralized for easy modification:
ticker_list = ["AAPL", "MSFT", "GOOGL", "AMZN", "GLD", "SPY"]

# Define a rolling 5-year window ending at today's date:
end_date = datetime.today()
start_date = end_date - timedelta(days=5 * 365) # past five years

# Output file path for return data from this file:
output_directory = Path("data/raw")  # Create a Path object pointing to folders named "data/raw" (relative path)
output_directory.mkdir(exist_ok=True)  # Create the "data/raw" folders if they don't already exist

def fetch_price_data(tickers, start, end):
    """
    Download adjusted close price data for the given tickers and date range.
    The Close price is used (adjusted on yFinances' end for any splits/dividends) for daily price data
    This method takes in one or many (in the form of a list) tickers, a start, and an end date, and outputs close data
    Returns a time-series (index) which can be plotted on the x-axis, and price data which can be plotted as y-axis
    """
    data = yf.download(
        tickers,
        start=start,
        end=end,
        progress=False # disable the visual progress bar in the console when downloading
    )["Close"] # Only fetch the data in the 'Close' column
    return data.round(2) # If this line wasn't added, the returned data would contain too much decimal place precision

def main():
    # Fetch raw price data using our defined method:
    prices = fetch_price_data(ticker_list, start_date, end_date)

    # Save processed data for reuse without recomputation:
    prices_csv_path = output_directory / "prices.csv"  # Build the full path: 'data/raw/prices.csv'
    prices.to_csv(prices_csv_path,
                  index=True)  # This creates 'prices.csv' in the 'prices_csv_path' dir. True = row indexing (dates)

    print(f"Raw price data saved to {prices_csv_path}")

# Allows the script to be run standalone or imported without side effects:
if __name__ == "__main__":
    main()