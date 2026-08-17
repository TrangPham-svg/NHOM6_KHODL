# NHÓM 6 – DATA WAREHOUSE & BUSINESS INTELLIGENCE

### Quy trình tổng thể

```text
Hotel Booking CSV
       ↓
Python Data Profiling & Validation
       ↓
SSIS – Extract
       ↓
SSIS – Transform
       ↓
Staging Database
       ↓
Dimension Tables
       ↓
FACT_BOOKING
       ↓
Data Warehouse – Star Schema
       ↓
Semantic Model / Data Model
       ↓
Power BI
       ↓
Dashboard & Business Insights
```

---

## 1. CÔNG NGHỆ SỬ DỤNG

| Thành phần | Công nghệ |
|---|---|
| Database | SQL Server 2022 |
| Database Management | SQL Server Management Studio (SSMS) |
| ETL | SQL Server Integration Services (SSIS) |
| ETL Development | Visual Studio + SSIS Extension |
| Data Validation | Python |
| Data Processing | Pandas, NumPy |
| BI & Visualization | Power BI Desktop |
| Dataset | `hotel_bookings.csv` |


---

## 2. CẤU TRÚC THƯ MỤC

```text
Nhom6_Khodl/
│
├── README.md
├── .gitignore
│
├── 01_Database_Scripts/
│   ├── 01_Create_Staging_DB.sql
│   ├── 02_Create_DW_StarSchema.sql
│   ├── 03_Create_DIM_DATE.sql
│   └── 04_Test_DW.sql
│
├── 02_Python_Validation/
│   ├── data_profiling_and_etl.py
│   ├── requirements.txt
│   ├── input/
│   │   └── hotel_bookings.csv
│   └── output/
│       ├── staging_cleaned_bookings.csv
│       ├── error_log_bookings.csv
│       ├── agg_revenue_by_month.csv
│       └── profiling_report.html
│
├── 03_SSIS_Project/
│   ├── ETL_HotelBooking.sln
│   ├── ETL_HotelBooking.dtproj
│   ├── ETL_HotelBooking.database
│   ├── ETL_HotelBooking.dtproj.user
│   ├── Project.params
│   └── PKG_Load_HotelBooking.dtsx
│
├── 04_Data_Warehouse/
│   ├── StarSchema/
│   ├── Testing/
│   └── Samples/
│
├── 05_Analysis/
│   ├── KPI/
│   ├── DAX/
│   ├── Seasonality/
│   └── Analysis_Result/
│
├── 06_PowerBI/
│   ├── HotelBooking_BI.pbix
│   └── Dashboard/
│
├── 07_Documentation/
│   ├── Word_Draft/
│   ├── Final/
│   ├── Figures/
│   └── Tables/
│
└── 08_Demo/
    └── Demo_Guide.md
```

---

## 3. PHÂN CÔNG QUẢN LÝ THƯ MỤC

### Thành viên 1 – Database & Data Modeling

**Phụ trách:**
```text
01_Database_Scripts/
04_Data_Warehouse/
```

**Nhiệm vụ:**
- Thiết kế và hoàn thiện Star Schema.
- Xây dựng Staging Database.
- Xây dựng Data Warehouse Database.
- Hoàn thiện DIM_DATE.
- Kiểm tra Primary Key, Foreign Key và các khóa thay thế.
- Kiểm tra tính toàn vẹn của mô hình.

**Phần Word:**
- Chương 1.
- Mục 2.1.
- Mục 2.4.
- Mục 2.5.

---

### Thành viên 2 – Data Profiling & Python QA

**Phụ trách:**
```text
02_Python_Validation/
```

**Nhiệm vụ:**
- Data Profiling dữ liệu nguồn.
- Kiểm tra duplicate.
- Kiểm tra NULL.
- Kiểm tra dữ liệu bất thường.
- Làm sạch và chuẩn hóa dữ liệu.
- Xuất dữ liệu sạch.
- Tạo dữ liệu lỗi phục vụ đối soát.
- Kiểm tra dữ liệu ngày tháng và thuộc tính dẫn xuất.

**Phần Word:**
- Mục 2.2.
- Mục 2.3.
- Phần Extract và Transform trong Chương 3.

---

### Thành viên 3 – SSIS Control Flow & Dimension ETL

**Phụ trách:**
```text
03_SSIS_Project/
```

**Nhiệm vụ:**
- Hoàn thiện Control Flow.
- Thiết lập Connection Manager.
- Thiết lập Project Parameters.
- Xây dựng Data Flow.
- Nạp các Dimension.
- Thiết lập Lookup và thứ tự thực thi ETL.
- Kiểm tra package có thể chạy từ đầu đến cuối.

