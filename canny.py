import cv2
import os
from tqdm import tqdm
from PIL import ImageOps

# Path to extracted frames


def edge_detection(T_lower=100, T_upper=200, input_folder="frames", output_folder="edges", border=True):
    os.makedirs(output_folder, exist_ok=True)
    # Process each frame
    for filename in tqdm(sorted(os.listdir(input_folder))):
        if filename.endswith(".png"):
            # Read the frame
            img_path = os.path.join(input_folder, filename)
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            # Apply edge detection (Canny)
            edges = cv2.Canny(image, T_lower, T_upper)
            top, bottom, left, right = 1, 1, 1, 1  # 1-pixel border on all sides
            border_color = [255, 255, 255]  # Black border in BGR format

            # Add the border
            if border:
                bordered_image = cv2.copyMakeBorder(
                    edges, top, bottom, left, right, cv2.BORDER_CONSTANT, value=border_color
                )

            # Save the edge-detected frame
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, bordered_image)


if __name__ == "__main__":
    input_folder = "frames"
    output_folder = "edges"

    edge_detection(T_lower=50, T_upper=150)
