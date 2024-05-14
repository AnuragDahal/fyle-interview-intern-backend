# This file contains helper functions that are used in the project.
import datetime

TIMESTAMP_WITH_TIMEZONE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


class GeneralObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def get_utc_now():
    return datetime.datetime.now(datetime.timezone.utc)
