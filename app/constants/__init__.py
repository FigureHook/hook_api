from enum import Enum


class SourceSite:
    GSC_ANNOUNCEMENT = "gsc_announcement"
    GSC_SHIPMENT = "gsc_shipment"
    GSC_DELAY = "gsc_delay"
    ALTER_ANNOUNCEMENT = "alter_announcement"
    NATIVE_ANNOUNCEMENT = "native_announcement"


class PeriodicTask(Enum):
    DISCORD_NEW_RELEASE_PUSH = 1
    PLURK_NEW_RELEASE_PUSH = 2


class WebhookCurrency(str, Enum):
    JPY = "JPY"
    USD = "USD"
    EUR = "EUR"


class WebhookLang(str, Enum):
    ZH_TW = "zh-TW"
    EN = "en"
    JA = "ja"
