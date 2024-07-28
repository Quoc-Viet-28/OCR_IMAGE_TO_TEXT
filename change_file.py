# Đổi tên các file bên trong folder D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\IMAGE thành số từ 1 đến n
import os
path = r'D:\NAM3_KY1\PYCHAMPROJECT\TrainModelOCR\pythonProject\IMAGE'
i = 1
for filename in os.listdir(path):
    if filename.endswith('.jpg'):
        os.rename(os.path.join(path, filename), os.path.join(path, f'{i}.jpg'))
        i += 1

