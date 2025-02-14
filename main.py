import argparse
from generateController import image2gcode

def main():
    parser = argparse.ArgumentParser(description="Convert an image to G-code.")
    parser.add_argument("input_dir", help="The directory containing the input image.")
    parser.add_argument("output_dir", help="The directory to save the output G-code.")
    parser.add_argument("filename", help="The name of the image file to convert.")
    parser.add_argument("--resize_factor", type=float, default=0.3, help="The resize factor for the image.")
    parser.add_argument("--width", type=int, default=480, help="The width of the image.")
    parser.add_argument("--height", type=int, default=None, help="The height of the image.")

    args = parser.parse_args()

    image2gcode(args.input_dir, args.output_dir, args.filename, args.resize_factor, args.width, args.height)

if __name__ == "__main__":
    main() 
