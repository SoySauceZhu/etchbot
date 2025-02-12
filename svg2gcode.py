import svgpathtools
import numpy as np

# Load SVG file and extract paths
svg_file = "svg/processed_konan.svg"
paths, attributes = svgpathtools.svg2paths(svg_file)

# Scale and Offset (if needed)
scale_factor = 1  # Modify if needed
offset_x, offset_y = 0, 0  # Adjust based on your machine's zero point

# Generate G-code
gcode = ["G21 ; Set units to mm", "G90 ; Absolute positioning", "G1 Z5 F500 ; Lift pen"]
for path in paths:
    for segment in path:
        x, y = segment.start.real * scale_factor + offset_x, segment.start.imag * scale_factor + offset_y
        gcode.append(f"G0 X{x:.2f} Y{y:.2f}")  # Move to start position
        gcode.append("G1 Z0 F500 ; Lower pen")  # Lower pen

        x, y = segment.end.real * scale_factor + offset_x, segment.end.imag * scale_factor + offset_y
        gcode.append(f"G1 X{x:.2f} Y{y:.2f} F1000")  # Draw line

gcode.append("G1 Z5 F500 ; Lift pen")
gcode.append("G0 X0 Y0 ; Return to origin")
gcode.append("M2 ; End of program")

# Save to file
with open("output.gcode", "w") as f:
    f.write("\n".join(gcode))

print("G-code file generated: output.gcode")
