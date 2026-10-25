CREATE SCHEMA IF NOT EXISTS atm_data;

CREATE TABLE IF NOT EXISTS atm_data.dim_location (
    location_id INT NOT NULL,
    location VARCHAR(50),
    streetname VARCHAR(255),
    street_number INT,
    zipcode INT,
    lat DECIMAL(10,3),
    lon DECIMAL(10,3),
    PRIMARY KEY (location_id)
);

CREATE TABLE IF NOT EXISTS atm_data.dim_atm (
    atm_id INT NOT NULL,
    atm_number VARCHAR(20),
    atm_manufacturer VARCHAR(50),
    atm_location_id INT,
    PRIMARY KEY (atm_id),
    FOREIGN KEY (atm_location_id)
        REFERENCES atm_data.dim_location(location_id)
);

CREATE TABLE IF NOT EXISTS atm_data.dim_date (
    date_id INT NOT NULL,
    full_date_time TIMESTAMP,
    year INT,
    month VARCHAR(20),
    day INT,
    hour INT,
    weekday VARCHAR(20),
    PRIMARY KEY (date_id)
);

CREATE TABLE IF NOT EXISTS atm_data.dim_card_type (
    card_type_id INT NOT NULL,
    card_type VARCHAR(30),
    PRIMARY KEY (card_type_id)
);

CREATE TABLE IF NOT EXISTS atm_data.fact_atm_trans (
    trans_id BIGINT NOT NULL,
    atm_id INT,
    weather_loc_id INT,
    date_id INT,
    card_type_id INT,
    atm_status VARCHAR(20),
    currency VARCHAR(10),
    service VARCHAR(20),
    transaction_amount INT,
    message_code VARCHAR(225),
    message_text VARCHAR(225),
    rain_3h DECIMAL(10,3),
    clouds_all INT,
    weather_id INT,
    weather_main VARCHAR(50),
    weather_description VARCHAR(255),
    PRIMARY KEY (trans_id),
    FOREIGN KEY (weather_loc_id)
        REFERENCES atm_data.dim_location(location_id),
    FOREIGN KEY (atm_id)
        REFERENCES atm_data.dim_atm(atm_id),
    FOREIGN KEY (date_id)
        REFERENCES atm_data.dim_date(date_id),
    FOREIGN KEY (card_type_id)
        REFERENCES atm_data.dim_card_type(card_type_id)
);
