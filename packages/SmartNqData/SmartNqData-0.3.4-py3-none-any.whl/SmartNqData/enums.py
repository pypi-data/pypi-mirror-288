# SmartNqData/enums.py

from enum import Enum, auto

class Timeframe(Enum):
    MINUTE = "Minute"
    FIVE_MINUTES = "FiveMinutes"
    TEN_MINUTES = "TenMinutes"
    FIFTEEN_MINUTES = "FifteenMinutes"
    THIRTY_MINUTES = "ThirtyMinutes"
    HOUR = "Hour"
    FOUR_HOURS = "FourHours"
    DAILY = "Daily"

class Indicator(Enum):
    ROC5 = auto()
    ROC10 = auto()
    ROC30 = auto()
    ROC60 = auto()
    ROC120 = auto()
    ROC240 = auto()
    EMA7 = auto()
    EMA14 = auto()
    EMA21 = auto()
    EMA50 = auto()
    EMA100 = auto()
    EMA200 = auto()
    RSI10 = auto()
    RSI30 = auto()
    RSI60 = auto()
    RSI120 = auto()
    RSI240 = auto()
    RSI480 = auto()
    MACD9 = auto()
    ATR14 = auto()
    ATR30 = auto()
    ATR60 = auto()
    ATR120 = auto()
    HMAH10 = auto()
    HMAH11 = auto()
    HMAL10 = auto()
    HMAL11 = auto()
    HMAC200 = auto()
    HMAC225 = auto()
    ADX7 = auto()
    ADX14 = auto()
    ADX20 = auto()
    KDJ14 = auto()
