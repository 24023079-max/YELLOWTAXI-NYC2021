import os
import requests

os.makedirs("Data/raw", exist_ok=True)
os.makedirs("Data/processed", exist_ok=True)

# tải dữ liệu theo tháng
for m in range(1, 13):
    month = f"{m:02d}"
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-{month}.parquet"
    path = f"Data/raw/yellow_tripdata_2021-{month}.parquet"

    if not os.path.exists(path):
        print("Downloading:", month)
        r = requests.get(url)
        with open(path, "wb") as f:
            f.write(r.content)

# tải thêm file taxi zone lookup
lookup_url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
lookup_path = "Data/raw/taxi_zone_lookup.csv"

if not os.path.exists(lookup_path):
    print("Downloading: taxi_zone_lookup.csv")
    r = requests.get(lookup_url)
    with open(lookup_path, "wb") as f:
        f.write(r.content)

print("DONE")