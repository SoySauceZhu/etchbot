import cv2
from processor import Processor
from canny import edge_detection


def resize_image_aspect_ratio(image, fixed_dimension, dimension_type='width'):
    
    # Get the current height and width of the image
    height, width = image.shape[:2]
    
    # Check if the fixed dimension is width or height
    if dimension_type == 'width':
        # Calculate new height based on fixed width
        new_width = fixed_dimension
        aspect_ratio = height / width
        new_height = int(new_width * aspect_ratio)
    elif dimension_type == 'height':
        # Calculate new width based on fixed height
        new_height = fixed_dimension
        aspect_ratio = width / height
        new_width = int(new_height * aspect_ratio)
    else:
        raise ValueError("dimension_type must be either 'width' or 'height'")
    
    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))
    
    return resized_image

img = cv2.imread("konan.jpg", cv2.IMREAD_GRAYSCALE)
img = resize_image_aspect_ratio(img, 480)

cv2.imshow("123", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

img = cv2.Canny(img, 50, 150)
cv2.imshow("123", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

img = Processor.process(img)
cv2.imshow("123", img)
cv2.waitKey(0)
cv2.destroyAllWindows()





