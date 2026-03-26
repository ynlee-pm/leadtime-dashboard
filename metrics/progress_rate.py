"""
평균 진도율 (Average Progress Rate) 계산
dashboard.html renderKPIs() 참조

평균 진도율 = 수강 종료된 수강생들의 진도율(%) 단순 평균
- 기준: courseEnded = True 인 수강생
- 진도율 범위: 0~100
- None, NaN, 음수는 제외
"""

from typing import Optional
from utils import avg


def calc_avg_progress(students: list[dict]) -> Optional[float]:
    """
    평균 진도율 계산

    Parameters
    ----------
    students : courseEnded=True 인 수강생 레코드 리스트
               각 레코드에 'progress' (float, 0~100) 필드 필요

    Returns
    -------
    평균 진도율 (0~100), 데이터 없으면 None
    """
    ended = [r for r in students if r.get("course_ended", False)]
    values = [r.get("progress") for r in ended]
    return avg(values)
