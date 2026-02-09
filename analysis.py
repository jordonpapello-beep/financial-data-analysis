import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt # Used for creating the plots based on our data
import seaborn as sns # Used for creating the plots based on our data

# Separate paths to get raw and processed data:
price_data_path = "data/raw/prices.csv"
returns_data_path = "data/processed/returns.csv"

# Output file paths for the plots created in this file (folder creations):
# 1.)  price_trends directory:
price_trends_output_directory = Path("plots/price_trends")  # Create a Path object pointing to "plots/price_trends"
price_trends_output_directory.mkdir(exist_ok=True)  # Create the "plots" folders if they don't already exist

# 2.) rolling_volatility directory:
rolling_volatility_output_directory = Path("plots/rolling_volatility")
rolling_volatility_output_directory.mkdir(exist_ok=True)

# 3.) rolling_volatility directory:
correlation_heatmap_output_directory = Path("plots/correlation_heatmap")
correlation_heatmap_output_directory.mkdir(exist_ok=True)

# 4.) return_distribution directory:
return_distribution_output_directory = Path("plots/return_distribution")
return_distribution_output_directory.mkdir(exist_ok=True)

def plot_price_trends(prices):
    """
    Plot adjusted prices with short- and long-term moving averages
    to visualize trend behavior for each asset.
    """
    # Loop over until you create a plot for every column (i.e. ticker) in 'prices':
    for col in prices.columns:
        # Plot theme:
        sns.set_theme(style="darkgrid") # Adds the grey backdrop and the gridlines

        # 1.) Plot the main figure:
        plt.figure(figsize=(11, 7)) # Set the dimensions of the image containing the plot
        prices[col].plot(label="Price") # '.plot()' is the standard lineplot method for matplotlib

        # 2.) Plotting the moving average lines:
        prices[col].rolling(50).mean().plot(label="50-day MA")
        prices[col].rolling(200).mean().plot(label="200-day MA")

        # 3.) Plot important points:
        plt.scatter(prices[col].idxmax(),# searches col for max value and returns the corresponding label from the index
                    prices[col].max(),
                    s=75, c='green', marker='o', edgecolors='black',
                    label=f'High: ${prices[col].max().round(2)}') # Highest price in date range
        plt.scatter(prices[col].idxmin(),# searches col for min value and returns the corresponding label from the index
                    prices[col].min(),
                    s=75, c='red', marker='o', edgecolors='black',
                    label=f'Low: ${prices[col].min().round(2)}') # Lowest price in date range

        # For more detailed tick marks:
        # 1.) y-axis: (# tolist() here isn't necessary but helps with warning message between plt and np)
        step_val = (prices[col].max().round(-1) - prices[col].min().round(-1))/12 # 12 steps

        plt.yticks(np.arange(prices[col].min().round(-1),# Set min tick mark = min value in [col] rounded to nearest $10
                             prices[col].max().round(-1),# Set max tick mark = max value in [col] rounded to nearest $10
                             step=round(step_val, 0)).tolist())

        # 2.) x-axis:
        # Create a step every 3 months:
        ticks = pd.date_range(start=prices.index.min(),
                              end=prices.index.max(),
                              freq='3MS')
        plt.xticks(ticks,
                   ticks.strftime('%b %Y'))

        # Labels choices:
        plt.title(f"{col} Price Trend for the Past 5 Years",
                  fontsize=18,
                  fontweight='bold')
        plt.xlabel("Date",
                   fontsize=14,
                   fontweight='bold')
        plt.ylabel("Price ($)",
                   fontsize=14,
                   fontweight='bold')

        plt.legend()

        plt.tight_layout(rect=(0, .18, 1, 1)) # Trims the margins around the plot for cleaner look

        # Force the rotation on the active axis down here because tight_layout() overwrites it:
        plt.tick_params(axis='x',
                        rotation=65) # 65 degrees

        # Caption:   figtext(x, y)
        plt.figtext(0.02, 0.01,
                    f"The plot above shows the price history for the past 5 years of {col}, as well as the 50-Day and "
                    f"200-Day moving averages. The dates at which the short-term and long-term moving averages cross "
                    f"each other are known as either \"Breakouts\" or \"Breakdowns\". The main these crossings can "
                    f"tells us are the swings in momentum in the stocks price:\n"
                    f"• \"Golden Cross\" (Bullish / Buy Signal): When the 50-Day crosses over the 200-Day, short-term "
                    f"momentum is accelerating faster than the long-term average. This suggests that the stock is "
                    f"entering a sustained \"Uptrend\".\n"
                    f"• \"Death Cross\" (Bearish / Sell Signal): When the 50-Day crosses under the 200-Day, short-term "
                    f"prices are dropping sharply relative to the yearly average. This indicates that the stock’s "
                    f"upward momentum has collapsed.\n"
                    f"• Why do we use 50 and 200 day averages? A 200 day average (40 weeks) is considered a long enough"
                    f" time by banks and hedge funds to determine if a stock is \"healthy\". A 50 day average "
                    f"(10 weeks) is fast enough to react to new earnings reports but slow enough to filter out "
                    f"daily \"noise\".",
                    wrap=True, # Wrap the text back to beginning and below, so it doesn't go off the screen
                    horizontalalignment='left',
                    fontsize=10,
                    style='italic')

        # Saving the plots to their own output directory (a plot for each column):
        plt.savefig(f"{price_trends_output_directory}/{col}_price_trend.png",
                    dpi=300) # High resolution

        plt.close() # Exit the plot

