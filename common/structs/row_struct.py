from dataclasses import dataclass
from datetime import datetime
from common.structs.airport import AircraftType


@dataclass(slots=True)
class Row:
    flight_number: int
    company: str
    departure_date: datetime
    arrival_date: datetime
    aircraft_model: str
    aircraft_type: str
    status: str = None

    @classmethod
    def from_csv(cls, csv_row, sep=','):
        csv_row = csv_row.split(sep)
        return cls(
            flight_number=csv_row[0],
            company=csv_row[1],
            departure_date=datetime.strptime(csv_row[2], '%Y-%m-%d %H:%M:%S'),
            arrival_date=datetime.strptime(csv_row[3], '%Y-%m-%d %H:%M:%S'),
            aircraft_model=csv_row[4],
            aircraft_type=AircraftType(csv_row[5]),
            status=csv_row[6] if csv_row[6] != '' else None,
        )
