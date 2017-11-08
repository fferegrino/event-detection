from typing import List

from structures.tweet import Tweet

class Burst:

    def __init__(self, entity: str):
        self.documents: List[Tweet] = []
        self.entity = entity

    def __len__(self):
        return len(self.documents)

    def add_document(self, d: Tweet):
        self.documents.append(d)

    def max_date(self):
        l = len(self)
        if l > 0:
            return self.documents[l - 1].timestamp_ms
        return 0

    def min_date(self):
        l = len(self)
        if l > 0:
            return self.documents[0].timestamp_ms
        return 0