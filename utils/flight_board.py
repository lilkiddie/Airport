from common.structs.row_struct import Row
from common.structs.airport import Aircraft, Flight, FlightBoard
from utils.converters import total_seconds


def get_flight_boards_from_csv(file_path: str, sep=',') -> tuple[FlightBoard, list[Aircraft]]:
    with open(file_path) as file:
        headers = tuple(file.readline().strip().split(sep))
        if set(headers) != set(Row.__slots__):
            raise ValueError('File is invalid')
        flights = {}
        aircrafts = []
        for csv_row in file.readlines():
            row = Row.from_csv(csv_row, sep)
            aircrafts.append(Aircraft(row.aircraft_model, row.flight_number, row.aircraft_type))
            flights[row.flight_number] = Flight(row.flight_number, row.date, row.status, row.type, total_seconds(row.date))

        return FlightBoard(flights), aircrafts
