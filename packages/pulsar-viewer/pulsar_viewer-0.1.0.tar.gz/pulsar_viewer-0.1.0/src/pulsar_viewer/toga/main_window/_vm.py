import asyncio
from typing import Protocol

from ._structs import MessageRow
from ...pulsar import PulsarPoller, Message


class MainWindowVM:
    """
    View Model for the main window. Doesn't directly depend on `toga`.
    """

    class Delegate(Protocol):
        def prepend_rows(self, rows: list[MessageRow]): ...
        def append_rows(self, rows: list[MessageRow]): ...

    _delegate: Delegate | None = None

    # Allows breaking the loop during testing.
    _should_continue_polling: bool = True

    def __init__(self, poller: PulsarPoller):
        self._poller = poller

    @classmethod
    def standard(cls, pulsar_url: str, topic_fq: str):
        return cls(
            # TODO: figure out how to configure these
            poller=PulsarPoller(
                pulsar_url=pulsar_url,
                topic_fq=topic_fq,
            )
        )

    def register_delegate(self, delegate: Delegate):
        self._delegate = delegate

    @property
    def pulsar_url(self) -> str:
        return self._poller.pulsar_url

    @property
    def topic_fq(self) -> str:
        return self._poller.topic_fq

    @property
    def initial_rows(self) -> list[MessageRow]:
        messages = self._poller.read_new_batch()

        return [self._message_to_row(msg) for msg in messages]

    @staticmethod
    def _message_to_row(msg: Message) -> MessageRow:
        return MessageRow(
            title=f"Ledger {msg.id.ledger_id}, Entry {msg.id.entry_id}",
            subtitle=msg.payload.decode(),
        )

    async def polling_loop(self):
        while self._should_continue_polling:
            if self._delegate is None:
                continue

            new_batch = self._poller.read_new_batch()
            new_rows = [self._message_to_row(msg) for msg in new_batch]
            self._delegate.append_rows(new_rows)

            await asyncio.sleep(1)
