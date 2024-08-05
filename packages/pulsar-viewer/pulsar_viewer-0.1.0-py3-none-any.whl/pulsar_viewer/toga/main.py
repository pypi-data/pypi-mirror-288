import click
import toga

from .app import AppCtrl


def app_main(pulsar_url: str, topic_fq: str):
    app_controller = AppCtrl.standard(pulsar_url=pulsar_url, topic_fq=topic_fq)
    app = toga.App(
        formal_name="Pulsar Viewer",
        app_id="com.alexjuda.pulsarviewer",
        startup=app_controller.startup,
    )

    for task in app_controller.background_tasks:
        app.add_background_task(task)

    app.main_loop()


@click.command()
@click.option(
    "--pulsar-url",
    default="pulsar://localhost:6650",
    help="Pulsar Client URL",
    show_default=True,
)
@click.option(
    "--topic",
    required=True,
    prompt="Fully-qualified topic name",
    help="Fully-qualified topic name, like persistent://mytenant/myns/mytopic",
)
def cli_main(pulsar_url: str, topic: str):
    app_main(pulsar_url=pulsar_url, topic_fq=topic)


if __name__ == "__main__":
    cli_main()
