"""
예상 매출 계산
dashboard.html calcRevenue(), renderKPIs() 참조

개별 수강생 예상 매출:
    - 수료 → 단가 (price) 전액
    - 미수료 → 단가 × (진도율 / 100)

1인당 예상 매출 = 총 예상 매출 / courseEnded 수강생 수
총 예상 매출    = 전체 필터된 수강생의 개별 예상 매출 합산
"""

from typing import Optional


def calc_individual_revenue(student: dict, price_map: dict[str, float]) -> Optional[float]:
    """
    수강생 1명의 예상 매출 계산

    Parameters
    ----------
    student   : 수강생 레코드 ('product_id', 'is_completed', 'progress' 필드 필요)
    price_map : { product_id: 단가 } 딕셔너리

    Returns
    -------
    예상 매출 (원), 단가 정보 없으면 None
    """
    product_id = student.get("product_id")
    price = price_map.get(product_id)

    if price is None:
        return None

    if student.get("is_completed", False):
        return price
    else:
        progress = student.get("progress") or 0
        return price * (progress / 100)


def calc_revenue_per_student(students: list[dict], price_map: dict[str, float]) -> Optional[float]:
    """
    1인당 예상 매출 계산 (courseEnded=True 수강생 기준)

    총 예상 매출 / courseEnded 수강생 수
    단가 정보가 없는 수강생은 0으로 처리 (분모에는 포함)

    Parameters
    ----------
    students  : courseEnded=True 인 수강생 리스트
    price_map : { product_id: 단가 }

    Returns
    -------
    1인당 평균 예상 매출 (원), 수강생 없으면 None
    """
    ended = [r for r in students if r.get("course_ended", False)]
    if not ended:
        return None

    total = sum(
        (calc_individual_revenue(r, price_map) or 0)
        for r in ended
    )
    return total / len(ended)


def calc_total_revenue(students: list[dict], price_map: dict[str, float]) -> float:
    """
    총 예상 매출 계산 (필터된 전체 수강생 기준)

    Parameters
    ----------
    students  : 필터된 수강생 전체 리스트 (courseEnded 무관)
    price_map : { product_id: 단가 }

    Returns
    -------
    총 예상 매출 합산 (원)
    """
    return sum(
        (calc_individual_revenue(r, price_map) or 0)
        for r in students
    )
