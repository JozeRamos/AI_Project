
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import sys
from file_reader import FileReader
from car import Car
INF = 2 ** 24

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def waitingTime(car_time, opening_hours):
    a = math.ceil(car_time/3600)
    while a > 23:
        a -= 24
    start_index = 23 - len(opening_hours[a:])
    next_day = len(opening_hours[a:])
    for i in range(start_index, 23):
        if opening_hours[i] == 1:
            return (i - start_index)*3600
    for i in range(0, start_index-1):
        if opening_hours[i] == 1:
            return (i + next_day)*3600
    return INF
        
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    establishments = FileReader.get_establishments()
    distances = FileReader.get_distances()

    cars = [Car(x) for x in range(100)]
    

