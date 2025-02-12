import cv2
import numpy as np


class GCodeGenerator:
    def __init__(self, image_path, scale_x=1.0, scale_y=1.0, safe_z=5.0, draw_z=0.0):
        """
        Initializes the GCodeGenerator class.

        Parameters:
        - image_path: Path to the edge-detected image.
        - scale_x, scale_y: Scaling factors to match the CNC or plotter dimensions.
        - safe_z: Height when the tool is lifted (e.g., pen up).
        - draw_z: Height when the tool is drawing (e.g., pen down).
        """
        self.image_path = image_path
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.safe_z = safe_z
        self.draw_z = draw_z
        self.gcode = []

    def load_image(self):
        """Loads the edge-detected image and extracts the main contour."""
        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise FileNotFoundError(f"Image not found: {self.image_path}")

        # Find contours
        contours, _ = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            raise ValueError("No contours found in the image!")

        # Select the largest contour (assuming it’s the main stroke)
        self.contour = max(contours, key=cv2.contourArea)

    def generate_gcode(self):
        """Generates G-code commands from the extracted contour."""
        if not hasattr(self, 'contour'):
            raise ValueError(
                "No contour data available. Run load_image() first.")

        self.gcode = [
            "G21 ; Set units to mm",
            "G90 ; Absolute positioning",
            f"G0 Z{self.safe_z} ; Lift pen"
        ]

        # Move to start position
        start_x, start_y = self.contour[0][0][0] * \
            self.scale_x, self.contour[0][0][1] * self.scale_y
        self.gcode.append(f"G0 X{start_x:.2f} Y{start_y:.2f} ; Move to start")
        self.gcode.append(f"G0 Z{self.draw_z} ; Lower pen")

        # Follow the contour path
        for point in self.contour:
            x, y = point[0]
            self.gcode.append(
                f"G1 X{x * self.scale_x:.2f} Y{y * self.scale_y:.2f}")

        # Lift the pen after drawing
        self.gcode.append(f"G0 Z{self.safe_z} ; Lift pen")
        self.gcode.append("G0 X0 Y0 ; Return to home")

    def save_gcode(self, output_path="output.gcode"):
        """Saves the generated G-code to a file."""
        if not self.gcode:
            raise ValueError(
                "No G-code generated. Run generate_gcode() first.")

        with open(output_path, "w") as file:
            file.write("\n".join(self.gcode))
        print(f"G-code saved as {output_path}")

    def process(self, output_path="output.gcode"):
        """Runs the full process: load image, generate G-code, and save to file."""
        self.load_image()
        self.generate_gcode()
        self.save_gcode(output_path)


# Example Usage
if __name__ == "__main__":
    gcode_gen = GCodeGenerator(
        "svg/processed_konan.jpg", scale_x=0.5, scale_y=0.5)
    gcode_gen.process("gcode/output.gcode")
