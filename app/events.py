from __future__ import annotations

from queue import Queue
from threading import Lock
from typing import Dict, List


class EventHub:
    def __init__(self) -> None:
        self._queues: List[Queue] = []
        self._lock = Lock()

    def subscribe(self) -> Queue:
        queue: Queue = Queue()
        with self._lock:
            self._queues.append(queue)
        return queue

    def unsubscribe(self, queue: Queue) -> None:
        with self._lock:
            if queue in self._queues:
                self._queues.remove(queue)

    def publish(self, event: Dict) -> None:
        with self._lock:
            queues = list(self._queues)
        for queue in queues:
            queue.put(event)


EVENT_HUB = EventHub()
