import cv2
import numpy as np
import matplotlib.pyplot as plt

from processor import Processor

def test_linked_array():
    array_zeros = np.zeros((10, 10))
    cluster1 = np.array([(0, 0), (1, 1)])
    cluster2 = np.array([(9, 0), (9, 1), (8, 0), (8, 1), (7, 1)])
    cluster3 = np.array([(9, 9), (9, 8), (8, 9), (8, 8)])
    cluster4 = np.array([(0, 9), (0, 8), (1, 9), (1, 8)])
    for i in cluster1:
        array_zeros[*i] = 1
    for i in cluster2:
        array_zeros[*i] = 2
    for i in cluster3:
        array_zeros[*i] = 3
    for i in cluster4:
        array_zeros[*i] = 4


    labeled = Processor.label_cluster(array_zeros)
    out = Processor.link_clusters(labeled)
    print("---------")
    print(out)


def test_shortest_distance_dilation():
    array_zeros = np.zeros((10, 10))
    cluster1 = np.array([(0, 0), (0, 1), (1, 0), (1, 1)])
    cluster2 = np.array([(9, 0), (9, 1), (8, 0), (8, 1), (7, 1)])
    cluster3 = np.array([(9, 9), (9, 8), (8, 9), (8, 8)])
    cluster4 = np.array([(0, 9), (0, 8), (1, 9), (1, 8)])
    for i in cluster1:
        array_zeros[*i] = 1
    for i in cluster2:
        array_zeros[*i] = 2
    for i in cluster3:
        array_zeros[*i] = 3
    for i in cluster4:
        array_zeros[*i] = 4

    print(array_zeros)
    start, end = Processor.shortest_distance_dilation(array_zeros, 2)
    print("\n")
    print(f"{start},{end}")




if __name__ == "__main__":
    # di("frames/output_0150.png")
    # test_shortest_distance_dilation()
    # test_linked_array()

    grid_size = 10
    grid = np.array([[0 for _ in range(grid_size)] for _ in range(grid_size)])  # Create a 10x10 grid

    start_point = (2, 3)
    end_point = (5, 5)  # Horizontal line
    grid = Processor.line(grid, start_point, end_point, replace=1)

    print(grid)
