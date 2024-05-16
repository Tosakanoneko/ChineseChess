import cv2
import numpy as np
def detect_and_modify_circles(image_path):
    # 读取图像
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # 定义结构元素
    kernel = np.ones((2,2), np.uint8)

    # 腐蚀图像
    eroded_img = cv2.erode(img, kernel, iterations=2)
    dilate_img = cv2.dilate(eroded_img, kernel, iterations=2)
    # cv2.imshow('dilate_img', dilate_img)
    # cv2.waitKey(0)
    # 在图像上检测圆形
    circles = cv2.HoughCircles(dilate_img, cv2.HOUGH_GRADIENT, dp=1, minDist=15, param1=75, param2=24, minRadius=39, maxRadius=49)
    print(circles)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        # circles = np.round(circles[0, :]).astype("int")
        # 将检测到的圆形像素值修改为240
        for (x, y, r) in circles[0]:
            # 将圆形像素值修改为240
            cv2.circle(dilate_img, (x, y), r, (240), thickness=+10)
            cv2.imshow("umg", dilate_img)
            cv2.waitKey(0)
        # 保存修改后的图像，覆盖原文件
        cv2.imwrite(output_path, dilate_img)

# 指定图片路径
image_path = "E:/JiChuang/Chinese-chess/detect_cnn/test/1.png"
output_path = "E:/JiChuang/Chinese-chess/detect_cnn/test/2.png"

# 调用函数进行圆形检测并修改图片
detect_and_modify_circles(image_path)
