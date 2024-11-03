import torch
import torch.nn as nn

model_path = './weights/train1/locust_model-20-epoch-0.965608ap-model.pth'

# 加载模型
model = torch.load(model_path, map_location=torch.device('cpu'))

# 打印模型结构
print(model)

# 或者更详细的列出模型每一层
for name, module in model.named_modules():
    print(f'{name}: {module}')
