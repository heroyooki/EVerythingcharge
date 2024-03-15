from datetime import datetime

import arrow
from propan import apply_types, Depends

from core.annotations import Settings


def get_utc() -> datetime:
    return arrow.utcnow().datetime


@apply_types
def get_formatted_utc(settings: Settings, utc: datetime = Depends(get_utc)) -> str:
    return utc.strftime(settings.UTC_DATETIME_FORMAT)
