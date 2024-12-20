import cv2
import os
from tqdm import tqdm

# Path to extracted frames
input_folder = "frames"
output_folder = "edges"
os.makedirs(output_folder, exist_ok=True)

# Process each frame
for filename in tqdm(sorted(os.listdir(input_folder))):
    if filename.endswith(".png"):
        # Read the frame
        img_path = os.path.join(input_folder, filename)
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        
        # Apply edge detection (Canny)
        edges = cv2.Canny(image, 100, 200)
        
        # Save the edge-detected frame
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, edges)
