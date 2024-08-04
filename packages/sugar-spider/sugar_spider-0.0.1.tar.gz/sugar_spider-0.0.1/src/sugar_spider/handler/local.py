from typing import List


class MemoryStore:
    def __init__(self):
        self.store = list()

    async def __call__(self, records: List[dict]):
        self.store += records
        return records
