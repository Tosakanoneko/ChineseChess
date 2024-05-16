import os
import cv2
import numpy as np
def detect_and_modify_circles(folder_path):
    # 遍历文件夹及其子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg"):  # 确保处理的是图片文件
                image_path = os.path.join(root, file)
                # 读取图像
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                        # 定义结构元素
                kernel = np.ones((2,2), np.uint8)

                # 腐蚀图像
                eroded_img = cv2.erode(img, kernel, iterations=2)
                dilate_img = cv2.dilate(eroded_img, kernel, iterations=2)
                # 在图像上检测圆形
                circles = cv2.HoughCircles(dilate_img, cv2.HOUGH_GRADIENT, dp=1, minDist=15, param1=75, param2=18, minRadius=33, maxRadius=49)

                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    # 将检测到的圆形像素值修改为240
                    for (x, y, r) in circles[0]:
                        # 将圆形像素值修改为240
                        cv2.circle(dilate_img, (x, y), r, (240), thickness=+20)

                    # 保存修改后的图像，覆盖原文件
                    cv2.imwrite(image_path, dilate_img)

# 指定文件夹路径
folder_path = "E:/JiChuang/Chinese-chess/detect_cnn/dataset3/"

# 调用函数进行圆形检测并修改图片
detect_and_modify_circles(folder_path)
