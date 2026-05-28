import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NYC Taxi Assistant", page_icon="🚕", layout="centered")
st.title("🚕 Trợ lý ảo Phân tích Dữ liệu Taxi NYC")
st.write("Đặt câu hỏi trực tiếp để trợ lý ảo trích xuất số liệu thời gian thực từ hệ thống.")

# Hàm nạp dữ liệu tối ưu lưu vào Cache của Streamlit để tránh load lại gây chậm web
@st.cache_data
def load_data_web():
    # 1. Các thư mục gốc có khả năng chứa dữ liệu cao nhất trên máy bạn
    base_folders = [
        "D:/YELLOWTAXI-NYC2021/Data/processed",
        "D:/YELLOWTAXI-NYC2021/Data/raw",
        "D:/YELLOWTAXI-NYC2021/Data"
    ]
    
    # 2. Cơ chế quét sâu (Deep Scan) tìm file .parquet thích hợp
    for folder in base_folders:
        if os.path.exists(folder):
            # Đi xuyên qua tất cả thư mục con bên trong (như clean_data, KPI_requirements...)
            for root, dirs, files in os.walk(folder):
                for file in files:
                    # Nếu thấy file parquet của Yellow Taxi
                    if file.endswith('.parquet') and "yellow" in file.lower():
                        full_path = os.path.join(root, file)
                        try:
                            # Tiến hành đọc file và trả về ngay lập tức
                            return pd.read_parquet(full_path, columns=['tpep_pickup_datetime', 'trip_distance', 'PULocationID'])
                        except Exception:
                            continue
                            
                    # Dự phòng: Nếu không thấy file parquet tổng lớn, nạp tạm file kpi daily dạng csv để chatbot chạy đỡ
                    elif file.endswith('.csv') and "kpi" in file.lower():
                        full_path = os.path.join(root, file)
                        try:
                            df_csv = pd.read_csv(full_path)
                            # Đồng bộ tên cột nếu là file KPI daily để code bên dưới không bị gãy
                            if 'trip_count' in df_csv.columns and 'tpep_pickup_datetime' not in df_csv.columns:
                                df_csv['tpep_pickup_datetime'] = pd.to_datetime('2021-01-01') # Tạo cột giả lập thời gian
                            return df_csv
                        except Exception:
                            continue
    return None

df = load_data_web()

if df is None:
    st.error("❌ Trợ lý ảo đã lùng sục toàn bộ thư mục Data nhưng không thấy file .parquet hoặc .csv nào chứa dữ liệu taxi cả. Bạn hãy kiểm tra xem file đang cất ở đâu nhé!")
else:
    # Khởi tạo lịch sử chat nếu chưa có
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Xin chào! Tớ là trợ lý ảo Taxi NYC. Hôm nay bạn muốn tra cứu số liệu gì nào?"}]

    # Hiển thị các tin nhắn cũ
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Nhận tin nhắn mới từ người dùng
    if user_query := st.chat_input("Nhập câu hỏi của bạn (Ví dụ: Tổng số chuyến đi là bao nhiêu?)..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        query_lower = user_query.lower().strip()
        with st.chat_message("assistant"):
            with st.spinner("Đang truy vấn cơ sở dữ liệu..."):
                
                if "tổng số chuyến" in query_lower or "bao nhiêu chuyến" in query_lower:
                    total_trips = len(df) if 'trip_count' not in df.columns else df['trip_count'].sum()
                    ans = f"Tổng số chuyến đi ghi nhận được trong hệ thống là **{total_trips:,}** chuyến."
                
                elif "quãng đường" in query_lower:
                    if 'trip_distance' in df.columns:
                        ans = f"Quãng đường di chuyển trung bình của các chuyến taxi đạt **{df['trip_distance'].mean():.2f} dặm**."
                    else:
                        ans = "Tập dữ liệu hiện tại đã được gom cụm nên không chứa cột thông tin chi tiết về quãng đường đơn lẻ."
                
                elif "giờ cao điểm" in query_lower or "mấy giờ" in query_lower:
                    if 'trip_count' in df.columns and 'pickup_hour' in df.columns:
                        peak = df.groupby('pickup_hour')['trip_count'].sum().idxmax()
                        ans = f"Dựa trên dữ liệu thu thập, giờ cao điểm đón khách nhiều nhất là lúc **{peak}h**."
                    else:
                        pickup_hours = pd.to_datetime(df['tpep_pickup_datetime']).dt.hour
                        peak = pickup_hours.value_counts().idxmax()
                        ans = f"Dựa trên biểu đồ tần suất, giờ cao điểm đón khách nhiều nhất trong ngày là lúc **{peak}h**."
                else:
                    ans = "Tớ chưa được lập trình để trả lời câu hỏi này. Bạn thử hỏi về: *tổng số chuyến đi*, *quãng đường trung bình* hoặc *giờ cao điểm* xem sao nhé!"
                
                st.write(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})