from typing import Any
from functools import cached_property
from unittest.mock import patch, AsyncMock


class AsyncMocker:
    def __init__(self, target: Any, attribute: str, on_await):
        self._target = target
        self._attribute = attribute
        self._on_await = on_await

    @cached_property
    def our_patch(self):
        mock = AsyncMock()

        def _side_effect(*args, **kwargs):
            self._on_await()

        mock.side_effect = _side_effect

        return patch.object(self._target, self._attribute, mock)

    def __enter__(self, *args, **kwargs):
        self.our_patch.__enter__(*args, **kwargs)

    def __exit__(self, *args, **kwargs):
        self.our_patch.__exit__(*args, **kwargs)


def trigger_coro(coro):
    try:
        coro.send(None)
    except StopIteration:
        pass
