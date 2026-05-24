# YELLOWTAXI-NYC2021
Python Pandas Matplotlib

📖 1. Tổng Quan Dự Án
1.1. Tải dữ liệu thô: python download_data.py

Script này sẽ tự động tải dữ liệu từ nguồn chính thức: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

1.2. Chạy notebook: Các file notebook nằm trong thư mục: Data/src/

Kết quả KPI
Sau khi chạy notebook, kết quả sẽ tạo ở:

Data/processed/KPI_requirements/kpi_daily_2021.csv
Data/processed/KPI_requirements/kpi_weekly_2021.csv
Data/processed/KPI_requirements/kpi_monthly_2021.csv Dự án này tập trung xử lý dữ liệu thô (Raw Data) của các chuyến xe taxi, tính toán các chỉ số KPI quan trọng và trực quan hóa dữ liệu để trả lời các câu hỏi kinh doanh như:
"Doanh thu thay đổi thế nào theo số lượng chuyến đi?" hay "Tốc độ di chuyển ảnh hưởng gì đến hiệu suất?"

📂 2. Cấu Trúc Thư Mục
Dưới đây là sơ đồ tổ chức file của nhóm:

Thư mục / File	Loại	Mô tả chi tiết
.idea/	⚙️	Cấu hình IDE (IntelliJ / PyCharm / VS Code).
Data/raw/	🗄️	Dữ liệu thô ban đầu, chưa qua xử lý.
Data/processed/	⚙️	Dữ liệu đã được xử lý và chuẩn hóa.
Data/processed/KPI_requirements/	📑	Dữ liệu KPI cuối cùng dùng cho phân tích và trực quan hóa.
Data/processed/clean_data/	🧹	Dữ liệu đã làm sạch.
Data/processed/bad_data/	⚠️	Dữ liệu lỗi / bất thường phục vụ kiểm tra chất lượng.
Data/processed/flex_fare/	💰	Dữ liệu liên quan đến giá cước linh hoạt.
Data/figures/	📊	Nơi lưu các biểu đồ kết quả (PNG, JPG).
Data/reports/	📝	Báo cáo trung gian và kết quả xuất.
Data/src/	🧑‍💻	Mã nguồn xử lý dữ liệu, phân tích và mô hình hóa.
Data/src/ML/	🤖	Notebook Machine Learning & dự báo.
Data/src/calcular_KPI/	📐	Module tính toán các chỉ số KPI.
Data/src/source_clean/	🧹	Module làm sạch và kiểm tra dữ liệu.
Data/src/source_figures/	📈	Module trực quan hóa dữ liệu và vẽ biểu đồ.
download_data.py	⬇️	Script tải dữ liệu từ nguồn bên ngoài.
pattern_clustering.ipynb	🔍	Notebook phân tích và phân cụm dữ liệu.
.gitignore	🚫	Cấu hình Git ignore.
README.md	📘	Hướng dẫn và mô tả tổng quan dự án.
requirements.txt	📄	Danh sách thư viện Python cần cài đặt.
Project-Root/
├── .idea/                         # Cấu hình IDE
├── Data/
│   ├── figures/                   # 📊 Ảnh biểu đồ kết quả
│   ├── raw/                       # Dữ liệu thô ban đầu
│   ├── processed/                 # Dữ liệu đã xử lý
│   │   ├── KPI_requirements/      # Dữ liệu KPI cuối cùng
│   │   ├── clean_data/            # Dữ liệu sạch
│   │   ├── bad_data/              # Dữ liệu lỗi / ngoại lệ
│   │   └── flex_fare/             # Dữ liệu giá cước linh hoạt
│   ├── reports/                   # Báo cáo & kết quả xuất
│   └── src/                       # Mã nguồn chính
│       ├── ML/                    # Machine Learning & Forecast
│       │   └── advanced_ml_forecast.ipynb
│       ├── calcular_KPI/          # Tính toán KPI
│       │   └── KPI_requirement.ipynb
│       ├── source_clean/          # Làm sạch dữ liệu
│       ├── source_figures/        # Trực quan hóa
│       │   ├── figures_KPI.ipynb
│       │   └── visualization.ipynb
│       ├── download_data.py       # Script tải dữ liệu
│       └── pattern_clustering.ipynb
├── .gitignore                     # Cấu hình Git ignore
├── README.md                      # Hướng dẫn dự án
└── requirements.txt               # Thư viện cần thiết

