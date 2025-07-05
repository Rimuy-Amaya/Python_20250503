import streamlit as st
import yfinance as yf
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt # 導入 matplotlib
import plotly.graph_objects as go # plotly 已經存在，只是重新確認

# --- 字型設定調整 START ---
# 設置 Matplotlib 字型為通用字型，確保在 Linux 環境下也能正確顯示
# 'DejaVu Sans' 是 Matplotlib 預設支持的字型，通常在 Linux 環境下也存在
# 'sans-serif' 是一個通用字型家族，系統會選擇一個適合的無襯線字型
plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
# 解決 Matplotlib 負號顯示為方塊的問題 (如果圖表中有負數)
plt.rcParams['axes.unicode_minus'] = False
# --- 字型設定調整 END ---

def download_tw_stocks():
    stock_list = ['2330.TW', '2303.TW', '2454.TW', '2317.TW']
    from datetime import datetime
    today_str = datetime.today().strftime('%Y-%m-%d')
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    for stock in stock_list:
        stock_code = stock.split('.')[0]
        filename = f"{stock_code}_{today_str}.csv"
        filepath = os.path.join(data_dir, filename)
        # 檢查今天是否已經下載過這個檔案，避免重複下載
        if os.path.exists(filepath):
            # 可以加入一個檢查，如果檔案是舊的（例如不是今天的），則重新下載
            # 但為了簡潔，這裡假設只要存在就跳過
            continue
        df = yf.download(
            stock,
            start="2010-01-01",
            end=today_str,
            auto_adjust=False
        )
        df.to_csv(filepath)

def load_adjclose_dataframe():
    code_to_name = {
        '2330': '台積電',
        '2303': '聯電',
        '2454': '聯發科',
        '2317': '鴻海'
    }
    data_dir = 'data'
    series_dict = {}
    for code, name in code_to_name.items():
        files = [f for f in os.listdir(data_dir) if f.startswith(code+'_') and f.endswith('.csv')]
        if not files:
            continue
        # 確保文件是按日期降序排列，以便選取最新檔案
        files.sort(key=lambda x: x.split('_')[1].replace('.csv', ''), reverse=True)
        filepath = os.path.join(data_dir, files[0])
        df = pd.read_csv(filepath, index_col=0)
        df.index = pd.to_datetime(df.index, errors='coerce')
        df = df[~df.index.isna()]
        if 'Adj Close' in df.columns:
            series_dict[name] = df['Adj Close']
    result_df = pd.DataFrame(series_dict)
    return result_df

# --- Streamlit App Start ---
# 初始化 session_state
if 'start_date_selected' not in st.session_state:
    st.session_state.start_date_selected = None
if 'end_date_selected' not in st.session_state:
    st.session_state.end_date_selected = None

with st.spinner('正在下載最新的股票資料...'):
    download_tw_stocks()
with st.spinner('正在載入股票資料...'):
    df = load_adjclose_dataframe()

st.title("台股歷史股價視覺化")
st.write("本應用程式提供台股歷史股價查詢與視覺化功能。請選擇您感興趣的股票及日期區間，即可查看股價走勢圖與詳細數據。")

options = sorted(list(df.columns))
default = [name for name in options if "台積電" in name]
selected = st.multiselect(
    "請選擇股票（可複選）",
    options=options,
    default=default
)

