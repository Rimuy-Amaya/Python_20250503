"""
主應用程式入口點。
此檔案將作為CLI應用程式的起點。
依據 lesson17_2.ipynb 的處理方式，初始化 pandas 讀取與分組聚合。
"""
import pandas as pd
import argparse
import os 

def process_csv_to_excel(csv_path: str, excel_path: str):
    """
    讀取CSV檔案，進行分組聚合，並輸出為Excel檔案。
    :param csv_path: 輸入的CSV檔案路徑
    :param excel_path: 輸出的Excel檔案路徑
    """
    tips_df = pd.read_csv(csv_path)
    tips_df.columns = ['總票價', '小費', '吸煙者', '日期', '時間', '大小']
    tips_df['小費比例'] = tips_df['小費'] / tips_df['總票價']
    grouped = tips_df.groupby(by=['吸煙者','日期'])
    functions = [('數量','count'),('平均','mean'),('最大值','max')]
    tips_df3 = grouped[['小費','總票價']].agg(functions)
    tips_df3.to_excel(excel_path)
    print(f"已將樞紐表結果輸出至 {excel_path}")

def process_excel_to_csv(excel_path: str, csv_path: str):
    """
    讀取Excel檔案，進行分組聚合，並輸出為CSV檔案。
    :param excel_path: 輸入的Excel檔案路徑
    :param csv_path: 輸出的CSV檔案路徑
    """
    tips_df = pd.read_excel(excel_path)
    tips_df.columns = ['總票價', '小費', '吸煙者', '日期', '時間', '大小']
    tips_df['小費比例'] = tips_df['小費'] / tips_df['總票價']
    grouped = tips_df.groupby(by=['吸煙者','日期'])
    functions = [('數量','count'),('平均','mean'),('最大值','max')]
    tips_df3 = grouped[['小費','總票價']].agg(functions)
    tips_df3.to_csv(csv_path)
    print(f"已將樞紐表結果輸出至 {csv_path}")

def main():
    """
    主程式，處理命令列參數並執行對應功能。
    """
    parser = argparse.ArgumentParser(description="CSV/Excel 樞紐表轉換工具")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--csv', type=str, help='輸入的CSV檔案路徑')
    group.add_argument('--excel', type=str, help='輸入的Excel檔案路徑')
    parser.add_argument('--out', type=str, required=True, help='輸出的檔案路徑 (副檔名需為 .csv 或 .xlsx)')
    args = parser.parse_args()

    if args.csv:
        process_csv_to_excel(args.csv, args.output)
    elif args.excel:
        process_excel_to_csv(args.excel, args.output)

if __name__ == "__main__":
    main()
