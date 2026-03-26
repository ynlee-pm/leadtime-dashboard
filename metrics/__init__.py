"""
Leadtime 대시보드 지표 계산 패키지

각 모듈:
    utils             - 공통 유틸 (avg, parse_kor_time, format_hours)
    lead_time         - 리드타임 평균 계산
    completion_rate   - 수료율
    progress_rate     - 평균 진도율
    full_completion_rate - 완강률
    price_realization - 단가 실현율
    revenue           - 예상 매출 (1인당 / 총)
    senior_ratio      - 시니어 비율
    correlation       - LT × 수료율 Pearson 상관계수 + 선형 회귀
"""

from .utils import avg, parse_kor_time, format_hours
from .lead_time import calc_lt_avg, lt_summary
from .completion_rate import calc_completion_rate
from .progress_rate import calc_avg_progress
from .full_completion_rate import calc_full_completion_rate
from .price_realization import calc_price_realization
from .revenue import calc_individual_revenue, calc_revenue_per_student, calc_total_revenue
from .senior_ratio import calc_senior_ratio, is_senior
from .correlation import pearson_r, linear_regression, calc_lt_completion_correlation

__all__ = [
    "avg", "parse_kor_time", "format_hours",
    "calc_lt_avg", "lt_summary",
    "calc_completion_rate",
    "calc_avg_progress",
    "calc_full_completion_rate",
    "calc_price_realization",
    "calc_individual_revenue", "calc_revenue_per_student", "calc_total_revenue",
    "calc_senior_ratio", "is_senior",
    "pearson_r", "linear_regression", "calc_lt_completion_correlation",
]
