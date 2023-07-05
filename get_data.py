import logging
import pandas as pd
import lxml
from bs4 import BeautifulSoup
from helper import SecAPI
from pytickersymbols import PyTickerSymbols
from sec_cik_mapper import StockMapper
from sec_edgar_downloader import Downloader
from tqdm import tqdm

dl = Downloader("./data/")
stock_mapper = StockMapper()
stock_data = PyTickerSymbols()
sec_api = SecAPI()

def get_ticker_data():
    """
    Function to get the tickers, CIK and name of the companies in the DOW JONES index.

    Output:
    final_stocks_dict: a dictionary of format {ticker: (CIK, name of company)}
    """
    dow_jones_stocks = list(stock_data.get_stocks_by_index('DOW JONES'))
    ticker_cik_dict = stock_mapper.ticker_to_cik
    dow_jones_stocks_symbol = {stock['symbol']:stock['name'] for stock in dow_jones_stocks}
    final_stocks_dict = {key: (value, dow_jones_stocks_symbol[key]) 
                         for key, value in ticker_cik_dict.items() if key in dow_jones_stocks_symbol.keys()}
    return final_stocks_dict

def download_sec_data(tickers):
    """
    Function to download the SEC filings since 2013 for a list of stocks in the data directory.
    """
    count = 0
    for key in tqdm(tickers, desc=f"Getting data...", unit='filing'):
        try:
            print(f"Downloading data for {key}")
            dl.get("10-K", key,  after="2013-01-01")
            count += 1
            if count == 11:
                break
        except:
            print(f"An error occured while downloading the filings for {key}. \nMoving to the next stock...")
            continue

if __name__ == "__main__":
    tickers = get_ticker_data()
    download_sec_data(tickers)
    print("Successfully downloaded SEC filings (Form 10-K) for DOW JONES stocks!")