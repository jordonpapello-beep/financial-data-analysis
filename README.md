# financial-data-analysis
OVERVIEW: 
---
This project is a modular Python-based data pipeline designed to automate the retrieval, processing, and visualization of stock market risk metrics. By transitioning from raw price data to advanced statistical measures, like **Logarithmic Returns** and **Rolling Volatility**, this tool provides a clear view of market trends, fluxuations, and asset correlations. This was accomplished through the use of Python with YFinance, Pandas, Matplotlib, and Seaborn. The project is built for investors and analysts who need to identify **volatility clustering**, **risk-adjusted returns**, and **portfolio diversification opportunities** across multiple tickers simultaneously.

---------------------------------------------------------------------------------------------------------------
PROJECT ORDER:
---
Here's the order this project's folders should be ran and viewed in:
- fetch_data.py
- clean_data.py
- analysis.py
- plots

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

Now we move into main() where we begin to transform the 'prcies' data by first loading in the data using our 'load_price_data()' function. Now that we have access to that DataFrame we set 'returns' equal to 'compute_log_returns(prices)', which performs the log return calculation on the entire 'prices' DataFrame. Similarly, we calculate the rolling volatility for 30 and 90 days for each column of our new 'returns' DataFrame and assign these indiviadual DataFrames to 'vol_30' and 'vol_90' respectively. All of the new data has been calculated, so the final steps are to combine the retruns and volatility data into one DataFrame, and save it like we did with 'prices.csv' in 'fetch_data.py'. We can add the volatitily data easily by looping over the columns in 'returns' and adding the 30 and 90 day column data for each ticker in 'returns'. Now that we have one DataFrame with all of our transformed data, we can save it to the dircetory that we set up at the beginning of the script. We call this relative file path 'returns.csv'.

**Note:** There wasn't any real 'data cleaning' as the fetched data was already in optimal form for the DataFrame transformations. But if the data needed to be cleaned(which it usually needs to be), it would've happended in this file which is why it is called 'clean_data.py'.

**Transforming Financial Data Complete**


**3.) analysis.py:**

This file is where the **data plotting** happens. This script uses **pyplot** from **matplotlib** and **seaborn** in conjuction with each other to create the plots for this project. We begin by


Visualization and Conclusions:
---
After creating the plots and viewing them, many conclusions can be drawn that would be cumbersome or near impossible to draw from looking at the original inventory sheets:
