"""
단가 실현율 (Unit Price Realization Rate) 계산
dashboard.html calcPriceRealization() 참조

공식:
    R = 수료율 + (1 - 수료율) × 미수료자_평균진도율

해석:
    - 수료한 수강생 → 단가 100% 실현
    - 미수료 수강생 → 진도율(%) 만큼 실현
    - R은 수강생 전체 기준 단가 실현 비율 (0~1)

예시:
    수료율=0.6, 미수료자 평균 진도율=40%
    → R = 0.6 + 0.4 × 0.4 = 0.76  (단가의 76% 실현)
"""

from typing import Optional
from utils import avg


def calc_price_realization(students: list[dict]) -> dict:
    """
    단가 실현율 계산 (courseEnded=True 수강생 기준)

    Parameters
    ----------
    students : courseEnded=True 인 수강생 레코드 리스트
               각 레코드에 'is_completed' (bool), 'progress' (float, 0~100) 필드 필요

    Returns
    -------
    {
        'R':                float | None,  # 단가 실현율 (0~1)
        'R_pct':            float | None,  # 단가 실현율 (0~100, %)
        'cr_rate':          float,         # 수료율 (0~1)
        'nc_avg_progress':  float,         # 미수료자 평균 진도율 (0~1)
    }
    """
    ended = [r for r in students if r.get("course_ended", False)]

    if not ended:
        return {"R": None, "R_pct": None, "cr_rate": 0.0, "nc_avg_progress": 0.0}

    completed    = [r for r in ended if r.get("is_completed", False)]
    not_completed = [r for r in ended if not r.get("is_completed", False)]

    cr_rate = len(completed) / len(ended)

    nc_progress_values = [r.get("progress") for r in not_completed]
    nc_avg = avg(nc_progress_values)
    nc_avg_progress = (nc_avg / 100) if nc_avg is not None else 0.0

    R = cr_rate + (1 - cr_rate) * nc_avg_progress

    return {
        "R":               R,
        "R_pct":           R * 100,
        "cr_rate":         cr_rate,
        "nc_avg_progress": nc_avg_progress,
    }
