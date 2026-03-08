# financial-data-analysis
OVERVIEW: 
---
This project is a modular Python-based data pipeline designed to automate the retrieval, processing, and visualization of stock market risk metrics. By transitioning from raw price data to advanced statistical measures, like **Logarithmic Returns** and **Rolling Volatility**, this tool provides a clear view of market trends, fluxuations, and asset correlations. This was accomplished through the use of Python with YFinance, Pandas, Matplotlib, and Seaborn. The project is built for investors and analysts who need to identify **volatility clustering**, **risk-adjusted returns**, and **portfolio diversification opportunities** across multiple tickers simultaneously.

---------------------------------------------------------------------------------------------------------------
PROJECT ORDER:
---
Here's the order this project's folders should be viewed and ran in:
- python files / `fetch_data.py`
  - data / raw / `prices.csv` (to view scraped data)
- python files / `clean_data.py`
  - data / processed / `returns.csv` (to view transformed data)
- python files / `analysis.py`
- plots / 
  - `price_trends`
  - `rolling_volatility`
  - `correlation_heatmap`
  - `return_distribution`

IN DEPTH DESCRIPTION:
---
Below is a description of each file, its purpose, and how it works. For a more specific description of individual lines of code, please view the Python files themselves. The files are **heavily commented** to help aid in the understanding of the code.


### 1. fetch_data.py: **Data Collection**

This script handles the **data collection** process by defining a ticker list and a rolling five-year window ending at the current day. 

* **Pathlib & Compatibility:** We use **pathlib** to ensure the code is **cross-platform compatible** (Windows, Mac, Linux). It automatically manages file path slashes and verifies folder existence to prevent **"File Not Found" errors**. 
* **The Fetching Function:** The **fetching function** utilizes the **download() function** from the `yfinance` library to scrape daily market close data into a **Pandas DataFrame**. 
* **Efficiency:** `download()` is used because it is specifically optimized for time-series data and interacts directly with Yahoo Finance’s historical price systems.

The raw data is saved as `prices.csv` for use in subsequent scripts without the need for re-downloading.

**Fetching Financial Data Complete**

---

### 2. clean_data.py: **Data Transformations**

This script executes **data transformations**, converting raw prices into a processed `returns` DataFrame.

* **Key Functions:** We define `load_price_data()`, `compute_log_returns()`, and `compute_rolling_volatility()` to structure the pipeline.
* **Log Returns & Volatility:** We transform price data into **daily log returns** (% rates of change) and calculate **rolling volatility** for 30 and 90-day windows.
* **Data Alignment:** We drop rows with NA values to ensure a clean comparison between assets (like Crypto) that trade outside the standard 252-day market.

All transformed metrics are merged into a single dataset and saved as `returns.csv`. While labeled "clean_data," this file primarily handles the mathematical heavy lifting required for analysis.

**Transforming Financial Data Complete**

---

### 3. analysis.py: **Data Plotting**

The final stage is **data plotting**, using **matplotlib** (**pyplot**) and **seaborn** to visualize the processed financial metrics.

* **Visual Portfolio:** The script generates four distinct plot types:
    * **price trends plots:** 5-year history with 50/200 day moving averages.
    * **rolling volatility plots:** Visualizing the intensity of price swings over 30/90 days.
    * **correlation heatmap:** Measuring how closely different asset prices follow one another.
    * **return distribution plots:** Showing the frequency and "shape" of daily log returns.
* **Clarity & Design:** Significant code is dedicated to making these plots visually professional and easy to read. 

**Note:** Detailed interpretations and captions for each visualization are located within the **plots** folder.

**Plotting Financial Data Complete**


Conclusions from Visualizations:
---
After creating the plots and viewing them, many conclusions can be drawn that would be cumbersome or near impossible to draw from looking at the raw financial data in table form. Here are the observations and conclusions that I have drawn from the plots created in this project:

**PLOTS LAST UPDATED: (Mar. 3rd 2026)**


**1.) Price Trends and Moving Averages (50/200 Day) Plots:**

**Stocks Analyzed:** AAPL, NVDA, TSLA

These plots visualize the relationship between the current price and its long-term institutional averages. The 50-day Moving Average (MA) represents intermediate momentum, while the 200-day MA represents the long-term trend "floor". For these plots 3 of the magnificent 7 tech stocks were plotted: Apple, Nvidia, Telsa.

**a.) AAPL:** The "Stair-Stepper":

*   **Observation:** Notice how often the price dips to touch the 50-day MA and then bounces back up. During larger market corrections, it may drop to the 200-day MA. 
  
