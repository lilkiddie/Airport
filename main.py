from common.structs.row_struct import Row
from utils.flight_board import get_flight_boards_from_csv

csv_row = 'S-0712,S7,2024-01-01 12:00:00,2024-01-01 13:30:00,Boeing-737,medium,'
print(Row.from_csv(csv_row))


