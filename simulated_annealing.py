import random
import math
from file_reader import FileReader
from car import Car
import numpy as np

INF = float('inf')


def waitingTime(car_time, opening_hours):
    a = math.ceil(car_time / 3600)
    while a > 23:
        a -= 24
    start_index = 23 - len(opening_hours[a:])
    next_day = len(opening_hours[a:])
    for i in range(start_index, 23):
        if opening_hours[i] == 1:
            return (i - start_index) * 3600
    for i in range(0, start_index - 1):
        if opening_hours[i] == 1:
            return (i + next_day) * 3600
    return INF

# set random establishments for all cars
"""def set_initial_solution(cars, establishments, distances):
    remaining_establishments = establishments.copy()

    for car in cars:
        car.route.append(depot)

        establishments_sample = random.sample(remaining_establishments, num_establishments // num_cars)
        car.route.extend(establishments_sample)
        remaining_establishments = [establishment for establishment in remaining_establishments if
                                    establishment not in establishments_sample]
    return cars"""

def set_initial_solution(cars, establishments, distances):
    for i in range(11):
        for car in cars:
            min_time = INF
            flag = False
            for estab in establishments:
                if estab.visited or (estab.id == car.place): continue
                time = float(estab.inspec_duration) + float(distances[car.place][int(estab.id)]) + waitingTime(
                    car.time + float(distances[car.place][int(estab.id)]), estab.opening_hours)
                if (time < min_time):
                    min_time = round(time, 2)
                    next_hop = estab
                    flag = True
            if not flag:
                continue

            car.place = next_hop.id

            next_hop.visited = True
            car.time = min_time + car.time
            car.route.append(next_hop)
    return cars

"""def calculate_route_cost(car, distances):
    total_time = 0

    for estab in car.route:
        next_hop_time = float(estab.inspec_duration) + \
                      float(distances[car.place][int(estab.id)]) + \
                      waitingTime(car.time + float(distances[car.place][int(estab.id)]), estab.opening_hours)
        car.place = estab.id
        car.time += next_hop_time
        total_time += next_hop_time

    return total_time  # in seconds"""

def calculate_route_cost(route, establishments, distances):
    routeTime = 0
    for k in range(len(route)-1):
        a = route[k]
        i = route[k+1]
        inspect = float(establishments[i.id].inspec_duration)
        dist = float(distances[a.id][int(establishments[i.id].id)])
        wait = waitingTime(routeTime + dist + 9 * 3600, establishments[i.id].opening_hours)
        routeTime += inspect + dist + wait
    return routeTime


# Define the simulated annealing algorithm
def simulated_annealing(cars, establishments, distances, initial_temperature=100, cooling_rate=0.001):
    # Perform the annealing process
    current_solution = cars
    max_routes_time = max(map(lambda car: calculate_route_cost(car.route, establishments, distances), current_solution))
    temperature = initial_temperature

    while temperature > 0.1:
        # Choose two random establishments and swap their assigned vehicles
        car1 = random.choice(cars)
        car2 = random.choice(cars)

        while car1 == car2:
            car2 = random.choice(cars)

        establishment1 = random.choice(car1.route)
        establishment2 = random.choice(car2.route)
        establishment1_index = car1.route.index(establishment1)
        establishment2_index = car2.route.index(establishment2)
        car1.route.remove(establishment1)
        car2.route.remove(establishment2)
        car1.route.insert(establishment1_index, establishment2)
        car2.route.insert(establishment2_index, establishment1)

        # Calculate the energy difference between the proposed solution and the current solution
        proposed_max_routes_time = max(map(lambda car: calculate_route_cost(car.route, establishments, distances), current_solution))
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
                car1.route.remove(establishment2)
                car2.route.remove(establishment1)
                car1.route.insert(establishment1_index, establishment1)
                car2.route.insert(establishment2_index, establishment2)

        # Decrease the temperature according to the cooling rate
        temperature *= 1 - cooling_rate
    return cars


def print_routes(cars, establishmnets, distances):
    for car in cars:
        print("Route:", end=" ")
        for estab in car.route:
            print(estab.id, end=" ")
        print("\t\tTime:", round(calculate_route_cost(car.route, establishments, distances) / 3600, 2))

    min_routes_time = min(map(lambda car: calculate_route_cost(car.route, establishments, distances), cars))
    max_routes_time = max(map(lambda car: calculate_route_cost(car.route, establishments, distances), cars))
    print()
    print("min routes time:", round(min_routes_time / 3600, 2))
    print("max routes time:", round(max_routes_time / 3600, 2))


if __name__ == '__main__':
    establishments = FileReader.get_establishments()
    # depot = establishments.pop(0)  # remove the depot
    num_establishments = len(establishments)

    cars = [Car(x) for x in range(num_establishments // 10)]  # instantiates cars with starting time = 9 hours
    num_cars = len(cars)

    distances = FileReader.get_distances()
    cars = set_initial_solution(cars, establishments, distances)

    best_cars = simulated_annealing(cars, establishments, distances)
    print_routes(best_cars, establishments, distances)

