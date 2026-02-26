from __future__ import annotations
import threading
import time
from typing import Callable, Mapping, Any, Optional

from .outbox import Outbox, OutboxMessage

Handler = Callable[[OutboxMessage], None]

class OutboxBus:
    """
    Hybrid bus:
    - Sync path: orchestrator emits to eventlog
    - Async path: orchestrator enqueues to outbox; worker delivers to handler(s)
    """
    def __init__(self, outbox: Outbox, poll_interval_s: float = 0.25) -> None:
        self.outbox = outbox
        self.poll_interval_s = poll_interval_s
        self._handlers: dict[str, Handler] = {}
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def subscribe(self, topic: str, handler: Handler) -> None:
        self._handlers[topic] = handler

    def publish_async(self, *, run_id: str, topic: str, payload: Mapping[str, Any]) -> int:
        return self.outbox.enqueue(run_id=run_id, topic=topic, payload=payload)

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, name="outbox-bus", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)

    def _loop(self) -> None:
        while not self._stop.is_set():
            msg = self.outbox.fetch_next_pending()
            if not msg:
                time.sleep(self.poll_interval_s)
                continue

            handler = self._handlers.get(msg.topic)
            if not handler:
                # no handler = dead (misconfig)
                self.outbox.mark_dead(msg.id, f"no handler for topic={msg.topic}")
                continue

            try:
                handler(msg)
                self.outbox.mark_sent(msg.id)
            except Exception as e:
                # deterministic: do not retry forever; mark dead
                self.outbox.mark_dead(msg.id, f"{type(e).__name__}: {e}")
