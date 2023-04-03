
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

#calculates the ammount of time a car has to wait
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

#gives a random solution for all cars
def randomSolution(cars, est, distances):
    cities = list(range(len(est)))

    for i in range(len(est)):        
        for car in cars:
            randomCity = cities[random.randint(0, len(cities) - 1)]
            inspect = float(est[randomCity].inspec_duration)
            dist = float(distances[car.place][int(est[randomCity].id)])
            wait = waitingTime(car.time + float(distances[car.place][int(est[randomCity].id)]), est[randomCity].opening_hours)
            time = inspect + dist + wait
            car.place = est[randomCity].id
            est[randomCity].visited = True
            car.time += time
            car.route.append(est[randomCity].id)
            cities.remove(randomCity)
            if len(cities) == 0:
                break
        if len(cities) == 0:
            break

#gives the time of a route
def routeTime(solution,est,distances):
    routeTime = 0
    for k in range(len(solution)-1):
        a = solution[k]
        i = solution[k+1]
        inspect = float(est[i].inspec_duration)
        dist = float(distances[a][int(est[i].id)])
        wait = waitingTime(routeTime + dist + 9 * 3600, est[i].opening_hours)
        routeTime += inspect + dist + wait
    return routeTime


#----------    HILL CLIMB    ----------#

#returns the neigbours of a route
def getNeighbours(solution):
    neighbours = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i] = solution[j]
            neighbour[j] = solution[i]
            neighbours.append(neighbour)
    return neighbours

#returns the neighbour route and its time
def getBestNeighbour(neighbours,est,dis):
    bestRouteTime = routeTime(neighbours[0],est,dis)
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentRouteTime = routeTime(neighbour,est,dis)
        if currentRouteTime < bestRouteTime:
            bestRouteTime = currentRouteTime
            bestNeighbour = neighbour
    return bestNeighbour, bestRouteTime

#Does the hill climb algorithm
def hillClimb(cars, est, dis, choice):
    if choice:
        randomSolution(cars,est, dis)
    else:
        greedy(cars,est,dis)
    b = cars[0].time
    for car in cars:
        if car.time > b:
            b = car.time
    print("Initial time: " + str(b/3600))
    for car in cars:
        car.time = routeTime(car.route,est,dis)
        neighbours = getNeighbours(car.route)
        bestNeighbour, bestNeighbourRouteTime = getBestNeighbour(neighbours,est,dis)
        temp = 0
        for i in range(700):
            temp += 1
            if temp > 20:
                break
            if car.time > bestNeighbourRouteTime:
                temp = 0
                car.route = bestNeighbour
                car.time = bestNeighbourRouteTime
            neighbours = getNeighbours(bestNeighbour)
            bestNeighbour, bestNeighbourRouteTime = getBestNeighbour(neighbours,est,dis)


#----------    HILL CLIMB    ----------#

#------------    GREEDY    ------------#
# Does the greedy algorithm for all car routes
def greedy(cars,establishments,distances):
    for i in range(10):
        for car in cars:   
            min_time = sys.maxsize
            flag = False
            for estab in establishments:               
                if estab.visited or (estab.id == car.place): continue
                time = float(estab.inspec_duration) + float(distances[car.place][int(estab.id)]) + waitingTime(car.time + float(distances[car.place][int(estab.id)]) + 9 * 3600, estab.opening_hours)
                if(time < min_time):
                     min_time = round(time,2)
                     next_hop = estab
                     flag = True
            if not flag:
                 continue
            car.place = next_hop.id

            next_hop.visited = True
            car.time = min_time + car.time
            car.route.append(next_hop.id)

#------------    GREEDY    ------------#

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    establishments = FileReader.get_establishments()
    distances = FileReader.get_distances()
    cars = [Car(x) for x in range(100)]

    while True:
        print("1) HILL CLIMB RANDOM")
        print("2) HILL CLIMB GREEDY")
        choice = input("0) exit")
        if choice == '1':
            hillClimb(cars,establishments, distances,1)
        elif choice == '2':
            hillClimb(cars,establishments, distances,0)
            for est in establishments:
                est.visited = False
        elif choice == '0':
            break
        else:
            continue

        b = cars[0].time
        for car in cars:
            print(car.route)
            print(car.time/3600)
            if car.time > b:
                b = car.time
            car.reset()
        print("Final time: " + str(b/3600))
    
