import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def to_date_key(date_series):
    is_missing = date_series.isna()
    safe_series = date_series.fillna(pd.Timestamp('1900-01-01'))
    date_key = safe_series.dt.strftime('%Y%m%d').astype(int)
    return date_key.where(~is_missing, -1)



# 1. CẤU HÌNH ĐƯỜNG DẪN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, 'input')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

RAW_DATA_PATH = os.path.join(INPUT_DIR, 'hotel_bookings.csv')
CLEANED_DATA_PATH = os.path.join(OUTPUT_DIR, 'staging_cleaned_bookings.csv')
ERROR_LOG_PATH = os.path.join(OUTPUT_DIR, 'error_log_bookings.csv')
AGG_PATH = os.path.join(OUTPUT_DIR, 'agg_revenue_by_month.csv')
EXCEL_STAR_SCHEMA_PATH = os.path.join(OUTPUT_DIR, 'Hotel_Booking_StarSchema.xlsx')
REPORT_HTML_PATH = os.path.join(OUTPUT_DIR, 'profiling_report.html')

print("=" * 70)
print("BẮT ĐẦU DATA PROFILING và ETL ")
print("=" * 70)

# 2. ĐỌC DỮ LIỆU THÔ
if not os.path.exists(RAW_DATA_PATH):
    raise FileNotFoundError(f"Không tìm thấy file dữ liệu gốc tại: {RAW_DATA_PATH}")

df_raw = pd.read_csv(RAW_DATA_PATH, low_memory=False)
print(f"\n[EXTRACT] Đã tải thành công: {len(df_raw):,} dòng × {len(df_raw.columns)} cột")

# 3. DATA PROFILING
print("\n" + "=" * 70)
print("1. DATA PROFILING")
print("=" * 70)

print(f"\n• Tổng số dòng          : {len(df_raw):,}")
print(f"• Tổng số cột           : {len(df_raw.columns)}")
print(f"• Kỳ dữ liệu            : {df_raw['arrival_date_year'].min()} – {df_raw['arrival_date_year'].max()}")
print(f"• Số loại khách sạn     : {df_raw['hotel'].nunique()} → {df_raw['hotel'].unique().tolist()}")

nulls = df_raw.isnull().sum()
nulls = nulls[nulls > 0].sort_values(ascending=False)
print("\n• Giá trị NULL:")
for col, cnt in nulls.items():
    pct = cnt / len(df_raw) * 100
    print(f"    - {col:25s}: {cnt:>7,} dòng ({pct:5.2f}%)")

n_dup = df_raw.duplicated().sum()
print(f"\n• Dòng trùng lặp hoàn toàn: {n_dup:,} ({n_dup/len(df_raw)*100:.1f}%)")

print("\n• Bất thường nghiệp vụ:")
print(f"    - adr < 0              : {(df_raw['adr'] < 0).sum()} dòng")
print(f"    - adults=children=babies=0 : {((df_raw['adults']==0) & (df_raw['children'].fillna(0)==0) & (df_raw['babies']==0)).sum()} dòng")
print(f"    - total_nights = 0     : {((df_raw['stays_in_weekend_nights'] + df_raw['stays_in_week_nights']) == 0).sum()} dòng")
print(f"    - meal = 'Undefined'   : {(df_raw['meal'] == 'Undefined').sum()} dòng")

try:
    from ydata_profiling import ProfileReport
    print("\n-> Đang tạo báo cáo Profiling HTML...")
    profile = ProfileReport(
        df_raw,
        title="Báo cáo khảo sát chất lượng dữ liệu Hotel Booking",
        explorative=True,
        minimal=True
    )
    profile.to_file(REPORT_HTML_PATH)
    print(f" [OK] Báo cáo: {REPORT_HTML_PATH}")
except ImportError:
    print("\n[INFO] Chưa cài nên bỏ qua báo cáo.")
except Exception as e:
    print(f"\n[WARNING] Không tạo báo cáo: {e}")

# 4. TRANSFORMATIONS
print("\n" + "=" * 70)
print("2–8. CÁC PHÉP BIẾN ĐỔI & LÀM SẠCH")
print("=" * 70)

df = df_raw.copy()

# 1. Xóa trùng
len_before = len(df)
df = df.drop_duplicates()
print(f"1. Xóa trùng lặp hoàn toàn     : {len_before - len(df):,} dòng → còn {len(df):,}")

