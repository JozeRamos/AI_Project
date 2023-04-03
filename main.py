# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import sys
from file_reader import FileReader
from car import Car

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    establishments = FileReader.get_establishments()
    distances = FileReader.get_distances()

    cars = [Car(x) for x in range(100)]

    # best local = inspec duration + travel time + getWaitingTime()
    # for i in range(len(distances)):

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
            print(
                f'car with id {car.id} in place {car.place} going to {next_hop.id} with {min_time} second, or {round(min_time / 3600, 2)}h with fulltime {car.time / 3600}')
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


import random
import math


# Define the distance function
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Define the cost function for a given solution
def cost(solution, distances):
    total_cost = 0
    for route in solution:
        prev_x, prev_y = 0, 0  # start at the depot
        for i in range(len(route)):
            curr_x, curr_y = distances[route[i]]
            total_cost += distance(prev_x, prev_y, curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y
        total_cost += distance(prev_x, prev_y, 0, 0)  # return to the depot
    return total_cost


# Define the simulated annealing algorithm
def simulated_annealing(distances, max_iterations=1000, initial_temperature=100, cooling_rate=0.01):
    n = len(distances)
    best_solution = None
    best_cost = float('inf')
    curr_solution = [list(range(1, n))]  # start with all nodes in a single route
    curr_cost = cost(curr_solution, distances)
    temperature = initial_temperature

    for i in range(max_iterations):
        new_solution = curr_solution.copy()

        # Generate a new neighbor solution
        r1, r2 = random.sample(range(len(new_solution)), 2)  # pick two random routes
        i, j = random.sample(range(len(new_solution[r1])), 2)  # pick two random nodes
        new_solution[r1].insert(j, new_solution[r1].pop(i))
        new_solution[r2].insert(0, new_solution[r1].pop())  # move the node from r1 to r2

        # Calculate the cost difference
        new_cost = cost(new_solution, distances)
        cost_diff = new_cost - curr_cost

        # Decide whether to accept the new solution
        if cost_diff < 0 or random.uniform(0, 1) < math.exp(-cost_diff / temperature):
            curr_solution = new_solution
            curr_cost = new_cost

            # Update the best solution if necessary
            if curr_cost < best_cost:
                best_solution = curr_solution.copy()
                best_cost = curr_cost

        # Decrease the temperature
        temperature *= 1 - cooling_rate

    return best_solution, best_cost


# Example usage
distances = [(0, 0)] + [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(10)]
solution, cost = simulated_annealing(distances)
print("Best solution:", solution)
print("Best cost:", cost)
