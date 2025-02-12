import cv2
import os
import subprocess
from PIL import Image
from processor import Processor
from heuristicGcode import Heuristic_gcode

def image2gcode(indir, outdir, filename):
    os.makedirs(indir, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)

    filename_without_suffix = os.path.splitext(filename)[0]

    input_file = os.path.join(indir, filename)
    image_output_file = os.path.join(outdir, "processed_"+filename_without_suffix+".jpg")
    gcode_output_file = os.path.join(outdir, "heuristic_"+filename_without_suffix+".gcode")

    input_image = cv2.imread(input_file, cv2.IMREAD_GRAYSCALE)
    input_image = Processor.resize(input_image, 480)
    edges = cv2.Canny(input_image, 50, 150)

    processed_image = Processor.process(edges)

    cv2.imwrite(image_output_file, processed_image)

    Heuristic_gcode(processed_image, gcode_output_file)   



def image2svg(indir, outdir, filename):
    os.makedirs(indir, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)

    input_path = os.path.join(indir, filename)
    output_path = os.path.join(outdir, "processed_"+filename)
    pnm_path = os.path.splitext(output_path)[0] + ".pnm"
    svg_path = os.path.splitext(output_path)[0] + ".svg"

    konan = cv2.imread(input_path)
    konan = Processor.resize(konan, 480)
    edges = cv2.Canny(konan, 50, 150)

    processed = Processor.process(edges)

    cv2.imwrite(output_path, processed)
    # # Use command line to convert processed image to bitmap
    # subprocess.run(["magick", output_path, pnm_path])

    img = Image.fromarray(processed)
    img.save(pnm_path, format="PPM")

    # Use command line to convert bitmap to svg
    subprocess.run(["potrace", pnm_path, "-s", "-o", svg_path])


def svg2gcode(indir, outdir, filename):
    os.makedirs(indir, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    pass


if __name__ == "__main__":
    filename = "konan.jpg"

    image2gcode("resources", "output", filename) 
    # image2svg("resources", "svg", filename)
    # svg2gcode("svg", "gcode", filename)