def plot_rolling_volatility(returns):
    """
    Compare 30-day or 90-day rolling volatility across all assets on a single chart
    to highlight relative risk over time.
    """
    # Make a plot for each range of volatility:
    for x in ['30', '90']:
        # Plot theme:
        sns.set_theme(style="darkgrid")  # Adds the grey backdrop and the gridlines

        # Main plot:
        plt.figure(figsize=(10, 6)) # Set the dimensions of the image containing the plot

        # Loop over until you create a line for each ticker:
        for col in ["MSFT", "GLD", "SPY", "SCHD"]:
            returns[f"{col}_vol_{x}"].plot(label=col)

        # Labels choices:
        plt.title(f"{x}-Day Rolling Volatility vs Time",
                  fontsize=18,
                  fontweight='bold')
        plt.xlabel("Date",
                   fontsize=14,
                   fontweight='bold')
        plt.ylabel(f"{x}-Day Rolling Volatility",
                   fontsize=14,
                   fontweight='bold')
        plt.legend()

        # For more detailed tick marks:
        # Create a step every 3 months:
        ticks = pd.date_range(start=returns.index.min(),
                              end=returns.index.max(),
                              freq='3MS')
        plt.xticks(ticks,
                   ticks.strftime('%b %Y'))  # rotate the x-axis tick labels

        plt.figtext(0.01, 0.015,
                    f"Rolling volatility measures how much a stock's price 'swings' over a specific moving window of "
                    f"time (e.g., the last 30/90 days) rather than looking at the entire year at once. It can be "
                    f"thought of as a statistical measure of the dispersion of returns over specified time windows. "
                    f"Therefore, this chart tracks the 'intensity' of price swings over time. Peaks in the line "
                    f"indicate periods of high market uncertainty (risk), while troughs suggest stable, trending"
                    f" price action. By annualizing the standard deviation of log returns, we can compare short-term "
                    f"price turbulence to historical yearly averages.The 30-day 'Fast' volatility reacts "
                    f"quickly to sudden news events, while the 90-day 'Slow' volatility provides a smoother "
                    f"view of the long-term risk environment. Let's say we get an initial result of 0.15, this would "
                    f" mean the stock has a 15% annualized volatility based on that specific time window. An increase "
                    f"in value would mean the price of the stock is swining wildly (high risk), and a decrease in "
                    f"value would mean the price of the stock is moving steadily/ predictably (low risk).",
                    wrap=True,
                    horizontalalignment='left',
                    fontsize=9,
                    style='italic')
        plt.tight_layout(rect=(0, 0.14, 1, 1))  # Trims the margins around plot for cleaner look, add space for caption

        # Force the rotation on the active axis down here because tight_layout() overwrites it:
        plt.tick_params(axis='x',
                        rotation=45) # 45 degrees

        # Saving the plot to its own output directory:
        plt.savefig(f"{rolling_volatility_output_directory}/{x}_day_rolling_volatility.png",
                    dpi=300) # High resolution

        plt.close()

def plot_correlation_heatmap(returns):
    """
    Visualize correlations between daily returns to assess how closely
    assets move together.
    """
    # Main plot:
    corr = returns[["AAPL", "MSFT", "GOOGL", "AMZN", "GLD", "SPY", "SCHD"]].corr()

    plt.figure(figsize=(6, 6.5)) # Set the dimensions of the image containing the plot
    sns.heatmap(corr, annot=True,
                cmap="coolwarm") # Color range style

    # Labels choices:
    plt.title("Stock Return Correlation Heatmap",
              fontsize=18,
              fontweight='bold')
    plt.ylabel("Correlation (-1.0  to  1.0)",
               fontsize=14,
               fontweight='bold')
    plt.gca().yaxis.set_label_position("right") # Moves the text label to the right (cleaner for this plot)
    plt.tight_layout(rect=(0, .2, 1, 1)) # Trims the margins around the plot for cleaner look

    # Caption:
    plt.figtext(0.015, 0.01,
                f"Above is a correlation heatmap on which our stocks are compared to each other one to one. This plot "
                f"tells us how closely or not two stocks prices follow each other. This helps immensly when "
                f"diversifying a protfolio. Here's what specific ranges of correlation between two stocks signifies:\n"
                f"• Positive Correlation (above 0 to 1): The two stocks move in the same or similar direction, by the "
                f"same relative amount. \n"
                f"• No Correlation (0): A correlation of 0 or close to 0 indicates that the stocks have no "
                f"relationship. If one goes up, the other is just as likely to go up as it is down or stay flat.\n"
                f"• Negative Correlation(Under 0 to -1): The two stocks move in the opposite or close to opposite "
                f"direction, by the same relative amount.",
                wrap=True,
                horizontalalignment='left',
                fontsize=9,
                style='italic')

    # Saving the plot to its own output directory:
    plt.savefig(f"{correlation_heatmap_output_directory}/correlation_heatmap.png",
                dpi=300) # High resolution

    plt.close()

