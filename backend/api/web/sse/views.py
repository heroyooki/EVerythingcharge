from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class Event(BaseModel):
    data: Any
    event: str = "message"
