select loan_id, pd_score, ifrs9_stage
from {{ ref('fct_loans') }}
where pd_score <= 0 or pd_score >= 1
   or (ifrs9_stage = 3 and pd_score < 0.5)