def plot_return_distribution(returns):
    """
    Plot the distribution of daily returns for a single asset to examine variability and tail behavior.
    """
    # Only want to make this plot for the ticker columns with log returns, not the rolling volatility of the returns:
    filtered_for_tickers = [t for t in returns.columns if "vol" not in t] # Only make a plot for columns w/o "vol"

    # Loop over until you create a histogram for each ticker:
    for col in filtered_for_tickers:
        # Main plot:
        plt.figure(figsize=(9, 6)) # Set the dimensions of the image containing the plot
        returns[col].dropna().hist(bins='auto', # matplotlib will determine how many bars are optimal for the histogram
                                   alpha=0.7)

        # Calculate the mean, 1std, and 95 percentile (VaR)
        mean_val = returns[col].mean() # expected return
        std_val = returns[col].std() # 68% of all data will fall within 1std of the mean
        var_95 = returns[col].quantile(0.05) # Value at Risk (VaR) the point where only 5% of days were worse.

        # Creates a line at x=0:
        plt.axvline(x=0,
                    color='black',
                    linestyle='--',
                    linewidth=1.5,
                    label='x = 0'
                    )
        # Creates a vertical line at the mean:
        plt.axvline(x=mean_val,
                    color='green',
                    linestyle='-',
                    linewidth=1.5,
                    label=f'Mean (Exp. Return) = {mean_val.round(4)}'
                    )
        # Creates a vertical line at +1std and -1std:
        plt.axvline(x=mean_val+std_val,
                    color='green',
                    linestyle='--',
                    linewidth=1.5,
                    label=f'+1 Standard Dev. = {(mean_val + std_val).round(4)}'
                    )
        plt.axvline(x=mean_val - std_val,
                    color='green',
                    linestyle='--',
                    linewidth=1.5,
                    label=f'-1 Standard Dev. = {(mean_val - std_val).round(4)}'
                    )
        # Creates a vertical line at Value at Risk:
        plt.axvline(x=var_95,
                    color='red',
                    linestyle='--',
                    linewidth=1.5,
                    label=f'Value at Risk = {var_95.round(5)}'
                    )

        # Labels choices:
        plt.title(f"{col}'s Daily Return Distribution for the Past 5 Years",
                  fontsize=18,
                  fontweight='bold')
        plt.xlabel("Daily Logarithmic Return",
                   fontsize=14,
                   fontweight='bold')
        plt.ylabel("Number of Occurrences",
                   fontsize=14,
                   fontweight='bold')
        plt.legend()

        # Caption:
        plt.figtext(0.03, 0.04,
                    f"This plot shows the distribution of daily logarithmic returns for {col} for the past 5 years. The"
                    f" height of a bar tells you the number of days {col} had a return of that value. The vertical "
                    f"lines can help us analyze the plot further: values to the left of x=0 were not profitable while "
                    f"values to the right of x=0 were profitable, the mean value line shows the avg. expected return "
                    f"per day, the two standard dev. lines show where 68% of the data falls and represents the normal "
                    f"swing range or volatility of {col}, and the red VaR line shows the point at which only 5% of "
                    f"days had a worse return. Ideal Plot Characteristics: \n• the mean to be to the right of x=0,"
                    f" which means the stock is consistently making money. \n• the shape of the curve is tall and "
                    f"skinny which indicates low variance and predictability. \n• the tail on the left side is thin "
                    f"indicating not many occurrences of heavy loss days, and the tail on the right is longer "
                    f"(positive skew).",
                    wrap=True,
                    horizontalalignment='left',
                    fontsize=9,
                    style='italic')
        plt.tight_layout(rect=(0, 0.16, 1, 1)) # Trims the margins around plot for cleaner look, add space for caption

        # Saving the plots to their own output directory (a plot for each column that we filtered):
        plt.savefig(f"{return_distribution_output_directory}/{col}_returns.png",
                    dpi=300) # High resolution

        plt.close()

def main():
    # Load datasets generated by previous pipeline stages:
    prices = pd.read_csv(price_data_path, index_col=0, parse_dates=True)
    returns = pd.read_csv(returns_data_path, index_col=0, parse_dates=True)

    # Generate all visual outputs:
    plot_price_trends(prices)
    plot_rolling_volatility(returns)
    plot_correlation_heatmap(returns)
    plot_return_distribution(returns)

    print("All plots generated.")

if __name__ == "__main__":
    main()