**Phần Word:**
- Mục 3.1.
- Mục 3.2.
- Mục 3.3.
- Phần Dimension ETL trong mục 3.4.

---

### Thành viên 4 – SSIS Fact ETL, Error Handling & Testing

**Phụ trách:**
```text
03_SSIS_Project/
04_Data_Warehouse/Testing/
```

**Nhiệm vụ:**
- Nạp FACT_BOOKING.
- Lookup khóa ngoại.
- Xử lý dữ liệu lỗi.
- Conditional Split.
- Error Log.
- Kiểm thử End-to-End.
- Kiểm tra Row Count.
- Kiểm tra Foreign Key.
- Kiểm tra số liệu tổng hợp.
- Đối chiếu kết quả Python và SSIS.

**Phần Word:**
- Mục 3.4.
- Mục 3.5.
- Phần đánh giá ETL trong Chương 6.

---

### Thành viên 5 – Data Analysis & Power BI

**Phụ trách:**
```text
05_Analysis/
06_PowerBI/
```

**Nhiệm vụ:**
- Xây dựng Semantic Model / Data Model.
- Thiết lập relationships.
- Xây dựng Measure bằng DAX.
- Phân tích Booking, Revenue, ADR, Cancellation Rate và Total Nights.
- Phân tích theo năm, quý và tháng.
- Phân tích mùa cao điểm và mùa thấp điểm.
- Phân tích theo Hotel, Country, Market Segment, Distribution Channel, Room Type và Customer Type.
- Xây dựng Dashboard Power BI.
- Đưa ra Business Insights và đề xuất hỗ trợ quyết định.

**Phần Word:**
- Chương 4.
- Chương 5.
- Phần phân tích BI trong Chương 6.

---

## 4. MÔI TRƯỜNG PYTHON

Khuyến nghị thống nhất:

```text
Python 3.11
```

Tạo virtual environment:

```bash
python -m venv .venv
```

Kích hoạt trên Windows:

```bash
.venv\Scripts\activate
```

Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

Kiểm tra Python:

```bash
python --version
```

---

## 5. DATABASE

Database chính sử dụng:

```text
SQL Server 2022
```

Có thể quản lý bằng:

```text
SQL Server Management Studio (SSMS)
```

Các script tạo Database nằm tại:

```text
01_Database_Scripts/
```

Thứ tự chạy:

```text
01_Create_Staging_DB.sql
        ↓
02_Create_DW_StarSchema.sql
        ↓
03_Create_DIM_DATE.sql
        ↓
04_Test_DW.sql
```

---

## 6. SSIS

Project SSIS nằm tại:

```text
03_SSIS_Project/
```

File solution:

```text
ETL_HotelBooking.sln
```

Package ETL chính:

```text
PKG_Load_HotelBooking.dtsx
```

Pipeline:

```text
Extract
   ↓
Transform
   ↓
Load Dimension
   ↓
Load Fact
   ↓
Error Handling
   ↓
Validation
```

---

## 7. POWER BI

File Power BI chính:

```text
06_PowerBI/HotelBooking_BI.pbix
```

Các nhóm phân tích chính:

- Booking.
- Cancellation.
- Revenue.
- ADR.
- Total Nights.
- Seasonality.
- Hotel.
- Guest Country.
- Market Segment.
- Distribution Channel.
- Room Type.
- Customer Type.

---

## 8. PHÂN TÍCH MÙA VỤ

Dữ liệu thời gian được chuẩn hóa thông qua:

```text
DIM_DATE
```

Phân tích theo:

```text
Year
Quarter
Month
Weekend / Weekday
Season
```

Mục tiêu:

- Xác định thời gian có nhu cầu đặt phòng cao.
- Xác định mùa cao điểm.
- Xác định mùa thấp điểm.
- Phân tích xu hướng đặt phòng theo thời gian.
- Phân tích thời gian lưu trú theo mùa.
- Hỗ trợ đề xuất điều chỉnh giá và nguồn lực kinh doanh.

---

## 9. DOCUMENTATION

Các hình ảnh và bảng biểu dùng trong báo cáo lưu tại:

```text
07_Documentation/Figures/
07_Documentation/Tables/
```

## 10. QUY TẮC
1. Không sửa trực tiếp file của thành viên khác nếu chưa thống nhất.
2. Mỗi thay đổi lớn phải được kiểm tra trước khi merge.
5. Các số liệu trong báo cáo phải được đối chiếu với SQL Server/SSIS/Power BI.
6. Python output được sử dụng làm dữ liệu tham chiếu kiểm thử, không thay thế Data Warehouse.
7. Data Warehouse chính thức được lưu trữ trên SQL Server.
8. Power BI lấy dữ liệu từ Data Warehouse đã hoàn thiện.
