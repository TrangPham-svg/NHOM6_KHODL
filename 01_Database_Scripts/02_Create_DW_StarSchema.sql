USE master;
GO

IF DB_ID(N'HotelBooking_DW') IS NULL
BEGIN
    CREATE DATABASE HotelBooking_DW;
END;
GO

USE HotelBooking_DW;
GO

-- 1. Dim_Date
IF OBJECT_ID(N'dbo.Dim_Date', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dim_Date
    (
        date_key        INT             NOT NULL PRIMARY KEY,
        full_date       DATE            NULL UNIQUE,   -- NULL cho phép ở dòng Unknown (full_date không xác định)
        year            INT             NOT NULL,
        month           INT             NOT NULL,
        week_number     INT             NOT NULL,
        day_of_month    INT             NOT NULL,
        month_name      NVARCHAR(20)    NULL,
        quarter         INT             NULL
    );
END;
GO

IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID(N'dbo.Dim_Date') AND name = N'month_name')
    ALTER TABLE dbo.Dim_Date ADD month_name NVARCHAR(20) NULL;
GO
IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID(N'dbo.Dim_Date') AND name = N'quarter')
    ALTER TABLE dbo.Dim_Date ADD quarter INT NULL;
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Dim_Date WHERE date_key = -1)
BEGIN
    INSERT INTO dbo.Dim_Date (date_key, full_date, year, month, week_number, day_of_month, month_name, quarter)
    VALUES (-1, NULL, 1900, 1, 1, 1, N'Unknown', 0);
END;
GO