*   **Conclusion:** This is an example of **Support and Resistance**. AAPL shows how moving averages act as a **"psychological floor"** for investors. This plot clearly identifies these **"buy-the-dip"** opportunities where the price respects its historical mean.

**b.) NVDA:** The Momentum Powerhouse:

*   **Observation:** Look for the **"Golden Cross"** (where the 50-day crosses above the 200-day). In the last 5 years, NVDA has spent significant time with a massive "spread" between the price and the 200-day MA.

*   **Conclusion:** This plot showcases **strong upward momentum**. When the price stays consistently above both MA lines, it indicates a "parabolic" trend where buyers are aggressive. This plot demonstrates how the script identifies assets that are significantly "extended" from their historical average.

**c.) TSLA:** The Volatility Case Study:

*   **Observation:** Unlike AAPL, TSLA often crashes through its moving averages with high velocity. You may see a **"Death Cross"** (50-day crossing below the 200-day) during its heavier correction periods.

*   **Conclusion:** This plot illustrates **Trend Reversals**. It shows that for high-beta (volatile) stocks, moving averages can be **"lagging indicators**." If the price is zigzagging through the averages frequently, it signals a period of **high uncertainty** or a **"sideways" market** rather than a clear trend.

---------------------


**2.) Rolling Volatilty Plots:**

**Assets Analyzed:** VTI, TSLA, BTC-USD, PG

The plots in this section visualize risk over time, a risk-spectrum. Instead of looking at a single average for the whole 5 years, rolling volatility shows how "jumpy" an asset was during specific time periods in the market. I used different classes of assets: VTI (Market Average), TSLA (Aggressive Growth), PG (Conservative), and BTC-USD (Speculative/Crypto). This variety of assets was used to show how the script distinguishes between different risk profiles. Here's some more detailed information about the selection of these asstes for these plots:

  • **VTI (Total Stock Market)**: Acts as the baseline. It should sit above PG but significantly below the "growth" assets. It represents the "systemic risk" of the entire market.
  
  • **PG (Procter & Gamble)**: Should consistently sit at the bottom of the plot. This would confirm its status as a "defensive staple." Even when the market gets wild, PG should stay in a tight, low-volatility band.
  
  • **TSLA & BTC-USD**: These should often compete for the top of the chart. Should see massive, jagged spikes during earnings calls (for Tesla) or regulatory news (for Bitcoin).

**a.) 30 Day Rolling Volatility (The "Signal"):**

*   **Observation:** This plot is much **"noisier**." It is excellent for identifying **event-driven risk**, such as a sudden market crash or a specific company scandal. It **reacts quickly** to change but also settles down faster.

**b.) 90 Day Rolling Volatility (The "Climate"):**

*   **Observation:** This plot is **smoother**. It filters out the "one-day wonders" and **shows structural shifts in risk**. If the 90-day line is trending upward, it suggests the market is entering a **long-term** "regime change" (e.g., the transition from the low-interest-rate era of 2021 to the high-inflation era of 2022).

**c.) 30 Day vs 90 Day: The "Risk Tiers" (PG & VTI vs. TSLA & BTC-USD):**

*   **Observation:** There is a permanent, visible "gap" on the Y-axis. PG and VTI almost always occupy the 0.1 to 0.3 range, while TSLA and BTC-USD frequently spike between 0.6 and 1.1.

*   **Conclusion:** This validates the **Asset Class Hierarchy**. Defensive stocks (PG) and broad market indexes (VTI) provide a "volatility floor". Investors holding TSLA or BTC-USD must be prepared for price swings that are 3 to 5 times more intense than the broader market.

**d.) 30 Day vs 90 Day: Sensitivity: 30-Day "Noise" vs. 90-Day "Trend":**

*   **Observation:** Compare the jaggedness of the lines. The 30-day plot (Fast) shows sharp, vertical spikes—specifically in mid-2025—that quickly retreat. The 90-day plot (Slow) turns those spikes into rounded "hills."

*   **Conclusion:** This demonstrates **Window Sensitivity**. A 30-day window is a "Tactical" view, great for identifying sudden shocks like earnings reports or news cycles. The 90-day window is a "Strategic" view, better for long-term investors to see if the overall "market climate" is becoming fundamentally more dangerous.


---------------------


**3.) Correlation Heatmaps:**

**Assets Analyzed:** SPY, QQQ, TLT, GLD, XLE, BTC-USD, KO

This heatmap visualizes the **Pearson Correlation Coefficient** between the daily log returns of each asset. It tells us how closely two assets move in relation to each other on a day-to-day basis. A variety of assets with varying correlations were specifically chosen in order to showcase what a diversified portfolio would look like on a heat map.

