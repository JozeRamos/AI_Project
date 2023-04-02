
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
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

def randomSolution(cars):
    cities = list(range(len(establishments)))

    for i in range(len(establishments)):        
        for car in cars:
            randomCity = cities[random.randint(0, len(cities) - 1)]
            inspect = float(establishments[randomCity].inspec_duration)
            dist = float(distances[car.place][int(establishments[randomCity].id)])
            wait = waitingTime(car.time + float(distances[car.place][int(establishments[randomCity].id)]), establishments[randomCity].opening_hours)
            time = inspect + dist + wait
            #print(time)
            car.place = establishments[randomCity].id
            establishments[randomCity].visited = True
            car.time += time
            car.route.append(establishments[randomCity].id)
            cities.remove(randomCity)
            if len(cities) == 0:
                break
        if len(cities) == 0:
            break
    # for car in cars:
    #     print(car.route)
    #     print(car.time/3600)        
    return

def routeTime(solution):
    routeTime = 0
    for k in range(len(solution)-1):
        a = solution[k]
        i = solution[k+1]
        inspect = float(establishments[i].inspec_duration)
        #print(inspect)
        dist = float(distances[a][int(establishments[i].id)])
        #print(dist)
        wait = waitingTime(routeTime + dist + 9 * 3600, establishments[i].opening_hours)
        #print(wait)
        routeTime += inspect + dist + wait
        #print("-----------------")
    return routeTime


def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route

def initialPopulation(popSize, cityList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))
    return population

def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i],routeTime(population[i])).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

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

def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

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

def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

def genetic(cars, popSize, eliteSize, mutationRate, generations):

    randomSolution(cars)
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
        

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    

    cars = [Car(x) for x in range(100)]

    genetic(cars, 100, 20, 0.01, 500)

    b = 0
    for car in cars:
        if b < car.time:
            b = car.time
    print("Final time: " + str(b/3600))

    