# 2. Trim
str_cols = df.select_dtypes(include=['object']).columns.tolist()
for col in str_cols:
    df[col] = df[col].astype(str).str.strip().replace({'nan': np.nan, 'None': np.nan, 'NULL': np.nan})
print(f"2. Trim khoảng trắng           : {len(str_cols)} cột chuỗi")

# 3. NULL
df['country']  = df['country'].fillna('UNK')
df['agent']    = df['agent'].fillna('NONE')
df['company']  = df['company'].fillna('NONE')
df['children'] = df['children'].fillna(0)
print("3. Xử lý NULL: country→UNK, agent→NONE, company→NONE, children→0")

# 4. Conversion
def to_agent_code(x):
    if x == 'NONE' or pd.isna(x):
        return 'NONE'
    try:
        return f"A-{int(float(x))}"
    except Exception:
        return str(x)

def to_company_code(x):
    if x == 'NONE' or pd.isna(x):
        return 'NONE'
    try:
        return f"C-{int(float(x))}"
    except Exception:
        return str(x)

df['agent']   = df['agent'].apply(to_agent_code)
df['company'] = df['company'].apply(to_company_code)
df['children'] = df['children'].astype(int)
df['meal'] = df['meal'].replace('Undefined', 'SC')

month_map = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
}
df['arrival_date_month_num'] = df['arrival_date_month'].map(month_map)
df['arrival_full_date'] = pd.to_datetime(
    dict(
        year=df['arrival_date_year'],
        month=df['arrival_date_month_num'],
        day=df['arrival_date_day_of_month']
    ),
    errors='coerce'
)
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')
print("4. Data Conversion: agent/company, meal SC, arrival_full_date, reservation_status_date")

# 5. Derived
df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
df['total_guests'] = df['adults'] + df['children'] + df['babies']
df['revenue'] = df['adr'] * df['total_nights']
df['booking_year_month'] = df['arrival_full_date'].dt.strftime('%Y-%m')
df['room_changed_flag'] = (df['reserved_room_type'] != df['assigned_room_type']).astype(int)
print("5. Derived Column: total_nights, total_guests, revenue, booking_year_month, room_changed_flag")

# 6. Conditional Split
mask_valid = (
    (df['adr'] >= 0) &
    (df['total_guests'] > 0) &
    (df['total_nights'] > 0)
)
df_valid = df[mask_valid].copy()
df_error = df[~mask_valid].copy()

def get_error_reason(row):
    reasons = []
    if row['adr'] < 0:
        reasons.append('adr_am')
    if row['total_guests'] <= 0:
        reasons.append('khong_co_khach')
    if row['total_nights'] <= 0:
        reasons.append('khong_co_dem')
    return ';'.join(reasons)

df_error['error_reason'] = df_error.apply(get_error_reason, axis=1)
print(f"6. Conditional Split: Valid={len(df_valid):,} | Error={len(df_error):,}")

# 7. Sort
df_valid = df_valid.sort_values('arrival_full_date').reset_index(drop=True)
print("7. Sort theo arrival_full_date")

# 8. Aggregate
agg = (
    df_valid
    .groupby(['hotel', 'booking_year_month'], as_index=False)
    .agg(
        total_bookings=('hotel', 'count'),
        total_revenue=('revenue', 'sum'),
        avg_adr=('adr', 'mean')
    )
    .sort_values(['hotel', 'booking_year_month'])
)
print(f"8. Aggregate Hotel×Tháng: {len(agg)} dòng | SUM bookings={agg['total_bookings'].sum():,}")

print("9. Union All: Không áp dụng (chỉ 1 nguồn hotel_bookings.csv)")

# 5. XUẤT FILE
print("\n" + "=" * 70)
print("XUẤT FILE...")
print("=" * 70)

df_valid.to_csv(CLEANED_DATA_PATH, index=False, encoding='utf-8-sig')
print(f"• staging_cleaned_bookings.csv : {len(df_valid):,} dòng")

df_error.to_csv(ERROR_LOG_PATH, index=False, encoding='utf-8-sig')
print(f"• error_log_bookings.csv       : {len(df_error):,} dòng")

agg.to_csv(AGG_PATH, index=False, encoding='utf-8-sig')
print(f"• agg_revenue_by_month.csv     : {len(agg)} dòng")

# 6. EXCEL STAR SCHEMA 
print("\n" + "=" * 70)
print("TẠO EXCEL STAR SCHEMA")
print("=" * 70)

