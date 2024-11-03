import cv2
from ultralytics import YOLO
import os

model = YOLO("./detect_local/best.pt")
# model = YOLO("./best.pt")

def classify_piece(img):
    """
    输入： 96*96棋子图片
    输出： 棋子类型
    """
    results = model.predict(img, save=False, verbose=False)
    best_id = results[0].probs.top1

    return best_id

if __name__ == '__main__':
    
    # 初始化摄像头
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # 确保摄像头索引正确
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        raise Exception("Could not open video device")
    # 设置摄像头分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    # 创建滑块窗口并设置大小
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 400, 200)
    def nothing(x):
        pass
    # 创建滑块控制X和Y坐标，以及矩形大小
    cv2.createTrackbar('X Coordinate', 'Trackbars', 0, 1280-96, nothing)
    cv2.createTrackbar('Y Coordinate', 'Trackbars', 0, 960-96, nothing)
    # 设置视频编码器和输出文件
    size = 96

    while True:
        ret, frame = cap.read()
        frame_cp = frame.copy()

        if ret:
            # 获取滑块的位置
            x = cv2.getTrackbarPos('X Coordinate', 'Trackbars')
            y = cv2.getTrackbarPos('Y Coordinate', 'Trackbars')

            # 在图像上绘制矩形
            cv2.rectangle(frame_cp, (x, y), (x+size, y+size), (0, 255, 0), 2)

            cropped_frame = frame[y:y+size, x:x+size]
            # cropped_gray_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

            results = model.predict(cropped_frame, save=False, verbose=False)

            best_id = results[0].probs.top1
            best_name = results[0].names[best_id]
            best_prob = round(results[0].probs.top1conf.item(), 2)
            print('best_name: ' + f'{best_name}' + ' best_prob: ' + f'{best_prob}')

            # 显示图像
            cv2.imshow("Camera", frame_cp)
            cv2.imshow("roi", cropped_frame)
            # time.sleep(0.1)
            # 检测按键操作
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break


    # 释放摄像头资源并关闭所有窗口
    cap.release()
    cv2.destroyAllWindows()
