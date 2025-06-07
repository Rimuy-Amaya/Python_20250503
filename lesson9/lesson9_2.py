import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style # 導入 Style
import os

# --- Global Variables ---
# 使用您提供的絕對路徑
NAMES_FILE_PATH = r"c:\Users\User\Documents\Amaya\Python_20250503\lesson9\names.txt"
all_names_list = []

# --- Functions ---
def load_names_and_get_status():
    """
    從指定的檔案載入姓名列表。
    返回一個狀態訊息，並更新全域變數 all_names_list。
    """
    global all_names_list
    local_names_list = []
    try:
        with open(NAMES_FILE_PATH, "r", encoding="utf-8") as f:
            local_names_list = [line.strip() for line in f if line.strip()]
        
        if not local_names_list:
            all_names_list = []
            return f"姓名文件 '{os.path.basename(NAMES_FILE_PATH)}' 為空或只包含空白行。"
        
        all_names_list = local_names_list
        return f"已成功從 '{os.path.basename(NAMES_FILE_PATH)}' 載入 {len(all_names_list)} 個姓名。"
    except FileNotFoundError:
        all_names_list = []
        return f"錯誤：找不到姓名文件於\n{NAMES_FILE_PATH}\n請檢查文件路徑。"
    except Exception as e:
        all_names_list = []
        return f"讀取姓名文件時發生錯誤: {e}"

def update_result_display(message):
    """更新結果顯示區域的文字。"""
    result_text_widget.config(state=tk.NORMAL)  # 允許編輯以清空和插入文字
    result_text_widget.delete(1.0, tk.END)      # 清除先前內容
    result_text_widget.insert(tk.END, message)  # 插入新內容
    result_text_widget.config(state=tk.DISABLED) # 禁止使用者編輯

def perform_search():
    """執行搜尋並更新結果顯示。"""
    query = search_entry.get().strip()

    if not query:
        update_result_display("請輸入查詢關鍵字。")
        return

    # all_names_list 在程式啟動時已載入
    # 如果載入失敗或檔案為空，all_names_list 會是空的
    found_names = [name for name in all_names_list if query in name]

    if found_names:
        display_text = "\n".join(found_names)
        update_result_display(display_text)
    else:
        update_result_display("查無此人")

# --- Main Application Setup ---
root = tk.Tk()
root.title("姓名搜尋器 (強化版)") # 設定視窗標題
root.geometry("550x520") # 略微調整視窗大小

# --- Color Palette (Dark Theme) ---
root_bg = "#282c34"
frame_bg = "#303540"
widget_bg = "#3A3F4B"
text_fg = "#ABB2BF"
accent_color = "#61AFEF" # Blue accent
button_text_fg = "#282c34" # Dark text on light blue button
entry_border_focus_color = accent_color
entry_border_idle_color = "#4A505C" # Slightly darker border for entry when not focused

# --- Style Configuration ---
style = Style(root)
try:
    # 嘗試使用 'clam' 主題，它通常看起來比較現代
    style.theme_use('clam') # 'clam' is often more customizable
except tk.TclError:
    print("Clam 主題不可用，嘗試 'alt'...")
    try:
        style.theme_use('alt')
    except tk.TclError:
        print("Alt 主題也不可用，使用預設主題。")
        style.theme_use('default')

# Configure root window background
root.config(bg=root_bg)

# 設定預設字體
default_font_family = "Segoe UI" if os.name == 'nt' else "TkDefaultFont" # Windows 上用 Segoe UI
base_font_size = 11 # 增加基礎字體大小
default_font = (default_font_family, base_font_size)
bold_font = (default_font_family, base_font_size, "bold")
label_frame_title_font = (default_font_family, base_font_size + 1, "bold") # LabelFrame 標題字體

# 全域 tk 控件字體 (例如 tk.Text)
root.option_add("*Font", default_font)

# ttk 控件的特定樣式設定
style.configure(".", background=root_bg, foreground=text_fg) # Base for many ttk widgets
style.configure("TFrame", background=frame_bg)
style.configure("TLabel", background=frame_bg, foreground=text_fg, padding=(0, 5))
style.configure("TButton",
                background=accent_color,
                foreground=button_text_fg,
                font=bold_font,
                padding=(10, 5),
                borderwidth=0,
                relief=tk.FLAT)
style.map("TButton",
          background=[('active', '#529BDA'), ('pressed', '#4088C0')], # Darker blue on active/pressed
          relief=[('pressed', tk.SUNKEN), ('!pressed', tk.FLAT)])

# Style for the Frame that will act as a border for the Entry
style.configure("EntryBorder.TFrame", background=entry_border_idle_color)

