"""
공통 유틸리티 함수
dashboard.html의 avg(), parseKorTime() 로직을 Python으로 옮긴 것
"""

import re
from typing import Optional


def avg(values: list[Optional[float]]) -> Optional[float]:
    """
    유효한 값(None, NaN, 음수 제외)의 평균을 반환
    값이 없으면 None 반환
    """
    valid = [v for v in values if v is not None and v == v and v >= 0]
    if not valid:
        return None
    return sum(valid) / len(valid)


def parse_kor_time(text: str) -> Optional[float]:
    """
    한국어 시간 문자열을 소수 시간(float hours)으로 변환
    예: "5시간30분45초" → 5.5125

    dashboard.html parseKorTime() 참조
    """
    if not text or not isinstance(text, str):
        return None

    hours = 0.0
    minutes = 0.0
    seconds = 0.0

    h_match = re.search(r"(\d+)시간", text)
    m_match = re.search(r"(\d+)분", text)
    s_match = re.search(r"(\d+)초", text)

    if h_match:
        hours = float(h_match.group(1))
    if m_match:
        minutes = float(m_match.group(1))
    if s_match:
        seconds = float(s_match.group(1))

    total = hours + minutes / 60 + seconds / 3600
    return total if total > 0 else None


def format_hours(hours: Optional[float]) -> str:
    """
    소수 시간을 사람이 읽기 쉬운 문자열로 변환
    - 1시간 미만: "XX분"
    - 1~24시간: "X.Xh"
    - 24시간 이상: "X일 Xh"
    """
    if hours is None:
        return "-"
    if hours < 1:
        return f"{round(hours * 60)}분"
    if hours < 24:
        return f"{hours:.1f}h"
    days = int(hours // 24)
    rem = hours % 24
    return f"{days}일 {rem:.0f}h"
