"""
리드타임 (Lead Time) 계산
dashboard.html 참조: lt_11, lt_ch1, lt_21, lt_ch2 계산 로직

리드타임 = 수강 시작일부터 특정 강의/챕터를 완료하기까지 걸린 시간 (소수 시간 단위)
"""

from typing import Optional
from utils import avg, parse_kor_time, format_hours


def calc_lt_avg(students: list[dict], lt_key: str) -> Optional[float]:
    """
    특정 리드타임 지표의 평균을 계산

    Parameters
    ----------
    students : 수강생 레코드 리스트 (lt_key 필드 포함)
    lt_key   : 'lt_11' | 'lt_ch1' | 'lt_21' | 'lt_ch2'

    Returns
    -------
    평균 리드타임 (소수 시간), 데이터 없으면 None
    """
    values = [r.get(lt_key) for r in students]
    return avg(values)


def parse_lt_fields(row: dict) -> dict:
    """
    원시 CSV 행의 한국어 시간 문자열을 소수 시간으로 파싱하여 반환

    원시 컬럼 매핑 (0-indexed):
      col 12 → lt_11  (1-1강 이수 리드타임)
      col 13 → lt_ch1 (1챕터 완료 리드타임)
      col 16 → lt_21  (2-1강 이수 리드타임)
      col 17 → lt_ch2 (2챕터 완료 리드타임)
    """
    return {
        "lt_11":  parse_kor_time(row.get("raw_lt_11", "")),
        "lt_ch1": parse_kor_time(row.get("raw_lt_ch1", "")),
        "lt_21":  parse_kor_time(row.get("raw_lt_21", "")),
        "lt_ch2": parse_kor_time(row.get("raw_lt_ch2", "")),
    }


def lt_summary(students: list[dict]) -> dict:
    """
    전체 수강생 기준 리드타임 요약 통계 반환

    Returns
    -------
    {
        'lt_11_avg':  float | None,  # 1-1강 평균 리드타임 (시간)
        'lt_ch1_avg': float | None,  # 1챕터 평균 리드타임 (시간)
        'lt_21_avg':  float | None,
        'lt_ch2_avg': float | None,
        'lt_11_display':  str,       # 사람이 읽기 쉬운 포맷
        'lt_ch1_display': str,
    }
    """
    lt_11_avg  = calc_lt_avg(students, "lt_11")
    lt_ch1_avg = calc_lt_avg(students, "lt_ch1")
    lt_21_avg  = calc_lt_avg(students, "lt_21")
    lt_ch2_avg = calc_lt_avg(students, "lt_ch2")

    return {
        "lt_11_avg":      lt_11_avg,
        "lt_ch1_avg":     lt_ch1_avg,
        "lt_21_avg":      lt_21_avg,
        "lt_ch2_avg":     lt_ch2_avg,
        "lt_11_display":  format_hours(lt_11_avg),
        "lt_ch1_display": format_hours(lt_ch1_avg),
    }
