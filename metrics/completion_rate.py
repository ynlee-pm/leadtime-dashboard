"""
수료율 (Completion Rate) 계산
dashboard.html renderKPIs() 참조

수료율 = 수료한 수강생 수 / 수강 종료된 수강생 수 × 100
- 기준: courseEnded = True (수강 종료일 < 현재 날짜) 인 수강생만 대상
- is_completed = True 인 수강생이 수료 처리됨
"""

from typing import Optional


def calc_completion_rate(students: list[dict]) -> dict:
    """
    수료율 계산

    Parameters
    ----------
    students : courseEnded=True 인 수강생 레코드 리스트
               각 레코드에 'is_completed' (bool) 필드 필요

    Returns
    -------
    {
        'completion_rate': float | None,   # 0~100 (%)
        'completed_count': int,
        'base_count':      int,            # courseEnded 수강생 수
    }
    """
    ended = [r for r in students if r.get("course_ended", False)]
    base_count = len(ended)

    if base_count == 0:
        return {"completion_rate": None, "completed_count": 0, "base_count": 0}

    completed_count = sum(1 for r in ended if r.get("is_completed", False))
    rate = completed_count / base_count * 100

    return {
        "completion_rate": rate,
        "completed_count": completed_count,
        "base_count":      base_count,
    }
