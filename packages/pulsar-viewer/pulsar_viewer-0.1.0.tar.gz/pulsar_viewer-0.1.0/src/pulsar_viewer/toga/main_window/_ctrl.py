from functools import cached_property

import toga
import toga.sources
import toga.style

from ._vm import MainWindowVM
from ._structs import MessageRow


class MainWindowCtrl:
    """
    Main Window's Controller. Glue code between toga and the View Model. Allows
    the View Model to encapsulate the logic without the dependence on toga.
    """

    def __init__(self, vm: MainWindowVM):
        self._vm = vm

    @classmethod
    def standard(cls, pulsar_url: str, topic_fq: str):
        vm = MainWindowVM.standard(pulsar_url=pulsar_url, topic_fq=topic_fq)
        ctrl = cls(vm=vm)
        vm.register_delegate(ctrl)
        return ctrl

    @property
    def background_tasks(self) -> list:
        return [self._polling_background_task]

    async def _polling_background_task(self, app: toga.App, **kwargs):
        await self._vm.polling_loop()

    @cached_property
    def data_source(self) -> toga.sources.ListSource:
        return toga.sources.ListSource(
            accessors=MessageRow._fields,
            data=self._vm.initial_rows,
        )

    @property
    def widget(self) -> toga.Widget:
        url_label = toga.Label(text=f"Pulsar URL: {self._vm.pulsar_url}")
        topic_label = toga.Label(text=f"Topic: {self._vm.topic_fq}")
        messages_view = toga.DetailedList(
            data=self.data_source,
            style=toga.style.Pack(flex=1),
        )
        vertical_box = toga.Box(
            children=[url_label, topic_label, messages_view],
            style=toga.style.Pack(direction="column"),
        )

        return vertical_box

    def prepend_rows(self, rows: list[MessageRow]):
        for row in rows[::-1]:
            self.data_source.insert(0, row)

    def append_rows(self, rows: list[MessageRow]):
        for row in rows:
            self.data_source.append(row)
