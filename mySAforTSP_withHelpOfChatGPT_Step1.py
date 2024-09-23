import random
import math

import matplotlib.pyplot as plt # (from my Discrete Improving Search code)
  

# Parameters for simulated annealing
initial_temperature = 1000
cooling_rate = 0.995
iterations_per_temperature = 1000

def euclidean_distance(point1, point2):
    """
        Euclidean distance between two points (from my Discrete Improving Search code)
        
        Arguments:
            point1, point2: (x,y)-coordinates of two points
            
        Returns:
            shortest distance from point1 to point2 'as the crow flies' 
    """
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def total_distance(locations, tour):
    """
        Calculates the total distance of a tour along all locations (from my Discrete Improving Search code)
        Replaces ChatGPT's tour_distance function

        Arguments:
            set of locations ({0,1,...,num_locations-1})
            tour (list): a permutation of the set of locations

        Returns:
            sum of all distances between two consecutive locations in tour 
    """
    totalDistance = 0
    for i in range(len(tour)):
        fromLocation = locations[tour[i]]
        toLocation = locations[tour[(i + 1) % len(tour)]]
        totalDistance += euclidean_distance(fromLocation, toLocation)

    return totalDistance

# Simulated annealing function
def simulated_annealing(locations, tour, temperature, cooling_rate, iterations_per_temp):
    current_tour = tour
    best_tour = tour
    current_distance = total_distance(locations, current_tour)
    best_distance = current_distance

    while temperature > 1e-3:
        for _ in range(iterations_per_temp):
            # Generate a neighboring solution by swapping two random cities
            i, j = random.sample(range(len(tour)), 2)
            neighbor_tour = current_tour[:]
            neighbor_tour[i], neighbor_tour[j] = neighbor_tour[j], neighbor_tour[i]
            neighbor_distance = total_distance(locations, neighbor_tour)

            # Decide whether to accept the neighbor solution
            delta = neighbor_distance - current_distance
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_tour = neighbor_tour
                current_distance = neighbor_distance

                # Update the best solution if necessary
                if current_distance < best_distance:
                    best_tour = current_tour
                    best_distance = current_distance

                print(f"Temperature {temperature:8.4f}, current distance {current_distance:6.2f}, best distance {best_distance:6.2f}", end='\r')

        # Cool the temperature
        temperature *= cooling_rate

    return best_tour, best_distance

def main():
    # Define an instance
    # (from my Discrete Improving Search code)
    # ----------
    num_locations = 5
    coordinates = [(2.5,5),(0,3),(5,3),(1,0),(4,0)]
    locations = coordinates
    distance = {}
    for i in range(num_locations):
        for j in range(num_locations):
                point1 = coordinates[i]
                point2 = coordinates[j]
                key = (point1,point2)
                distance[key] = euclidean_distance(point1,point2)

    # Generate a poor tour     
    # (from my Discrete Improving Search code)
    # ----------
    rnd_tour = [0,1,2,3,4]
    total_distance_rnd_tour = total_distance(coordinates,rnd_tour)

    # Call the simulated annealing function
    best_tour, best_distance = simulated_annealing(locations, rnd_tour, initial_temperature, cooling_rate, iterations_per_temperature)

    # Print the results
    print("\n")
    print("Best Tour:", best_tour)
    print("Best Distance:", best_distance)


    # Plot the random solution and the discrete improving search solution 
    # (from my Discrete Improving Search code)
    # ---

    # Separate the x and y values into separate lists
    x = [coord[0] for coord in coordinates]
    y = [coord[1] for coord in coordinates]

    # In Figure 1, we show both the random solution and the NN solution
    plt.figure(1)
    plt.scatter(x, y)
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')

    for i in range(1, len(coordinates)):
        x1, y1 = coordinates[best_tour[i - 1]]
        x2, y2 = coordinates[best_tour[i]]
        plt.plot([x1, x2], [y1, y2], 'b-')  
    x1, y1 = coordinates[best_tour[len(coordinates)-1]]
    x2, y2 = coordinates[best_tour[0]]
    plt.plot([x1, x2], [y1, y2], 'b-')  

    for i in range(1, len(coordinates)):
        x1, y1 = coordinates[rnd_tour[i - 1]]
        x2, y2 = coordinates[rnd_tour[i]]
        plt.plot([x1, x2], [y1, y2], '--', color='grey', linewidth=0.8)  
    x1, y1 = coordinates[rnd_tour[len(coordinates)-1]]
    x2, y2 = coordinates[rnd_tour[0]]
    plt.plot([x1, x2], [y1, y2], '--', color='grey', linewidth=0.8)  

    plt.title(f'Solutions on {len(coordinates)} nodes; RND tour: {total_distance_rnd_tour:.2f}, SA tour: {best_distance:.2f}')
    plt.show()

if __name__ == "__main__":
    main()