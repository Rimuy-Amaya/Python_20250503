import yfinance as yf
import os
from datetime import date


def download_data():
    """
    1. 下載yfinance的4檔股票資料,股票有:2330.TW,2303.TW,2454.TW,2317.TW
    2. 在目前目錄下建立一個data的資料夾,如果已經有這個資料夾,就不建立
    3. 下載的4檔股票必需儲存為4個csv檔,檔名為2330.csv,2303.csv,2454.csv,2317.csv
    4. 如果已經有這些檔案,就不下載
    5. 抓取資料的區間範圍是，直到「今天」
    """

    # Create data directory if it doesn't exist
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)

    stocks = {
        '2330.TW': '2330.csv',
        '2303.TW': '2303.csv',
        '2454.TW': '2454.csv',
        '2317.TW': '2317.csv'
    }

    for ticker, filename in stocks.items():
        filepath = os.path.join(data_dir, filename)
        if not os.path.exists(filepath):
            df = yf.download(ticker, start='2000-01-01', end=date.today(), auto_adjust=True)
            df.to_csv(filepath)
            print(f"Downloaded {ticker} to {filepath}")
        else:
            print(f"{filepath} already exists, skipping download.")

def main():
    download_data()

if __name__ == "__main__":
    main()
