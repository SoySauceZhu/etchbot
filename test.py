import cv2
import numpy as np
import matplotlib.pyplot as plt

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



if __name__ == "__main__":
    di("frames/output_0150.png")