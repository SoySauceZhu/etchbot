import cv2
import numpy as np
from scipy.ndimage import label, binary_dilation


class Processor:
    def __init__(self):
        pass

    def resize(image, width=None, height=None, interpolation=cv2.INTER_AREA):
        """
        Resize an image while maintaining its aspect ratio.

        Parameters:
            image (numpy.ndarray): The input image.
            width (int, optional): The desired width. If None, height must be specified.
            height (int, optional): The desired height. If None, width must be specified.
            interpolation (int, optional): Interpolation method. Default is cv2.INTER_AREA.

        Returns:
            numpy.ndarray: The resized image.
        """
        # Get original dimensions
        original_height, original_width = image.shape[:2]

        if width is not None and height is None:
            # Scale based on width
            scale_factor = width / original_width
            new_width = width
            new_height = int(original_height * scale_factor)
        elif height is not None and width is None:
            # Scale based on height
            scale_factor = height / original_height
            new_height = height
            new_width = int(original_width * scale_factor)
        else:
            raise ValueError(
                "Specify either width or height, not both or neither.")

        # Resize the image
        return cv2.resize(image, (new_width, new_height), interpolation=interpolation)

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

        start = [int(item) for item in points1[min_index[0]]]
        end = [int(item) for item in points2[min_index[1]]]

        return min_distance, start, end

    def draw_line(input_array, start, end, replace=1):
        """
        Draw a line between two points in a binary image array.

        Parameters:
        - binary_picture_array: 2D numpy array representing the binary image.
        - start: Tuple (x1, y1) representing the starting point.
        - end: Tuple (x2, y2) representing the ending point.

        Returns:
        - Updated binary_picture_array with the line drawn.
        """
        input_array = np.array(input_array)
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
            input_array[x1, y1] = replace

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

        return input_array

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

    def shortest_distance_dilation(labeled_array, start_cluster_id):
        start_mask = (labeled_array == start_cluster_id)

        other_cluster_mask = (labeled_array != 0) & ~start_mask

        array_shape = labeled_array.shape

        dilate_mask = start_mask.copy()
        visited = np.zeros(array_shape, dtype=bool)
        distance = 0

        start_p = None
        end_p = None

        while True:
            distance += 1

            # Default dilate structure
            dilate_mask = binary_dilation(dilate_mask)

            overlap = dilate_mask & other_cluster_mask
            if np.any(overlap):
                # start_points = np.argwhere(dilate_mask & start_mask)
                start_points = np.argwhere(start_mask)
                end_points = np.argwhere(overlap)

                _, start_p, end_p = Processor.find_min_distance(
                    start_points, end_points)

                return start_p, end_p

            visited |= dilate_mask

            if np.all(visited):
                break

        return None, None

    def link_clusters(labeled_array):
        linked = np.array([[1 if item != 0 else 0 for item in row]
                           for row in labeled_array])

        cluster_ids = np.sort(np.unique(labeled_array))

        if len(cluster_ids) <= 2:   # Only 0, 1 the labeled array
            return linked

        while len(cluster_ids) > 2:
            start_cluster_id = cluster_ids[1]
            start, end = Processor.shortest_distance_dilation(
                labeled_array, start_cluster_id)

            linked = Processor.draw_line(linked, start, end)

            labeled_array = Processor.label_cluster(linked)
            cluster_ids = np.sort(np.unique(labeled_array))

        return linked

    def output_image(cluster):
        """
        Takes in a 2D array, convert to binary image (0,0,0) or (255,255,255)
        """
        out = np.zeros((*cluster.shape, 3), dtype=np.uint8)
        out[cluster > 0] = [255, 255, 255]
        return out

    def process(image):
        image = Processor.label_cluster(image)
        image = Processor.ignore_cluster(image)
        image = Processor.link_clusters(image)
        image = Processor.output_image(image)
        return image
