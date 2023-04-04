import math
import pandas as pdb
import numpy as np
import random
import operator
from file_reader import FileReader
from car import Car
from copy import deepcopy
from fitness import Fitness
INF = float('inf')

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

    for i in range(10):        
        for car in cars:
            randomCity = cities[random.randint(1, len(cities) - 1)]
            inspect = float(establishments[randomCity].inspec_duration)
            dist = float(distances[car.place][int(establishments[randomCity].id)])
            wait = waitingTime(car.time + float(distances[car.place][int(establishments[randomCity].id)]), establishments[randomCity].opening_hours)
            time = inspect + dist + wait
            car.place = establishments[randomCity].id
            establishments[randomCity].visited = True
            car.time += time
            car.route.append(establishments[randomCity].id)
            cities.remove(randomCity)
            if len(cities) == 1:
                break
        if len(cities) == 1:
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
        currentRouteTime = routeTime([0] + neighbour)
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
        car.time = routeTime(car.route[1:])
        neighbours = getNeighbours(car.route[1:])
        bestNeighbour, bestNeighbourRouteTime = getBestNeighbour(neighbours)
        temp = 0
        for i in range(700):
            temp += 1
            if temp > 20:
                break
            if car.time > bestNeighbourRouteTime:
                temp = 0
                car.route = [0] + bestNeighbour
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
        fitnessResults[i] = Fitness(population[i],routeTime([0] + population[i])).routeFitness()
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
        pop = initialPopulation(popSize, car.route[1:])
        for i in range(0, generations):
            pop = nextGeneration(pop, eliteSize, mutationRate)
        time = 1 / rankRoutes(pop)[0][1]
        bestRouteIndex = rankRoutes(pop)[0][0]
        car.route = [0] + pop[bestRouteIndex]
        car.time = time

#-----------   GENETIC ALGO   -----------#
        
#------------    GREEDY    ------------#
# Does the greedy algorithm for all car routes
def greedy(cars):
    for i in range(10):
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

#------------    SIMULATED ANNEALING    ------------#
def simulated_annealing(cars, is_random, initial_temperature=100, cooling_rate=0.001):
    # Set initial solution
    if is_random:
        randomSolution(cars)
    else:
        greedy(cars)

    # Worse time
    b = cars[0].time
    for car in cars:
        if car.time > b:
            b = car.time
    print("Initial time:", b / 3600)

    # Perform the annealing process
    current_solution = cars
    max_routes_time = max(map(lambda car: routeTime(car.route), current_solution))
    temperature = initial_temperature

    while temperature > 0.1:
        # Choose two random establishments and swap their assigned vehicles
        car1 = random.choice(cars)
        car2 = random.choice(cars)

        while car1 == car2:
            car2 = random.choice(cars)

        establishment1_id = random.choice(car1.route)
        establishment2_id = random.choice(car2.route)
        establishment1_index = car1.route.index(establishment1_id)
        establishment2_index = car2.route.index(establishment2_id)
        car1.route.remove(establishment1_id)
        car2.route.remove(establishment2_id)
        car1.route.insert(establishment1_index, establishment2_id)
        car2.route.insert(establishment2_index, establishment1_id)

        # Calculate the energy difference between the proposed solution and the current solution
        proposed_max_routes_time = max(map(lambda car: routeTime(car.route), current_solution))
        #print("proposed", proposed_max_routes_time / 3600)
        energy_diff = proposed_max_routes_time - max_routes_time

        # Determine whether to accept the proposed solution
        if energy_diff < 0:
            max_routes_time = proposed_max_routes_time
        else:
            acceptance_probability = math.exp(-energy_diff / temperature)
            if random.random() < acceptance_probability:
                max_routes_time = proposed_max_routes_time
            else:
                # Revert to the previous assignments
                car1.route.remove(establishment2_id)
                car2.route.remove(establishment1_id)
                car1.route.insert(establishment1_index, establishment1_id)
                car2.route.insert(establishment2_index, establishment2_id)

        # Decrease the temperature according to the cooling rate
        temperature *= 1 - cooling_rate

    for car in cars:
        car.time = routeTime(car.route)
#------------    SIMULATED ANNEALING    ------------#

#------------        TABU SEARCH        ------------#

#Get the list of routes (ids) sorted by their time and its route. The worst route will be on index 0
def getSortedRouts(best_solution):
    sol = list(enumerate(best_solution))
    sol = sorted(sol, key= lambda x : routeTime(x[1]))

    res = []
    sorted_solution = []
    res.append(sol[0][0])
    sorted_solution.append(sol[0][1])
    for i in range(1,len(best_solution)):
        res.append(sol[i][0])
        sorted_solution.append(sol[i][1])
    return list(reversed(res)), list(reversed(sorted_solution))

