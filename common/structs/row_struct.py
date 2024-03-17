from dataclasses import dataclass
from datetime import datetime
from common.consts import FlightType, AircraftType



@dataclass(slots=True)
class Row:
    flight_number: int
    company: str
    date: datetime
    aircraft_model: str
    aircraft_type: str
    type: FlightType
    status: str = None

    @classmethod
    def from_csv(cls, csv_row: str, sep: str =',') -> 'Row':
        csv_row = csv_row.split(sep)
        return cls(
            flight_number=csv_row[0],
            company=csv_row[1],
            date=datetime.strptime(csv_row[2], '%Y-%m-%d %H:%M:%S'),
            aircraft_model=csv_row[3],
            aircraft_type=AircraftType(csv_row[4]),
            status=csv_row[5] if csv_row[5] != '' else None,
            type=FlightType.from_str(csv_row[6])
        )
