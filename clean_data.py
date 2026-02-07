import pandas as pd # For DataFrame manipulation and conversion to and from CSV files
import numpy as np # For arithmatic
from pathlib import Path

# Input from ingestion step:
input_path = "data/raw/prices.csv" # We created this path in 'fetch_data.py'

# Output file path for return data from this file:
output_directory = Path("data/processed")  # Create a Path object pointing to folders named 'data/processed'
output_directory.mkdir(exist_ok=True)  # Create the 'data/processed' folders if they don't already exist

def load_price_data(path):
    """
    Load price data with dates parsed and set as the DataFrame index, enabling time-series operations.
    Can be thought of as a simple 'get' method.
    """
    return pd.read_csv(path, index_col=0, parse_dates=True)

def compute_log_returns(prices):
    """
    Compute log returns, which are additive over time and commonly used in financial analysis.
    A Logarithmic Return measures the rate of change in a stock's price using the natural logarithm.
    It can be thought of as the 'Continuously Compounded' return of an investment.

    How them method works:

    1.) prices / prices.shift(1): This calculates the Price Ratio. It divides today's price by
                                  yesterday's price (e.g., $105/$100 = $1.05 ).
    2.) np.log(...):              This takes the Natural Log (ln) of that ratio.
                                  Therefore, if the price went up by 5% (Simple Return), the
                                  Log Return would be roughly 0.0488 (4.88%).

    Why use Log Returns instead of Simple Returns?

    While 'Simple Returns' (e.g., +5%) are easier for us to read, 'Log Returns' are the standard for
    Financial Data Science for three main reasons:
        1.) Time Additivity: You can simply sum log returns to find the total return over a period.
                             Simple returns must be multiplied (which is math-heavy) To calculate the
                             total return using simple returns, you have to account for compounding:

                             Return_Total = [ (1 + r_1) • ( 1+ r_2) • ... • (1 + r_n) ] - 1)

        2.) Symmetry:        A 10% gain followed by a 10% loss doesn't bring a simple return back to zero,
                             but with log returns, (+0.10) and (-0.10) cancel out perfectly.

        3.) Normalization:   Log returns follow a Normal Distribution more closely than simple prices, which
                             makes them better for Machine Learning and Statistical Models.
    """
    return np.log(prices / prices.shift(1))

def compute_rolling_volatility(returns, window):
    """
    This method computes annualized rolling volatility using a specified window.
    The sqrt(252) factor annualizes daily standard deviation.
    Rolling volatility measures how much a stock's price 'swings' over a specific moving window of
    time (e.g., the last 30 days) rather than looking at the entire year at once.
    Can be thought of as a statistical measure of the dispersion of returns over specified time windows.

    How the method works:

    1.) .rolling(window=window): This creates a 'sliding window'. If your window is 30, it looks at days 1–30,
                                 then 2–31, then 3–32, and so on.

    2.) .std():                  This calculates the Standard Deviation of the log returns within that window.
                                 This is the 'raw volatility' (how much the daily returns vary from their average).

    3.) * np.sqrt(252):          This Annualizes the number. Since there are roughly 252 trading days in a year,
                                 multiplying by the square root of time converts a 'daily' risk number into
                                 a 'yearly' risk percentage.

    Why use a 'Rolling' calculation?

    1.) Identify Trends: Volatility isn't constant. A stock might be calm in January but wild in July.
                         A rolling calculation shows you when the risk increased.

    2.) Risk Management: You can use this to see if a stock is becoming 'too hot' or risky compared to its
                         historical average.

    3.) Comparison:      It allows you to see if two stocks (like AAPL and MSFT) are becoming more or less
                         correlated in their risk levels over time.

    Example: Let's say we get an initial result of 0.15.
    Meaning: This means the stock has a 15% annualized volatility based on that specific time window.
    Increase in Value: The price is swinging wildly (high risk).
    Decrease in Value: The price is moving steadily and predictably (low risk).
    """
    return returns.rolling(window=window).std() * np.sqrt(252)

def main():
    # Load raw price data that we created in our 'fetch_data.py' script:
    prices = load_price_data(input_path)

    # Core table/DataFrame transformations:
    returns = compute_log_returns(prices) # Table of daily % rates of change in the stocks' price using natural logs
    vol_30 = compute_rolling_volatility(returns, 30) # Table of % swing in a stocks price over the last 30 days
    vol_90 = compute_rolling_volatility(returns, 90) # Table of % swing in a stocks price over the last 90 days

    # Combine returns and volatility metrics into a single dataset:
    output = returns.copy() # It's good practice to save a copy of a generated DataFrame before manipulating it further
    for col in returns.columns: # Loop over columns in 'returns' DataFrame
        # The following lines create a new column in 'output' DataFrame for each ticker, and fill it with the
        # 30/90-day volatility values for that specific ticker (i.e. we'll get a 30 and 90-day column for each stock):
        output[f"{col}_vol_30"] = vol_30[col]
        output[f"{col}_vol_90"] = vol_90[col]

    # Save processed data for reuse without recomputation:
    returns_csv_path = output_directory / "returns.csv"  # Build the full path: data/processed/returns.csv
    output.to_csv(returns_csv_path,
                  index=True)  # This creates 'returns.csv' in the 'returns_csv_path' dir. True = row indexing (dates)

    print(f"Processed returns and volatility saved to {returns_csv_path}")

if __name__ == "__main__":
    main()
