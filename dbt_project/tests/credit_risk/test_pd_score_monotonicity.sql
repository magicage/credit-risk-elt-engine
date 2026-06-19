select loan_id, pd_score, ifrs9_stage
from {{ ref('fct_loans') }}
where 1 = 0
