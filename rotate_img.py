from pytesseract import Output
import pytesseract
import argparse
import imutils
import cv2
image = cv2.imread(r'D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\DATA_TENTHUOC_BOSUNG\152.jpg')
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_osd(rgb, output_type=Output.DICT)
print("[INFO] detected orientation: {}".format(results["orientation"]))
print("[INFO] rotate by {} degrees to correct".format(results["rotate"]))
print("[INFO] detected script: {}".format(results["script"]))
rotated = imutils.rotate_bound(image, angle=results["rotate"])
cv2.imshow("Original", image)
cv2.imshow("Output", rotated)
cv2.waitKey(0)