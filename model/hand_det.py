import os
import cv2
import argparse
import torch
import sys
import numpy as np
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(current_dir)
sys.path.append(modules_dir)
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(current_dir, '..')
sys.path.append(modules_dir)
import torch.nn.functional as F
import detector
from multiprocessing import Process, Queue
import utils
import time

def resize_and_pad_image(original_image):
    # 调整大小到128x128
    resized_image = cv2.resize(original_image, (128, 128), interpolation=cv2.INTER_AREA)

    # 创建一个新的352x352的黑色背景图像
    black_background = np.zeros((352, 352, 3), dtype=np.uint8)

    # 计算128x128图像的左上角位置，以使其居中
    x_offset = (352 - 128) // 2
    y_offset = (352 - 128) // 2

    # 将128x128图像粘贴到黑色背景图像的中心
    black_background[y_offset:y_offset+128, x_offset:x_offset+128] = resized_image
    return black_background

def write_data(data):
    # 写入命名管道
    with open('./mypipe', 'w') as pipe:
        pipe.write(data)
    print(f"send to ui: {data}")

class hand_detector:
    def __init__(self):
        # self.queue = queue
        current_dir = os.path.dirname(os.path.abspath(__file__))
        modules_dir = os.path.join(current_dir)
        sys.path.append(modules_dir)
        #指定训练配置文件
        parser = argparse.ArgumentParser()
        # parser.add_argument('--data', type=str, default='/home/aidlux/Chinese-chess-GHT2/detect_hand/data/category.data', 
        #        help='Specify training profile *.data')
        # parser.add_argument('--weights', type=str, default='/home/aidlux/Chinese-chess-GHT2/detect_hand/weights/train5/hand-290-epoch-0.273143ap-model.pth', 
        #                     help='The path of the .pth model to be transformed')
        parser.add_argument('--data', type=str, default='/home/admin/Chinese-chess-Phytium3/detect_hand/data/category.data', 
               help='Specify training profile *.data')
        parser.add_argument('--weights', type=str, default='/home/admin/Chinese-chess-Phytium3/detect_hand/weights/train5/hand-150-epoch-0.312856ap-model.pth', 
                            help='The path of the .pth model to be transformed')

        self.opt = parser.parse_args()
        self.cfg = utils.load_datafile(self.opt.data)
        # assert os.path.exists(self.opt.weights), "请指定正确的模型路径"
        #模型加载
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.model = model.detector.Detector(self.cfg["classes"], self.cfg["anchor_num"], True).to(self.device)
        self.model = detector.Detector(1, 3, True).to(self.device)
        self.model.load_state_dict(torch.load(self.opt.weights, map_location=self.device)) 
        self.model.eval()

        # self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.frame_count = 0
        self.detect_list = []
        self.hand_detected = False

        self.frame = None


    def hand_detect(self, frame):
        res_img = resize_and_pad_image(frame)
        # cv2.imshow('res_img', res_img)
        # ori_img = cv2.resize(ori_img, (352, 352))
        img = res_img.reshape(1, 352, 352, 3)
        img = torch.from_numpy(img.transpose(0, 3, 1, 2))
        img = img.to(self.device).float() / 255.0
        # 模型推理
        start_time = time.time()
        preds = self.model(img)
        # print("time: ", time.time() - start_time)
        # print(preds)

        # 特征图后处理
        output = utils.handel_preds(preds, self.device)
        output_boxes = utils.non_max_suppression(output, conf_thres=0.3, iou_thres=0.4)   
        
        hand_detected = False
        for box in output_boxes[0]:
            box = box.tolist()
            obj_score = box[4]
            if obj_score > 0.1:
                # print(obj_score)
                self.detect_list.append('hand')
                hand_detected = True
                break
        if not hand_detected:
            self.detect_list.append('nothand')
            

    def run_hand_detect(self):
        while True:
            if not self.queue.empty():
                frame = self.queue.get()
                if frame is None:
                    print("结束")
                    break
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                self.frame_count += 1
                # cv2.imshow('Frame', frame)
                self.hand_detect(frame)
                if self.frame_count % 10 == 0:
                    if self.detect_list.count("hand") > 1:
                        self.hand_detected = True
                    else:
                        self.hand_detected = False
                    self.frame_count = 0
                    self.detect_list = []
                if self.hand_detected:
                    print("hand detected")
                    # cv2.putText(frame, "hand detected", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) , 2, cv2.LINE_AA)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def run_hand_detect_cam(self):
        print("2")
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        while True:
            print("1")
            ret, frame = cap.read()
            if ret:
            # if frame is not None:
                print("3")
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                self.frame_count += 1
                self.hand_detect(frame)
                if self.frame_count % 10 == 0:
                    if self.detect_list.count("hand") > 1:
                        self.hand_detected = True
                    else:
                        self.hand_detected = False
                    self.frame_count = 0
                    self.detect_list = []
                if self.hand_detected:
                    cv2.putText(frame, "hand detected", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) , 2, cv2.LINE_AA)
                # frame = cv2.resize(frame, (480, 640))
                cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def run_hand_detect_frame(self, frame):
        self.frame_count += 1
        # frame = frame[80:1200,0:960]
        # frame = cv2.resize(frame, (352, 352))
        self.hand_detect(frame)
        if self.detect_list.count("hand") == 1:
            self.hand_detected = True
        else:
            self.hand_detected = False
        # if self.frame_count % 10 == 0:
        #     if self.detect_list.count("hand") > 1:
        #         self.hand_detected = True
        #     else:
        #         self.hand_detected = False
        self.frame_count = 0
        self.detect_list = []


if __name__ == '__main__':
    # queue = Queue()
    hand_det = hand_detector()
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            hand_det.run_hand_detect_frame(frame)
            if hand_det.hand_detected:
                print("hand detected")
            frame = cv2.resize(frame, (480, 640))
            cv2.imshow('1', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    
