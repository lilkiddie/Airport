from common.structs.row_struct import Row
from common.structs.airport import Aircraft, Flight, FlightBoard
from functools import partial


def get_flight_boards_from_csv(file_path, sep=','):
    with open(file_path) as file:
        headers = tuple(file.readline().strip().split(sep))
        if headers != Row.__slots__:
            raise ValueError('File is invalid')
        flights = {}
        for csv_row in file.readlines():
            row = Row.from_csv(csv_row, sep)
            aircraft = Aircraft(row.aircraft_model, row.aircraft_type)
            flights[row.flight_number] = Flight(row.flight_number, row.departure_date, row.arrival_date, row.status, aircraft)

        return FlightBoard(flights)
