select loan_id, ifrs9_stage, loan_status, dbt_updated_at
from {{ ref('fct_loans') }}
where ifrs9_stage = 1 
  and loan_status in ('charged_off', 'default')