📊 3. Kết Quả Trực Quan Hóa (Highlights)
🚀 4. Hướng Dẫn Cài Đặt & Chạy Code
Để tái hiện lại kết quả nghiên cứu, vui lòng làm theo các bước sau:

Bước 1: Cài đặt thư viện Mở terminal tại thư mục gốc và chạy lệnh:

pip install -r requirements.txt
Để đảm bảo dự án chạy mượt mà và không xung đột thư viện, vui lòng thực hiện theo đúng trình tự sau:

1️⃣ Chuẩn bị môi trường
Yêu cầu máy tính đã cài đặt:

Python (Phiên bản 3.8 trở lên).
VS Code (khuyên dùng) hoặc PyCharm.
Jupyter Extension (nếu dùng VS Code).
2️⃣ Thiết lập Môi trường ảo (Virtual Environment)
Dự án khuyến khích sử dụng môi trường ảo để quản lý thư viện. Mở Terminal (CMD/PowerShell) tại thư mục gốc của dự án và chạy lệnh:

# Tạo môi trường ảo (nếu chưa có folder .venv)
python -m venv .venv

# Kích hoạt môi trường:
# -> Trên Windows:
.venv\Scripts\activate

# -> Trên macOS/Linux:
source .venv/bin/activate
3️⃣ Kiểm tra dữ liệu đầu vào
3. Luồng xử lý dữ liệu
3.1. Tải dữ liệu
Sử dụng file download_data.py để tải dữ liệu Yellow Taxi Trip Data năm 2021
Dữ liệu gốc được lưu tại: Data/raw/
3.2. Làm sạch dữ liệu
Module: src/source_clean/
Các bước kiểm tra chính:

Thời gian chuyến đi (trip duration)
Khoảng cách di chuyển (trip distance)
Tốc độ di chuyển
Doanh thu và các khoản phụ phí
Phân loại dữ liệu sau khi xử lý:

Clean data – dữ liệu hợp lệ
Bad data – dữ liệu lỗi / không hợp lệ
Flex fare trips – các chuyến không tính theo đồng hồ
3.3. Tính toán KPI
Module: src/calcular_KPI/
Các KPI chính:

Số chuyến đi (Trips)
Doanh thu (Revenue)
Thời gian và quãng đường di chuyển
Output:

kpi_daily_2021.csv – KPI theo ngày
kpi_monthly_2021.csv – KPI theo tháng
3.4. Phân tích nâng cao (Machine Learning)
Module: src/ML/
Kỹ thuật sử dụng:

Chuẩn hóa dữ liệu bằng StandardScaler
Phân cụm bằng KMeans Clustering
Mục tiêu:

Phân nhóm các khu vực đón khách (Pickup Zones) dựa trên hành vi di chuyển và doanh thu
3.5. Trực quan hóa
Module: src/source_figures/
Các biểu đồ chính:

KPI theo ngày / tháng
So sánh đặc điểm giữa các cluster
Phân bố doanh thu và số chuyến đi
Output:

Các file ảnh (.png) được lưu tại: Data/figures/
4️⃣ Cài đặt thư viện phụ thuộc
Sau khi kích hoạt môi trường ảo, chạy lệnh sau để tải toàn bộ thư viện cần thiết:

pip install -r requirements.txt
5. Cách chạy dự án
5.1. Kích hoạt môi trường ảo
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
5.2. Tải dữ liệu
python src/download_data.py

5.3. Chạy notebook
Thực hiện lần lượt các notebook để: Làm sạch dữ liệu Tính toán KPI Phân tích Machine Learning Vẽ biểu đồ trực quan
