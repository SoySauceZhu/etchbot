import xml.etree.ElementTree as ET
from svgpathtools import parse_path

class SVGtoGCode:
    def __init__(self, svg_file, output_file="output.gcode", scale=1.0, feedrate=1000):
        self.svg_file = svg_file
        self.output_file = output_file
        self.scale = scale  # Scaling factor for SVG to G-code conversion
        self.feedrate = feedrate  # Feedrate for movement
        self.gcode_lines = []

    def parse_svg(self):
        """Extracts path data from the SVG file."""
        tree = ET.parse(self.svg_file)
        root = tree.getroot()
        namespace = {"svg": "http://www.w3.org/2000/svg"}
        
        paths = []
        for elem in root.findall(".//svg:path", namespace):
            d = elem.attrib.get("d", None)
            if d:
                paths.append(parse_path(d))
        
        return paths

    def convert_to_gcode(self):
        """Converts the parsed SVG path into G-code."""
        paths = self.parse_svg()
        
        self.gcode_lines.append("G21 ; Set units to mm")
        self.gcode_lines.append("G90 ; Absolute positioning")
        self.gcode_lines.append("G0 Z5 ; Lift pen/laser")

        for path in paths:
            start = path.start
            self.gcode_lines.append(f"G0 X{start.real * self.scale:.3f} Y{start.imag * self.scale:.3f} ; Move to start")
            self.gcode_lines.append("G1 Z0 ; Lower pen/laser")
            
            for segment in path:
                end = segment.end
                self.gcode_lines.append(f"G1 X{end.real * self.scale:.3f} Y{end.imag * self.scale:.3f} F{self.feedrate}")

            self.gcode_lines.append("G0 Z5 ; Lift pen/laser after stroke")

        self.gcode_lines.append("M30 ; Program end")

    def save_gcode(self):
        """Saves the generated G-code to a file."""
        with open(self.output_file, "w") as f:
            f.write("\n".join(self.gcode_lines))
        print(f"G-code saved to {self.output_file}")

    def generate_gcode(self):
        """Main function to run the conversion."""
        self.convert_to_gcode()
        self.save_gcode()


# Example usage:
if __name__ == "__main__":
    converter = SVGtoGCode("svg/processed_konan.svg")
    converter.generate_gcode()
