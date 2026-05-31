import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path.cwd()
while PROJECT_ROOT != PROJECT_ROOT.parent and not (PROJECT_ROOT / 'Data').exists():
    PROJECT_ROOT = PROJECT_ROOT.parent

DATA_DIR = PROJECT_ROOT / 'Data'
CLEAN_DATA_DIR = DATA_DIR / 'processed' / 'clean_data'
FIGURE_DIR = DATA_DIR / 'figures'
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title='Taxi Data Assistant',
    page_icon='🚕',
    layout='wide',
)

@st.cache_data
def load_clean_data():
    files = sorted(CLEAN_DATA_DIR.glob('clean_2021-*.parquet'))
    columns = ['tpep_pickup_datetime', 'trip_distance', 'total_amount', 'passenger_count']
    df_list = [pd.read_parquet(path, columns=columns) for path in files]
    df = pd.concat(df_list, ignore_index=True)
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
    return df

@st.cache_data
def load_summary(df):
    total_trips = len(df)
    income = df['total_amount'].sum()
    avg_distance = df['trip_distance'].mean()
    median_distance = df['trip_distance'].median()
    trips_by_hour = df.groupby('pickup_hour').size().reindex(range(24), fill_value=0)
    return {
        'total_trips': int(total_trips),
        'income': float(income),
        'avg_distance': float(avg_distance),
        'median_distance': float(median_distance),
        'trips_by_hour': trips_by_hour,
    }

@st.cache_data
def load_saved_images():
    return {
        'distance': FIGURE_DIR / 'trip_distance_distribution.png',
        'hourly': FIGURE_DIR / 'trips_by_hour_line.png',
    }

def keyword_response(query: str, summary: dict) -> str:
    normalized = query.lower()
    if re.search(r'qu[aá]ng d[ưư]o[ạa]ng|distance|km', normalized):
        return (
            f"Tổng số chuyến đi: {summary['total_trips']:,}. "
            f"Quãng đường trung bình {summary['avg_distance']:.2f} km và trung vị {summary['median_distance']:.2f} km. "
            "Biểu đồ phân bố quãng đường đã được lưu trong Data/figures/."
        )
    if re.search(r'gi[oờ]|hour|th[gh]i', normalized):
        return (
            "Biểu đồ đường lượng chuyến theo giờ đang hiển thị bên dưới. "
            "Trục Y được đồng bộ đến 1.2 triệu chuyến để so sánh dễ dàng."
        )
    if re.search(r't[oổ]ng chuy[eế]n|s[ốo] chuy[eế]n|trips|count', normalized):
        return f"Tổng cộng có {summary['total_trips']:,} chuyến đi đã được ghi nhận trong dữ liệu sạch năm 2021."
    if re.search(r'doanh thu|revenue|ti[eê]p thu|t[oố]ng ti[eê]n', normalized):
        return f"Tổng doanh thu ước tính khoảng {summary['income']:.2f} USD từ dữ liệu đã làm sạch."
    return (
        "Xin chào! Tôi là Trợ lý Taxi Data.\n"
        "Bạn có thể hỏi về: quãng đường, giờ chạy, tổng số chuyến, hoặc doanh thu.\n"
        "Ví dụ: 'Cho tôi biết lượng chuyến theo giờ' hoặc 'Phân bố quãng đường như thế nào?'."
    )

st.title('Trợ lý ảo Yellow Taxi 2021')
st.write(
    'Sử dụng dữ liệu đã làm sạch từ `Data/processed/clean_data/` để trả lời nhanh các câu hỏi về quãng đường, lượng chuyến và doanh thu.'
)

data = load_clean_data()
summary = load_summary(data)
images = load_saved_images()

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader('Tổng quan dữ liệu')
    st.metric('Tổng số chuyến đi', f"{summary['total_trips']:,}")
    st.metric('Quãng đường trung bình', f"{summary['avg_distance']:.2f} km")
    st.metric('Doanh thu tổng', f"${summary['income']:.2f}")
    
    st.subheader('Biểu đồ lượng chuyến theo giờ')
    fig, ax = plt.subplots(figsize=(10, 4))
    summary['trips_by_hour'].plot(ax=ax, color='#0077b6', marker='o')
    ax.set_xlabel('Giờ trong ngày')
    ax.set_ylabel('Số chuyến đi')
    ax.set_title('Lượng chuyến đi theo giờ (24h)')
    ax.set_ylim(0, 1_200_000)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    st.caption('Trục Y được mở rộng đến 1.2 triệu chuyến để đồng bộ quy mô hiển thị.')

with col2:
    st.subheader('Hình ảnh đã lưu')
    if images['distance'].exists():
        st.image(str(images['distance']), caption='Phân bố quãng đường', use_column_width=True)
    if images['hourly'].exists():
        st.image(str(images['hourly']), caption='Lượng chuyến theo giờ', use_column_width=True)

st.markdown('---')

st.subheader('Hỏi trợ lý ảo')
query = st.text_input('Nhập câu hỏi của bạn', 'Phân bố quãng đường như thế nào?')
if query:
    answer = keyword_response(query, summary)
    st.info(answer)

st.markdown('### Một số câu hỏi gợi ý')
st.write('- Quãng đường di chuyển trung bình?')
st.write('- Lượng chuyến theo giờ hôm nay ra sao?')
st.write('- Tổng số chuyến trong dữ liệu?')
st.write('- Doanh thu ước tính?')
