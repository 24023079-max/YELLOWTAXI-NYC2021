from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

ROOT = Path.cwd()
while ROOT != ROOT.parent and not (ROOT / 'Data').exists():
    ROOT = ROOT.parent

CLEAN_DIR = ROOT / 'Data' / 'processed' / 'clean_data'
FIGURE_DIR = ROOT / 'Data' / 'figures'
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

files = sorted(CLEAN_DIR.glob('clean_2021-*.parquet'))
if not files:
    raise FileNotFoundError('Không tìm thấy file clean_2021-*.parquet trong Data/processed/clean_data')

print(f'Load {len(files)} clean files...')
columns = ['tpep_pickup_datetime', 'trip_distance', 'total_amount']
df = pd.concat([pd.read_parquet(path, columns=columns) for path in files], ignore_index=True)
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour

# Save trip distance distribution
plt.figure(figsize=(12, 6))
sns.set(style='whitegrid', palette='deep')
ax = sns.histplot(df['trip_distance'].clip(upper=50), bins=80, kde=False, color='#2a9d8f')
ax.set_title('Phân bố quãng đường di chuyển (km) - Yellow Taxi 2021', fontsize=16)
ax.set_xlabel('Trip Distance (km)')
ax.set_ylabel('Số chuyến đi')
ax.set_ylim(0, 1_200_000)
ax.set_xlim(0, 50)
plt.tight_layout()
trip_dist_path = FIGURE_DIR / 'trip_distance_distribution.png'
plt.savefig(trip_dist_path, dpi=200)
plt.close()
print(f'Saved {trip_dist_path}')

# Save trips by hour-of-day line plot
hourly_counts = df.groupby('pickup_hour').size().reindex(range(24), fill_value=0).rename('trip_count')
max_hourly = int(hourly_counts.max() * 1.05)
plt.figure(figsize=(14, 6))
ax = sns.lineplot(x=hourly_counts.index, y=hourly_counts.values, marker='o', color='#e76f51')
ax.set_title('Lượng chuyến đi theo giờ trong ngày - Yellow Taxi 2021', fontsize=16)
ax.set_xlabel('Giờ trong ngày (0-23)')
ax.set_ylabel('Tổng số chuyến đi trong năm')
ax.set_xticks(range(24))
ax.set_ylim(0, max_hourly)
plt.tight_layout()
hourly_path = FIGURE_DIR / 'trips_by_hour_line.png'
plt.savefig(hourly_path, dpi=200)
plt.close()
print(f'Saved {hourly_path}')

print('Đã lưu xong các biểu đồ vào Data/figures/')
