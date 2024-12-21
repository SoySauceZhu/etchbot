import cv2
import numpy as np
from scipy.ndimage import label, binary_dilation
import os
from tqdm import tqdm
from scipy.ndimage import label


class Processor:
    def __init__(self):
        pass

    def output_image(cluster):
        """
        Takes in a 2D array, convert to binary image (0,0,0) or (255,255,255)
        """
        out = np.zeros((*cluster.shape, 3), dtype=np.uint8)
        out[cluster > 0] = [255, 255, 255]
        return out

    def find_min_distance(points1, points2):
        """
        takes in two array of indices (positions)
        """
        points1 = np.array(points1)
        points2 = np.array(points2)

        # Calculate the distance matrix
        distances = np.linalg.norm(points1[:, np.newaxis] - points2, axis=2)

        # Find the minimum distance and corresponding points
        min_index = np.unravel_index(np.argmin(distances), distances.shape)
        min_distance = distances[min_index]

        return min_distance, points1[min_index[0]], points2[min_index[1]]

    def draw_line(input_array, start, end, replace=-1):
        """
        Draw a line between two points in a binary image array.

        Parameters:
        - binary_picture_array: 2D numpy array representing the binary image.
        - start: Tuple (x1, y1) representing the starting point.
        - end: Tuple (x2, y2) representing the ending point.

        Returns:
        - Updated binary_picture_array with the line drawn.
        """
        binary_picture_array = input_array.copy()
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
            # Assuming 1 is the line and 0 is the background
            binary_picture_array[x1, y1] = replace

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

    def process(image):
        image = Processor.label_cluster(image)
        image = Processor.ignore_cluster(image)
        image = Processor.link_clusters(image)
        image = Processor.output_image(image)
        return image

    def label_cluster(image):
        """
        Label the connected clusters in a given image (ndarray)
        input: ndarray
        output: ndarray
        """
        # Convert to binary image (array)
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Convert array either 1 or 0
        binary_image = (image != 0).astype(int)

        # 4-connectivity structure
        structure = np.array([[1, 1, 1],
                              [1, 1, 1],
                              [1, 1, 1]])

        labeled_array, _ = label(binary_image, structure=structure)

        return labeled_array

    def ignore_cluster(labeled_array, size=50):
        """
        Ignore clusters less than 50 pixels
        """
        arr = labeled_array.copy()
        num_features = arr.max()

        # arr == i evaluated to 1
        cluster_sizes = np.array([np.sum(arr == i)
                                 for i in range(1, num_features + 1)])

        # np.where return the indices of items that satisfies (cluster_size < size)
        small_clusters = np.where(cluster_sizes < size)[0] + 1

        # replace small indices with zeros
        for cluster_id in small_clusters:
            arr[arr == cluster_id] = 0

        return arr

    def shortest_distance_dilation(labeled_array, cluster_id, exemption=[]):
        """
        Find the shortest distance between a target cluster and the rest of the clusters using dilation.

        Parameters:
            labeled_array (ndarray): 2D array with labeled clusters (output of ndimage.label).
            cluster_id (int): The ID of the target cluster.

        Returns:
            min_distance (int): The shortest distance between the target cluster and the others.
            start_point (tuple): The starting point on the target cluster boundary.
            end_point (tuple): The closest point on the nearest cluster boundary.
            end_cluster_id (int)
        """
        # Create a binary mask for the target cluster
        target_mask = (labeled_array == cluster_id)

        exemption_array = labeled_array.copy()

        for i in exemption:
            exemption_array[exemption_array == i] = 0

        # Create a binary mask for all other clusters
        other_clusters_mask = (exemption_array != 0) & ~target_mask

        # Extract the shape of the array
        array_shape = labeled_array.shape

        # Initialize variables
        dilated_mask = target_mask.copy()
        visited = np.zeros(array_shape, dtype=bool)
        distance = 0

        # Track the points for the shortest distance
        start_point = None
        end_point = None

        # Perform iterative dilation
        while True:
            distance += 1

            # Dilate the current mask
            dilated_mask = binary_dilation(dilated_mask)

            # Check for overlap with other clusters
            overlap = dilated_mask & other_clusters_mask
            if np.any(overlap):
                # Find the boundary points for the target cluster and overlapping clusters
                # TODO: OR or OXR?
                target_boundary = np.argwhere(dilated_mask & target_mask)
                overlap_points = np.argwhere(overlap)

                # Compute the Euclidean distances and find the minimum
                # min_distance = np.inf
                # for t_point in target_boundary:
                #     for o_point in overlap_points:
                #         dist = np.linalg.norm(t_point - o_point)
                #         if dist < min_distance:
                #             min_distance = dist
                #             start_point = tuple(t_point)
                #             end_point = tuple(o_point)

                min_distance, start_point, end_point = Processor.find_min_distance(
                    target_boundary, overlap_points)

                return int(min_distance), start_point, end_point, labeled_array[*end_point]

            # Update the visited array
            visited |= dilated_mask

            # Stop if the entire array has been visited
            if np.all(visited):
                break

        # If no other clusters are found, return None
        return None, None, None, None

    def link_clusters(labeled_array):
        cluster_ids = np.unique(labeled_array)
        cluster_ids = cluster_ids[cluster_ids > 0]
        cluster_ids = list(cluster_ids)

        linked_array = labeled_array.copy()

        visited = []

        id = cluster_ids[0]
        visited.append(id)
        while set(visited) != set(cluster_ids):

            # Find next cluster
            _, start, end, id = Processor.shortest_distance_dilation(
                labeled_array, id, visited)

            # Link the next cluster
            linked_array = Processor.draw_line(linked_array, start, end)
            visited.append(id)

        linked_array[linked_array != 0] = 1
        return linked_array


def main():
    input_folder = "edges"
    output_folder = "processed"
    for filename in tqdm(sorted(os.listdir(input_folder))):
        if filename.endswith(".png"):
            img_path = os.path.join(input_folder, filename)

            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            out = Processor.process(image)

            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, out)


if __name__ == "__main__":
    main()
    # img = cv2.imread("edges/frame_0665.png")
    # label = Processor.label_cluster(img)
    # ignore = Processor.ignore_cluster(label)
    # linked = Processor.link_clusters_with_shortest_path(ignore)
    # out1 = Processor.output_image(ignore)
    # out2 = Processor.output_image(linked)

    # test.show_images_in_row(out1, out2)
