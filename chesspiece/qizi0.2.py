import cv2
import numpy as np

# 存储前一帧圆的信息
previous_circles = None
alpha = 0.8  # 平滑系数，用于帧间平滑

def merge_circles(circles):
    if circles is None:
        return None
    circles = np.uint16(np.around(circles))
    filtered_circles = []
    merged = set()
    for i in range(len(circles[0])):
        if i in merged:
            continue
        x1, y1, r1 = circles[0][i]
        center1 = np.array([x1, y1])
        radius1 = r1
        merge_count = 1
        for j in range(i + 1, len(circles[0])):
            if j in merged:
                continue
            x2, y2, r2 = circles[0][j]
            center2 = np.array([x2, y2])
            if np.linalg.norm(center1 - center2) < 15:
                center1 = (center1 * merge_count + center2) / (merge_count + 1)
                radius1 = (radius1 * merge_count + r2) / (merge_count + 1)
                merge_count += 1
                merged.add(j)
        filtered_circles.append((int(center1[0]), int(center1[1]), int(radius1)))
    return filtered_circles

def count_red_pixels(img, x, y, radius):
    """计算圆内部的红色像素数量"""
    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.circle(mask, (x, y), radius, 255, -1)
    masked = cv2.bitwise_and(img, img, mask=mask)
    # 定义红色的阈值，HSV颜色空间中的红色
    lower_red = np.array([80, 33, 97])
    upper_red = np.array([179, 255, 255])
    # lower_red2 = np.array([170, 120, 70])
    # upper_red2 = np.array([180, 255, 255])
    red_mask = cv2.inRange(cv2.cvtColor(masked, cv2.COLOR_BGR2HSV), lower_red, upper_red)
    # red_mask2 = cv2.inRange(cv2.cvtColor(masked, cv2.COLOR_BGR2HSV), lower_red2, upper_red2)
    # red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    return cv2.countNonZero(red_mask)

def detect_circles(img, param1, param2, minRadius, maxRadius, red_threshold):
    global alpha
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 2)
    gray = cv2.equalizeHist(gray)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 15, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    if circles is not None:
        circles = merge_circles(circles)
    if circles:
        for x, y, r in circles:
            num_red_pixels = count_red_pixels(img, x, y, r)
            color = (0, 0, 0)  # 黑色
            if num_red_pixels > red_threshold:
                color = (0, 0, 255)  # 红色
            cv2.circle(img, (x, y), 1, (0, 100, 100), 3)
            cv2.circle(img, (x, y), r, color, 1)
    cv2.imshow('Detected Circles', img)
    return circles

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cv2.namedWindow('Detected Circles')
cv2.createTrackbar('Param1', 'Detected Circles', 30, 300, lambda x: None)
cv2.createTrackbar('Param2', 'Detected Circles', 30, 300, lambda x: None)
cv2.createTrackbar('Min Radius', 'Detected Circles', 17, 30, lambda x: None)
cv2.createTrackbar('Max Radius', 'Detected Circles', 25, 50, lambda x: None)
cv2.createTrackbar('Red Threshold', 'Detected Circles', 11, 100, lambda x: None)  # 新增红色像素阈值滑块

while True:
    ret, frame = cap.read()
    if ret:
        param1 = cv2.getTrackbarPos('Param1', 'Detected Circles')
        param2 = cv2.getTrackbarPos('Param2', 'Detected Circles')
        minRadius = cv2.getTrackbarPos('Min Radius', 'Detected Circles')
        maxRadius = cv2.getTrackbarPos('Max Radius', 'Detected Circles')
        red_threshold = cv2.getTrackbarPos('Red Threshold', 'Detected Circles')  # 获取红色像素阈值
        detect_circles(frame, param1, param2, minRadius, maxRadius, red_threshold)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
