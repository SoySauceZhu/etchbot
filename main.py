import cv2
import os
import subprocess
from processor import Processor


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
    subprocess.run(["convert", output_path, pnm_path])
    subprocess.run(["potrace", pnm_path, "-s", "-o", svg_path])


def svg2gcode(indir, outdir, filename):
    os.makedirs(indir, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    pass


if __name__ == "__main__":
    filename = "konan.jpg"

    image2svg("resources", "svg", filename)
    svg2gcode("svg", "gcode", filename)
