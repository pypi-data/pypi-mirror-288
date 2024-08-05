import toga
from ..main_window import MainWindowCtrl


class AppCtrl:
    def __init__(self, main_window_ctrl: MainWindowCtrl):
        self._main_window_ctrl = main_window_ctrl

    @classmethod
    def standard(cls, pulsar_url: str, topic_fq: str):
        return cls(
            main_window_ctrl=MainWindowCtrl.standard(
                pulsar_url=pulsar_url, topic_fq=topic_fq
            )
        )

    def startup(self, app: toga.App, **kwargs) -> toga.Widget:
        """
        Matches `toga.app.AppStartupMethod`. Returns content of the main window.
        """
        return self._main_window_ctrl.widget

    @property
    def background_tasks(self) -> list:
        return self._main_window_ctrl.background_tasks
