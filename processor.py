import test
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label, generate_binary_structure, binary_dilation
from scipy.spatial.distance import cdist
import os
from tqdm import tqdm
import pandas as pd
from scipy.ndimage import label, center_of_mass
from scipy.spatial import distance
from skimage.graph import route_through_array
import distance


class Processor:
    def __init__(self):
        pass

    def process(image):
        image = Processor.label_cluster(image)
        image = Processor.ignore_cluster(image)
        image = Processor.link_clusters_with_shortest_path(image)
        image = Processor.output_image(image)
        return image

    def label_cluster(image):
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        binary_image = (image == 255).astype(int)

        structure = np.array([[1, 1, 1],  # 4-connectivity structure
                              [1, 1, 1],
                              [1, 1, 1]])

        labeled_array = label(binary_image, structure=structure)

        return labeled_array[0]

    def ignore_cluster(labeled_array, size=50):
        arr = labeled_array.copy()
        num_features = arr.max()
        cluster_sizes = np.array([np.sum(arr == i)
                                 for i in range(1, num_features + 1)])

        small_clusters = np.where(cluster_sizes < size)[0] + 1

        for cluster_id in small_clusters:
            arr[arr == cluster_id] = 0

        return arr

    def output_image(cluster):
        out = np.zeros((*cluster.shape, 3), dtype=np.uint8)
        out[cluster > 0] = [255, 255, 255]
        return out

    # def link_clusters_with_shortest_path(labeled_array):
    #     """
    #     Links clusters in a labeled array with the shortest path.

    #     Parameters:
    #         labeled_array (numpy.ndarray): 2D array where clusters are labeled with integers.

    #     Returns:
    #         numpy.ndarray: Array where clusters are linked with paths.
    #     """
    #     # Ensure the labeled_array is valid
    #     if not isinstance(labeled_array, np.ndarray):
    #         raise ValueError("Input must be a numpy array.")

    #     # Find the centroids of each labeled cluster
    #     cluster_ids = np.unique(labeled_array)
    #     cluster_ids = cluster_ids[cluster_ids > 0]  # Exclude background (label 0)
    #     centroids = np.array(center_of_mass(labeled_array, labeled_array, cluster_ids))

    #     # Create a new array to hold the result
    #     result_array = np.copy(labeled_array)

    #     # Iterate over pairs of centroids to link them
    #     for i in range(len(centroids)):
    #         for j in range(i + 1, len(centroids)):
    #             # Use the Manhattan distance as the cost
    #             cost_array = np.ones_like(labeled_array, dtype=float)
    #             # cost_array[labeled_array > 0] = np.inf  # Prevent paths through clusters

    #             start = tuple(map(int, centroids[i]))
    #             end = tuple(map(int, centroids[j]))

    #             # Find the shortest path using skimage.graph.route_through_array
    #             path, _ = route_through_array(cost_array, start, end, fully_connected=True)

    #             # Overlay the path onto the result array
    #             for coord in path:
    #                 result_array[coord] = -1  # Mark the path with -1 (or any unused label)

    #     result_array[result_array != 0] = 1
    #     return result_array

    def link_clusters_with_shortest_path(labeled_array):
        """
        Links clusters in a labeled array with the shortest path.

        Parameters:
            labeled_array (numpy.ndarray): 2D array where clusters are labeled with integers.

        Returns:
            numpy.ndarray: Array where clusters are linked with paths.
        """
        # Ensure the labeled_array is valid
        if not isinstance(labeled_array, np.ndarray):
            raise ValueError("Input must be a numpy array.")

        # Identify unique clusters (excluding background)
        cluster_ids = np.unique(labeled_array)
        # Exclude background (label 0)
        cluster_ids = cluster_ids[cluster_ids > 0]

        # Create a new array to hold the result
        result_array = np.copy(labeled_array)

        # Generate a cost array where traversing labeled clusters is expensive
        cost_array = np.ones_like(labeled_array, dtype=float)

        # Link all clusters
        for i in range(0, len(cluster_ids), 2):
            j = i+1
            if j == len(cluster_ids):
                break

            cluster_a = cluster_ids[i]
            cluster_b = cluster_ids[j]

            # Find the border pixels of each cluster
            structure = generate_binary_structure(2, 2)
            border_a = binary_dilation(
                labeled_array == cluster_a, structure) & (labeled_array == 0)
            border_b = binary_dilation(
                labeled_array == cluster_b, structure) & (labeled_array == 0)

            # test.show_images_in_row(Processor.output_image(border_a), Processor.output_image(border_b))


            # Get coordinates of border pixels
            coords_a = np.argwhere(border_a)
            coords_b = np.argwhere(border_b)


            _, point_a, point_b = distance.find_min_distance(coords_a, coords_b)
            result_array = distance.draw_line(result_array, point_a, point_b)   # update result_array


        return result_array
            #     # Find the shortest path between the closest border pixels
            #     min_distance = np.inf
            #     best_path = None

            #     for start in coords_a:
            #         for end in coords_b:
            #             try:
            #                 path, cost = route_through_array(cost_array, tuple(
            #                     start), tuple(end), fully_connected=True)
            #                 if cost < min_distance:
            #                     min_distance = cost
            #                     best_path = path
            #             except ValueError:
            #                 continue

            #     # Overlay the best path onto the result array
            #     if best_path:
            #         for coord in best_path:
            #             # Mark the path with -1 (or any unused label)
            #             result_array[coord] = -1

            # result_array[result_array != 0] = 1            



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
