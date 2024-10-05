from enum import Enum


class Period(str, Enum):
    WEEKLY = "period_7"
    MONTHLY = "period_30"
    ALL = "period_all"