**a.) The "Red Zone": SPY vs. QQQ (0.95):**

*   **Observation:** The deep red square at the intersection of SPY (S&P 500) and QQQ (Nasdaq 100) shows a near-perfect correlation of 0.95.

*   **Conclusion:** This identifies **portfolio redundancy**. Holding both SPY and QQQ doesn't provide significant diversification because they move in conjuction. If one crashes, the other almost certainly will too.

**b.) The "Diversifiers": GLD and TLT:**

*   **Observation:** Notice the vast "blue sea" around Gold (GLD) and Treasury Bonds (TLT). Their correlations with the S&P 500 are extremely low (0.12 and 0.06, respectively).
  
*   **Conclusion:** These are the **hedges** because they have nearly **zero correlation** with the stock market, they act as **anchor for a portfolio**. When stocks are volatile, **these assets move independently**, smoothing out the total portfolio's value.
  
  
**c.) The "Mirror Move": XLE vs. TLT (-0.12):**

*   **Observation:** This is one of the few **negative correlations** on the map.
  
*   **Conclusion:** Negative correlation is the "holy grail" of **risk management**. It suggests that when Energy (XLE) tends to go down, Bonds (TLT) tend to go up. This highlights how **this script can find assets that actually offset each other's losses**.


**d.) The "Uncorrelated Wildcard": BTC-USD:**

*   **Observation:** Bitcoin shows a **low correlation with defensive staples** like KO (0.058) and Gold (0.088), but a **moderate correlation with Tech/QQQ** (0.40).
  
*   **Conclusion:** This proves that **Bitcoin is a unique "risk-on" asset**. It **doesn't behave like digital gold (low correlation to GLD)** but rather like a high-octane tech stock, yet **it still provides more diversification than simply adding another equity**.

---------------------


**4.) Return Distribution Plots:** 

**Stocks Analyzed:** PEP, TSLA

These histograms visualize the frequency of daily gains and losses over the past 5 years. By overlaying statistical markers like Standard Deviation and Value at Risk (VaR), we can quantify the "shape of risk" for each ticker.
Comparing PEP (Pepsi) and TSLA (Tesla) provides a perfect visual contrast between a "Steady Performer" and a "High-Risk/High-Reward" asset. Important Note: the plots may appear to have similar shapes until you consider their domains. Make sure ton double check the x-axis domain when reading the plots.

**a.) The "Tall & Skinny" Profile: PEP (Pepsi):**

*   **Observation:** The bars are **tightly clustered** around the mean. The distance between the **+1 and −1 Standard Deviation lines is narrow (±1.1%)**, and the **VaR** line is close to the center (at roughly −1.7%).

*   **Conclusion:** This is a **Low-Variance asset**. For a conservative investor, this plot is "comfortable" because **most days result in very small changes**. The likelihood of a sudden, catastrophic daily drop is statistically very low, as evidenced by the thin "tails" on either side.

**b.) The "Wide & Fat-Tailed" Profile: TSLA (Tesla):**

*   **Observation:** The **distribution is much wider and shorter**. The **Standard Deviation (±3.8%) is nearly triple that of Pepsi**. Notice the extreme distance between the Lowest Return (−16.7%) and Greatest Return (+20.4%).

*   **Conclusion:** This illustrates **High Volatility and Kurtosis**. Tesla has "Fat Tails," meaning **"extreme" events happen far more often than a normal distribution would predict**. While the mean return is similar to Pepsi's, the daily "swing" is much more violent.

**c.) Value at Risk (VaR) Comparison:**

*   **Observation:** Compare the red dashed lines. PEP's VaR is −1.7%, while TSLA's is −5.9%

*   **Conclusion:** VaR tells us the "95% confidence" worst-case scenario. **For every $1,000 invested, you can expect to lose no more than $17 in a single day for Pepsi (95% of the time)**. For **Tesla, that number jumps to $59**. This single line **allows an investor to quantify exactly how much "pain" they must be willing to endure to hold the asset**.

**d.) Positive Skew & Outliers:**

 *  **Observation:** Look at the blue vertical lines (Max/Min). TSLA’s "Greatest Return" line is significantly further to the right than its "Lowest Return" line is to the left.

*   **Conclusion:** This indicates a **Positive Skew**. Despite the high risk, the "outlier" days for Tesla are more **skewed toward massive gains than massive losses over this 5-year period**. This helps explain why investors tolerate the high volatility—the "upside surprises" are mathematically larger than the "downside shocks."
