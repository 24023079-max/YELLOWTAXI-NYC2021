import streamlit as st
import pandas as pd
import os
import glob

# =====================================================================
# CẤU HÌNH TRANG WEB
# =====================================================================
st.set_page_config(
    page_title="NYC Taxi AI Assistant",
    page_icon="🚕",
    layout="wide"
)

st.title("🚕 NYC Taxi AI Assistant")
st.markdown("Hỏi tôi bất kỳ điều gì về hệ thống Taxi NYC 2021!")

# =====================================================================
# HÀM TẢI DỮ LIỆU SẠCH (TỪ processed/clean_data/)
# =====================================================================
@st.cache_data
def load_all_clean_data():
    """
    Tự động tìm và gộp tất cả các file clean_2021-*.parquet trong thư mục.
    """
    
    # Đường dẫn từ thư mục Data/src/
    base_path = "Data/processed/clean_data"
    
    if not os.path.exists(base_path):
        st.error(f"❌ Không tìm thấy thư mục: {base_path}")
        return pd.DataFrame()
    
    # Tìm tất cả file
    files = sorted(glob.glob(f"{base_path}/clean_2021-*.parquet"))
    
    if len(files) == 0:
        st.error("❌ Không tìm thấy file dữ liệu sạch!")
        return pd.DataFrame()
    
    # Đọc và gộp
    dfs = []
    for f in files:
        df_month = pd.read_parquet(f)
        dfs.append(df_month)
    
    full_df = pd.concat(dfs, ignore_index=True)
    st.success(f"✅ Đã load dữ liệu sạch: {len(full_df):,} chuyến đi từ {len(files)} tháng")
    
    return full_df

# =====================================================================
# HÀM TẢI QA IMPACT
# =====================================================================
@st.cache_data
def load_qa_impact():
    path = "Data/processed/qa_impact_analysis.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

# =====================================================================
# HÀM TẢI PHÂN CỤM
# =====================================================================
@st.cache_data
def load_cluster_data():
    cluster_path = "Data/processed/advanced_pattern/cluster_summary.csv"
    if os.path.exists(cluster_path):
        return pd.read_csv(cluster_path)
    return pd.DataFrame()

# =====================================================================
# BỘ NÃO XỬ LÝ CÂU HỎI
# =====================================================================
def get_bot_response(user_input, df, qa_df, cluster_df):
    user_input = user_input.lower()
    
    response = "Xin lỗi, tôi chưa hiểu rõ. Thử hỏi: 'Tổng doanh thu?', 'Số chuyến?', 'Tip?', 'Khoảng cách?', 'Giờ cao điểm?'"
    
    if "số chuyến" in user_input or "trip" in user_input:
        total = len(df)
        response = f"Hệ thống có tổng cộng **{total:,}** chuyến đi trong năm 2021."
    
    elif "doanh thu" in user_input or "revenue" in user_input:
        revenue = df["total_amount"].sum()
        response = f"Tổng doanh thu là **${revenue:,.2f}**."
    
    elif "cước" in user_input or "fare" in user_input:
        fare = df["fare_amount"].sum()
        response = f"Tổng tiền cước cơ bản là **${fare:,.2f}**."
    
    elif "tip" in user_input:
        avg_tip = df["tip_amount"].mean()
        total_tip = df["tip_amount"].sum()
        response = f"💰 Tổng tip: **${total_tip:,.2f}**\n\nTrung bình: **${avg_tip:.2f}**"
    
    elif "khoảng cách" in user_input or "dặm" in user_input or "distance" in user_input:
        avg_dist = df["trip_distance"].mean()
        response = f"📍 Khoảng cách trung bình: **{avg_dist:.2f}** dặm."
    
    elif "thời gian" in user_input or "phút" in user_input:
        avg_duration = df["trip_duration"].mean()
        response = f"⏱️ Thời gian trung bình: **{avg_duration:.2f}** phút."
    
    elif "tốc độ" in user_input or "speed" in user_input:
        if "speed_mph" in df.columns:
            avg_speed = df["speed_mph"].mean()
            response = f"🚀 Tốc độ trung bình: **{avg_speed:.2f}** dặm/giờ."
    
    elif "giờ cao điểm" in user_input or "peak" in user_input:
        if "tpep_pickup_datetime" in df.columns:
            df["pickup_hour"] = pd.to_datetime(df["tpep_pickup_datetime"]).dt.hour
            hour_counts = df.groupby("pickup_hour").size()
            peak_hour = hour_counts.idxmax()
            response = f"🕒 Giờ cao điểm: **{peak_hour}:00** ({hour_counts[peak_hour]:,} chuyến)."
    
    elif "chất lượng" in user_input or "qa" in user_input:
        if not qa_df.empty:
            total_risk = qa_df['revenue_risk'].sum()
            response = f"📊 QA: Đã loại bỏ *${total_risk:,.2f}** doanh thu nhiễu."
    
    elif "vùng" in user_input or "location" in user_input:
        top_pu = df['PULocationID'].value_counts().head(5)
        response = f"📍 Top 5 vùng đón khách:\n" + "\n".join([f"- Vùng {k}: {v:,} chuyến" for k, v in top_pu.items()])
    
    elif "cụm" in user_input or "cluster" in user_input:
        if not cluster_df.empty:
            response = f"📊 Phân cụm:\n\n" + cluster_df.to_string(index=False)
        else:
            response = "Chưa có kết quả phân cụm."
    
    return response

# =====================================================================
# MAIN
# =====================================================================
def main():
    with st.spinner("Đang tải dữ liệu..."):
        df = load_all_clean_data()
        qa_df = load_qa_impact()
        cluster_df = load_cluster_data()
    
    if not df.empty:
        st.caption(f"📊 Data: {len(df):,} rows × {df.shape[1]} cols")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("Bạn muốn hỏi gì?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        response = get_bot_response(prompt, df, qa_df, cluster_df)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    main()