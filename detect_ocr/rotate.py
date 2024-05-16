import cv2
import numpy as np
from pretreat import process_frame
from test_ocr import ocr
import time
def detect_and_draw_lines(img):
    # 加载图像
    # img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # if img is None:
    #     print("Error: Image cannot be loaded.")
    #     return

    # 应用Canny边缘检测
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    # cv2.imshow('edges', edges)

    # 使用霍夫线变换检测直线
    lines = cv2.HoughLinesP(edges, 0.5, np.pi / 180, threshold=10, minLineLength=10, maxLineGap=1)

    if lines is not None:
        # 提取线段长度并排序选出最长的10条
        lines = sorted(lines, key=lambda x: np.linalg.norm([x[0][2] - x[0][0], x[0][3] - x[0][1]]), reverse=True)
        top_lines = lines[:10]

        # 计算角度并绘制直线
        angles = []
        for line in top_lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            angles.append(angle)

        # 显示图像和角度
        # cv2.imshow('Image with Lines', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return angles[0]
    else:
        print("No lines were detected.")
        return []

def rotate_image(img, angle):
    rotated_images = []  # 用于存储旋转后的图像
    current_angle = angle  # 初始旋转角度

    for _ in range(4):  # 进行四次旋转
        # 获取图像尺寸
        (h, w) = img.shape[:2]

        # 计算旋转的中心点
        center = (w // 2, h // 2)

        # 获取旋转矩阵
        M = cv2.getRotationMatrix2D(center, current_angle, 1.0)

        # 执行旋转，指定边框颜色为白色
        rotated_img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255), flags=cv2.INTER_CUBIC)

        # 将旋转后的图像添加到列表中
        rotated_images.append(rotated_img)

        # 更新角度为下一个90度
        current_angle += 90

    return rotated_images

def pretreat_img(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = process_frame(img)
    cv2.imshow('proc', img)
    angles = detect_and_draw_lines(img)
    if angles:
        imgs = rotate_image(frame, angles)
        return imgs
    else:
        return

def ocr_all(frames):
    probes = []
    max_probe = 0
    max_word = None
    for frame in frames:
        result = ocr(frame)
        # print("result:", result)
        if result:
            probes.append((result))
    for word, probe in probes:
        if probe > max_probe:
            max_probe = probe
            max_word = word
    return max_word, max_probe

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    # 设置摄像头分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

    # 定义圆心坐标和半径
    center_x, center_y = 621, 271
    radius = 70
    frames = []
    # 调用函数
    # image_path = "E:/JiChuang/Chinese-chess/detect_cnn/dataset3/5/51.png"  # 替换为你的图片路径
    while True:
        ret, frame = cap.read()        
        # 截取圆形区域
        frame = frame[center_y - radius:center_y + radius, center_x - radius:center_x + radius]
        cv2.imshow('frame', frame)

        frames = pretreat_img(frame)
        if frames:
            max_word, max_probe = ocr_all(frames)
            if max_word:
                print((max_word, max_probe))
        if cv2.waitKey(1)==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

