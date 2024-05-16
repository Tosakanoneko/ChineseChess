import cv2

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 初始化点的坐标
x, y = 0, 0

# 定义滑块的回调函数
def on_trackbar(val):
    global x, y
    x = cv2.getTrackbarPos('X', 'Frame')
    y = cv2.getTrackbarPos('Y', 'Frame')

# 创建一个窗口
cv2.namedWindow('Frame')

# 创建滑块
cv2.createTrackbar('X', 'Frame', 0, 640, on_trackbar)  # 假设摄像头分辨率为640x480
cv2.createTrackbar('Y', 'Frame', 0, 480, on_trackbar)

while True:
    # 从摄像头读取帧
    ret, frame = cap.read()
    if not ret:
        break

    # 获取当前点的像素值
    if x < frame.shape[1] and y < frame.shape[0]:
        pixel_value = frame[y, x]


        # 显示像素值
        cv2.putText(frame, f'BGR: {pixel_value}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # 在图像上绘制一个圆点
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    # 显示图像
    cv2.imshow('Frame', frame)

    # 按下'q'键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
