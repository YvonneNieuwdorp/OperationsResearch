VERYBIGNUMBER = 424242424242
NUMLOCATIONS = 5

import matplotlib.pyplot as plt     
import logging                      
import time                         

logger = logging.getLogger(name='tsp-logger')
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(message)s',
                    handlers=[logging.FileHandler("tsp.log")])

def euclidean_distance(point1, point2):
    """
        Euclidean distance between two points
        
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
        Calculates the total distance of a tour along all locations

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

def two_opt_tour_best_improvement(locations, distance, init_tour):
    logger.debug(msg="Apply Discrete Improving Search with 2-exchange neighborhood and best improvement on TSP (2-opt)")        
    startTime = time.time()

    # STEP 0: start with initial tour
    num_locations = len(locations)
    curr_tour = init_tour
    total_distance_curr_tour = total_distance(locations,curr_tour)
    logger.info(msg=f"Initial tour has distance {total_distance_curr_tour:.2f}")    

    while True:
        # determine feasible improving move and gain 
        max_gain = -VERYBIGNUMBER
        fi_move_found = False # 
        for i in range(1,num_locations-1):           # from i=1 upto and including num_locations-2
            for j in range(i+2,num_locations + 1):     # from j=i+2 upto and including num_locations
                if (i==1 and j==num_locations):      # then j=0=i-1; not a feasible tour 
                    break

                loc_imin1 = locations[curr_tour[i-1]]
                loc_i = locations[curr_tour[i]]
                loc_jmin1 = locations[curr_tour[j-1]]
                if j == num_locations:
                    loc_j = locations[curr_tour[0]]
                else:
                    loc_j = locations[curr_tour[j]]

                gain = (distance[loc_imin1,loc_i]+distance[loc_jmin1,loc_j])-(distance[loc_imin1,loc_jmin1]+distance[loc_i,loc_j])
                logger.info(msg=f"Evaluate move ({i},{j})->Remove: ({i-1},{i}) and ({j-1},{j}); gain: {gain:.2f}")    

                # if necessary: update best feasible improving move
                if (gain>0 and gain>max_gain):
                    max_gain = gain
                    move = (i,j)
                    fi_move_found = True
        
        # STEP 1: if no move is both improving and feasible: stop; local optimum
        if not(fi_move_found):
            break

        # STEP 2: choose improving feasible move (=best feasible improving move)
        i,j = move

        # STEP 3: update the tour (apply the improving feasible move)
        neighbor_tour = curr_tour[:]
        neighbor_tour[i:j] = reversed(curr_tour[i:j])
        total_distance_neighbor_tour = total_distance(locations,neighbor_tour)
        logger.info(msg=f"Selected feasible improving move ({i},{j}) with gain {max_gain:.2f}, resulting tour has length {total_distance_neighbor_tour:.2f}")    

        curr_tour = neighbor_tour

    endTime = time.time()

    total_distance_two_opt_tour = total_distance(locations, curr_tour)
    logger.info(msg=f"2-opt tour has distance {total_distance_two_opt_tour:.2f}; time: {endTime-startTime:.6f}")    

    return curr_tour

def main():
    
    # Define an instance
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

    logger.info(msg=f"Specific instance with {num_locations} locations")    

    # Generate a poor tour     
    # ----------
    rnd_tour = [0,1,2,3,4]
    total_distance_rnd_tour = total_distance(coordinates,rnd_tour)
    logger.info(msg=f"Random tour has distance {total_distance_rnd_tour:.2f}") 

    # Apply 2-opt to random tour
    # ----------
    dis_tour = two_opt_tour_best_improvement(coordinates,distance,rnd_tour)
    total_distance_dis_tour = total_distance(coordinates,dis_tour)

    # Plot the random solution and the discrete improving search solution
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
        x1, y1 = coordinates[dis_tour[i - 1]]
        x2, y2 = coordinates[dis_tour[i]]
        plt.plot([x1, x2], [y1, y2], 'b-')  
    x1, y1 = coordinates[dis_tour[len(coordinates)-1]]
    x2, y2 = coordinates[dis_tour[0]]
    plt.plot([x1, x2], [y1, y2], 'b-')  
 
    for i in range(1, len(coordinates)):
        x1, y1 = coordinates[rnd_tour[i - 1]]
        x2, y2 = coordinates[rnd_tour[i]]
        plt.plot([x1, x2], [y1, y2], '--', color='grey', linewidth=0.8)  
    x1, y1 = coordinates[rnd_tour[len(coordinates)-1]]
    x2, y2 = coordinates[rnd_tour[0]]
    plt.plot([x1, x2], [y1, y2], '--', color='grey', linewidth=0.8)  
 
    plt.title(f'Solutions on {len(coordinates)} nodes; RND tour: {total_distance_rnd_tour:.2f}, 2OPT tour: {total_distance_dis_tour:.2f}')
    plt.show()

if __name__ == "__main__":
    main()
