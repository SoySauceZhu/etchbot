import cv2
from processor import Processor

konan = cv2.imread("resources/konan.jpg")
konan = Processor.resize(konan, 480)
edges = cv2.Canny(konan, 50, 150)
# edges = Processor.resize(edges, 480)

processed = Processor.process(edges)

cv2.imshow("123", processed)
cv2.waitKey(0)

cv2.imwrite("processed/konan.jpg", processed)

