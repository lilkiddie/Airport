# from common.structs.row_struct import Row
from common.structs.airport import Airport
from utils.flight_board import get_flight_boards_from_csv
from random import choices, randint
import pprint

N_RUNWAYS = 1


class Experiment:
    def __init__(self, filepath: str, airport_name: str = 'Test', n_runways: int = 5):
        flight_board, aircrafts = get_flight_boards_from_csv(filepath)
        self.airport = Airport(airport_name, flight_board, aircrafts, n_runways)
        self._ticks = 0
        self._history = []

    def __call__(self):
        print(f'{self.__class__.__name__} ticks')
        self.airport()
        self._ticks += 1


experiment = Experiment('test.csv', 'test', N_RUNWAYS)

pprint.pprint(experiment.airport.flight_board.flights)
print()


experiment()
