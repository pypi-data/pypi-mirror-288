from typing import TypedDict, List, Optional, Literal
from datetime import datetime
from enum import Enum


class NamespaceAndTopics(TypedDict):
    namespace: str
    topic: str


Level = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class QueryInput(TypedDict):
    namespace_and_topics: List[NamespaceAndTopics]
    level: Optional[Level]
    before: Optional[datetime]
    after: Optional[datetime]
    limit: Optional[int]


class FridayLogRecord(TypedDict):
    id: int
    namespace: str
    topic: str
    level: Level
    data: str
    timestamp: datetime


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
