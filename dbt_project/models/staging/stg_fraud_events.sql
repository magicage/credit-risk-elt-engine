{{ config(materialized='view') }}

with source as (
    select * from {{ source('credit_risk_src', 'fraud_logs') }}
),

-- use LATERAL FLATTEN to flatten JSON arrays into multiple rows
flattened as (
    select
        log_id,
        payload:customer_id::STRING as customer_id,
        -- f.value represents each element in the flattened array
        f.value:action::STRING as event_action,
        f.value:ts::TIMESTAMP as event_timestamp,
        received_at
    from source,
    LATERAL FLATTEN(input => payload:events) f
)

select * from flattened