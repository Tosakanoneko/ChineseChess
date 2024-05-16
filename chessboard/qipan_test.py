import cv2
import numpy as np

# 初始化摄像头
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 创建滑块回调函数
def nothing(x):
    pass

# 创建一个窗口
cv2.namedWindow('Chessboard Detector')

class chessboard():
    def __init__(self):
        self.width = 0
        self.height = 0
        self.x_pos = 0
        self.y_pos = 0
        self.points = []

    # 读取滑块的初始值
    def load_slider_values(self):
        try:
            with open('slider_config.txt', 'r') as file:
                values = file.read().split(',')
                cb.width, cb.height,cb.x_pos, cb.y_pos = [int(v) for v in values]
        except FileNotFoundError:
            return [348, 364, 91, 118]  # 默认值

    def draw_chessboard(self, frame):
        # 获取滑块的值
        self.width = cv2.getTrackbarPos('Width', 'Chessboard Detector')
        self.height = cv2.getTrackbarPos('Height', 'Chessboard Detector')
        self.x_pos = cv2.getTrackbarPos('X Position', 'Chessboard Detector')
        self.y_pos = cv2.getTrackbarPos('Y Position', 'Chessboard Detector')

        # 在画面中指定位置绘制一个矩形来代表棋盘边框
        top_left_x = self.x_pos
        top_left_y = self.y_pos
        bottom_right_x = self.x_pos + self.width
        bottom_right_y = self.y_pos + self.height
        cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (255, 0, 0), 1)

        # 绘制8等分的垂直线
        step_x = self.width // 8
        for i in range(1, 8):
            cv2.line(frame, (top_left_x + i * step_x, top_left_y), (top_left_x + i * step_x, bottom_right_y), (0, 255, 0), 1)

        # 绘制9等分的水平线
        step_y = self.height // 9
        for i in range(1, 9):
            cv2.line(frame, (top_left_x, top_left_y + i * step_y), (bottom_right_x, top_left_y + i * step_y), (0, 255, 0), 1)
        return frame

    # 保存滑块的值
    def save_slider_values(self):
        with open('slider_config.txt', 'w') as file:
            file.write(f'{self.width},{self.height},{self.x_pos},{self.y_pos}')
            print('chessboard config saved')

cb = chessboard()
# 读取滑块值
cb.load_slider_values() 
# 创建滑块，控制棋盘边框的长和高
cv2.createTrackbar('Width', 'Chessboard Detector', cb.width, 1000, nothing)
cv2.createTrackbar('Height', 'Chessboard Detector', cb.height, 1000, nothing)
cv2.createTrackbar('X Position', 'Chessboard Detector', cb.x_pos, 1000, nothing)
cv2.createTrackbar('Y Position', 'Chessboard Detector', cb.y_pos, 1000, nothing)

while True:
    # 读取摄像头画面
    ret, frame = cap.read()

    if not ret:
        continue
    
    cb.draw_chessboard(frame)

    # 显示图像
    cv2.imshow('Chessboard Detector', frame)

    # 按'q'退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cb.save_slider_values()
# 释放摄像头并关闭所有窗口
cap.release()
cv2.destroyAllWindows()
