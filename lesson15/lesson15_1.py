import yfinance as yf
import os
from datetime import date, datetime


def download_data():
    """
    1. 每日下載yfinance的4檔股票資料: 2330.TW, 2303.TW, 2454.TW, 2317.TW
    2. 在目前目錄下建立一個名為 'data' 的資料夾 (如果不存在)。
    3. 下載的股票資料儲存為包含日期的CSV檔 (例如: 2330_2023-10-27.csv)。
    4. 如果當日檔案已存在，則跳過下載。
    5. 每日下載新檔案後，會自動刪除該股票對應的舊日期檔案。
    6. 抓取資料的區間範圍是從 '2000-01-01' 到今天。
    """

    # Create data directory if it doesn't exist
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)

    tickers = ['2330.TW', '2303.TW', '2454.TW', '2317.TW']
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')

    for ticker in tickers:
        stock_code = ticker.split('.')[0]
        # 檔名加上今天的日期，例如: 2330_2023-10-27.csv
        filename = f"{stock_code}_{today_str}.csv"
        filepath = os.path.join(data_dir, filename)

        # 如果今日檔案已存在，則跳過
        if os.path.exists(filepath):
            print(f"檔案 {filepath} 今天已下載，跳過。")
            continue

        # 下載新資料
        print(f"正在下載 {ticker} 的資料...")
        try:
            # 下載從指定日期到今天的資料
            df = yf.download(ticker, start='2000-01-01', end=today, auto_adjust=True)

            if df.empty:
                print(f"未下載到 {ticker} 的資料，可能為假日或股票已下市。")
                continue

            # 儲存為新的 CSV 檔
            df.to_csv(filepath)
            print(f"成功下載並儲存 {ticker} 至 {filepath}")

            # 刪除此股票的舊檔案
            for old_file in os.listdir(data_dir):
                if old_file.startswith(f"{stock_code}_") and old_file.endswith(".csv") and old_file != filename:
                    old_filepath = os.path.join(data_dir, old_file)
                    os.remove(old_filepath)
                    print(f"已刪除舊檔案: {old_filepath}")
        except Exception as e:
            print(f"下載 {ticker} 資料失敗: {e}")

def main():
    download_data()

if __name__ == "__main__":
    main()
