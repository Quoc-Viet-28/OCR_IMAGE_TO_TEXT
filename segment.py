# import cv2
# import numpy as np
# from ultralytics import SAM
# from skimage.filters import threshold_local
# import imutils
# import re
# def is_white_inside_box(gray, box):
#     x_tl, y_tl = box["top_left"]
#     x_br, y_br = box["bottom_right"]
#     roi = gray[y_tl:y_br, x_tl:x_br]
#     return np.all(roi == 255)
# def get_segment_points(approx):
#     if len(approx) == 4:
#         approx = approx.reshape(4, 2)
#         print("bằng 4")
#         print(approx)
#         return approx
#     else:
#         print("khác 4")
#         x, y, w, h = cv2.boundingRect(approx)
#         approx = np.array(
#             [[x, y], [x + w, y], [x + w, y + h], [x, y + h]], dtype=np.float32
#         )
#         print(approx)
#         return approx
# def do_lines_intersect(line1, line2):
#     x1, y1 = line1[0]
#     x2, y2 = line1[1]
#     x3, y3 = line2[0]
#     x4, y4 = line2[1]
#     det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
#     if (
#         (line1[0] == line2[0]).all()
#         or (line1[0] == line2[1]).all()
#         or (line1[1] == line2[0]).all()
#         or (line1[1] == line2[1]).all()
#     ):
#         return False
#     else:
#         if det == 0:
#             return False
#         else:
#             intersection_x = (
#                 (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
#             ) / det
#             intersection_y = (
#                 (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
#             ) / det
#
#             if (
#                 min(x1, x2) <= intersection_x <= max(x1, x2)
#                 and min(y1, y2) <= intersection_y <= max(y1, y2)
#                 and min(x3, x4) <= intersection_x <= max(x3, x4)
#                 and min(y3, y4) <= intersection_y <= max(y3, y4)
#             ):
#                 return True
#             else:
#                 return False
#
#
# def find_intersecting_lines(coordinates):
#     intersecting_lines = []
#     for i in range(len(coordinates)):
#         for j in range(i + 1, len(coordinates)):
#             line1 = [coordinates[i], coordinates[j]]
#             for k in range(len(coordinates)):
#                 for l in range(k + 1, len(coordinates)):
#                     line2 = [coordinates[k], coordinates[l]]
#                     if do_lines_intersect(line1, line2):
#                         intersecting_lines.append((line1, line2))
#     return intersecting_lines[0]
# def find_top_and_bottom_coordinates(diagonalline):
#     tl = []
#     tr = []
#     bl = []
#     br = []
#     coord1, coord2 = diagonalline[0]
#     coord3, coord4 = diagonalline[1]
#     data = [coord1, coord2, coord3, coord4]
#     temp = 999999
#     idex = 0
#     i = 0
#     for item in data:
#         if item[1] < temp:
#             idex = i
#             temp = item[1]
#         i += 1
#     if idex == 1:
#         coord1 = data[1]
#         coord2 = data[0]
#     if idex == 3:
#         coord3 = data[3]
#         coord4 = data[2]
#     if idex == 0 or idex == 1:
#         x1 = coord1[0] - coord2[0]
#         # nghien ben phai
#         if x1 < 0:
#             tl = coord1
#             br = coord2
#             if coord3[0] < coord4[0]:
#                 bl = coord3
#                 tr = coord4
#             else:
#                 bl = coord4
#                 tr = coord3
#         # nghien ben trai
#         else:
#             tr = coord1
#             bl = coord2
#             if coord3[0] < coord4[0]:
#                 # pass
#                 br = coord4
#                 tl = coord3
#             else:
#                 br = coord3
#                 tl = coord4
#     else:
#         x1 = coord3[0] - coord4[0]
#         # nghien ben phai
#         if x1 < 0:
#             tl = coord3
#             br = coord4
#             if coord1[0] < coord2[0]:
#                 # pass
#                 bl = coord1
#                 tr = coord2
#             else:
#                 bl = coord2
#                 tr = coord1
#         else:
#             tr = coord3
#             bl = coord4
#             if coord1[0] < coord2[0]:
#                 # pass
#                 br = coord2
#                 tl = coord1
#             else:
#                 br = coord1
#                 tl = coord2
#     return tl, tr, bl, br
# w_b = 50
# h_b = 5
# image = cv2.imread(r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\t4.webp")
# orig = image.copy()
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# cv2.imshow("gray", gray)
# cv2.waitKey(0)
# h, w = gray.shape
# x_center = w // 2
# y_center = h // 2
# result = False
# while not result:
#     print("x_center: ", x_center)
#     print("y_center: ", y_center)
#     x_tl = int(x_center - (w_b / 2))
#     y_tl = int(y_center - (h_b / 2))
#     x_br = int(x_center + (w_b / 2))
#     y_br = int(y_center + (h_b / 2))
#     print("x_topleft: ", x_tl)
#     print("y_topleft: ", y_tl)
#     print("x_botright: ", x_br)
#     print("y_botright: ", y_br)
#     orig_copy = orig.copy()
#     cv2.rectangle(orig_copy, (x_tl, y_tl), (x_br, y_br), (0, 255, 0), 1)
#     cv2.imshow("box", orig_copy)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     result = is_white_inside_box(gray, {"top_left": (x_tl, y_tl), "bottom_right": (x_br, y_br)})
#     print(result)
#     if result:
#             print("True - Coordinates: x =", x_center, ", y =", y_center)
#             break
#     y_center = y_center + 5
# contours = []
# true_cnts = []
# if result:
#     model = SAM(r'D:\dev-viet\project1\sam_b.pt')
#     res_img=model(image, points=[x_center, y_center], labels=[0], save = True, conf = 0.25, iou = 0.45)
#     if res_img is not None:
#         for r in res_img:
#             if r.masks is not None:
#                 Masks=r.masks.xy
#                 for m in Masks:
#                     contours.append(m)
#             else:
#                 print("masks is none")
#         for cnt in contours:
#             cnt_np = np.array(cnt, dtype=np.float32)
#             true_cnts = [cnt_np]
#         true_cnts = sorted(true_cnts, key = cv2.contourArea, reverse = True)[:5]
#         for c in true_cnts:
#             peri = cv2.arcLength(c, True)
#             approx = cv2.approxPolyDP(c, 0.04 * peri, True)
#             approx = get_segment_points(approx)
#             diagonalline = find_intersecting_lines(approx)
#             topleft, topright, botleft, botright = find_top_and_bottom_coordinates(diagonalline)
#             approx_2 = np.array(
#                     [topleft, topright, botright, botleft], dtype=np.float32
#                 )
#             widthA = np.sqrt(
#                     ((botright[0] - botleft[0]) ** 2)
#                     + ((botright[1] - botleft[1]) ** 2)
#                 )
#             widthB = np.sqrt(
#                     ((topright[0] - topleft[0]) ** 2)
#                     + ((topright[1] - topleft[1]) ** 2)
#                 )
#             heightA = np.sqrt(
#                     ((topright[0] - botright[0]) ** 2)
#                     + ((topright[1] - botright[1]) ** 2)
#                 )
#             heightB = np.sqrt(
#                     ((topleft[0] - botleft[0]) ** 2) + ((topleft[1] - botleft[1]) ** 2)
#                 )
#             print("WidthA:", widthA)
#             print("WidthB:", widthB)
#             print("heightA:", heightA)
#             print("heightB:", heightB)
#             maxWidth = max(int(widthA), int(widthB))
#             maxHeight = max(int(heightA), int(heightB))
#             new_corners = np.array(
#                     [
#                         [0, 0],
#                         [maxWidth - 1, 0],
#                         [maxWidth - 1, maxHeight - 1],
#                         [0, maxHeight - 1],
#                     ],
#                     dtype=np.float32,
#                 )
#             print("Max Width:", maxWidth)
#             print("Max Height:", maxHeight)
#             print("Corner Points:", new_corners)
#             matrix = cv2.getPerspectiveTransform(approx_2, new_corners)
#             new_image = cv2.warpPerspective(image, matrix, (maxWidth, maxHeight))
#             warped = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
#             T = threshold_local(warped, 11, offset=10, method = 'gaussian')
#             warped = (warped > T).astype(np.uint8) * 255
#             print("STEP 3: Apply perspective transform")
#             cv2.imshow("Original", orig)
#             cv2.imshow("Scanned", warped)
#             cv2.imwrite("Scanned.jpg", warped)
#             cv2.waitKey(0)
#

