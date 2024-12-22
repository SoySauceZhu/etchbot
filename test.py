import cv2
import numpy as np
import matplotlib.pyplot as plt

from new_processor import Processor

def show_images_in_row(image1, image2):
    # Convert images from BGR (OpenCV format) to RGB (Matplotlib format)
    image1_rgb = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    image2_rgb = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

    # Create a figure with 1 row and 2 columns
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Display the images in the subplots
    axes[0].imshow(image1_rgb)
    axes[0].axis('off')  # Hide the axes for a cleaner view
    axes[0].set_title("Image 1")

    axes[1].imshow(image2_rgb)
    axes[1].axis('off')  # Hide the axes for a cleaner view
    axes[1].set_title("Image 2")

    # Show the plot
    plt.show()

def di(path):

    # Load a binary image
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded
    if image is None:
        print("Error: Image not found.")
        exit()

    # Create a kernel (structuring element)
    kernel = np.ones((5, 5), np.uint8)

    # Apply dilation
    for _ in range(100):
        for _ in range(10):
            dilated_image = cv2.dilate(image, kernel, iterations=1)

        # Display the original and dilated images
        cv2.imshow('Original Image', image)
        cv2.imshow('Dilated Image', dilated_image)

        # Wait for a key press and close the windows
        cv2.waitKey(0)


def test_linked_array():
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

    out = Processor.link_clusters(array_zeros)
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
    test_linked_array()