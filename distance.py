import numpy as np

def find_min_distance(points1, points2):
    points1 = np.array(points1)
    points2 = np.array(points2)

    # Calculate the distance matrix
    distances = np.linalg.norm(points1[:, np.newaxis] - points2, axis=2)

    # Find the minimum distance and corresponding points
    min_index = np.unravel_index(np.argmin(distances), distances.shape)
    min_distance = distances[min_index]

    return min_distance, points1[min_index[0]], points2[min_index[1]]

import numpy as np

def draw_line(binary_picture_array, start, end):
    """
    Draw a line between two points in a binary image array.
    
    Parameters:
    - binary_picture_array: 2D numpy array representing the binary image.
    - start: Tuple (x1, y1) representing the starting point.
    - end: Tuple (x2, y2) representing the ending point.
    
    Returns:
    - Updated binary_picture_array with the line drawn.
    """
    x1, y1 = start
    x2, y2 = end

    # Calculate differences
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        # Set the pixel in the binary image
        binary_picture_array[x1, y1] = 1  # Assuming 1 is the line and 0 is the background
        
        # Check if we reached the end point
        if x1 == x2 and y1 == y2:
            break

        # Calculate the error
        err2 = err * 2
        if err2 > -dy:
            err -= dy
            x1 += sx
        if err2 < dx:
            err += dx
            y1 += sy

    return binary_picture_array



if __name__ == "__main__":
    # Example usage
    points1 = [(1, 2), (3, 4), (5, 6)]
    points2 = [(7, 8), (9, 10)]
    binary_picture_array = np.zeros((20, 20), dtype=int)

    for (x,y) in points1:
        binary_picture_array[x][y] = 1
    for (x,y) in points2:
        binary_picture_array[x][y] = 1

    print(binary_picture_array)

    min_distance, point1, point2 = find_min_distance(points1, points2)

    array = np.zeros((20,20))

    print(f'Min distance: {min_distance}, Points: {point1}, {point2}')

    # Example usage

    updated_array = draw_line(binary_picture_array, point1, point2)
    print(updated_array)