#############SỬ DỤNG HÀM IMAGE TO DATA##############
from pytesseract import Output
import pytesseract
import argparse
import cv2
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to input image to be OCR'd", default=r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\IMAGE\crop_1.jpg")
ap.add_argument("-c", "--min_conf", type=int, default=0, help="mininum confidence value to filter weak text detection")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])
orig_image = image.copy()
orig_h, orig_w = orig_image.shape[:2]
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
## --PSM 4 Assume a Single Column of Text of Variable Sizes
## --PSM 5 Assume a Single Uniform Block of Vertically Aligned Text
config = r"--oem 1 --psm 4 tessedit_char_whitelist=0123456789ZzJjWw"
results = pytesseract.image_to_data(gray, output_type=Output.DICT, lang = "vie", config = config)
for i in range(0, len(results["text"])):
    x = results["left"][i]
    y = results["top"][i]
    w = results["width"][i]
    h = results["height"][i]
    sumx=x+w
    sumy=y+h
    text = results["text"][i]
    conf = int(results["conf"][i])
    if conf > args["min_conf"]:
        print("Confidence: {}".format(conf))
        print("Text: {}".format(text))
        print("")
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        cv2.rectangle(image, (x, y), (sumx, sumy), (0, 255, 0), 1)
        #cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 1)
