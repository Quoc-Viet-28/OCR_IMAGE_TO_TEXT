import torch
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(torch.cuda.device_count())
    print("CUDA is available")