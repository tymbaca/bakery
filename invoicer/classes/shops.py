import datetime
from enum import Enum
from typing import NamedTuple, Optional


class Coordinates(NamedTuple):
    latitude: str
    longitude: str

    @property
    def value(self):
        return f"{self.latitude}, {self.longitude}"


class Shop(NamedTuple):
    id: str
    organisation: str
    address: str
    # coordinates: Coordinates
    # shop_name: Optional[str] = None
    # products:


class Workday(NamedTuple):
    shops: tuple[Shop]
    date: datetime.date


