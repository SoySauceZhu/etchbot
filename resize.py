import re
import sys

# Function to resize G-code
def resize_gcode(gcode, scale=0.5):
    resized_gcode = []
    
    for line in gcode.splitlines():
        # Match X and Y coordinates
        match = re.match(r'G1(?: X([\d\.]+))?(?: Y([\d\.]+))?(?: F([\d\.]+))?', line)
        if match:
            x, y, f = match.groups()
            new_x = f"X{float(x) * scale:.2f}" if x else ""
            new_y = f"Y{float(y) * scale:.2f}" if y else ""
            new_f = f"F{f}" if f else ""  # Keep feed rate unchanged
            resized_line = f"G1 {new_x} {new_y} {new_f}".strip()
            resized_gcode.append(resized_line)
        else:
            resized_gcode.append(line)  # Keep other lines unchanged

    return "\n".join(resized_gcode)

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    size = float(sys.argv[3])

    with open(input_file, "r") as file:
        gcode_content = file.read()


    resized_gcode = resize_gcode(gcode_content, scale=size)

    with open(output_file, "w") as file:
        file.write(resized_gcode)

    print(f"Processed G-code saved to {output_file}")