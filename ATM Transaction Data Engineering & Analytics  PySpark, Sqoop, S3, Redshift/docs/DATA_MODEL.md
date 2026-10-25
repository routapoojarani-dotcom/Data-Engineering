# Data Model

The warehouse is organized as a star schema.

```text
                 DIM_LOCATION
                      |
                      |
DIM_ATM -------- FACT_ATM_TRANS -------- DIM_DATE
                      |
                      |
                DIM_CARD_TYPE
```

## Dimensions

### DIM_LOCATION

- location_id
- location
- streetname
- street_number
- zipcode
- lat
- lon

### DIM_ATM

- atm_id
- atm_number
- atm_manufacturer
- atm_location_id

### DIM_DATE

- date_id
- full_date_time
- year
- month
- day
- hour
- weekday

### DIM_CARD_TYPE

- card_type_id
- card_type

## Fact

`FACT_ATM_TRANS` contains transaction-level measures and operational/context attributes including transaction identifier, ATM and dimension keys, ATM status, currency, service, transaction amount, message fields and weather attributes.
