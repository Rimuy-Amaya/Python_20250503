"""
主應用程式入口點。
此檔案將作為CLI應用程式的起點。
依據 lesson17_2.ipynb 的處理方式，初始化 pandas 讀取與分組聚合。
"""
import pandas as pd
import argparse
import os

def process_data(input_path: str, output_path: str):
    """
    讀取輸入檔案（CSV或Excel），進行分組聚合，並輸出為指定格式的檔案。
    :param input_path: 輸入檔案路徑 (CSV 或 Excel)
    :param output_path: 輸出的檔案路徑 (CSV 或 Excel)
    """
    # 判斷輸入檔案類型並讀取
    _, input_ext = os.path.splitext(input_path)
    if input_ext.lower() == '.csv':
        tips_df = pd.read_csv(input_path)
    elif input_ext.lower() in ['.xls', '.xlsx']:
        tips_df = pd.read_excel(input_path)
    else:
        raise ValueError("不支援的輸入檔案格式。請提供 .csv 或 .xlsx 檔案。")

    # 資料處理邏輯
    tips_df.columns = ['總票價', '小費', '吸煙者', '日期', '時間', '大小']
    tips_df['小費比例'] = tips_df['小費'] / tips_df['總票價']
    grouped = tips_df.groupby(by=['吸煙者','日期'])
    functions = [('數量','count'),('平均','mean'),('最大值','max')]
    tips_df3 = grouped[['小費','總票價']].agg(functions)

    # 判斷輸出檔案類型並寫入
    _, output_ext = os.path.splitext(output_path)
    if output_ext.lower() == '.csv':
        tips_df3.to_csv(output_path)
        print(f"已將樞紐表結果輸出至 CSV 檔案：{output_path}")
    elif output_ext.lower() in ['.xls', '.xlsx']:
        tips_df3.to_excel(output_path)
        print(f"已將樞紐表結果輸出至 Excel 檔案：{output_path}")
    else:
        raise ValueError("不支援的輸出檔案格式。請指定 .csv 或 .xlsx 副檔名。")


def main():
    """
    主程式，處理命令列參數並執行對應功能。
    """
    parser = argparse.ArgumentParser(description="CSV/Excel 樞紐表轉換工具")

    # 這裡不再使用 mutually_exclusive_group，因為 process_data 可以處理兩種輸入
    parser.add_argument('--input', type=str, required=True, help='輸入的檔案路徑 (副檔名需為 .csv 或 .xlsx)')
    parser.add_argument('--out', type=str, required=True, help='輸出的檔案路徑 (副檔名需為 .csv 或 .xlsx)')

    args = parser.parse_args()

    # 呼叫通用的處理函式
    try:
        process_data(args.input, args.out)
    except ValueError as e:
        print(f"錯誤：{e}")
        parser.print_help()


if __name__ == "__main__":
    main()