from dataclasses import dataclass


@dataclass
class Message:
    @dataclass
    class ID:
        partition: int
        ledger_id: int
        entry_id: int
        batch_index: int

    payload: bytes
    id: ID
