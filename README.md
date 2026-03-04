# financial-data-analysis
OVERVIEW: 
---
This project is a modular Python-based data pipeline designed to automate the retrieval, processing, and visualization of stock market risk metrics. By transitioning from raw price data to advanced statistical measures, like **Logarithmic Returns** and **Rolling Volatility**, this tool provides a clear view of market trends, fluxuations, and asset correlations. This was accomplished through the use of Python with YFinance, Pandas, Matplotlib, and Seaborn. The project is built for investors and analysts who need to identify **volatility clustering**, **risk-adjusted returns**, and **portfolio diversification opportunities** across multiple tickers simultaneously.

---------------------------------------------------------------------------------------------------------------
PROJECT ORDER:
---
Here's the order this project's folders should be ran and viewed in:
- python files / fetch_data.py
  - data / raw / prices.csv (to view scraped data)
- python files / clean_data.py
  - data / processed / returns.csv (to view transformed data)
- python files / analysis.py
- plots / 
  - price_trends
  - rolling_volatility
  - correlation_heatmap
  - return_distribution

IN DEPTH DESCRIPTION:
---
Below is a description of each file, its purpose, and how it works. For a more specific description of individual lines of code, please view the Python files themselves. The files are **heavily commented** to help aid in the understanding of the code.

**1.) fetch_data.py:**

This file is where the **data collection** happens. First we define the list of tickers that we want data on, and a rolling time window for the data that we want to collect(five years is used here). Since we define the time window to have an 'end_date' of today, we can always be sure that when this file is ran, it will collect data from five years ago up until the current day. Next we create a Path object from pathlib to make the dircetory/relative file path where we want our data to be stored.

  • The significance of using **pathlib** is that it makes the code **cross-platfrom compatible**. Whether this code is ran on Mac, Windows, or Linux, pathlib will automatically detect the user's operating system and flip the slashes in a file path's name for you. Furthermore, pathlib allows you to check if a folder exists before trying to save any data/plots to it, preventing any **"File Not Found" errors**. 

Now we define our **fetching function** which will scrape the financial data from the Yahoo Finance website, and write it to a **Pandas DataFrame**. More specifically, we use the **download() function** from the yfinance library to collect the daily market close data for all of the tickers in our ticker list during our five year time window (close data is rounded to nearest cent). 

• It's optimal to use the download() function here beacuse this function is best tailored to collect time-series data for multiple tickers. Out of the three yfinance scraping functions we could have used (download(), get_info(), fast_info), this is the only one that returns a Pandas DataFrame. Furthermore, Yahoo stores historical prices in a completely different system than fundamental data which get_info() accesses. download() hits this historical system directly and efficiently.

Now that **fetch_price_data()** is defined, we can run it in main() by assigning it to a variable which  will store the returned DataFrame from the function. Finally, we save this raw price data to the directory that was set up in the beginning so that we can access it from our other Python scripts without having to re-download/re-fetch the data from Yahoo Finance. We call this CSV file 'prices.csv'. 

**Fetching Financial Data Complete**


**2.) clean_data.py:**

This file is where the **data transformations** happen. More specifically, where we will take the data from 'prices.csv' and manipulate/add to it to form a new DataFrame. This new 'returns' DataFrame transforms the daily price data in 'prices' into daily % rates of change in the stocks' prices using natural logs(called log returns). Also, we will add columns which calculate the rolling volatility for the past 30 and 90 days for each stock(% swing in stocks price over time range).

So to start, we assign a variable to the name of our relative file path for 'prices.csv' so we can load it in later, and we also create a Path object to make the dircetory/relative file path where we want 'returns' to be stored in once we  create it. Now we need to define three funtions: **'load_price_data()'** which will read the 'prices' CSV file so we can manipulate it, **'compute_log_returns()'**, and **'compute_rolling_volatility()'**. 

• For more information on what both **daily log returns** and **rolling volatility** are and how they're calculated, refer to their functions in'clean_data.py'. Their significance are explained in depth in the comments.

• Furthermore, we technically don't need to add **'load_price_data()'** to read the csv, but I believe it's cleaner to use it than to have **pd.read_csv(path, index_col=0, parse_dates=True)** in main.

