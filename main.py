from ultralytics import YOLO
import cv2
import csv
import json
import os
import re
#csv_file_path = r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\Data_TenThuoc\uniqueNone.csv"
csv_file_path= r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\Data_TenThuoc\unique.csv"
def compare_strings(str1, str2, index):
    str1 = str1.lower()
    str2 = str2.lower()
    str2 = str2.replace("-", "")
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
def read_csv_file(csv_file_path):
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            return list(reader), header
    except FileNotFoundError:
        print(f"Error: File not found at {csv_file_path}")
        return None, None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None
def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    return s
def get_matching_rows(input_text, matching_rows, index, count_split, count_text, count_text_2):
    if input_text != "":
        reader, header = read_csv_file(csv_file_path)
        text_column_index = header.index('TenThuoc')
        print(f"Input text: '{input_text}', index: {index}, count_split: {count_split}, count_text: {count_text}")
        if count_split == 0:
                one_row = []
                for row in reader:
                    row_none = no_accent_vietnamese(row[text_column_index])
                    if compare_strings(input_text, row_none, index):
                        matching_rows.append(row)
                for row_f in matching_rows:
                    if len(row_f[text_column_index].split()) == 1:
                        print("vaoaosooo")
                        one_row.append(row_f)
                        success=save_to_json(one_row, json_file_path)
                        if success:
                            one_row.clear()
        else:
                new_matching_rows = []
                new_matching_rows_2 = []
                print("đã vào else")
                for row_2 in matching_rows:
                    row_none = no_accent_vietnamese(row_2[text_column_index])
                    if compare_strings(input_text, row_none, index):
                        print("đã vào đây laanfnnn 2")
                        new_matching_rows.append(row_2)
                matching_rows = [row_text for row_text in matching_rows if row_text in new_matching_rows]
                if len(new_matching_rows) == 0:
                    print("vao day day day day")
                    for r in reader:
                        row_none = no_accent_vietnamese(r[text_column_index])
                        if compare_strings(input_text, row_none, 0):
                            if len(r[text_column_index].split()) == 1:
                                print("vao day test")
                                new_matching_rows.append(r)
                            else:
                                print("vao day test falt")
                                new_matching_rows_2.append(r)
                                count_split = 0
                                index = 0
                                count_text = 0
                if new_matching_rows_2:
                    matching_rows = new_matching_rows_2.copy()
                    new_matching_rows_2.clear()
                    for row_3 in matching_rows:
                        if len(matching_rows) == 1 and index == len(row_3[text_column_index].split()) - 1:
                            success = save_to_json(matching_rows, json_file_path)
                            if success:
                                matching_rows.clear()
                if new_matching_rows:
                    matching_rows = new_matching_rows.copy()
                    for row_3 in matching_rows:
                        if len(matching_rows) == 1 and index == len(row_3[text_column_index].split())-1:
                            success = save_to_json(matching_rows, json_file_path)
                            if success:
                                matching_rows.clear()
        if len(matching_rows) == 0:
                count_split = 0
                index = 0
                count_text = 0
        else:
                count_split += 1
                index += 1
                count_text += 1
        print("index", index)
        print("count_text", count_text)
    else:
        matching_rows=[]
        count_split=0
        index=0
        count_text=0
        count_text_2=0
    return matching_rows, count_split, index, count_text, count_text_2

def save_to_json(matching_rows_2, json_file_path):
    drug_dict = {}
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    if os.path.exists(json_file_path):
        try:
            if os.path.getsize(json_file_path) == 0:  # Check if the file is empty
                print(f"Tệp JSON {json_file_path} trống. Khởi tạo dictionary mới.")
                drug_dict = {}
            else:
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    drug_dict = json.load(json_file)
        except json.JSONDecodeError as e:
            print(f"Lỗi khi đọc tệp JSON: Nội dung không phải là JSON hợp lệ. Chi tiết lỗi: {str(e)}")
            drug_dict = {}
        except Exception as e:
            print(f"Lỗi không xác định khi đọc tệp JSON: {str(e)}")
            drug_dict = {}
    existing_values = set(drug_dict.values())
    max_index = 0
    for key in drug_dict.keys():
        if key.startswith('presName'):
            try:
                index = int(key[8:])
                if index > max_index:
                    max_index = index
            except ValueError:
                pass
    for row in matching_rows_2:
        if row[0] not in existing_values:
            max_index += 1
            drug_dict[f'presName{max_index}'] = row[0]
            existing_values.add(row[0])
    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(drug_dict, json_file, ensure_ascii=False, separators=(',', ':'))
        print("dữ liệu lưu vào json là: ", drug_dict)
        print(f"Dữ liệu đã được lưu vào tệp {json_file_path}")
        return True
    except Exception as e:
        print(f"Lỗi khi lưu vào tệp JSON: {str(e)}")
        return False

