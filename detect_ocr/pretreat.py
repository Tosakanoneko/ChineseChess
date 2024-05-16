# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import Image
from test_ocr import ocr
import time
# from rotate import detect_and_draw_lines, rotate_image
# 打开摄像头
cap = cv2.VideoCapture(0)

# 设置摄像头分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

# 定义圆心坐标和半径
center_x, center_y = 600, 480
radius = 48

def mask_outside_circle(image, x, y, r):
    # 创建一个与原图像同大小的全白遮罩
    mask = np.full(image.shape, 255, dtype=np.uint8)
    # 在遮罩上绘制黑色的圆形
    cv2.circle(mask, (x, y), r, (0, 0, 0), -1)
    # 将遮罩应用到原图像
    masked_image = cv2.bitwise_or(image, mask)
    return masked_image

def process_frame(frame):
    """ 
    将检测到的圆框内部的字保留，包括圆框以及圆框外部的图像像素值全部设置为255 
    如果没有检测到圆形，则返回全白图像
    """
    # 转换为PIL Image，再回到numpy array
    im_pil = Image.fromarray(frame)
    im = np.array(im_pil)
    # 二值化处理
    im[im == 0] = 255
    piece = np.where(im > 140, 255, 0).astype(np.uint8)
    # 定义结构元素
    kernel = np.ones((2, 2), np.uint8)
    # 腐蚀和膨胀处理
    eroded_img = cv2.erode(piece, kernel, iterations=2)
    dilated_img = cv2.dilate(eroded_img, kernel, iterations=1)
    # 圆形检测
    circles = cv2.HoughCircles(dilated_img, cv2.HOUGH_GRADIENT, dp=1, minDist=15, param1=149, param2=25, minRadius=24, maxRadius=31) # param1=75, param2=20, minRadius=35, maxRadius=48
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for (x, y, r) in circles[0]:
            cv2.circle(dilated_img, (x, y), r, (255), thickness=+20)
            dilated_img = mask_outside_circle(dilated_img, x, y, r)
        return dilated_img
    else:
        # 如果没有检测到圆形，则返回全白图像
        return np.full(frame.shape, 255, dtype=np.uint8)
    
# if __name__ == '__main__':
#     # 主循环
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         # 转换为灰度图像
#         img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         # 截取圆形区域
#         cropped_frame = img_gray[center_y - radius:center_y + radius, center_x - radius:center_x + radius]
#         cv2.imshow('gray', cropped_frame)
#         processed_img = process_frame(cropped_frame)
#         angles = detect_and_draw_lines(processed_img)
#         rotated_img = rotate_image(frame, angles)
#         # print(ocr(processed_img))
#         cv2.imshow('Processed Frame', rotated_img)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#         # time.sleep(0.5)

#     # 释放摄像头并关闭窗口
#     cap.release()
#     cv2.destroyAllWindows()
