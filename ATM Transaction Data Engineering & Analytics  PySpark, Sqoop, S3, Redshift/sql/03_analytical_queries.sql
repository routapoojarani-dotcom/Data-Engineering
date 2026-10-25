-- 1. Top ATMs with the highest inactive-transaction rate
SELECT
    a.atm_number,
    a.atm_manufacturer,
    l.location,
    COUNT(f.trans_id) AS total_transaction_count,
    SUM(CASE WHEN f.atm_status = 'Inactive' THEN 1 ELSE 0 END) AS inactive_count,
    ROUND(
        100.0 * SUM(CASE WHEN f.atm_status = 'Inactive' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(f.trans_id), 0),
        2
    ) AS inactive_count_percent
FROM atm_data.fact_atm_trans f
JOIN atm_data.dim_atm a ON f.atm_id = a.atm_id
JOIN atm_data.dim_location l ON a.atm_location_id = l.location_id
GROUP BY a.atm_number, a.atm_manufacturer, l.location
HAVING ROUND(
    100.0 * SUM(CASE WHEN f.atm_status = 'Inactive' THEN 1 ELSE 0 END)
    / NULLIF(COUNT(f.trans_id), 0), 2
) > 50
ORDER BY inactive_count DESC
LIMIT 10;


-- 2. ATM failures by weather condition
SELECT
    f.weather_main,
    COUNT(f.trans_id) AS total_transaction_count,
    SUM(CASE WHEN f.atm_status = 'Inactive' THEN 1 ELSE 0 END) AS inactive_count,
    ROUND(
        100.0 * SUM(CASE WHEN f.atm_status = 'Inactive' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(f.trans_id), 0),
        2
    ) AS inactive_count_percent
FROM atm_data.fact_atm_trans f
WHERE COALESCE(f.weather_main, '') <> ''
GROUP BY f.weather_main
ORDER BY inactive_count_percent DESC
LIMIT 10;


-- 3. Highest-volume ATMs
SELECT
    a.atm_number,
    a.atm_manufacturer,
    l.location,
    COUNT(f.trans_id) AS total_transaction_count
FROM atm_data.fact_atm_trans f
JOIN atm_data.dim_atm a ON f.atm_id = a.atm_id
JOIN atm_data.dim_location l ON a.atm_location_id = l.location_id
GROUP BY a.atm_number, a.atm_manufacturer, l.location
ORDER BY total_transaction_count DESC
LIMIT 10;


-- 4. Monthly inactive-transaction trend
SELECT
    d.year,
    d.month,
    COUNT(f.trans_id) AS total_transaction_count,
    SUM(CASE WHEN f.atm_status = 'Inactive' THEN 1 ELSE 0 END) AS inactive_count,
    ROUND(
        100.0 * SUM(CASE WHEN f.atm_status = 'Inactive' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(f.trans_id), 0),
        2
    ) AS inactive_count_percent
FROM atm_data.fact_atm_trans f
JOIN atm_data.dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- 5. Highest total withdrawal amount by ATM
SELECT
    a.atm_number,
    a.atm_manufacturer,
    l.location,
    SUM(f.transaction_amount) AS total_transaction_amount
FROM atm_data.fact_atm_trans f
JOIN atm_data.dim_atm a ON f.atm_id = a.atm_id
JOIN atm_data.dim_location l ON a.atm_location_id = l.location_id
GROUP BY a.atm_number, a.atm_manufacturer, l.location
ORDER BY total_transaction_amount DESC
LIMIT 10;


-- 6. Failed transactions by card type
SELECT
    ct.card_type,
    COUNT(f.trans_id) AS total_transaction_count,
    SUM(CASE WHEN f.atm_status = 'Inactive' THEN 1 ELSE 0 END) AS inactive_count,
    ROUND(
        100.0 * SUM(CASE WHEN f.atm_status = 'Inactive' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(f.trans_id), 0),
        2
    ) AS inactive_count_percent
FROM atm_data.fact_atm_trans f
JOIN atm_data.dim_card_type ct ON f.card_type_id = ct.card_type_id
GROUP BY ct.card_type
ORDER BY inactive_count_percent DESC
LIMIT 10;


-- 7. Weekday vs weekend transaction volumes
SELECT
    a.atm_number,
    a.atm_manufacturer,
    l.location,
    CASE
        WHEN d.weekday IN ('Saturday', 'Sunday') THEN 1
        ELSE 0
    END AS weekend_flag,
    COUNT(f.trans_id) AS total_transaction_count
FROM atm_data.fact_atm_trans f
JOIN atm_data.dim_atm a ON f.atm_id = a.atm_id
JOIN atm_data.dim_location l ON a.atm_location_id = l.location_id
JOIN atm_data.dim_date d ON f.date_id = d.date_id
GROUP BY
    a.atm_number,
    a.atm_manufacturer,
    l.location,
    weekend_flag
ORDER BY
    a.atm_number,
    a.atm_manufacturer,
    l.location,
    weekend_flag,
    total_transaction_count
LIMIT 10;


-- 8. Most active weekday at a selected location
-- Change <location> to the required location.
WITH weekday_counts AS (
    SELECT
        d.weekday,
        COUNT(f.trans_id) AS transaction_count
    FROM atm_data.fact_atm_trans f
    JOIN atm_data.dim_date d ON f.date_id = d.date_id
    JOIN atm_data.dim_location l ON f.weather_loc_id = l.location_id
    WHERE l.location = '<location>'
    GROUP BY d.weekday
),
top_weekday AS (
    SELECT weekday
    FROM weekday_counts
    ORDER BY transaction_count DESC
    LIMIT 1
)
SELECT
    a.atm_number,
    a.atm_manufacturer,
    l.location,
    d.weekday,
    COUNT(f.trans_id) AS total_transaction_count
FROM atm_data.fact_atm_trans f
JOIN atm_data.dim_atm a ON f.atm_id = a.atm_id
JOIN atm_data.dim_location l ON a.atm_location_id = l.location_id
JOIN atm_data.dim_date d ON f.date_id = d.date_id
JOIN top_weekday tw ON d.weekday = tw.weekday
WHERE l.location = '<location>'
GROUP BY a.atm_number, a.atm_manufacturer, l.location, d.weekday
ORDER BY total_transaction_count;
