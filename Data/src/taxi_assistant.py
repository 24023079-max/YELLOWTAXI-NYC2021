import os
import pandas as pd

def load_data():
    """Hàm nạp dữ liệu thông minh, tự động dò đường tránh lỗi sập đường dẫn"""
    # 1. Định vị thư mục chứa file trợ lý hiện tại
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
    
    # 2. Các phương án đường dẫn có thể xảy ra (Quét cả file KPI lẫn file gốc)
    attempts = [
        # Phương án 1: Nếu file trợ lý nằm trong src/ hoặc src/source_figures/ (Lùi 2 tầng)
        os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "Data", "processed", "KPI_requirements", "kpi_daily_2021.csv")),
        # Phương án 2: Nếu file trợ lý nằm ngay trong thư mục gốc dự án
        os.path.abspath(os.path.join(CURRENT_DIR, "Data", "processed", "KPI_requirements", "kpi_daily_2021.csv")),
        # Phương án 3: Thử quét file Parquet tổng nếu bạn muốn trợ lý tính toán sâu hơn
        os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "Data", "processed", "yellow_tripdata_2021_full.parquet")),
        # Phương án 4: Ép cứng về đường dẫn tuyệt đối chuẩn trên máy bạn
        "D:/YELLOWTAXI-NYC2021/Data/processed/KPI_requirements/kpi_daily_2021.csv"
    ]
    
    FULL_PATH = None
    for path in attempts:
        if os.path.exists(path):
            FULL_PATH = path
            break

    # 3. Kiểm tra kết quả dò tìm
    if FULL_PATH is None:
        print("❌ LỖI CHÍ MẠNG: Trợ lý đã thử mọi cách nhưng vẫn không tìm thấy file dữ liệu!")
        print(f"📍 Thư mục hiện tại Trợ lý đang đứng quét là: {CURRENT_DIR}")
        print("💡 Hãy đảm bảo bạn đã chạy file code này bên trong thư mục dự án YELLOWTAXI-NYC2021 nhé.")
        return None
        
    print(f"📂 [Trợ lý] Đang nạp dữ liệu từ vị trí tìm thấy: {FULL_PATH}")
    
    # 4. Đọc file tương ứng với định dạng tìm được
    if FULL_PATH.endswith('.parquet'):
        return pd.read_parquet(FULL_PATH)
    return pd.read_csv(FULL_PATH)

def taxi_bot(user_question, df):
    """Bộ não xử lý câu hỏi của trợ lý ảo"""
    question = user_question.lower().strip()
    
    # Chuẩn bị trước một số thông tin nền cơ bản từ df để tính toán
    if 'pickup_hour' not in df.columns and 'tpep_pickup_datetime' in df.columns:
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour

    # --- LUẬT TRẢ LỜI 1: HỎI VỀ TỔNG SỐ CHUYẾN ĐI ---
    if "tổng số chuyến" in question or "bao nhiêu chuyến" in question:
        total_trips = len(df) if 'trip_count' not in df.columns else df['trip_count'].sum()
        return f"🤖 Trợ lý: Tổng số chuyến đi ghi nhận trong tập dữ liệu là {total_trips:,} chuyến."
    
    # --- LUẬT TRẢ LỜI 2: HỎI VỀ GIỜ CAO ĐIỂM ---
    elif "giờ cao điểm" in question or "đi nhiều nhất vào lúc mấy giờ" in question:
        if 'pickup_hour' in df.columns:
            hourly_rank = df.groupby('pickup_hour').size() if 'trip_count' not in df.columns else df.groupby('pickup_hour')['trip_count'].sum()
            peak_hour = hourly_rank.idxmax()
            return f"🤖 Trợ lý: Giờ cao điểm đón khách nhiều nhất trong ngày là lúc {peak_hour}h với tổng cộng {hourly_rank.max():,} chuyến đi."
        return "🤖 Trợ lý: Dữ liệu hiện tại không hỗ trợ cột thời gian theo giờ để tính toán."

    # --- LUẬT TRẢ LỜI 3: HỎI VỀ QUÃNG ĐƯỜNG ---
    elif "quãng đường trung bình" in question or "đi xa không" in question:
        if 'trip_distance' in df.columns:
            avg_distance = df['trip_distance'].mean()
            return f"🤖 Trợ lý: Quãng đường di chuyển trung bình của mỗi chuyến taxi là {avg_distance:.2f} dặm (khoảng {avg_distance*1.609:.2f} km)."
        return "🤖 Trợ lý: Rất tiếc, tập dữ liệu được nạp chưa có thông tin về quãng đường (trip_distance)."

    # --- LUẬT TRẢ LỜI 4: LỜI CHÀO ---
    elif "hello" in question or "chào" in question:
        return "🤖 Trợ lý: Xin chào! Tớ là trợ lý ảo phân tích dữ liệu Taxi New York 2021. Bạn muốn hỏi gì về dữ liệu nào?"
    
    # --- THOÁT ---
    elif "thoát" in question or "tạm biệt" in question:
        return "goodbye"

    # --- KHÔNG HIỂU ---
    else:
        return "🤖 Trợ lý: Tớ chưa hiểu câu hỏi này. Bạn có thể hỏi về 'tổng số chuyến', 'giờ cao điểm' hoặc 'quãng đường trung bình' nhé!"

# =============================================
# CHƯƠNG TRÌNH CHÍNH (MAIN LOOP)
# =============================================
if __name__ == "__main__":
    print("🤖 Đang khởi động Trợ lý ảo...")
    df_data = load_data()
    
    if df_data is not None:
        print("\n=======================================================")
        print("🚕 TRỢ LÝ ẢO TAXI NYC 2021 ĐÃ SẴN SÀNG TƯƠNG TÁC!")
        print("💡 Gõ 'thoát' hoặc 'tạm biệt' để dừng chương trình.")
        print("=======================================================\n")
        
        while True:
            user_input = input("👤 Bạn: ")
            response = taxi_bot(user_input, df_data)
            
            if response == "goodbye":
                print("🤖 Trợ lý: Tạm biệt bạn! Chúc bạn bảo vệ đồ án thật tốt.")
                break
            
            print(response)
            print("-" * 50)