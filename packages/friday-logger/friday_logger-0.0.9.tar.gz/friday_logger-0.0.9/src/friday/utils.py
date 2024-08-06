from datetime import datetime


from friday.types import DATETIME_FORMAT, FridayLogRecord, Level


def datetime_to_string(value: datetime):

    "Converts the datetime object to string format used by friday database"

    return value.strftime(DATETIME_FORMAT)


def datetime_from_string(value: str):

    "Converts the timestamp string to datetime object"

    return datetime.strptime(value, DATETIME_FORMAT)


def parse_friday_log(data: dict) -> FridayLogRecord:

    return FridayLogRecord(
        id=data["id"],
        namespace=data["namespace"],
        topic=data["topic"],
        level=data["level"],
        data=data["data"],
        timestamp=datetime_from_string(data["timestamp"]),
    )
