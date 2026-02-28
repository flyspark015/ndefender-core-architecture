from __future__ import annotations

from typing import Callable, List

from .models import EventEnvelope


class EventBus:
    def __init__(self) -> None:
        self._subscribers: List[Callable[[EventEnvelope], None]] = []

    def subscribe(self, handler: Callable[[EventEnvelope], None]) -> None:
        self._subscribers.append(handler)

    def publish(self, event: EventEnvelope) -> None:
        for handler in list(self._subscribers):
            handler(event)
