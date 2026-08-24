USE master;
GO

IF DB_ID(N'HotelBooking_Staging') IS NULL
BEGIN
    CREATE DATABASE HotelBooking_Staging;
END;
GO

USE HotelBooking_Staging;
GO

-- 1. Staging_Bookings
IF OBJECT_ID(N'dbo.Staging_Bookings', N'U') IS NOT NULL
    DROP TABLE dbo.Staging_Bookings;
GO

CREATE TABLE dbo.Staging_Bookings
(
    hotel                           NVARCHAR(50)    NULL,
    is_canceled                     BIT             NULL,
    lead_time                       INT             NULL,
    arrival_date_year               INT             NULL,
    arrival_date_month              NVARCHAR(20)    NULL,
    arrival_date_week_number        INT             NULL,
    arrival_date_day_of_month       INT             NULL,
    arrival_date_month_num          INT             NULL,
    arrival_full_date               DATE            NULL,
    booking_year_month              NVARCHAR(7)     NULL,
    stays_in_weekend_nights         INT             NULL,
    stays_in_week_nights            INT             NULL,
    total_nights                    INT             NULL,
    adults                          INT             NULL,
    children                        INT             NULL,
    babies                          INT             NULL,
    total_guests                    INT             NULL,
    meal                            NVARCHAR(20)    NULL,
    country                         NVARCHAR(10)    NULL,
    market_segment                  NVARCHAR(50)    NULL,
    distribution_channel            NVARCHAR(50)    NULL,
    is_repeated_guest               BIT             NULL,
    previous_cancellations          INT             NULL,
    previous_bookings_not_canceled  INT             NULL,
    reserved_room_type              NVARCHAR(10)    NULL,
    assigned_room_type              NVARCHAR(10)    NULL,
    room_changed_flag               BIT             NULL,
    booking_changes                 INT             NULL,
    deposit_type                    NVARCHAR(30)    NULL,
    agent                           NVARCHAR(20)    NULL,
    company                         NVARCHAR(20)    NULL,
    days_in_waiting_list            INT             NULL,
    customer_type                   NVARCHAR(30)    NULL,
    adr                             DECIMAL(12,2)   NULL,
    revenue                         DECIMAL(18,2)   NULL,
    required_car_parking_spaces     INT             NULL,
    total_of_special_requests       INT             NULL,
    reservation_status              NVARCHAR(30)    NULL,
    reservation_status_date         DATE            NULL,
    load_date                       DATETIME2(0)    NOT NULL DEFAULT (SYSDATETIME())
);
GO

CREATE NONCLUSTERED INDEX IX_Staging_Bookings_hotel ON dbo.Staging_Bookings (hotel);
GO
CREATE NONCLUSTERED INDEX IX_Staging_Bookings_arrival_full_date ON dbo.Staging_Bookings (arrival_full_date);
GO
CREATE NONCLUSTERED INDEX IX_Staging_Bookings_country ON dbo.Staging_Bookings (country);
GO
CREATE NONCLUSTERED INDEX IX_Staging_Bookings_agent ON dbo.Staging_Bookings (agent);
GO

-- 2. Error_Log
IF OBJECT_ID(N'dbo.Error_Log', N'U') IS NOT NULL
    DROP TABLE dbo.Error_Log;
GO

CREATE TABLE dbo.Error_Log
(
    error_log_id                    BIGINT IDENTITY(1,1) PRIMARY KEY,
    source_row_number               BIGINT          NULL,
    error_column                    NVARCHAR(100)   NULL,
    error_reason                    NVARCHAR(500)   NOT NULL,
    hotel                           NVARCHAR(50)    NULL,
    is_canceled                     BIT             NULL,
    lead_time                       INT             NULL,
    arrival_date_year               INT             NULL,
    arrival_date_month              NVARCHAR(20)    NULL,
    arrival_date_day_of_month       INT             NULL,
    stays_in_weekend_nights         INT             NULL,
    stays_in_week_nights            INT             NULL,
    total_nights                    INT             NULL,
    adults                          INT             NULL,
    children                        INT             NULL,
    babies                          INT             NULL,
    total_guests                    INT             NULL,
    meal                            NVARCHAR(20)    NULL,
    country                         NVARCHAR(10)    NULL,
    market_segment                  NVARCHAR(50)    NULL,
    distribution_channel            NVARCHAR(50)    NULL,
    reserved_room_type              NVARCHAR(10)    NULL,
    assigned_room_type              NVARCHAR(10)    NULL,
    deposit_type                    NVARCHAR(30)    NULL,
    agent                           NVARCHAR(20)    NULL,
    company                         NVARCHAR(20)    NULL,
    customer_type                   NVARCHAR(30)    NULL,
    adr                             DECIMAL(12,2)   NULL,
    revenue                         DECIMAL(18,2)   NULL,
    reservation_status              NVARCHAR(30)    NULL,
    reservation_status_date         DATE            NULL,
    error_date                      DATETIME2(0)    NOT NULL DEFAULT (SYSDATETIME())
);
GO

-- 3. Procedure truncate
IF OBJECT_ID(N'dbo.usp_Truncate_Staging', N'P') IS NOT NULL
    DROP PROCEDURE dbo.usp_Truncate_Staging;
GO

CREATE PROCEDURE dbo.usp_Truncate_Staging
AS
BEGIN
    SET NOCOUNT ON;
    TRUNCATE TABLE dbo.Staging_Bookings;
END
GO

PRINT N'>>> HotelBooking_Staging sẵn sàng.';
GO
