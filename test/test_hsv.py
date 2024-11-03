import cv2
import numpy as np

def nothing(x):
    pass

# 打开摄像头
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 创建一个窗口
cv2.namedWindow('Sliders')

# 创建滑块，用于调整红色的HSV阈值
cv2.createTrackbar('Low H', 'Sliders', 124, 255, nothing)
cv2.createTrackbar('High H', 'Sliders', 255, 255, nothing)
cv2.createTrackbar('Low S', 'Sliders', 24, 255, nothing)
cv2.createTrackbar('High S', 'Sliders', 255, 255, nothing)
cv2.createTrackbar('Low V', 'Sliders', 133, 255, nothing)
cv2.createTrackbar('High V', 'Sliders', 255, 255, nothing)

while True:
    # 读取摄像头的帧
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    if not ret:
        print("无法从摄像头读取图像")
        break

    # 转换到HSV色彩空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 获取滑块的值
    low_h = cv2.getTrackbarPos('Low H', 'Sliders')
    high_h = cv2.getTrackbarPos('High H', 'Sliders')
    low_s = cv2.getTrackbarPos('Low S', 'Sliders')
    high_s = cv2.getTrackbarPos('High S', 'Sliders')
    low_v = cv2.getTrackbarPos('Low V', 'Sliders')
    high_v = cv2.getTrackbarPos('High V', 'Sliders')

    # 设置HSV的红色范围
    lower_red = np.array([low_h, low_s, low_v])
    upper_red = np.array([high_h, high_s, high_v])

    # 创建红色像素的掩码
    red_mask = cv2.inRange(hsv, lower_red, upper_red)

    # # 形态学操作
    # kernel = np.ones((5, 5), np.uint8)
    # # 腐蚀
    # red_mask = cv2.erode(red_mask, kernel, iterations=1)
    # # 膨胀
    # red_mask = cv2.dilate(red_mask, kernel, iterations=1)


    # 显示原始视频流和红色像素的位置
    frame = cv2.resize(frame, (480, 640))
    red_mask = cv2.resize(red_mask, (480, 640))
    cv2.imshow('Original', frame)
    cv2.imshow('red_mask', red_mask)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头和所有资源
cap.release()
cv2.destroyAllWindows()
