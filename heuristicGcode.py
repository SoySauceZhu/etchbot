import cv2
import numpy as np
import matplotlib.pyplot as plt

def Heuristic_gcode(image_path, gcode_path):
    # Load the binary image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Image not found or unable to read")
    
    # Flip the image upside down
    image = np.flipud(image)
    
    # Get coordinates of non-zero pixels
    # y_coords, x_coords = np.nonzero(image > 127)
    y_coords, x_coords = np.nonzero(image > 127)
    points = np.column_stack((y_coords, x_coords))
    
    # Create a graph representation of the non-zero pixels
    pixel_set = set(map(tuple, points))
    visited = set()
    path = []
    
    def dfs(point):
        stack = [point]
        while stack:
            p = stack.pop()
            path.append(p)
            if p in visited:
                continue
            visited.add(p)
            # Check all 8 possible directions (adjacent pixels)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                neighbor = (p[0] + dx, p[1] + dy)
                if neighbor in pixel_set and neighbor not in visited:
                    stack.append(neighbor)
    
    # Start DFS from the first nonzero pixel
    dfs(tuple(points[0]))
    
    # Write G-code
    with open(gcode_path, 'w') as gcode_file:
        gcode_file.write("G21 ; Set units to mm\n")
        gcode_file.write("G90 ; Absolute positioning\n")
        gcode_file.write(f"G0 X{path[0][1]} Y{path[0][0]}\n")  # Move to start position
        for p in path:
            gcode_file.write(f"G1 X{p[1]} Y{p[0]} F1000\n")
    
    # Plot the image
    plt.imshow(image, cmap='gray')
    
    # Draw the path
    path = np.array(path)
    plt.plot(path[:, 1], path[:, 0], 'r-', linewidth=0.8)
    
    plt.show()

# Example usage
Heuristic_gcode('svg/processed_konan.jpg', 'gcode/heuristic.gcode')
