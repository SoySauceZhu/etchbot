# etchbot

## Software:

### 1. AI modified picture: Cartoonify
https://openaccess.thecvf.com/content_cvpr_2018/papers/Chen_CartoonGAN_Generative_Adversarial_CVPR_2018_paper.pdf

https://github.com/ahmedbesbes/cartoonify

https://github.com/FilipAndersson245/cartoon-gan

### 2. Image processing:
1. edge detection -> label the edge clusters -> ignore minor cluster -> link the clusters -> binary image

   - edge detection: cv2.canny
   - label: scipy.ndimage.label
   - ignore minor cluster: ignore clusters that smaller than 50 pixels
   - linking: find shortest path by distance matrix, then connect with line

2. edge detection -> label the edge clusters -> discretize (g-code or scatter plot) -> re-connect the plot (traveling salesman) -> binary image

### 3. bitmap to svg
https://pypi.org/project/pypotrace/

https://potrace.sourceforge.net/

### 4. svg to Gcode
https://github.com/sameer/svg2gcode

https://ncviewer.com

### 4. alternative: svg to driver config file
~~I don't like this~~

### 5. Gcode Motor Driver
https://github.com/MarginallyClever/GcodeCNCDemo

https://github.com/grbl/grbl

## Hardware:
~~Mingjie know little about hardware~~

~~3D printed frame? I guess~~

