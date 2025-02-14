def find_max_coordinates(gcode_path):
    max_x = float('-inf')
    max_y = float('-inf')

    with open(gcode_path, 'r') as gcode_file:
        for line in gcode_file:
            if line.startswith('G1'):
                parts = line.split()
                for part in parts:
                    if part.startswith('X'):
                        x_value = float(part[1:])
                        if x_value > max_x:
                            max_x = x_value
                    elif part.startswith('Y'):
                        y_value = float(part[1:])
                        if y_value > max_y:
                            max_y = y_value

    return max_x, max_y

# Example usage
gcode_path = 'output/heuristic_konan.gcode'
max_x, max_y = find_max_coordinates(gcode_path)
print(f"Max X: {max_x}, Max Y: {max_y}")
