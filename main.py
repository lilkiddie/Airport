import pygame
# from common.structs.row_struct import Row
from common.structs.message_queue import MessageQueue, Request
from common.structs.airport import ControlRoom, Runway, RunwayType
from utils.flight_board import get_flight_boards_from_csv

N_RUNWAYS = 10

queue = MessageQueue()
flight_board = get_flight_boards_from_csv('test.csv', sep=',')
runways = [Runway(id, RunwayType.land) for id in range(1, N_RUNWAYS)]
control_room = ControlRoom(flight_board, runways=runways)
aircrafts = [flight.aircraft for flight in flight_board.flights.values()]


queue.put_message(Request(flight_board.flights['S-0712'], RunwayType.land))


while True:
    while request:=queue.get_message() is not None:
        control_room(request)