with pd.ExcelWriter(EXCEL_STAR_SCHEMA_PATH, engine='openpyxl') as writer:

    all_dates = pd.concat([
        df_valid[['arrival_full_date']].rename(columns={'arrival_full_date': 'full_date'}),
        df_valid[['reservation_status_date']].rename(columns={'reservation_status_date': 'full_date'})
    ]).dropna().drop_duplicates().sort_values('full_date').reset_index(drop=True)

    dim_date = all_dates.copy()
    dim_date['date_key'] = dim_date['full_date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['year'] = dim_date['full_date'].dt.year
    dim_date['month'] = dim_date['full_date'].dt.month
    dim_date['week_number'] = dim_date['full_date'].dt.isocalendar().week.astype(int)
    dim_date['day_of_month'] = dim_date['full_date'].dt.day
    dim_date['month_name'] = dim_date['full_date'].dt.month_name()
    dim_date['quarter'] = dim_date['full_date'].dt.quarter
    dim_date = dim_date[['date_key', 'full_date', 'year', 'month', 'week_number',
                         'day_of_month', 'month_name', 'quarter']]

    unknown_date_row = pd.DataFrame([{
        'date_key': -1, 'full_date': pd.NaT, 'year': 1900, 'month': 1,
        'week_number': 1, 'day_of_month': 1, 'month_name': 'Unknown', 'quarter': 0
    }])
    dim_date = pd.concat([unknown_date_row, dim_date], ignore_index=True)

    dim_date.to_excel(writer, sheet_name='Dim_Date', index=False)

    dim_hotel = pd.DataFrame({
        'hotel_key': [1, 2],
        'hotel_name': ['Resort Hotel', 'City Hotel']
    })
    dim_hotel.to_excel(writer, sheet_name='Dim_Hotel', index=False)

    countries = sorted(df_valid['country'].unique())
    dim_country = pd.DataFrame({
        'country_key': range(1, len(countries) + 1),
        'country_code': countries
    })
    dim_country.to_excel(writer, sheet_name='Dim_Guest_Country', index=False)

    segs = sorted(df_valid['market_segment'].unique())
    dim_seg = pd.DataFrame({
        'market_segment_key': range(1, len(segs) + 1),
        'market_segment': segs
    })
    dim_seg.to_excel(writer, sheet_name='Dim_Market_Segment', index=False)

    chans = sorted(df_valid['distribution_channel'].unique())
    dim_chan = pd.DataFrame({
        'channel_key': range(1, len(chans) + 1),
        'distribution_channel': chans
    })
    dim_chan.to_excel(writer, sheet_name='Dim_Distribution_Channel', index=False)

    room_codes = sorted(set(df_valid['reserved_room_type'].unique()) |
                        set(df_valid['assigned_room_type'].unique()))
    dim_room = pd.DataFrame({
        'room_type_key': range(1, len(room_codes) + 1),
        'room_type_code': room_codes
    })
    dim_room.to_excel(writer, sheet_name='Dim_Room_Type', index=False)

    meals = sorted(df_valid['meal'].unique())
    dim_meal = pd.DataFrame({
        'meal_key': range(1, len(meals) + 1),
        'meal_plan': meals
    })
    dim_meal.to_excel(writer, sheet_name='Dim_Meal', index=False)

    cust = sorted(df_valid['customer_type'].unique())
    dim_cust = pd.DataFrame({
        'customer_type_key': range(1, len(cust) + 1),
        'customer_type': cust
    })
    dim_cust.to_excel(writer, sheet_name='Dim_Customer_Type', index=False)

    dep = sorted(df_valid['deposit_type'].unique())
    dim_dep = pd.DataFrame({
        'deposit_type_key': range(1, len(dep) + 1),
        'deposit_type': dep
    })
    dim_dep.to_excel(writer, sheet_name='Dim_Deposit_Type', index=False)

    agents = sorted(df_valid['agent'].unique())
    dim_agent = pd.DataFrame({
        'agent_key': range(1, len(agents) + 1),
        'agent_id': agents
    })
    dim_agent.to_excel(writer, sheet_name='Dim_Agent', index=False)

    hotel_map = dict(zip(dim_hotel['hotel_name'], dim_hotel['hotel_key']))
    country_map = dict(zip(dim_country['country_code'], dim_country['country_key']))
    seg_map = dict(zip(dim_seg['market_segment'], dim_seg['market_segment_key']))
    chan_map = dict(zip(dim_chan['distribution_channel'], dim_chan['channel_key']))
    room_map = dict(zip(dim_room['room_type_code'], dim_room['room_type_key']))
    meal_map = dict(zip(dim_meal['meal_plan'], dim_meal['meal_key']))
    cust_map = dict(zip(dim_cust['customer_type'], dim_cust['customer_type_key']))
    dep_map = dict(zip(dim_dep['deposit_type'], dim_dep['deposit_type_key']))
    agent_map = dict(zip(dim_agent['agent_id'], dim_agent['agent_key']))

    fact = df_valid.head(5000).copy()

    fact['arrival_date_key'] = to_date_key(fact['arrival_full_date'])
    fact['reservation_status_date_key'] = to_date_key(fact['reservation_status_date'])
    fact['hotel_key'] = fact['hotel'].map(hotel_map)
    fact['country_key'] = fact['country'].map(country_map)
    fact['market_segment_key'] = fact['market_segment'].map(seg_map)
    fact['channel_key'] = fact['distribution_channel'].map(chan_map)
    fact['reserved_room_type_key'] = fact['reserved_room_type'].map(room_map)
    fact['assigned_room_type_key'] = fact['assigned_room_type'].map(room_map)
    fact['meal_key'] = fact['meal'].map(meal_map)
    fact['customer_type_key'] = fact['customer_type'].map(cust_map)
    fact['deposit_type_key'] = fact['deposit_type'].map(dep_map)
    fact['agent_key'] = fact['agent'].map(agent_map)
    fact['estimated_revenue'] = fact['revenue']
    fact['company_id'] = fact['company']

    fact_cols = [
        'arrival_date_key', 'reservation_status_date_key',
        'hotel_key', 'country_key', 'market_segment_key', 'channel_key',
        'reserved_room_type_key', 'assigned_room_type_key',
        'meal_key', 'customer_type_key', 'deposit_type_key', 'agent_key',
        'is_canceled', 'lead_time',
        'stays_in_weekend_nights', 'stays_in_week_nights', 'total_nights',
        'adults', 'children', 'babies',
        'is_repeated_guest', 'previous_cancellations', 'previous_bookings_not_canceled',
        'booking_changes', 'days_in_waiting_list',
        'adr', 'estimated_revenue',
        'required_car_parking_spaces', 'total_of_special_requests',
        'reservation_status', 'company_id', 'room_changed_flag'
    ]
    fact[fact_cols].to_excel(writer, sheet_name='Fact_Booking_Sample', index=False)

    meta = pd.DataFrame({
        'Thông tin': [
            'Tổng dòng nguồn (raw)',
            'Dòng sau xóa trùng',
            'Dòng hợp lệ (Valid) – nạp Fact',
            'Dòng lỗi (Error Log)',
            'Số Dimension',
            'Grain Fact',
            'Thiết kế Dim_Room_Type',
            'Thiết kế Dim_Date',
            'Tên measure doanh thu',
            'Union All',
            'Ngày tạo file',
            'Người tạo'
        ],
        'Giá trị': [
            f'{len(df_raw):,}',
            f'{len(df):,}',
            f'{len(df_valid):,}',
            f'{len(df_error):,}',
            '10',
            '1 dòng = 1 lượt đặt phòng',
            'Role-playing (reserved_room_type_key + assigned_room_type_key)',
            'Role-playing (arrival_date_key + reservation_status_date_key)',
            'estimated_revenue (= adr × total_nights)',
            'Không áp dụng (1 nguồn)',
            datetime.now().strftime('%Y-%m-%d %H:%M'),
            'Nhóm 6'
        ]
    })
    meta.to_excel(writer, sheet_name='_README', index=False)

print("• Hotel_Booking_StarSchema.xlsx đã tạo")

# 7. TÓM TẮT
print("\n" + "=" * 70)
print("TÓM TẮT KẾT QUẢ")
print("=" * 70)
print(f"{'Chỉ tiêu':<40} {'Kỳ vọng':>12} {'Thực tế':>12}")
print("-" * 70)
print(f"{'Dòng nguồn':<40} {119390:>12,} {len(df_raw):>12,}")
print(f"{'Dòng trùng bị xóa':<40} {31994:>12,} {n_dup:>12,}")
print(f"{'Dòng Valid (nạp Fact)':<40} {86638:>12,} {len(df_valid):>12,}")
print(f"{'Dòng Error':<40} {758:>12,} {len(df_error):>12,}")
print(f"{'Aggregate Hotel×Tháng':<40} {52:>12} {len(agg):>12}")
print("=" * 70)
print("Đã xuất file thành công")
print("=" * 70)