cv2.imshow("Image", image)
cv2.waitKey(0)


# #############LẤY CÁC BOX XUNG QUANH CÁC TỪ ########
# import pytesseract
# from pytesseract import Output
# import cv2
# img = cv2.imread(r'D:\dev-viet\project1\donthuoc_web_cut.jpg')
# pytesseract.pytesseract.tesseract_cmd = r"D:\dev-viet\tesseract.exe"
# config = r"--psm 4 tessedit_char_whitelist=ZzJjWw"
# d = pytesseract.image_to_data(img, output_type=Output.DICT, config=config, lang = "vie")     # ở đây để output_type=Output.DICT để trả về dạng dictionary
# # in ra để biết các keys trong dict là gì
# print(d)
# # số bounding boxes trả về
# n_boxes = len(d['level'])
# # duyệt qua các bounding boxes đó
# for i in range(n_boxes):
#     # lấy x, y, w, h cho từng bounding box
#     (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
#     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)  # vẽ
# cv2.imshow('img', img)
# cv2.waitKey(0)

##############LẤY CÁC BOX XUNG QUANH KÍ TỰ###################
# import cv2
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r"D:\dev-viet\tesseract.exe"
# img = cv2.imread(r'D:\dev-viet\project1\donthuocpre.png')
# config = r"--oem 1 --psm 7 tessedit_char_whitelist=ZzJjWw"
# h, w, c = img.shape

# boxes = pytesseract.image_to_boxes(img, config = config, lang ="vie")
# """
#     # Hàm trên trả về string gồm các dòng, một số dòng có định dạng như sau
#     # O 199 19 230 51 0
#     # C 232 19 261 51 0
#     # R 265 20 295 50 0
# """
# print(type(boxes))
# print(boxes)

# for b in boxes.splitlines():
#     b = b.split(' ')    # loại bỏ các kí tự khoảng trắng ở đầu và cuối
#     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 1)

# cv2.imshow('img', img)
# cv2.waitKey(0)


