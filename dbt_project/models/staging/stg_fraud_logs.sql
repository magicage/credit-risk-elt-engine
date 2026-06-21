{{ config(materialized='view') }}

with source as (
    select * from {{ source('credit_risk_src', 'fraud_logs') }}
),

parsed as (
    select
        log_id,
        --  use Dot Notation and :: to cast data types
        payload:customer_id::STRING as customer_id,
        payload:device.os::STRING as device_os,
        payload:device.browser::STRING as device_browser,
        payload:device.fingerprint::STRING as device_fingerprint,
        payload:location.country::STRING as geo_country,
        payload:location.risk_score::FLOAT as geo_risk_score,
        received_at
    from source
)

select * from parsed