def euclidean_distance(point1,point2):
    x1,y1 = point1
    x2,y2 = point2
    return ((x1-x2) ** 2 + (y1-y2) **2) ** 0.5

import matplotlib.pyplot as plt     # for visualization of the tours

VERYBIGNUMBER = 424242424242

def main():

    """Define the traveling salesman instance
        - n locations
        - d_(i,j) distance matrix
        - x_i,y_i x,y-coordinates of locations
    """
    num_locations = 4 # so: locations {0,1,2,3}
    coordinates = [(0,0),(1,0),(0,1),(1,1)]
    distance = {}
    for loc1 in range(num_locations):
        for loc2 in range(num_locations):
            pnt1 = coordinates[loc1]
            pnt2 = coordinates[loc2]
            dist = euclidean_distance(pnt1,pnt2)
            key = (pnt1,pnt2)
            distance[key] = dist


    """Make the feasible tour,
       Calculate the tour length
    """
    """ tour = [0,1,2,3]
    tour_distance = 0
    for loc in range(len(tour)):
        from_pnt = coordinates[tour[loc]]
        if (loc<len(tour)-1):
            to_pnt = coordinates[tour[loc+1]]
        else:
            to_pnt= coordinates[tour[0]]
        tour_distance += euclidean_distance(from_pnt,to_pnt)
    """ 

    # STEP 0: Initialization
    # initialize the tour
    tour = []

    """Greedy constructive search on TSP: Nearest neighbor
        Start with a 'tour' containing only one location: the first one
        this is the last visited location
        Until all locations are visited:
            pick as the next location the one closest to the last visited location (not yet in tour)
            add this to the tour
            this will be the new last visited location
    """
    # start with a tour containing of the (randomly chosen) first location only
    tour = [0]

    # initialize the tour distance
    tour_distance = 0

    # initialize the visited status for all locations; only the first location is visited
    visited = [False]*num_locations
    visited[0] = True

    # initialize the last visited location; this is the first location (0)
    last_visited = 0

    # STEP 1: STOPPING
    # If all locations are visited, stop.
    while visited.count(False) > 0: # not all locations have been visited

        # STEP 2 (GREEDY): STEP
        # Add the location not-yet visited and with minimum distance to last visited location
        # initialize minimum distance
        min_distance = VERYBIGNUMBER

        # Enumerate all possibilities (all locations), and determine nearest
        for j in range(num_locations):
            # If location not visited and is closer by than current 'nearest': update 
            if not(visited[j]) and euclidean_distance(coordinates[last_visited],coordinates[j])<min_distance:
                min_distance = euclidean_distance(coordinates[last_visited],coordinates[j])
                nearest = j 

        # Extend the tour: add the nearest location to the very end of the tour        
        tour.append(nearest)
        print(f"Next added location {nearest}")

        # Update all relevant information: tour distance, visited status, and last visited location
        tour_distance += min_distance 
        visited[nearest] = True 
        last_visited = nearest

        # STEP 3: INCREMENT

    # Finalize the tour distance computation: add the distance from the last location to the start
    tour_distance += euclidean_distance(coordinates[last_visited],coordinates[0]) 

    """Visualize the tour,
       and the tour length
    """
    x = [coord[0] for coord in coordinates]
    y = [coord[0] for coord in coordinates]
    plt.figure(1)
    plt.scatter(x, y)
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    for loc in range(len(tour)-1):
        x1, y1 = coordinates[tour[loc]]
        x2, y2 = coordinates[tour[loc+1]]
        plt.plot([x1, x2], [y1, y2], 'b-')  
    x1, y1 = coordinates[tour[len(tour)-1]]
    x2, y2 = coordinates[tour[0]]
    plt.plot([x1, x2], [y1, y2], 'b-')  
    plt.title(f'Solution on {len(tour)} locations; tour: {tour_distance:.2f}')
    plt.show()


if __name__ == "__main__":
    main()