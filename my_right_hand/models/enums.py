from enum import Enum


class RelationshipTypes(Enum):
    PERSONAL = "personal"
    CUSTOMER = "customer"
    SUPERIOR = "superior"
    EMPLOYEE = "employee"
    SELF = "self"
    OTHER = "other"


class FrequencyPeriod(Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    ONE_TIME = "one_time"


class ThreeTier(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskTypes(Enum):
    BUSINESS = "business"
    PERSONAL = "personal"


class Critera(Enum):
    CHECK_AND_CLOSE = "check_and_close"
    THIRD_PARTY_CONFIRM = "third_party_confirm"
    FIRST_PARTY_CONFIRM = "first_party_confirm"
