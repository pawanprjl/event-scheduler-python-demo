from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from app.events.event_type import EventType


@dataclass
class Event:
    type: EventType
    data: Dict[str, Any]
    timestamp: datetime
    correlation_id: Optional[str] = None  # For tracking related events

    @classmethod
    def create(
        cls,
        event_type: EventType,
        data: Dict[str, Any] = None,  # type: ignore
        correlation_id: str = None,  # type: ignore
    ):
        return cls(
            type=event_type,
            data=data or {},
            timestamp=datetime.now(),
            correlation_id=correlation_id,
        )
