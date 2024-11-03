

import cv2
import numpy as np


def nothing(x):
    pass

# 创建一个窗口和滑块条来调整参数
cv2.namedWindow('Trackbars')
cv2.createTrackbar('p_1', 'Trackbars', 115, 255, nothing)
cv2.createTrackbar('p_2', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('min_r', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('max_r', 'Trackbars', 255, 255, nothing)

# 打开摄像头
cap = cv2.VideoCapture(0)
# center_x, center_y = 600, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
cv2.namedWindow('Chessboard')
# cv2.resizeWindow('Chessboard', 480, 640)
cv2.namedWindow('Threshold')
cv2.resizeWindow('Threshold', 480, 640)

# radius = 48
while True:
    # # 读取一帧图像
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # frame = frame[center_y - radius:center_y + radius, center_x - radius:center_x + radius]
    # frame = cv2.imread("E:/JiChuang/Chinese-chess/detect_cnn/test/1.png")

    # # 将图像转换为 HSV 颜色空间
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # # 定义红色的 HSV 范围
    # lower_red = np.array([127, 115, 0]) #[80, 33, 97]
    # upper_red = np.array([255, 255, 255])#[179, 255, 255]
    # # 使用 inRange 函数检测在指定范围内的颜色
    # mask = cv2.inRange(hsv, lower_red, upper_red)

    # # 对图像进行平滑处理
    # blurred = cv2.GaussianBlur(mask, (11, 11), 0)

    # # 对图像进行二值化处理
    # _, thresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)
    thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # # 定义结构元素
    # kernel = np.ones((2,2), np.uint8)

    # # 腐蚀图像
    # eroded_img = cv2.erode(thresh, kernel, iterations=2)
    # dilate_img = cv2.dilate(eroded_img, kernel, iterations=2)


    # 使用霍夫圆检测
    p_1 = cv2.getTrackbarPos('p_1', 'Trackbars')
    p_2 = cv2.getTrackbarPos('p_2', 'Trackbars')
    min_r = cv2.getTrackbarPos('min_r', 'Trackbars')
    max_r = cv2.getTrackbarPos('max_r', 'Trackbars')
    circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, dp=1, minDist=15,
                               param1=p_1, param2=p_2, minRadius=min_r, maxRadius=max_r)

    # 仅在找到至少一个圆时执行后续操作
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # 画出圆形
            cv2.circle(frame, (x, y), r, (0, 255, 255), 2)
            cv2.circle(frame, (x, y), 2, (255, 0, 255), 2)

    # 显示原始图像和处理后的图像
    frame = cv2.resize(frame, (480, 640))
    cv2.imshow('Chessboard', frame)
    cv2.imshow('Threshold', thresh)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头并关闭所有窗口
# cap.release()
cv2.destroyAllWindows()