#Returns the best neighbour for the current solution.
def get_tabu_neighbors(solution, size, tabu_history):
    num_neighbors = 100

    best_neighbor = solution
    best_neighbor_cost = INF

    changeableSolution = deepcopy(solution)

    #this sets are to make sure we are not testing 
    insertedSet = set()
    swapSet = set()

    #get the sorted list of solutions so we can work on improving the worst route
    lista, changeableSolution = getSortedRouts(changeableSolution)

    #The neighbours are found by insertions and swaps on the routes
    for _ in range(num_neighbors):
        i = random.sample(lista[:1],1)[0]
        j = random.sample(lista[len(lista)-size//2:],1)[0]

        # Insert a customer into a different route
        if len(changeableSolution[i]) > 0 and len(changeableSolution[j]) > 1:           
            k = random.randrange(len(changeableSolution[i]))
            l = random.randrange(len(changeableSolution[j]))

            while((i,k,j,l) in insertedSet):
                k = random.randrange(len(changeableSolution[i]))
                l = random.randrange(len(changeableSolution[j]))
            insertedSet.add((i,k,j,l))
            customer = changeableSolution[i][k]
            changeableSolution[i] = [ele for ele in changeableSolution[i] if ele != customer]
            changeableSolution[j].insert(l, customer)
            neighbor_cost = evaluate_route_cost(changeableSolution)

            #check if solution is better than current one and is not on tabu history
            if tupleize(changeableSolution) not in tabu_history and neighbor_cost < best_neighbor_cost:
                best_neighbor_cost = neighbor_cost
                best_neighbor = deepcopy(changeableSolution)
            changeableSolution[j].remove(customer)
            changeableSolution[i].insert(k, customer)

        i = random.sample(lista[:1],1)[0]
        j = random.sample(lista[1:],1)[0]

        # Swap customers between two routes
        if len(changeableSolution[i]) > 0 and len(changeableSolution[j]) > 0:
            k = random.randrange(len(changeableSolution[i]))
            l = random.randrange(len(changeableSolution[j]))

            while((i,k,j,l) in swapSet):
                k = random.randrange(len(changeableSolution[i]))
                l = random.randrange(len(changeableSolution[j]))
            swapSet.add((i,k,j,l))
            changeableSolution[i][k], changeableSolution[j][l] = changeableSolution[j][l], changeableSolution[i][k]
            neighbor_cost = evaluate_route_cost(changeableSolution)

            #check if solution is better than current one and is not on tabu history
            if tupleize(changeableSolution) not in tabu_history and neighbor_cost < best_neighbor_cost:
                best_neighbor_cost = neighbor_cost
                best_neighbor = deepcopy(changeableSolution)
            changeableSolution[i][k], changeableSolution[j][l] = changeableSolution[j][l], changeableSolution[i][k]
    
    return best_neighbor

def tupleize(solution):
    # Convert each route to a tuple and return a tuple of tuples
    return tuple(tuple(route) for route in solution)

#get the list of routes
def getSolutionList(cars):
    solution = []
    for car in cars:
        solution.append(car.route)

    return solution

def evaluate_route_cost(routes):
    min_time = -1

    for route in routes:
        time = routeTime(route)

        if(time > min_time):
            min_time = time
    return min_time

#Performs the tabu search
def tabu_search(cars, is_random):
    tabu_history = {}
    num_iterations = 1000
    tabu_limit = 10
    
    if(is_random):
        randomSolution(cars)
    else:
        greedy(cars)

    b = 0
    for car in cars:
        if b < car.time:
            b = car.time
    print("Initial time: " + str(b/3600-9))

    current_solution = getSolutionList(cars)

    best_solution_cost = evaluate_route_cost(current_solution)
    best_solution = current_solution

    tabu_history[tupleize(current_solution)] = tabu_limit
    for _ in range(num_iterations):
        #decrease the tabu limit on the tabu history
        for x in tabu_history:
            tabu_history[x] -= 1
        tabu_history = {x: tabu_history[x] for x in tabu_history if tabu_history[x] > 0}
        best_neighbor = get_tabu_neighbors(current_solution, len(establishments), tabu_history)
        
        current_solution = best_neighbor

        tabu_history[tupleize(best_neighbor)] = tabu_limit

        route_cost = evaluate_route_cost(best_neighbor)
        if(route_cost < best_solution_cost):           
            best_solution_cost = route_cost
            best_solution = best_neighbor
            

    for i in range(len(cars)):
        cars[i].route = best_solution[i]
        cars[i].time = routeTime(best_solution[i])
        
#------------        TABU SEARCH        ------------#

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cars = [Car(x) for x in range(100)]
    num_establishments = len(establishments)
    num_cars = len(cars)

    while True:
        print("1) HILL CLIMB RANDOM")
        print("2) HILL CLIMB GREEDY")
        print("3) GENETIC RANDOM")
        print("4) GENETIC GREEDY")
        print("5) SIMULATED ANNEALING RANDOM")
        print("6) SIMULATED ANNEALING GREEDY")
        print("7) TABU SEARCH RANDOM")
        print("8) TABU SEARCH GREEDY")
        print("0) exit")
        choice = input()
        for establishment in establishments:
            if establishment.id != 0:
                establishment.visited = False
        if choice == '1':
            hillClimb(cars,1)
        elif choice == '2':
            hillClimb(cars,0)
        elif choice == '3':
            genetic(cars, 100, 20, 0.01, 500,1)
        elif choice == '4':
            genetic(cars, 100, 20, 0.01, 500,0)
        elif choice == '5':
            simulated_annealing(cars, 1)
        elif choice == '6':
            simulated_annealing(cars, 0)
        elif choice == '7':
            tabu_search(cars, 1)
        elif choice == '8':
            tabu_search(cars, 0)
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
    