from datetime import datetime, timezone
from pulsar_viewer.pulsar import PulsarPoller
import json
import time

import pytest
from pytest import fixture
import pulsar


def _current_timestamp() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp())


def _produce(pulsar_url: str, topic: str, msg: dict):
    payload = json.dumps(msg).encode()

    client = pulsar.Client(pulsar_url)
    producer = client.create_producer(
        topic,
        producer_name="test_pulsar_poller",
    )
    producer.send(payload)


class TestReadNewBatch:
    @staticmethod
    @fixture(scope="class")
    def topic():
        timestamp = _current_timestamp()
        topic = f"persistent://tests/integration/test_pulsar_poller-{timestamp}"
        return topic

    @staticmethod
    @fixture(scope="class")
    def pulsar_url():
        return "pulsar://localhost:6650"

    @staticmethod
    @fixture(scope="class")
    def poller(pulsar_url: str, topic: str):
        return PulsarPoller(
            pulsar_url=pulsar_url,
            topic_fq=topic,
        )

    @staticmethod
    @pytest.mark.dependency()
    def test_empty_topic(poller: PulsarPoller):
        batch = poller.read_new_batch()

        assert batch == []

    @staticmethod
    @pytest.mark.dependency(depends=["TestReadNewBatch::test_empty_topic"])
    def test_reading_after_sending(pulsar_url: str, topic: str, poller: PulsarPoller):
        msg = {"hello": "world!"}
        _produce(pulsar_url=pulsar_url, topic=topic, msg=msg)
        _produce(pulsar_url=pulsar_url, topic=topic, msg=msg)

        # Give Pulsar some time to ingest the data
        time.sleep(0.5)

        batch = poller.read_new_batch()

        assert len(batch) == 2
        for read_msg in batch:
            assert json.loads(read_msg.payload.decode()) == msg

            assert read_msg.id is not None
            # The default values are -1. Looks like Pulsar starts the indices
            # with 0.
            assert read_msg.id.ledger_id >= 0
            assert read_msg.id.entry_id >= 0

    @staticmethod
    @pytest.mark.dependency(depends=["TestReadNewBatch::test_reading_after_sending"])
    def test_no_new_data(poller: PulsarPoller):
        batch = poller.read_new_batch()

        assert batch == []