# Style for the TEntry itself (to have no default border, colors handled by wrapper and direct config)
style.configure("Custom.TEntry",
                fieldbackground=widget_bg,
                foreground=text_fg,
                insertwidth=2, # Cursor thickness
                borderwidth=0, # No ttk border, handled by wrapper Frame
                padding=(8, 6)) # Internal padding for text in entry

# Corrected TLabelFrame style: Use a string value for relief
style.configure("TLabelFrame", background=frame_bg, borderwidth=1, relief='groove') # Use string for relief
style.configure("TLabelFrame.Label", background=frame_bg, foreground=accent_color, font=label_frame_title_font, padding=(10,2))

style.configure("Vertical.TScrollbar",
                background=widget_bg,
                troughcolor=frame_bg,
                bordercolor=frame_bg,
                arrowcolor=text_fg,
                relief=tk.FLAT,
                arrowsize=14)
style.map("Vertical.TScrollbar",
          background=[('active', accent_color)],
          relief=[('active', tk.RAISED)])


# --- Data Loading ---
# 程式啟動時載入姓名並獲取狀態訊息
initial_status_message = load_names_and_get_status()

# --- GUI Elements ---
# 主框架，增加一些邊距
main_frame = ttk.Frame(root, padding="20", style="TFrame")
main_frame.pack(fill=tk.BOTH, expand=True)

# 操作框架 (包含標籤、輸入框、按鈕)
action_frame = ttk.Frame(main_frame, padding=(0,0,0,10), style="TFrame") # Bottom padding
action_frame.pack(fill=tk.X)

ttk.Label(action_frame, text="輸入姓名:", style="TLabel").pack(side=tk.LEFT, padx=(0, 10))

# Entry with custom border Frame
entry_border_frame = ttk.Frame(action_frame, style="EntryBorder.TFrame", padding=2) # Padding acts as border thickness
entry_border_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

search_entry = ttk.Entry(entry_border_frame, width=35, style="Custom.TEntry")
search_entry.pack(fill=tk.BOTH, expand=True) # Entry fills the border frame
search_entry.config(font=(default_font_family, base_font_size + 1)) # Slightly larger font for entry
search_entry.focus()
# Change border color of the wrapper frame on focus
search_entry.bind("<FocusIn>", lambda e: entry_border_frame.config(style="Focus.EntryBorder.TFrame"))
search_entry.bind("<FocusOut>", lambda e: entry_border_frame.config(style="EntryBorder.TFrame"))
style.configure("Focus.EntryBorder.TFrame", background=entry_border_focus_color)


# 搜尋按鈕
search_button = ttk.Button(action_frame, text="搜尋", command=perform_search, width=10, style="TButton")
search_button.pack(side=tk.LEFT, ipady=2) # Internal y-padding to make button taller

# 結果顯示框架
result_frame = ttk.LabelFrame(main_frame, text="搜尋結果", style="TLabelFrame")
result_frame.pack(fill=tk.BOTH, expand=True, pady=(15,0)) # Top padding

result_text_widget = tk.Text(
    result_frame,
    wrap=tk.WORD,
    height=12, # 略微增加高度
    state=tk.DISABLED,
    background=widget_bg,
    foreground=text_fg,
    font=(default_font_family, base_font_size),
    relief=tk.SOLID, # Use solid relief
    bd=0, # Border handled by highlight
    highlightthickness=1, # This will be the main border
    highlightbackground=frame_bg, # Border color when not focused
    highlightcolor=accent_color, # Border color when focused
    padx=10, # Internal padding for text
    pady=10,
    insertbackground=text_fg, # Cursor color
    selectbackground=accent_color, # Selection color
    selectforeground=button_text_fg
)

result_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text_widget.yview, style="Vertical.TScrollbar")
result_text_widget.config(yscrollcommand=result_scrollbar.set)

result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,5), pady=(5,5))
result_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,0), pady=(5,5))

# --- Initial Message Display ---
# 根據載入狀態設定初始訊息
if "錯誤" in initial_status_message:
    update_result_display(initial_status_message)
elif "為空" in initial_status_message and not all_names_list: # 檔案存在但為空
    update_result_display(initial_status_message + "\n請在文件中添加姓名，或直接搜尋（將顯示查無此人）。")
elif "成功載入" in initial_status_message and all_names_list:
    update_result_display(initial_status_message + "\n請輸入姓名進行搜尋。")
else: # 其他情況，例如成功載入但列表為空（理論上被"為空"捕捉）
    update_result_display(initial_status_message)


# --- Bindings ---
# 允許在輸入框中按下 Enter 鍵觸發搜尋
root.bind('<Return>', lambda event: perform_search())

# --- Start GUI ---
root.mainloop()
