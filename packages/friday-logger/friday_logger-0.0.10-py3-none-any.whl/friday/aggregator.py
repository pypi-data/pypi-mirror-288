from datetime import datetime
from friday.types import FridayLogRecord, NamespaceAndTopics, Level
from friday.utils import datetime_to_string, parse_friday_log
from typing import List, Optional
from urllib.parse import urljoin
import json
import requests


class Aggregator:
    def __init__(self, friday_endpoint: str):
        self.friday_endpoint = friday_endpoint

    # TODO: infer these types from QueryInput
    def query(
        self,
        namespace_and_topics: Optional[List[NamespaceAndTopics]] = None,
        level: Optional[Level] = None,
        before: Optional[datetime] = None,
        after: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> List[FridayLogRecord]:
        data = {}
        if namespace_and_topics:
            data["namespacesAndTopics"] = namespace_and_topics
        if level:
            data["level"] = level
        if before:
            data["before"] = datetime_to_string(before)
        if after:
            data["after"] = datetime_to_string(after)
        if limit:
            data["limit"] = limit

        resp = requests.get(
            urljoin(self.friday_endpoint, "getLogs"), params={"input": json.dumps(data)}
        )

        data = resp.json()["result"]["data"]
        parsed_data = [parse_friday_log(log) for log in data]
        return parsed_data