Now we move into main() where we begin to transform the 'prcies' data by first loading in the data using our 'load_price_data()' function. Furthermore, we drop any rows in 'prices.csv' that have rows with NA values in them. This helps when comparing assets in the table that don't trade on the nonstandard 252 day market. Now that we have access to that DataFrame we set 'returns' equal to 'compute_log_returns(prices)', which performs the log return calculation on the entire 'prices' DataFrame. Similarly, we calculate the rolling volatility for 30 and 90 days for each column of our new 'returns' DataFrame and assign these indiviadual DataFrames to 'vol_30' and 'vol_90' respectively. All of the new data has been calculated, so the final steps are to combine the retruns and volatility data into one DataFrame, and save it like we did with 'prices.csv' in 'fetch_data.py'. We can add the volatitily data easily by looping over the columns in 'returns' and adding the 30 and 90 day column data for each ticker in 'returns'. Now that we have one DataFrame with all of our transformed data, we can save it to the dircetory that we set up at the beginning of the script. We call this relative file path 'returns.csv'.

**Note:** There wasn't any real 'data cleaning' as the fetched data was already in optimal form for the DataFrame transformations. But if the data needed to be cleaned(which it usually needs to be), it would've happended in this file which is why it is called 'clean_data.py'.

**Transforming Financial Data Complete**


**3.) analysis.py:**

This file is where the **data plotting** happens. This script uses **pyplot** from **matplotlib** and **seaborn** in conjuction with each other to create the plots for this project. We begin by assigning the names of 'prices.csv' and 'returns.csv' realtive file paths to variables, creating directories for our plots, and by creating our loading function as we did in 'clean_data.py' so we can use our DataFrames in this script. Once these steps are done, all thats left to do is create a fucntion for each type of plot we want, and to run them in main().

The plots we made for this project include the following: **price trends plots** which plots the daily price history of a stock over the past five years along with its 50/200 day moving averages, **rolling volatilty plots** which plots the intensity of price swings for multiple stocks over either 30/90 day periods, **correlation heatmap** which tells you how closely or not stocks' prices follow eachother(if they're correlated), and **return distribution plots** which show the distribution curves of daily logarithmic returns for individual stocks over the past five years. 

A lot of the code in the functions for the plots described above is just to make them more appealing to look at. It is important I believe to note that the same plots can be coded with less lines of code (although they wouldn't be a visually pleasing, and therefore would be harder to read). 

• **Note:** More detailed descriptions and examples for what the individual plots signify can be found on the plots themselves in their captions in the **plots** folder. 

**Plotting Financial Data Complete**


Conclusions from Visualizations:
---
After creating the plots and viewing them, many conclusions can be drawn that would be cumbersome or near impossible to draw from looking at the raw financial data in table form. Here are the observations and conclusions that I have drawn from the plots created in this project:

**PLOTS LAST UPDATED: (Mar. 3rd 2026)**


**1.) Price Trends and Moving Averages (50/200 Day) Plots:**

**Stocks Analyzed:** AAPL, NVDA, TSLA

These plots visualize the relationship between the current price and its long-term institutional averages. The 50-day Moving Average (MA) represents intermediate momentum, while the 200-day MA represents the long-term trend "floor". For these plots 3 of the magnificent 7 tech stocks were plotted: Apple, Nvidia, Telsa.

**a.) AAPL:** The "Stair-Stepper":

  **Observation:** Notice how often the price dips to touch the 50-day MA and then bounces back up. During larger market corrections, it may drop to the 200-day MA. 
  
  **Conclusion:** This is an example of **Support and Resistance**. AAPL shows how moving averages act as a **"psychological floor"** for investors. This plot clearly identifies these **"buy-the-dip"** opportunities where the price respects its historical mean.

**b.) NVDA:** The Momentum Powerhouse:

  **Observation:** Look for the **"Golden Cross"** (where the 50-day crosses above the 200-day). In the last 5 years, NVDA has spent significant time with a massive "spread" between the price and the 200-day MA.

  **Conclusion:** This plot showcases **strong upward momentum**. When the price stays consistently above both MA lines, it indicates a "parabolic" trend where buyers are aggressive. This plot demonstrates how the script identifies assets that are significantly "extended" from their historical average.

