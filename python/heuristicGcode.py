import cv2
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def Heuristic_gcode(image, gcode_path, resize_factor=1.0):
    logging.info("Starting Heuristic_gcode function")
    
    # Flip the image upside down
    image = np.flipud(image)
    logging.info("Image flipped upside down")

    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        logging.info("Converted image to grayscale")

    # Get coordinates of non-zero pixels
    # y_coords, x_coords = np.nonzero(image)
    y_coords, x_coords = np.nonzero(image > 127)
    points = np.column_stack((y_coords, x_coords))
    logging.info(f"Found {len(points)} non-zero pixels")

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
        logging.info(f"DFS completed with path length: {len(path)}")

    # Start DFS from the first nonzero pixel
    dfs(tuple(points[0]))

    # Write G-code
    with open(gcode_path, 'w') as gcode_file:
        gcode_file.write("G21 ; Set units to mm\n")
        gcode_file.write("G90 ; Absolute positioning\n")
        # Move to start position
        gcode_file.write(f"G0 X{path[0][1] * resize_factor:.2f} Y{path[0][0] * resize_factor:.2f}\n")
        for p in path:
            gcode_file.write(f"G1 X{p[1] * resize_factor:.2f} Y{p[0] * resize_factor:.2f} F1800\n")
    logging.info(f"G-code written to {gcode_path}")

    # Plot the image
    # plt.imshow(image, cmap='gray')

    # # Draw the path
    # path = np.array(path)
    # plt.plot(path[:, 1], path[:, 0], 'r-', linewidth=0.8)

    # plt.show()


# Example usage
if __name__ == "__main__":
    image = cv2.imread('resources/EiffelTower.jpg', cv2.IMREAD_GRAYSCALE)
    image = cv2.bitwise_not(image)
    Heuristic_gcode(image, 'output/heuristic_EiffelTower.gcode')
