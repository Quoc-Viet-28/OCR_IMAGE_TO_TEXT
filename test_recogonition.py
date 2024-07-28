from ultralytics import YOLO
import cv2
import csv
import json
import os
csv_file_path = r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\Data_TenThuoc\uniqueNone.csv"
json_file_path = r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\fullDatabaseNone.json"
def compare_strings(str1, str2, index):
    count = 0
    str2_words = str2.split()
    if len(str2_words) > index:
        str2_word = str2_words[index]
    else:
        str2_word = str2
    if len(str1) != len(str2_word):
        return False
    for i in range(len(str1)):
        if str1[i] == str2_word[i]:
            count += 1
    ratio = count / len(str2_word)
    if ratio >= 0.8:
        return True
    return False
def get_matching_rows(input_text, matching_rows, index, count_split, count_text):
    if count_split == 0:
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # Đọc dòng tiêu đề
                try:
                    text_column_index = header.index('TenThuoc')
                except ValueError:
                    print("Error: Required column 'TenThuoc' not found in CSV file.")
                    return None
                for row in reader:
                    if compare_strings(input_text, row[text_column_index], index):
                        matching_rows.append(row)
                print('Matching rows:', matching_rows)
        except FileNotFoundError:
            print(f"Error: File not found at {csv_file_path}")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    else:
        new_matching_rows = []
        print("đã vào else")
        for row in matching_rows:
            if compare_strings(input_text, row[0], index):
                    new_matching_rows.append(row)
            else:
                if count_text == len(row[0].split()):
                    new_matching_rows.append(row)
                else:
                    print("không tìm thấy")
        matching_rows = new_matching_rows.copy()
    print("index", index)
    print("count_text", count_text)
    count_split += 1
    index += 1
    count_text += 1
    return matching_rows, count_split, index, count_text
def save_to_json(matching_rows_2, json_file_path):
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                drug_dict = json.load(json_file)
        except Exception as e:
            print(f"Lỗi khi đọc tệp JSON: {str(e)}")
            drug_dict = {}
    else:
        drug_dict = {}
    existing_values = set(drug_dict.values())
    max_index = 0
    for key in drug_dict.keys():
        if key.startswith('TenThuoc'):
            try:
                index = int(key[8:])
                if index > max_index:
                    max_index = index
            except ValueError:
                pass
    for row in matching_rows_2:
        if row[0] not in existing_values:
            max_index += 1
            drug_dict[f'TenThuoc{max_index}'] = row[0]
            existing_values.add(row[0])
    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(drug_dict, json_file, ensure_ascii=False, indent=4)
        print(f"Dữ liệu đã được lưu vào tệp {json_file_path}")
    except Exception as e:
        print(f"Lỗi khi lưu vào tệp JSON: {str(e)}")
def detect_text(results):
    listName = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', ',', 'D', 'Đ', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', '+', 'd', '.', 'đ', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', ')', '(', 'o', 'p', '%', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    #listName = model.names
    for result in results:
        bb_list = result.boxes.numpy()
        center_list = []
        y_sum = 0
        for bb in bb_list:
            xyxy = bb.xyxy
            x_c = (xyxy[0][0] + xyxy[0][2]) / 2
            y_c = (xyxy[0][1] + xyxy[0][3]) / 2
            cls = bb.cls
            y_sum += y_c
            center_list.append([x_c, y_c, listName[int(cls[0])]])
        if len(center_list) <= 0:
            return ""
        l_point = center_list[0]
        r_point = center_list[0]
        for cp in center_list:
            if cp[0] < l_point[0]:
                l_point = cp
            if cp[0] > r_point[0]:
                r_point = cp
        text = ""
        for i, l in enumerate(sorted(center_list, key=lambda x: x[0])):
            text += str(l[2])
        return text
matching_rows = []
count_split = 0
index = 0
count_text = 0
model = YOLO(r'D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\recogonition_v8m.pt')
#model = YOLO(r'D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\text_recogonition_v8L_2.pt')
#model = YOLO(r'D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\text_recogonition_v8l.pt')
image_path = r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\DATA_BOSUNG_RECO\106_12.jpg"
image = cv2.imread(image_path)
image = cv2.resize(image, (640, 640))
results = model(image ,imgsz=640, iou=0.25, conf=0.7)  # results list
text = detect_text(results)
print(text)
text_2=""
matching_rows_, count_split, index, count_text = get_matching_rows(text,matching_rows,index,count_split,count_text)
matching_rows, count_split, index, count_text = get_matching_rows(text_2,matching_rows,index,count_split,count_text)
print('Matching rows:', matching_rows)
save_to_json(matching_rows,json_file_path)