**c.) TSLA:** The Volatility Case Study:

  **Observation:** Unlike AAPL, TSLA often crashes through its moving averages with high velocity. You may see a **"Death Cross"** (50-day crossing below the 200-day) during its heavier correction periods.

  **Conclusion:** This plot illustrates **Trend Reversals**. It shows that for high-beta (volatile) stocks, moving averages can be **"lagging indicators**." If the price is zigzagging through the averages frequently, it signals a period of **high uncertainty** or a **"sideways" market** rather than a clear trend.

---------------------


**2.) Rolling Volatilty Plots:**

**Assets Analyzed:** VTI, TSLA, BTC-USD, PG

The plots in this section visualize risk over time, a risk-spectrum. Instead of looking at a single average for the whole 5 years, rolling volatility shows how "jumpy" an asset was during specific time periods in the market. I used different classes of assets: VTI (Market Average), TSLA (Aggressive Growth), PG (Conservative), and BTC-USD (Speculative/Crypto). This variety of assets was used to show how the script distinguishes between different risk profiles. Here's some more detailed information about the selection of these asstes for these plots:

  • **VTI (Total Stock Market)**: Acts as the baseline. It should sit above PG but significantly below the "growth" assets. It represents the "systemic risk" of the entire market.
  
  • **PG (Procter & Gamble)**: Should consistently sit at the bottom of the plot. This would confirm its status as a "defensive staple." Even when the market gets wild, PG should stay in a tight, low-volatility band.
  
  • **TSLA & BTC-USD**: These should often compete for the top of the chart. Should see massive, jagged spikes during earnings calls (for Tesla) or regulatory news (for Bitcoin).

**a.) 30 Day Rolling Volatility (The "Signal"):**

  **Observation:** This plot is much **"noisier**." It is excellent for identifying **event-driven risk**, such as a sudden market crash or a specific company scandal. It **reacts quickly** to change but also settles down faster.

**b.) 90 Day Rolling Volatility (The "Climate"):**

  **Observation:** This plot is **smoother**. It filters out the "one-day wonders" and **shows structural shifts in risk**. If the 90-day line is trending upward, it suggests the market is entering a **long-term** "regime change" (e.g., the transition from the low-interest-rate era of 2021 to the high-inflation era of 2022).

**c.) 30 Day vs 90 Day: The "Risk Tiers" (PG & VTI vs. TSLA & BTC-USD):**

  **Observation:** There is a permanent, visible "gap" on the Y-axis. PG and VTI almost always occupy the 0.1 to 0.3 range, while TSLA and BTC-USD frequently spike between 0.6 and 1.1.

  **Conclusion:** This validates the **Asset Class Hierarchy**. Defensive stocks (PG) and broad market indexes (VTI) provide a "volatility floor". Investors holding TSLA or BTC-USD must be prepared for price swings that are 3 to 5 times more intense than the broader market.

**d.) 30 Day vs 90 Day: Sensitivity: 30-Day "Noise" vs. 90-Day "Trend":**

**Observation:** Compare the jaggedness of the lines. The 30-day plot (Fast) shows sharp, vertical spikes—specifically in mid-2025—that quickly retreat. The 90-day plot (Slow) turns those spikes into rounded "hills."

**Conclusion:** This demonstrates **Window Sensitivity**. A 30-day window is a "Tactical" view, great for identifying sudden shocks like earnings reports or news cycles. The 90-day window is a "Strategic" view, better for long-term investors to see if the overall "market climate" is becoming fundamentally more dangerous.


---------------------


**3.) Correlation Heatmaps:**

**Stocks/Funds Analyzed:** SPY, QQQ, TLT, GLD, XLE, BTC-USD, KO

This heatmap visualizes the **Pearson Correlation Coefficient** between the daily log returns of each asset. It tells us how closely two assets move in relation to each other on a day-to-day basis. A variety of assets with varying correlations were specifically chosen in order to showcase what a diversified portfolio would look like on a heat map.

**a.) The "Red Zone": SPY vs. QQQ (0.95):**

  **Observation:** The deep red square at the intersection of SPY (S&P 500) and QQQ (Nasdaq 100) shows a near-perfect correlation of 0.95.

  **Conclusion:** This identifies **portfolio redundancy**. Holding both SPY and QQQ doesn't provide significant diversification because they move in conjuction. If one crashes, the other almost certainly will too.

