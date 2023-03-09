
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
        b = 0
        start_index = len(opening_hours) - len(opening_hours[a:])
        for i in range(start_index, len(opening_hours)-1):
            if opening_hours[i] == 1:
                return (i - start_index)*3600
        for i in range(b, len(opening_hours)-1):
            if opening_hours[i] == 1:
                return (i - start_index)*3600 + 3600 * 24 - a * 60
        return INF
        
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    establishments = FileReader.get_establishments()
    distances = FileReader.get_distances()

    cars = [Car(x) for x in range(100)]
    
    # best local = inspec duration + travel time + getWaitingTime()
    #for i in range(len(distances)):

    for i in range(11):
        for car in cars:   
            min_time = sys.maxsize
            flag = False
            for estab in establishments:               
                if estab.visited or (estab.id == car.place): continue
                time = float(estab.inspec_duration) + float(distances[car.place][int(estab.id)]) + waitingTime(car.time + float(distances[car.place][int(estab.id)]), estab.opening_hours)
                if(time < min_time):
                     min_time = round(time,2)
                     next_hop = estab
                     flag = True
            if not flag:
                 continue
            print(f'car with id {car.id} in place {car.place} going to {next_hop.id} with {min_time} second, or {round(min_time/3600,2)}h with fulltime {car.time/3600}')
            car.place = next_hop.id

            next_hop.visited = True
            car.time = min_time + car.time
            car.route.append(next_hop.id)
    
    print(f'total estabs: {len(establishments)}')
    print(f'visited estabs: {len([x for x in establishments if x.visited])}')
    print(f'not visited estabs: {len([x for x in establishments if not x.visited])}')
  #  for estab in establishments:
 #      if not estab.visited:
#             print(f'estab {estab.id} is not visited!')


        
        



#inspec duration + travel time + getWaitingTime()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
