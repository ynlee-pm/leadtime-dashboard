"""
완강률 (Full Completion Rate) 계산
dashboard.html renderKPIs() 참조

완강률 = 수료한 수강생 중 진도율 100% 달성자 수 / 수료한 수강생 수 × 100
- 기준: is_completed = True 인 수강생만 대상
- 완강 조건: progress >= 100
"""

from typing import Optional


def calc_full_completion_rate(students: list[dict]) -> dict:
    """
    완강률 계산

    Parameters
    ----------
    students : courseEnded=True 인 수강생 레코드 리스트
               각 레코드에 'is_completed' (bool), 'progress' (float) 필드 필요

    Returns
    -------
    {
        'full_completion_rate': float | None,   # 0~100 (%)
        'fully_progressed_count': int,          # 진도율 100% 수료생 수
        'completed_count':        int,          # 전체 수료생 수
    }
    """
    ended = [r for r in students if r.get("course_ended", False)]
    completed = [r for r in ended if r.get("is_completed", False)]
    completed_count = len(completed)

    if completed_count == 0:
        return {
            "full_completion_rate":   None,
            "fully_progressed_count": 0,
            "completed_count":        0,
        }

    fully_progressed = [r for r in completed if (r.get("progress") or 0) >= 100]
    rate = len(fully_progressed) / completed_count * 100

    return {
        "full_completion_rate":   rate,
        "fully_progressed_count": len(fully_progressed),
        "completed_count":        completed_count,
    }