**b.) The "Diversifiers": GLD and TLT:**

  **Observation:** Notice the vast "blue sea" around Gold (GLD) and Treasury Bonds (TLT). Their correlations with the S&P 500 are extremely low (0.12 and 0.06, respectively).
  
  **Conclusion:** These are the **hedges** because they have nearly **zero correlation** with the stock market, they act as **anchor for a portfolio**. When stocks are volatile, **these assets move independently**, smoothing out the total portfolio's value.
  
  
**c.) The "Mirror Move": XLE vs. TLT (-0.12):**

  **Observation:** This is one of the few **negative correlations** on the map.
  
  **Conclusion:** Negative correlation is the "holy grail" of **risk management**. It suggests that when Energy (XLE) tends to go down, Bonds (TLT) tend to go up. This highlights how **this script can find assets that actually offset each other's losses**.


**d.) The "Uncorrelated Wildcard": BTC-USD:**

  **Observation:** Bitcoin shows a **low correlation with defensive staples** like KO (0.058) and Gold (0.088), but a **moderate correlation with Tech/QQQ** (0.40).
  
  **Conclusion:** This proves that **Bitcoin is a unique "risk-on" asset**. It **doesn't behave like digital gold (low correlation to GLD)** but rather like a high-octane tech stock, yet **it still provides more diversification than simply adding another equity**.

---------------------


**4.) Return Distribution Plots:** 

**Stocks/Funds Analyzed:** PEP, TSLA

These histograms visualize the frequency of daily gains and losses over the past 5 years. By overlaying statistical markers like Standard Deviation and Value at Risk (VaR), we can quantify the "shape of risk" for each ticker.
Comparing PEP (Pepsi) and TSLA (Tesla) provides a perfect visual contrast between a "Steady Performer" and a "High-Risk/High-Reward" asset. Important Note: the plots may appear to have similar shapes until you consider their domains. Make sure ton double check the x-axis domain when reading the plots.

**a.) The "Tall & Skinny" Profile: PEP (Pepsi):**

  **Observation:** The bars are **tightly clustered** around the mean. The distance between the **+1 and −1 Standard Deviation lines is narrow (±1.1%)**, and the **VaR** line is close to the center (at roughly −1.7%).

  **Conclusion:** This is a **Low-Variance asset**. For a conservative investor, this plot is "comfortable" because **most days result in very small changes**. The likelihood of a sudden, catastrophic daily drop is statistically very low, as evidenced by the thin "tails" on either side.

**b.) The "Wide & Fat-Tailed" Profile: TSLA (Tesla):**

  **Observation:** The **distribution is much wider and shorter**. The **Standard Deviation (±3.8%) is nearly triple that of Pepsi**. Notice the extreme distance between the Lowest Return (−16.7%) and Greatest Return (+20.4%).

  **Conclusion:** This illustrates **High Volatility and Kurtosis**. Tesla has "Fat Tails," meaning **"extreme" events happen far more often than a normal distribution would predict**. While the mean return is similar to Pepsi's, the daily "swing" is much more violent.

**c.) Value at Risk (VaR) Comparison:**

  **Observation:** Compare the red dashed lines. PEP's VaR is −1.7%, while TSLA's is −5.9%

  **Conclusion:** VaR tells us the "95% confidence" worst-case scenario. **For every $1,000 invested, you can expect to lose no more than $17 in a single day for Pepsi (95% of the time)**. For **Tesla, that number jumps to $59**. This single line **allows an investor to quantify exactly how much "pain" they must be willing to endure to hold the asset**.

**d.) Positive Skew & Outliers:**

  **Observation:** Look at the blue vertical lines (Max/Min). TSLA’s "Greatest Return" line is significantly further to the right than its "Lowest Return" line is to the left.

  **Conclusion:** This indicates a **Positive Skew**. Despite the high risk, the "outlier" days for Tesla are more **skewed toward massive gains than massive losses over this 5-year period**. This helps explain why investors tolerate the high volatility—the "upside surprises" are mathematically larger than the "downside shocks."
