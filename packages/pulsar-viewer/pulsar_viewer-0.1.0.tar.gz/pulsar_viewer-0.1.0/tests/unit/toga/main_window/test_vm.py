import asyncio
from unittest.mock import create_autospec

from pytest import fixture
from pulsar_viewer.toga.main_window._vm import MainWindowVM
from pulsar_viewer.toga.main_window._structs import MessageRow
from pulsar_viewer.pulsar import PulsarPoller, Message

from ._async_mocker import AsyncMocker, trigger_coro


def _example_message(message_i: int):
    return Message(
        payload=b"m" + str(message_i).encode(),
        id=Message.ID(partition=-1, batch_index=-1, ledger_id=0, entry_id=message_i),
    )


class TestMainWindowVM:
    @staticmethod
    def test_factory():
        vm = MainWindowVM.standard(pulsar_url=":url:", topic_fq=":topic:")

        assert vm is not None
        assert vm._delegate is None
        assert isinstance(vm._poller, PulsarPoller)
        assert vm.pulsar_url == ":url:"
        assert vm.topic_fq == ":topic:"

    @staticmethod
    def test_initial_rows():
        # Given
        poller_mock = create_autospec(PulsarPoller)
        poller_mock.read_new_batch.return_value = [
            _example_message(1),
            _example_message(2),
        ]
        vm = MainWindowVM(poller=poller_mock)

        # When
        rows = vm.initial_rows

        # Then
        assert len(rows) == 2

        assert rows[0].title == "Ledger 0, Entry 1"
        assert rows[0].subtitle == "m1"

        assert rows[1].title == "Ledger 0, Entry 2"
        assert rows[1].subtitle == "m2"

    class TestPollingLoop:
        @fixture
        @staticmethod
        def poller_mock():
            return create_autospec(PulsarPoller)

        @fixture
        @staticmethod
        def vm(poller_mock):
            return MainWindowVM(poller=poller_mock)

        @fixture
        @staticmethod
        def delegate_spy(vm):
            delegate_spy = create_autospec(MainWindowVM.Delegate)
            vm.register_delegate(delegate_spy)
            return delegate_spy

        @staticmethod
        def test_empty_data(vm, delegate_spy):
            # Given
            def _sleep_callback():
                vm._should_continue_polling = False

            sleep_mocker = AsyncMocker(asyncio, "sleep", on_await=_sleep_callback)

            with sleep_mocker:
                # When
                coro = vm.polling_loop()
                trigger_coro(coro)

            # Then
            delegate_spy.append_rows.assert_called_once()
            delegate_spy.append_rows.assert_called_with([])

        @staticmethod
        def test_batches(poller_mock, vm, delegate_spy):
            # Given
            sleep_counter = 0
            poller_mock.read_new_batch.return_value = [
                _example_message(1),
                _example_message(2),
            ]

            def _sleep_callback():
                nonlocal sleep_counter

                if sleep_counter == 0:
                    poller_mock.read_new_batch.return_value = [
                        _example_message(3),
                        _example_message(4),
                    ]
                else:
                    vm._should_continue_polling = False

                sleep_counter += 1

            sleep_mocker = AsyncMocker(asyncio, "sleep", on_await=_sleep_callback)

            with sleep_mocker:
                # When
                coro = vm.polling_loop()
                trigger_coro(coro)

            # Then
            assert (
                len(delegate_spy.append_rows.call_args_list) == 2
            ), "Invalid number of batches"

            batch1: list[MessageRow] = delegate_spy.append_rows.call_args_list[0].args[
                0
            ]
            assert batch1[0].title == "Ledger 0, Entry 1"
            assert batch1[0].subtitle == "m1"

            assert batch1[1].title == "Ledger 0, Entry 2"
            assert batch1[1].subtitle == "m2"

            batch2: list[MessageRow] = delegate_spy.append_rows.call_args_list[1].args[
                0
            ]
            assert batch2[0].title == "Ledger 0, Entry 3"
            assert batch2[0].subtitle == "m3"

            assert batch2[1].title == "Ledger 0, Entry 4"
            assert batch2[1].subtitle == "m4"
