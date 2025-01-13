import datetime
from dataclasses import dataclass
from enum import Enum


class Country(Enum):
    """
    Calendar Country List.

    An enumeration of countries.

    Countries eligible for calendars exclusion.
    """

    ALL= "global"
    US = "usa"
    GB = "england"
    FR = "france"
    DE = "germany"
    JP = "japan"


@dataclass
class CalendarExtract():
    """
    Hold the data class associated with each column of common calendar file.
    """

    country : Country
    exclude_date : datetime.datetime

    def __post_init__(self):
        self.exclude_date = datetime.datetime.strptime(self.exclude_date, '%Y-%m-%d')
        if self.country.lower() not in [b1.value for b1 in Country]:
            print("Unexpected country in calendar input file: Skipping", self.country)