-- 2. Dim_Hotel
IF OBJECT_ID(N'dbo.Dim_Hotel', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dim_Hotel
    (
        hotel_key       INT IDENTITY(1,1) PRIMARY KEY,
        hotel_name      NVARCHAR(50)    NOT NULL UNIQUE
    );
END;
GO

-- 3. Dim_Guest_Country
IF OBJECT_ID(N'dbo.Dim_Guest_Country', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dim_Guest_Country
    (
        country_key     INT IDENTITY(1,1) PRIMARY KEY,
        country_code    NVARCHAR(10)    NOT NULL UNIQUE
    );
END;
GO

-- 4. Dim_Market_Segment
IF OBJECT_ID(N'dbo.Dim_Market_Segment', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dim_Market_Segment
    (
        market_segment_key  INT IDENTITY(1,1) PRIMARY KEY,
        market_segment      NVARCHAR(50)    NOT NULL UNIQUE
    );
END;
GO

-- 5. Dim_Distribution_Channel
IF OBJECT_ID(N'dbo.Dim_Distribution_Channel', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dim_Distribution_Channel
    (
        channel_key             INT IDENTITY(1,1) PRIMARY KEY,
        distribution_channel    NVARCHAR(50)    NOT NULL UNIQUE
    );
END;
GO

-- 6. Dim_Room_Type (role-playing)
IF OBJECT_ID(N'dbo.Dim_Room_Type', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dim_Room_Type
    (
        room_type_key   INT IDENTITY(1,1) PRIMARY KEY,
        room_type_code  NVARCHAR(10)    NOT NULL UNIQUE
    );
END;
GO

-- 7. Dim_Meal
IF OBJECT_ID(N'dbo.Dim_Meal', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dim_Meal
    (
        meal_key    INT IDENTITY(1,1) PRIMARY KEY,
        meal_plan   NVARCHAR(20)    NOT NULL UNIQUE
    );
END;
GO

-- 8. Dim_Customer_Type
IF OBJECT_ID(N'dbo.Dim_Customer_Type', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dim_Customer_Type
    (
        customer_type_key   INT IDENTITY(1,1) PRIMARY KEY,
        customer_type       NVARCHAR(50)    NOT NULL UNIQUE
    );
END;
GO

-- 9. Dim_Deposit_Type
IF OBJECT_ID(N'dbo.Dim_Deposit_Type', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dim_Deposit_Type
    (
        deposit_type_key    INT IDENTITY(1,1) PRIMARY KEY,
        deposit_type        NVARCHAR(50)    NOT NULL UNIQUE
    );
END;
GO

-- 10. Dim_Agent
IF OBJECT_ID(N'dbo.Dim_Agent', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Dim_Agent
    (
        agent_key   INT IDENTITY(1,1) PRIMARY KEY,
        agent_id    NVARCHAR(20)    NOT NULL UNIQUE
    );
END;
GO

-- 11. Fact_Booking
IF OBJECT_ID(N'dbo.Fact_Booking', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Fact_Booking
    (
        booking_key                     BIGINT IDENTITY(1,1) PRIMARY KEY,
        arrival_date_key                INT             NOT NULL,
        reservation_status_date_key     INT             NOT NULL,
        hotel_key                       INT             NOT NULL,
        country_key                     INT             NOT NULL,
        market_segment_key              INT             NOT NULL,
        channel_key                     INT             NOT NULL,
        reserved_room_type_key          INT             NOT NULL,
        assigned_room_type_key          INT             NOT NULL,
        meal_key                        INT             NOT NULL,
        customer_type_key               INT             NOT NULL,
        deposit_type_key                INT             NOT NULL,
        agent_key                       INT             NOT NULL,
        is_canceled                     BIT             NOT NULL,
        lead_time                       INT             NOT NULL,
        stays_in_weekend_nights         INT             NOT NULL,
        stays_in_week_nights            INT             NOT NULL,
        total_nights                    INT             NOT NULL,
        adults                          INT             NOT NULL,
        children                        INT             NOT NULL,
        babies                          INT             NOT NULL,
        is_repeated_guest               BIT             NOT NULL,
        previous_cancellations          INT             NOT NULL,
        previous_bookings_not_canceled  INT             NOT NULL,
        booking_changes                 INT             NOT NULL,
        days_in_waiting_list            INT             NOT NULL,
        adr                             DECIMAL(12,2)   NOT NULL,
        estimated_revenue               DECIMAL(18,2)   NULL,
        required_car_parking_spaces     INT             NOT NULL,
        total_of_special_requests       INT             NOT NULL,
        reservation_status              NVARCHAR(30)    NOT NULL,
        company_id                      NVARCHAR(20)    NULL,
        room_changed_flag               BIT             NOT NULL
    );
END;
GO

-- Foreign Keys
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_FactBooking_ArrivalDate')
    ALTER TABLE dbo.Fact_Booking ADD CONSTRAINT FK_FactBooking_ArrivalDate
        FOREIGN KEY (arrival_date_key) REFERENCES dbo.Dim_Date(date_key);
GO
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_FactBooking_ReservationStatusDate')
    ALTER TABLE dbo.Fact_Booking ADD CONSTRAINT FK_FactBooking_ReservationStatusDate
        FOREIGN KEY (reservation_status_date_key) REFERENCES dbo.Dim_Date(date_key);
GO
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_FactBooking_Hotel')
    ALTER TABLE dbo.Fact_Booking ADD CONSTRAINT FK_FactBooking_Hotel
        FOREIGN KEY (hotel_key) REFERENCES dbo.Dim_Hotel(hotel_key);
GO
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_FactBooking_Country')
    ALTER TABLE dbo.Fact_Booking ADD CONSTRAINT FK_FactBooking_Country
        FOREIGN KEY (country_key) REFERENCES dbo.Dim_Guest_Country(country_key);
GO
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_FactBooking_MarketSegment')
    ALTER TABLE dbo.Fact_Booking ADD CONSTRAINT FK_FactBooking_MarketSegment
        FOREIGN KEY (market_segment_key) REFERENCES dbo.Dim_Market_Segment(market_segment_key);
GO
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_FactBooking_DistributionChannel')
    ALTER TABLE dbo.Fact_Booking ADD CONSTRAINT FK_FactBooking_DistributionChannel
        FOREIGN KEY (channel_key) REFERENCES dbo.Dim_Distribution_Channel(channel_key);
GO
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_FactBooking_ReservedRoom')
    ALTER TABLE dbo.Fact_Booking ADD CONSTRAINT FK_FactBooking_ReservedRoom
        FOREIGN KEY (reserved_room_type_key) REFERENCES dbo.Dim_Room_Type(room_type_key);
GO
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_FactBooking_AssignedRoom')
    ALTER TABLE dbo.Fact_Booking ADD CONSTRAINT FK_FactBooking_AssignedRoom
        FOREIGN KEY (assigned_room_type_key) REFERENCES dbo.Dim_Room_Type(room_type_key);
GO
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_FactBooking_Meal')
    ALTER TABLE dbo.Fact_Booking ADD CONSTRAINT FK_FactBooking_Meal
        FOREIGN KEY (meal_key) REFERENCES dbo.Dim_Meal(meal_key);
GO
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_FactBooking_CustomerType')
    ALTER TABLE dbo.Fact_Booking ADD CONSTRAINT FK_FactBooking_CustomerType
        FOREIGN KEY (customer_type_key) REFERENCES dbo.Dim_Customer_Type(customer_type_key);
GO
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_FactBooking_DepositType')
    ALTER TABLE dbo.Fact_Booking ADD CONSTRAINT FK_FactBooking_DepositType
        FOREIGN KEY (deposit_type_key) REFERENCES dbo.Dim_Deposit_Type(deposit_type_key);
GO
IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = N'FK_FactBooking_Agent')
    ALTER TABLE dbo.Fact_Booking ADD CONSTRAINT FK_FactBooking_Agent
        FOREIGN KEY (agent_key) REFERENCES dbo.Dim_Agent(agent_key);
GO

PRINT N'>>> HotelBooking_DW sẵn sàng.';
GO
