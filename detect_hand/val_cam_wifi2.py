# OpenMV、Zero双向通信
import os
import cv2
import argparse
import socket
import numpy as np
import zmq
import base64

import torch
import model.detector
import utils.utils

# OpenMV的IP地址和端口
HOST = '192.168.137.5'
PORT = 8080

# 创建ZMQ上下文和PUB套接字
context = zmq.Context()
socket1 = context.socket(zmq.PUB)
socket1.bind("tcp://*:5555")  # 监听5555端口

if __name__ == '__main__':
    # 指定训练配置文件
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='./data/data3/category.data', help='Specify training profile *.data')
    parser.add_argument('--weights', type=str, default='./weights/train2/locust_model-30-epoch-0.983871ap-model.pth', help='The path of the .pth model to be transformed')

    opt = parser.parse_args()
    cfg = utils.utils.load_datafile(opt.data)
    assert os.path.exists(opt.weights), "请指定正确的模型路径"
    
    # 模型加载
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.detector.Detector(cfg["classes"], cfg["anchor_num"], True).to(device)
    model.load_state_dict(torch.load(opt.weights, map_location=device)) 
    model.eval()
    
    # 创建socket连接
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    # 发送HTTP请求
    request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(HOST)
    s.send(request.encode())
    
    data = b''
    while True:
        data += s.recv(4096)
        start = data.find(b'\xff\xd8')  # JPEG图像开始
        end = data.find(b'\xff\xd9')    # JPEG图像结束
        if start != -1 and end != -1:
            jpg = data[start:end+2]
            data = data[end+2:]
            ori_img = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
            
            if ori_img is not None:
                res_img = cv2.resize(ori_img, (cfg["width"], cfg["height"]), interpolation=cv2.INTER_LINEAR)
                img = res_img.reshape(1, cfg["height"], cfg["width"], 3)
                img = torch.from_numpy(img.transpose(0, 3, 1, 2))
                img = img.to(device).float() / 255.0    
                
                # 模型推理
                preds = model(img)
                
                # 特征图后处理
                output = utils.utils.handel_preds(preds, cfg, device)
                output_boxes = utils.utils.non_max_suppression(output, conf_thres=0.3, iou_thres=0.4)   
                
                # 加载label names
                LABEL_NAMES = []
                with open(cfg["names"], 'r') as f:
                    for line in f.readlines():
                        LABEL_NAMES.append(line.strip())
                
                h, w, _ = ori_img.shape
                scale_h, scale_w = h / cfg["height"], w / cfg["width"]  
                
                # 绘制预测框
                for box in output_boxes[0]:
                    box = box.tolist()
                    obj_score = box[4]
                    if obj_score > 0.7:
                        category = LABEL_NAMES[int(box[5])] 
                        x1, y1 = int(box[0] * scale_w), int(box[1] * scale_h)
                        x2, y2 = int(box[2] * scale_w), int(box[3] * scale_h)   
                        cv2.rectangle(ori_img, (x1, y1), (x2, y2), (255, 255, 0), 2)
                        cv2.putText(ori_img, '%.2f' % obj_score, (x1, y1 - 5), 0, 0.7, (0, 255, 0), 2)    
                        cv2.putText(ori_img, category, (x1, y1 - 25), 0, 0.7, (0, 255, 0), 2)   
                cv2.imshow('result', ori_img)

                # 发送到Zero
                _, buffer = cv2.imencode('.jpg', ori_img)
                jpg_as_text = base64.b64encode(buffer)
                socket1.send(jpg_as_text)

                if cv2.waitKey(1) == ord('q'):
                    break

    s.close()
    cv2.destroyAllWindows()
