"""
시니어 비율 (Senior Ratio) 계산
dashboard.html renderKPIs() 참조

시니어 정의: 나이 >= 40세
시니어 비율 = 시니어 수강생 수 / 전체 수강생 수 × 100
"""

from typing import Optional

SENIOR_AGE_THRESHOLD = 40


def is_senior(age: Optional[int]) -> bool:
    """나이가 시니어 기준(40세 이상)인지 판별"""
    if age is None:
        return False
    return age >= SENIOR_AGE_THRESHOLD


def calc_senior_ratio(students: list[dict]) -> dict:
    """
    시니어 비율 계산

    Parameters
    ----------
    students : 수강생 레코드 리스트 ('age' 또는 'is_senior' 필드 필요)

    Returns
    -------
    {
        'senior_ratio': float | None,   # 0~100 (%)
        'senior_count': int,
        'total_count':  int,
    }
    """
    total = len(students)
    if total == 0:
        return {"senior_ratio": None, "senior_count": 0, "total_count": 0}

    senior_count = sum(
        1 for r in students
        if r.get("is_senior", False) or is_senior(r.get("age"))
    )

    return {
        "senior_ratio": senior_count / total * 100,
        "senior_count": senior_count,
        "total_count":  total,
    }