def convert_and_delete_json(json_file_path):
    if json_file_path and os.path.exists(json_file_path):
        try:
            with open(json_file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
            json_string = json.dumps(data, ensure_ascii=False, indent=4)
            # Xóa tệp JSON sau khi gán chuỗi JSON thành công
            os.remove(json_file_path)
            print(f"Tệp {json_file_path} đã bị xóa.")
            return json_string
        except json.JSONDecodeError as e:
            print(f"Lỗi khi đọc tệp JSON: Nội dung không phải là JSON hợp lệ. Chi tiết lỗi: {str(e)}")
            return None
        except Exception as e:
            print(f"Lỗi không xác định khi xử lý tệp JSON: {str(e)}")
            return None
    else:
        print(f"Tệp {json_file_path} không tồn tại.")
        return None
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
        # for cp in center_list:
        #     if cp[0] < l_point[0]:
        #         l_point = cp
        #     if cp[0] > r_point[0]:
        #         r_point = cp
        text = ""
        for i, l in enumerate(sorted(center_list, key=lambda x: x[0])):
            text += str(l[2])
        return text
def read_by_line(results, image, json_string,):
    model_2 = YOLO(r'D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\recogonition_v8m.pt')
    matching_rows = []
    count_split = 0
    index = 0
    count_text = 0
    count_text_2 = 0
    center_line = []
    center_list = []
    min_center_x = float('inf')
    min_center_y = float('inf')
    count_line = 0
    bb_list = []
    json_string = ""
    for reslut in results:
        bb_list = reslut.boxes.numpy()
        for bb in bb_list:
            xyxy = bb.xyxy
            x_c = (xyxy[0][0] + xyxy[0][2]) / 2
            y_c = (xyxy[0][1] + xyxy[0][3]) / 2
            center_list.append([x_c, y_c])
    center_list = sorted(center_list, key=lambda x: x[1])
    for ct in center_list:
        min_center_x = center_list[count_line][0]
        min_center_y = center_list[count_line][1]
        print(min_center_y)
        for ct_2 in center_list:
            if abs(ct_2[1] - min_center_y) < 15:
                center_line.append(ct_2)
        center_line = sorted(center_line, key=lambda x: x[0])
        for ct in center_line:
            if ct in center_list:
                center_list.remove(ct)
                print("đã xóa", ct)
        for ct_3 in center_line:
            for box in bb_list:
                if ct_3[0] == (box.xyxy[0][0] + box.xyxy[0][2]) / 2 and ct_3[1] == (box.xyxy[0][1] + box.xyxy[0][3]) / 2:
                    print("nhảy vào line ", count_line)
                    box_int = box.xyxy.astype(int)
                    cv2.rectangle(image, (box_int[0][0], box_int[0][1]), (box_int[0][2], box_int[0][3]),
                                  (255, 0, 255), 1)
                    cv2.imwrite(r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\OUT.jpg", image)
                    crop_img = image[box_int[0][1]:box_int[0][3], box_int[0][0]:box_int[0][2]]
                    crop_img = cv2.resize(crop_img, (640, 640))
                    results_2 = model_2(crop_img, imgsz=640, iou=0.25)
                    text = detect_text(results_2)
                    text = text.replace("(", "")
                    text = text.replace(")", "")
                    text = text.strip("()")
                    text = text.replace(".", "")
                    text = text.replace("-", "")
                    matching_rows, count_split, index, count_text, count_text_2 = get_matching_rows(text, matching_rows, index, count_split, count_text, count_text_2)
                    print("matching_rows", matching_rows)
                    print(text)
                    # cv2.imshow("crop_img", crop_img)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
        center_line.clear()
    json_string = convert_and_delete_json(json_file_path)
    print("Chuỗi JSON thu được:")
    print(json_string)
def initJSON(json_file_path,name):
    json_file_path = fr"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\{name}.json"
    return json_file_path

json_string = ""
model = YOLO(r'D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\FULLDATA_V9.pt')
image = cv2.imread(r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\tiengviet5.jpg")
#image = cv2.imread(r"D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\anhtest\19030729_701334230069459_5689213752896010430_n.jpg")
image = cv2.resize(image, (640, 640))
results = model(image, imgsz=640, iou=0.25)
name = "VoQuocViet"
json_file_path = ""
json_file_path = initJSON(json_file_path,name)
json_string=read_by_line(results, image, json_string)
print(json_string)