if not df.empty:
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = pd.to_datetime(df.index, errors='coerce')
        df = df[~df.index.isna()]

    # 獲取最新資料中的日期範圍，而非今天的日期，因為下載的資料可能不是到今天
    max_data_date = df.index[-1].date()
    min_data_date = df.index[0].date()


    # 預設日期區間 (調整為從載入資料的最後7天)
    # 確保只有在df不為空且有足夠數據時才取日期
    if len(df.index) >= 7:
        last_7_dates = df.index[-7:]
        start_default = last_7_dates[0].date()
        end_default = last_7_dates[-1].date()
    else: # 如果資料不足7天，則取所有資料的範圍
        start_default = min_data_date
        end_default = max_data_date


    # 如果 session_state 中的日期為 None，則設定為預設值
    if st.session_state.start_date_selected is None:
        st.session_state.start_date_selected = start_default
    if st.session_state.end_date_selected is None:
        st.session_state.end_date_selected = end_default

    # 確保 session_state 中的日期在資料範圍內
    st.session_state.start_date_selected = max(st.session_state.start_date_selected, min_data_date)
    st.session_state.end_date_selected = min(st.session_state.end_date_selected, max_data_date)
    st.session_state.start_date_selected = min(st.session_state.start_date_selected, st.session_state.end_date_selected) # 確保開始日期不晚於結束日期

    # 快速選擇按鈕
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button('近一週'):
            st.session_state.start_date_selected = max((pd.Timestamp(max_data_date) - pd.Timedelta(weeks=1)).date(), min_data_date)
            st.session_state.end_date_selected = max_data_date
    with col2:
        if st.button('近一月'):
            st.session_state.start_date_selected = max((pd.Timestamp(max_data_date) - pd.Timedelta(days=30)).date(), min_data_date)
            st.session_state.end_date_selected = max_data_date
    with col3:
        if st.button('近三月'):
            st.session_state.start_date_selected = max((pd.Timestamp(max_data_date) - pd.Timedelta(days=90)).date(), min_data_date)
            st.session_state.end_date_selected = max_data_date
    with col4:
        if st.button('今年以來'):
            # 今年以來的計算應該基於資料的最新年份，而不是當前年份
            current_data_year = max_data_date.year
            st.session_state.start_date_selected = max(pd.to_datetime(f'{current_data_year}-01-01').date(), min_data_date)
            st.session_state.end_date_selected = max_data_date

    # 日期選擇器
    start_date_input = st.date_input("開始時間", value=st.session_state.start_date_selected, min_value=min_data_date, max_value=max_data_date)
    end_date_input = st.date_input("結束時間", value=st.session_state.end_date_selected, min_value=min_data_date, max_value=max_data_date)

    # 更新 session_state 中的日期 (確保日期順序正確)
    if start_date_input != st.session_state.start_date_selected:
        st.session_state.start_date_selected = start_date_input
    if end_date_input != st.session_state.end_date_selected:
        st.session_state.end_date_selected = end_date_input

    # 確保結束日期不早於開始日期
    if st.session_state.end_date_selected < st.session_state.start_date_selected:
        st.session_state.end_date_selected = st.session_state.start_date_selected

else:
    st.warning("資料為空，無法選擇日期。請檢查股票代碼或網路連線。")
    st.session_state.start_date_selected = None
    st.session_state.end_date_selected = None

if selected and st.session_state.start_date_selected and st.session_state.end_date_selected:
    # 調整 mask，因為 df.index 已經是 datetime 物件，直接比較即可
    mask = (df.index.date >= st.session_state.start_date_selected) & (df.index.date <= st.session_state.end_date_selected)
    filtered_df = df.loc[mask, selected]
    filtered_df = filtered_df.apply(pd.to_numeric, errors='coerce')
    filtered_df = filtered_df.dropna(axis=0, how='all').dropna(axis=1, how='all')

    if not filtered_df.empty:
        for col in filtered_df.columns:
            # 使用 plotly 繪圖，plotly 預設支持中文，不需要額外字型配置
            chart_data = filtered_df[[col]].round(0)
            st.subheader(f"{col} 股價走勢")
            # 動態調整y軸起始值
            min_val = chart_data.min().min()
            max_val = chart_data.max().max()
            margin = (max_val - min_val) * 0.1 if max_val > min_val else 1 # 避免除以零
            y_min = int(min_val - margin) if min_val - margin >= 0 else 0 # Y軸不能為負
            y_max = int(max_val + margin)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=chart_data.index, y=chart_data[col], mode='lines', name=col))
            fig.update_layout(
                yaxis=dict(range=[y_min, y_max], tickformat=',d'),
                xaxis_title="日期",
                yaxis_title="收盤價",
                showlegend=False,
                # 調整字型，確保中文顯示
                font=dict(
                    family="Arial, sans-serif", # Plotly 的字型設置，Arial 通常也是安全選擇
                    size=12,
                    color="#7f7f7f"
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        st.subheader("篩選後的股價資料")
        st.dataframe(filtered_df.round(2))
    else:
        st.info("所選區間內無可用數值資料，請調整日期範圍或股票選項。")
else:
    st.info("請選擇股票與日期區間")
# --- Streamlit App End ---