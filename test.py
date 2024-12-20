import cv2
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
