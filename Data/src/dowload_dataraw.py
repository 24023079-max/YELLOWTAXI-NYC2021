import os
import requests

months = range(1, 13)
os.makedirs("Data/raw", exist_ok=True)

for m in months:
    month = f"{m:02d}"
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-{month}.parquet"
    filename = f"yellow_tripdata_2021-{month}.parquet"

    print("Downloading:", filename)
    r = requests.get(url)

    with open(f"Data/raw/{filename}", "wb") as f:
        f.write(r.content)

print("DONE!")