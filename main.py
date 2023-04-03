
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import inspect
import math
import random
import pandas as pdb
import numpy as np
import matplotlib.pyplot as plt
import random
import operator
from file_reader import FileReader
from car import Car
from fitness import Fitness
INF = 2 ** 24

establishments = FileReader.get_establishments()
distances = FileReader.get_distances()

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
def randomSolution(cars):
    cities = list(range(len(establishments)))

    for i in range(len(establishments)):        
        for car in cars:
            randomCity = cities[random.randint(0, len(cities) - 1)]
            inspect = float(establishments[randomCity].inspec_duration)
            dist = float(distances[car.place][int(establishments[randomCity].id)])
            wait = waitingTime(car.time + float(distances[car.place][int(establishments[randomCity].id)]), establishments[randomCity].opening_hours)
            time = inspect + dist + wait
            car.place = establishments[randomCity].id
            establishments[randomCity].visited = True
            car.time += time
            car.route.append(establishments[randomCity].id)
            cities.remove(randomCity)
            if len(cities) == 0:
                break
        if len(cities) == 0:
            break

#gives the time of a route
def routeTime(solution):
    routeTime = 0
    for k in range(len(solution)-1):
        a = solution[k]
        i = solution[k+1]
        inspect = float(establishments[i].inspec_duration)
        dist = float(distances[a][int(establishments[i].id)])
        wait = waitingTime(routeTime + dist + 9 * 3600, establishments[i].opening_hours)
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
def getBestNeighbour(neighbours):
    bestRouteTime = routeTime(neighbours[0])
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentRouteTime = routeTime(neighbour)
        if currentRouteTime < bestRouteTime:
            bestRouteTime = currentRouteTime
            bestNeighbour = neighbour
    return bestNeighbour, bestRouteTime

#Does the hill climb algorithm
def hillClimb(cars, choice):
    if choice:
        randomSolution(cars)
    else:
        greedy(cars)
    b = cars[0].time
    for car in cars:
        if car.time > b:
            b = car.time
    print("Initial time: " + str(b/3600))
    for car in cars:
        car.time = routeTime(car.route)
        neighbours = getNeighbours(car.route)
        bestNeighbour, bestNeighbourRouteTime = getBestNeighbour(neighbours)
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
            bestNeighbour, bestNeighbourRouteTime = getBestNeighbour(neighbours)


#----------    HILL CLIMB    ----------#



#-----------   GENETIC ALGO   -----------#

#creates a random route
def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route

#creates the initial population
def initialPopulation(popSize, cityList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))
    return population

#returns a sorted list with the best routes
def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i],routeTime(population[i])).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

#returns the best results to form the mating pool
def selection(popRanked, eliteSize):
    selectionResults = []
    df = pdb.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

#creates a mating pool for the population
def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

#Breeds two parents together to form a child
def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child

#Creates the next generation with crossover
def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

#returns a mutated individual
def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

#returns a mutated population to help avoid local convergence
def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

#Return the Next Generation by putting all the pieces together
def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

#Does the genetic algorithm
def genetic(cars, popSize, eliteSize, mutationRate, generations,choice):
    if choice:
        randomSolution(cars)
    else:
        greedy(cars)

    b = 0
    for car in cars:
        if b < car.time:
            b = car.time
    print("Initial time: " + str(b/3600-9))

    for car in cars:
        #print(car.time/3600-9)
        pop = initialPopulation(popSize, car.route)
        for i in range(0, generations):
            pop = nextGeneration(pop, eliteSize, mutationRate)
        time = 1 / rankRoutes(pop)[0][1]
        bestRouteIndex = rankRoutes(pop)[0][0]
        car.route = pop[bestRouteIndex]
        car.time = time

#-----------   GENETIC ALGO   -----------#
        
#------------    GREEDY    ------------#
# Does the greedy algorithm for all car routes
def greedy(cars):
    for i in range(11):
        for car in cars:  
            min_time = INF
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
    cars = [Car(x) for x in range(100)]

    while True:
        print("1) HILL CLIMB RANDOM")
        print("2) HILL CLIMB GREEDY")
        print("3) GENETIC RANDOM")
        print("4) GENETIC GREEDY")
        print("0) exit")
        choice = input()
        for est in establishments:
            est.visited = False
        if choice == '1':
            hillClimb(cars,1)
        elif choice == '2':
            hillClimb(cars,0)
        elif choice == '3':
            genetic(cars, 100, 20, 0.01, 500,1)
        elif choice == '4':
            genetic(cars, 100, 20, 0.01, 500,0)
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
