# import cv2
# import os
# # List of class names
# names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'Commas', 'D', 'Dinhoavietnamese', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'athuong', 'bthuong', 'cthuong', 'cong', 'dthuong', 'dot', 'dvietnamese', 'ethuong', 'fthuong', 'gthuong', 'hthuong', 'ithuong', 'jthuong', 'kthuong', 'lthuong', 'mthuong', 'nthuong', 'ngoacphai', 'ngoactrai', 'othuong', 'pthuong', 'percent', 'qthuong', 'rthuong', 'sthuong', 'tthuong', 'uthuong', 'vthuong', 'wthuong', 'xthuong', 'ythuong', 'zthuong']
# # Function to read YOLO format labels
# def read_yolo_labels(label_file, image_width, image_height):
#     with open(label_file, 'r') as f:
#         lines = f.readlines()
#     labels = []
#     for line in lines:
#         parts = line.strip().split()
#         class_index = int(parts[0])
#         label = names[class_index]
#         # YOLO labels are normalized, so convert them to pixel values
#         x_center, y_center, width, height = map(float, parts[1:])
#         x_min = int((x_center - width / 2) * image_width)
#         y_min = int((y_center - height / 2) * image_height)
#         x_max = int((x_center + width / 2) * image_width)
#         y_max = int((y_center + height / 2) * image_height)
#         labels.append((label, x_min, y_min, x_max, y_max))
#     return labels
# # Function to crop image based on label coordinates
# def crop_objects(image_file, labels, output_folder):
#     image = cv2.imread(image_file)
#     for label, x_min, y_min, x_max, y_max in labels:
#         object_image = image[y_min:y_max, x_min:x_max]
#         object_filename = os.path.join(output_folder, label + '.jpg')
#         if os.path.exists(object_filename):
#             count = 1
#             while True:
#                 new_filename = os.path.join(output_folder, label + '_' + str(count) + '.jpg')
#                 if not os.path.exists(new_filename):
#                     object_filename = new_filename
#                     break
#                 count += 1
#         cv2.imwrite(object_filename, object_image)
# images_dir = r'D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\Text_Recogonition_1920\train\images'
# labels_dir = r'D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\Text_Recogonition_1920\train\labels'
# output_folder = r'D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\TEXT_CUT_TRAIN_1920_2'
# # Create output folder if it doesn't exist
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)
# # Loop through each image and its corresponding label file
# for image_filename in os.listdir(images_dir):
#     if image_filename.endswith('.jpg'):
#         image_path = os.path.join(images_dir, image_filename)
#         label_filename = os.path.join(labels_dir, os.path.splitext(image_filename)[0] + '.txt')
#         if os.path.exists(label_filename):
#             image = cv2.imread(image_path)
#             image_height, image_width, _ = image.shape
#             labels = read_yolo_labels(label_filename, image_width, image_height)
#             crop_objects(image_path, labels, output_folder)
# import os
# import shutil
#
# # Đường dẫn đến thư mục chứa các tệp cần di chuyển
# source_folder = r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\TEXT_CUT_TRAIN_1920_2"
# dich_folder = r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\datasets\train"
# # Lặp qua tất cả các tệp trong thư mục nguồn
# for filename in os.listdir(source_folder):
#     file_path = os.path.join(source_folder, filename)
#     # Kiểm tra xem tệp có phải là tệp không
#     if os.path.isfile(file_path):
#         # Tách phần tiền tố ra khỏi tên tệp (tenfile_) để lấy tên thư mục
#         folder_name = filename.split("_")[0]  # Lấy tên thư mục bằng cách lấy phần trước dấu gạch dưới cuối cùng
#         # Đường dẫn đến thư mục đích
#         destination_folder = os.path.join(dich_folder, folder_name)
#         # Tạo thư mục nếu chưa tồn tại
#         if not os.path.exists(destination_folder):
#             os.makedirs(destination_folder)
#         # Di chuyển tệp vào thư mục đích
#         shutil.move(file_path, destination_folder)




