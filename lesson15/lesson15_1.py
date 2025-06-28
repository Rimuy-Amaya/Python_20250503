import yfinance as yf
import os
import pandas as pd
from datetime import date, datetime


def download_data():
    """
    1. 每日下載yfinance的4檔股票資料: 2330.TW, 2303.TW, 2454.TW, 2317.TW
    2. 在目前目錄下建立一個名為 'data' 的資料夾 (如果不存在)。
    3. 下載的股票資料儲存為包含最新交易日期的CSV檔 (例如: 2330_2023-10-26.csv)。
    4. 智慧判斷是否需要下載：僅在有新交易日資料時才下載並更新檔案。
    5. 每日下載新檔案後，會自動刪除該股票對應的舊日期檔案。
    6. 抓取資料的區間範圍是從 '2000-01-01' 到今天。
    """

    # Create data directory if it doesn't exist
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)

    tickers = ['2330.TW', '2303.TW', '2454.TW', '2317.TW']

    for ticker in tickers:
        stock_code = ticker.split('.')[0]
        print(f"\n--- 正在檢查 {ticker} ({stock_code}) 的資料更新 ---")
        try:
            # 1. 嘗試下載最新資料 (關閉進度條，讓輸出更簡潔)
            df = yf.download(ticker, start='2000-01-01', end=date.today(), auto_adjust=True, progress=False)

            if df.empty:
                print(f"未下載到 {ticker} 的任何資料，跳過。")
                continue

            # 2. 取得資料的最後一個交易日
            last_trade_date = df.index.max().date()
            last_trade_date_str = last_trade_date.strftime('%Y-%m-%d')
            new_filename = f"{stock_code}_{last_trade_date_str}.csv"
            new_filepath = os.path.join(data_dir, new_filename)

            # 3. 檢查最新資料是否已存在，若存在則無需更新
            if os.path.exists(new_filepath):
                print(f"資料已是最新 (最新到 {last_trade_date_str})，無需更新。")
                continue
            
            # 4. 如果是新資料，則儲存並刪除舊檔
            print(f"發現新資料，最新交易日為: {last_trade_date_str}")
            df.to_csv(new_filepath)
            print(f"成功儲存新資料至: {new_filepath}")

            # 刪除此股票的舊檔案
            for old_file in os.listdir(data_dir):
                if old_file.startswith(f"{stock_code}_") and old_file.endswith(".csv") and old_file != new_filename:
                    old_filepath = os.path.join(data_dir, old_file)
                    os.remove(old_filepath)
                    print(f"已刪除舊檔案: {old_filepath}")
        except Exception as e:
            print(f"處理 {ticker} 時發生錯誤: {e}")

def process_and_combine_data():
    """
    讀取 data/ 資料夾中最新的股票CSV檔，
    抽取出 'Close' 欄位，並將它們合併成一個 DataFrame。
    """
    data_dir = 'data'
    stock_map = {
        '2330': '台積電',
        '2303': '聯電',
        '2317': '鴻海',
        '2454': '聯發科'
    }
    all_close_prices = []

    print("\n--- 開始處理並合併資料 ---")
    for code, name in stock_map.items():
        # 尋找該股票最新的CSV檔
        try:
            files = [f for f in os.listdir(data_dir) if f.startswith(f"{code}_") and f.endswith(".csv")]
            if not files:
                print(f"找不到股票 {code} ({name}) 的任何資料檔案。")
                continue
            
            latest_file = sorted(files, reverse=True)[0]
            filepath = os.path.join(data_dir, latest_file)
            print(f"讀取檔案: {filepath}")

            # yfinance 儲存的CSV檔有額外2行標頭資訊，且日期欄位被命名為'Price'
            # 我們需要調整參數來正確讀取
            df = pd.read_csv(
                filepath,
                skiprows=[1, 2],          # 跳過第2和第3行
                index_col='Price',        # 將第一欄 (欄位名為Price) 作為索引
                parse_dates=True,
                usecols=['Price', 'Close']  # 僅讀取這兩欄
            )
            # 將索引的名稱從 'Price' 改回 'Date'，方便後續使用
            df.index.name = 'Date'
            df.rename(columns={'Close': name}, inplace=True)
            all_close_prices.append(df)
        except Exception as e:
            print(f"處理檔案 {code} 時發生錯誤: {e}")

    if not all_close_prices:
        print("沒有任何資料可供合併。")
        return None

    # 使用 pd.concat 依據索引 (Date) 合併所有 DataFrame
    combined_df = pd.concat(all_close_prices, axis=1)
    
    # 處理缺失值：
    # 使用 'ffill' (forward-fill) 策略，將前一個交易日的收盤價填充到因假日或停牌造成的 NaN 空格中。
    # 這是處理金融時間序列數據的標準做法，可以確保數據的連續性，且避免使用未來數據。
    combined_df.fillna(method='ffill', inplace=True)

    print("\n合併後的收盤價資料預覽 (最後5筆):")
    print(combined_df.tail())
    return combined_df

def main():
    download_data()
    process_and_combine_data()

if __name__ == "__main__":
    main()
