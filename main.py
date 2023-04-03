from copy import deepcopy
import math
import random
import sys
from file_reader import FileReader
from car import Car
INF = 2**63-1

def waitingTime(car_time, opening_hours):
    a = math.ceil(car_time/3600)
    
    while a > 23:
        a -= 24

    start_index = 24 - len(opening_hours[a:])
    next_day = len(opening_hours[a:])
    for i in range(start_index, 23):
        if opening_hours[i] == 1:
            return (i - start_index)*3600
    for i in range(0, start_index-1):
        if opening_hours[i] == 1:
            return (i + next_day)*3600
    return INF

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
    return

def routeTime(solution,est,distances):
    routeTime = 0
    #solution.insert(0,0)
    for k in range(len(solution)-1):
        a = solution[k]
        i = solution[k+1]
        if(a == i):
            continue
        inspect = float(est[i].inspec_duration)

        dist = float(distances[a][int(est[i].id)])

        wait = waitingTime(routeTime + dist + 9*3600, est[i].opening_hours)

        routeTime += inspect + dist + wait
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
        print(car.time/3600)
        while bestNeighbourRouteTime < car.time:
            car.route = bestNeighbour
            car.time = bestNeighbourRouteTime
            neighbours = getNeighbours(car.route)
            bestNeighbour, bestNeighbourRouteTime = getBestNeighbour(neighbours,est,dis)
            print(car.time/3600)
        print("-------------------------")
    b = 0
    for car in cars:
        if car.time > b:
            b = car.time
    print(b/3600)
    return


def getSortedRouts(best_solution,est,dis):
    sol = list(enumerate(best_solution))
    sol = sorted(sol, key= lambda x : routeTime(x[1],est,dis))

    res = []
    res.append(sol[0][0])
    for i in range(1,len(best_solution)):
        res.append(sol[i][0])
    return list(reversed(res))


import random

def get_neighbors(solution, size, est, dis, tabu_history):
    # Generate a set of new solutions by swapping customers or inserting customers
    num_neighbors = 100

    best_neighbor = solution
    best_neighbor_cost = INF

    changeableSolution = deepcopy(solution)

    insertedSet = set()
    swapSet = set()

    lista = getSortedRouts(changeableSolution,est,dis)
    for _ in range(num_neighbors):
        i = random.sample(lista[:1],1)[0]
        j = random.sample(lista[len(lista)-size//2:],1)[0]

        # Insert a customer into a different route
        if len(solution[i]) > 0 and len(solution[j]) > 1:           
            k = random.randrange(len(solution[i]))
            l = random.randrange(len(solution[j]))

            while((i,k,j,l) in insertedSet):
                k = random.randrange(len(solution[i]))
                l = random.randrange(len(solution[j]))
            insertedSet.add((i,k,j,l))
            customer = solution[i][k]
            solution[i] = [ele for ele in solution[i] if ele != customer]
            solution[j].insert(l, customer)
            neighbor_cost = evaluate_route_cost(solution, est, dis)
            if tupleize(solution) not in tabu_history and neighbor_cost < best_neighbor_cost:
                best_neighbor_cost = neighbor_cost
                best_neighbor = deepcopy(solution)
            solution[j].remove(customer)
            solution[i].insert(k, customer)

        i = random.sample(lista[:1],1)[0]
        j = random.sample(lista[1:],1)[0]

        # Swap customers between two routes
        if len(solution[i]) > 0 and len(solution[j]) > 0:
            k = random.randrange(len(solution[i]))
            l = random.randrange(len(solution[j]))

            while((i,k,j,l) in swapSet):
                k = random.randrange(len(solution[i]))
                l = random.randrange(len(solution[j]))
            swapSet.add((i,k,j,l))
            solution[i][k], solution[j][l] = solution[j][l], solution[i][k]
            neighbor_cost = evaluate_route_cost(solution, est, dis)
            if tupleize(solution) not in tabu_history and neighbor_cost < best_neighbor_cost:
                best_neighbor_cost = neighbor_cost
                best_neighbor = deepcopy(solution)
            solution[i][k], solution[j][l] = solution[j][l], solution[i][k]
    
    return best_neighbor






def tupleize(solution):
    # Convert each route to a tuple and return a tuple of tuples
    return tuple(tuple(route) for route in solution)

def getSolutionList(cars):
    solution = []
    for car in cars:
        solution.append(car.route)

    return solution

def evaluate_route_cost(routes, est, dis):
    min_time = -1

    for route in routes:
        time = routeTime(route, est, dis)

        if(time > min_time):
            min_time = time
    return min_time

def tabu_search(cars, est, dis):
    tabu_history = {}
    num_iterations = 1000
    tabu_limit = 10
    
    greedy(cars ,est, dis)
    current_solution = getSolutionList(cars)

    print(current_solution)
    best_solution = current_solution
    best_solution_cost = evaluate_route_cost(current_solution, est, dis)

    worst = 0 ##
    best = INF
    for x in best_solution:
        a = routeTime(x,establishments,distances)
        if(a > worst):
            worst = a
        if(a < best):
            best = a
    print(worst/3600 ,best/3600 ) ##

    tabu_history[tupleize(current_solution)] = tabu_limit
    for _ in range(num_iterations):
        for x in tabu_history:
            tabu_history[x] -= 1
        tabu_history = {x: tabu_history[x] for x in tabu_history if tabu_history[x] > 0}

        best_neighbor = get_neighbors(current_solution, len(est) ,est, dis,tabu_history)
        current_solution = best_neighbor

        tabu_history[tupleize(current_solution)] = tabu_limit

        if( evaluate_route_cost(current_solution,est,dis) < best_solution_cost):
            print(f'upgraded {best_solution_cost - evaluate_route_cost(current_solution,est,dis)} in time')
            best_solution_cost = evaluate_route_cost(current_solution,est,dis)
            best_solution = current_solution

    return best_solution, best_solution_cost

def greedy(cars,establishments,distances):
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
            car.place = next_hop.id

            next_hop.visited = True
            car.time = min_time + car.time
            car.route.append(next_hop.id)
        
if __name__ == '__main__':
    establishments = FileReader.get_establishments()[:1000]
    distances = FileReader.get_distances()

    
    cars = [Car(x) for x in range(100)]
    #greedy(cars,establishments,distances)
    best_solution,time = tabu_search(cars,establishments, distances)

    worst = 0
    best = INF
    for x in best_solution:
        a = routeTime(x,establishments,distances)
        if(a > worst):
            worst = a
        if(a < best):
            best = a
    print(worst/3600,best/3600)
    
