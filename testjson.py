import torch
from ultralytics import YOLO
from sklearn.metrics import f1_score

# Tải mô hình YOLOv8 đã được train
model = YOLO(r'D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\recogonition_v8m.pt')

# Định nghĩa hàm để tính toán F1 score
def calculate_f1(model, dataset_path):
    results = model.predict(dataset_path)
    y_true = []
    y_pred = []
    for result in results:
        y_true.append(result['gt_classes'])  # ground truth classes
        y_pred.append(result['pred_classes'])  # predicted classes

    # Flatten danh sách các nhãn
    y_true_flat = [item for sublist in y_true for item in sublist]
    y_pred_flat = [item for sublist in y_pred for item in sublist]

    # Tính toán F1 score
    f1 = f1_score(y_true_flat, y_pred_flat, average='weighted')
    return f1

# Đường dẫn đến dữ liệu thử nghiệm của bạn
test_data_path = r"C:\Users\20522\Downloads\FULL_CLASS_RECOGONITION\valid\images"

# Tính toán F1 score
f1 = calculate_f1(model, test_data_path)
print('F1 Score:', f1)
