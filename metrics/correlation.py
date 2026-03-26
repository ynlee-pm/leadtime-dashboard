"""
리드타임 × 수료율 상관관계 분석
dashboard.html renderCourseChart() 참조

Pearson 상관계수 및 선형 회귀(trend line) 계산
산점도에서 각 과정별 (LT 평균, 수료율) 점을 기반으로 분석
"""

import math
from typing import Optional
from utils import avg
from completion_rate import calc_completion_rate


def pearson_r(xs: list[float], ys: list[float]) -> Optional[float]:
    """
    Pearson 상관계수 계산

    Parameters
    ----------
    xs, ys : 같은 길이의 수치 리스트

    Returns
    -------
    r 값 (-1~1), 계산 불가하면 None
    """
    n = len(xs)
    if n < 2 or len(ys) != n:
        return None

    x_mean = sum(xs) / n
    y_mean = sum(ys) / n

    cov_xy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    var_x  = sum((x - x_mean) ** 2 for x in xs)
    var_y  = sum((y - y_mean) ** 2 for y in ys)

    denom = math.sqrt(var_x * var_y)
    if denom == 0:
        return None

    return cov_xy / denom


def linear_regression(xs: list[float], ys: list[float]) -> Optional[dict]:
    """
    단순 선형 회귀 계산 (y = slope * x + intercept)

    Returns
    -------
    {
        'slope':     float,
        'intercept': float,
    }
    또는 None (계산 불가 시)
    """
    n = len(xs)
    if n < 2 or len(ys) != n:
        return None

    x_mean = sum(xs) / n
    y_mean = sum(ys) / n

    cov_xy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    var_x  = sum((x - x_mean) ** 2 for x in xs)

    if var_x == 0:
        return None

    slope     = cov_xy / var_x
    intercept = y_mean - slope * x_mean

    return {"slope": slope, "intercept": intercept}


def interpret_pearson(r: Optional[float]) -> str:
    """
    Pearson r 값을 해석 문자열로 변환
    dashboard.html 해석 기준 참조
    """
    if r is None:
        return "데이터 부족"
    if r < -0.3:
        return "부(-)의 상관 (LT 짧을수록 수료율 높음)"
    if r > 0.3:
        return "정(+)의 상관 (LT 길수록 수료율 높음)"
    return "약한 상관관계"


def calc_lt_completion_correlation(
    students_by_course: dict[str, list[dict]],
    lt_key: str = "lt_ch1",
) -> dict:
    """
    과정별 LT 평균 vs 수료율 상관관계 분석

    Parameters
    ----------
    students_by_course : { 과정명: 수강생 리스트 }
    lt_key             : 분석할 LT 지표 ('lt_11' | 'lt_ch1' | 'lt_21' | 'lt_ch2')

    Returns
    -------
    {
        'points':      [{'course', 'x' (lt_avg), 'y' (cr_pct), 'n' (수강생수)}, ...],
        'pearson_r':   float | None,
        'regression':  {'slope', 'intercept'} | None,
        'interpretation': str,
    }
    """
    points = []

    for course, members in students_by_course.items():
        ended = [r for r in members if r.get("course_ended", False)]
        if not ended:
            continue

        lt_values = [r.get(lt_key) for r in ended]
        lt_avg = avg(lt_values)
        if lt_avg is None:
            continue

        cr_info = calc_completion_rate(ended)
        if cr_info["completion_rate"] is None:
            continue

        points.append({
            "course": course,
            "x":      lt_avg,
            "y":      cr_info["completion_rate"],
            "n":      len(ended),
        })

    if len(points) < 2:
        return {
            "points":         points,
            "pearson_r":      None,
            "regression":     None,
            "interpretation": "데이터 부족",
        }

    xs = [p["x"] for p in points]
    ys = [p["y"] for p in points]

    r = pearson_r(xs, ys)
    reg = linear_regression(xs, ys)

    return {
        "points":         points,
        "pearson_r":      r,
        "regression":     reg,
        "interpretation": interpret_pearson(r),
    }
