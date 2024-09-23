def euclidean_distance(point1,point2):
    x1,y1 = point1
    x2,y2 = point2
    return ((x1-x2) ** 2 + (y1-y2) **2) ** 0.5

import matplotlib.pyplot as plt     # for visualization of the tours

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
    tour = [0,1,2,3]
    tour_distance = 0
    for loc in range(len(tour)):
        from_pnt = coordinates[tour[loc]]
        if (loc<len(tour)-1):
            to_pnt = coordinates[tour[loc+1]]
        else:
            to_pnt= coordinates[tour[0]]
        tour_distance += euclidean_distance(from_pnt,to_pnt)
    print(f"Tour has length {tour_distance:.2f}")     

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