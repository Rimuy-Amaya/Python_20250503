import tkinter as tk
from tkinter import ttk

# 全域變數，儲存從檔案讀取的姓名
all_names = []

def load_names(file_path):
    """從指定的檔案路徑讀取姓名列表"""
    global all_names
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            all_names = [name.strip() for name in f if name.strip()]
        # print(f"成功載入 {len(all_names)} 個名字。") # 用於調試
    except FileNotFoundError:
        all_names = []
        # print(f"錯誤：找不到檔案 {file_path}") # 用於調試
        # 可以在GUI上顯示錯誤訊息，但目前需求是找不到時顯示查無此人
        # 這裡假設檔案一定存在，若不存在，搜尋時也會是空的結果
    except Exception as e:
        all_names = []
        # print(f"讀取檔案時發生錯誤: {e}") # 用於調試

def search_name():
    """根據輸入框中的文字搜尋姓名"""
    search_term = search_entry.get().strip()
    
    # 清空先前的搜尋結果
    results_listbox.delete(0, tk.END)
    
    if not search_term:
        results_label.config(text="請輸入搜尋關鍵字")
        return

    found_names = [name for name in all_names if search_term in name]
    
    if found_names:
        for name in found_names:
            results_listbox.insert(tk.END, name)
        results_label.config(text=f"找到 {len(found_names)} 個結果：")
    else:
        results_label.config(text="查無此人")

# --- GUI 設定 ---
# 主視窗
root = tk.Tk()
root.title("姓名搜尋器")
root.geometry("400x450") # 設定視窗大小

# 載入姓名 (在GUI啟動前)
file_path = r"c:\Users\User\Documents\Amaya\Python_20250503\lesson9\names.txt"
load_names(file_path)

# --- 介面元件 ---
# 標題
title_label = ttk.Label(root, text="姓名搜尋", font=("Arial", 16))
title_label.pack(pady=10)

# 搜尋框和按鈕的框架
search_frame = ttk.Frame(root)
search_frame.pack(pady=10, padx=10, fill=tk.X)

search_label = ttk.Label(search_frame, text="輸入姓名：")
search_label.pack(side=tk.LEFT, padx=(0, 5))

search_entry = ttk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
search_entry.focus() # 讓游標預設在輸入框

search_button = ttk.Button(search_frame, text="搜尋", command=search_name)
search_button.pack(side=tk.LEFT)

# 搜尋結果提示標籤
results_label = ttk.Label(root, text="請輸入關鍵字並點擊搜尋")
results_label.pack(pady=(10, 0))

# 搜尋結果列表框
results_listbox_frame = ttk.Frame(root)
results_listbox_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

results_listbox = tk.Listbox(results_listbox_frame)
results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 捲軸
scrollbar = ttk.Scrollbar(results_listbox_frame, orient=tk.VERTICAL, command=results_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_listbox.config(yscrollcommand=scrollbar.set)


# 讓Enter鍵也能觸發搜尋
root.bind('<Return>', lambda event=None: search_button.invoke())

# 啟動主循環
root.mainloop()
