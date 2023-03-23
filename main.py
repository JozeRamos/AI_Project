
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import inspect
import math
import random
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
    return 0

def randomSolution(cars, est, distances):
    cities = list(range(len(est)))

    for i in range(len(est)):        
        for car in cars:
            randomCity = cities[random.randint(0, len(cities) - 1)]
            time = float(est[randomCity].inspec_duration) + float(distances[car.place][int(est[randomCity].id)]) + waitingTime(car.time + float(distances[car.place][int(est[randomCity].id)]), est[randomCity].opening_hours)
            #print(time)
            car.place = est[randomCity].id
            est[randomCity].visited = True
            car.time += time
            car.route.append(est[randomCity].id)
            cities.remove(randomCity)
            if len(cities) == 0:
                break
        if len(cities) == 0:
            break
    # for car in cars:
    #     print(car.route)
    #     print(car.time/3600)        
    return

def routeTime(solution,est,distances):
    routeTime = 0
    for k in range(len(solution)-1):
        a = solution[k]
        i = solution[k+1]
        inspect = float(est[i].inspec_duration)
        #print(inspect)
        dist = float(distances[a][int(est[i].id)])
        #print(dist)
        wait = waitingTime(routeTime + float(distances[a][int(est[i].id)]), est[i].opening_hours)
        #print(wait)
        routeTime += inspect + dist + wait
        #print("-----------------")
    return routeTime

def getNeighbours(solution):
    neighbours = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i] = solution[j]
            neighbour[j] = solution[i]
            neighbours.append(neighbour)
    return neighbours

def getBestNeighbour(neighbours,est,dis):
    bestRouteTime = routeTime(neighbours[0],est,dis)
    #bestRouteLength = routeLength(tsp, neighbours[0])
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentRouteTime = routeTime(neighbour,est,dis)
        #currentRouteLength = routeLength(tsp, neighbour)
        if currentRouteTime < bestRouteTime:
            bestRouteTime = currentRouteTime
            bestNeighbour = neighbour
    return bestNeighbour, bestRouteTime

def hillClimb(cars, est, dis):
    randomSolution(cars,est, dis)
    for car in cars:
        neighbours = getNeighbours(car.route)
        bestNeighbour, bestNeighbourRouteTime = getBestNeighbour(neighbours,est,dis)
        #print(car.time/3600)
        #for i in range(700):        
        for x in range(700):
            car.route = bestNeighbour
            car.time = bestNeighbourRouteTime
            neighbours = getNeighbours(car.route)
            bestNeighbour, bestNeighbourRouteTime = getBestNeighbour(neighbours,est,dis)
            #print(car.time/3600)
        #print("-------------------------")
    b = 0
    for car in cars:
        if car.time > b:
            b = car.time
    #print(b/3600)
    return
        
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    establishments = FileReader.get_establishments()
    distances = FileReader.get_distances()

    cars = [Car(x) for x in range(100)]
    hillClimb(cars,establishments, distances)
    b = cars[0].time
    for car in cars:
        print(car.route)
        print(car.time/3600-9)
        if car.time > b:
            b = car.time
        #print(car.id)
    print(b/3600-9)
    
