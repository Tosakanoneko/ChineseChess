#平滑处理外轮廓和位置
import cv2
import numpy as np

# 存储前一帧圆的信息
previous_circles = None
alpha = 0.9  # 平滑系数，用于帧间平滑

def merge_circles(circles):
    """合并距离过近的圆，距离阈值为15像素"""
    if circles is None:
        return None
    circles = np.uint16(np.around(circles))
    filtered_circles = []

    # 用于记录哪些圆已经被合并
    merged = set()

    for i in range(len(circles[0])):
        if i in merged:
            continue

        # 当前圆的中心和半径
        x1, y1, r1 = circles[0][i]
        center1 = np.array([x1, y1])
        radius1 = r1
        merge_count = 1

        # 检查是否有需要合并的圆
        for j in range(i + 1, len(circles[0])):
            if j in merged:
                continue

            x2, y2, r2 = circles[0][j]
            center2 = np.array([x2, y2])
            if np.linalg.norm(center1 - center2) < 15:
                # 更新圆心和半径的平均值
                center1 = (center1 * merge_count + center2) / (merge_count + 1)
                radius1 = (radius1 * merge_count + r2) / (merge_count + 1)
                merge_count += 1
                merged.add(j)

        # 将合并后的圆加入到列表中
        filtered_circles.append((int(center1[0]), int(center1[1]), int(radius1)))

    return filtered_circles

def detect_circles(img, param1, param2, minRadius, maxRadius, previous_circles):
    global alpha
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 2)
    gray = cv2.equalizeHist(gray)  # 直方图均衡化
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 15,
                               param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

    if circles is not None:
        circles = merge_circles(circles)

    # 绘制圆
    if circles:
        for x, y, r in circles:
            cv2.circle(img, (x, y), 1, (0, 100, 100), 3)
            cv2.circle(img, (x, y), r, (255, 0, 255), 1)

    cv2.imshow('Detected Circles', img)
    return circles  # 返回当前帧的圆位置和半径

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cv2.namedWindow('Detected Circles')

cv2.createTrackbar('Param1', 'Detected Circles', 30, 300, lambda x: None)
cv2.createTrackbar('Param2', 'Detected Circles', 30, 300, lambda x: None)
cv2.createTrackbar('Min Radius', 'Detected Circles', 17, 100, lambda x: None)
cv2.createTrackbar('Max Radius', 'Detected Circles', 25, 100, lambda x: None)

while True:
    ret, frame = cap.read()
    if ret:
        param1 = cv2.getTrackbarPos('Param1', 'Detected Circles')
        param2 = cv2.getTrackbarPos('Param2', 'Detected Circles')
        minRadius = cv2.getTrackbarPos('Min Radius', 'Detected Circles')
        maxRadius = cv2.getTrackbarPos('Max Radius', 'Detected Circles')
        
        previous_circles = detect_circles(frame, param1, param2, minRadius, maxRadius, previous_circles)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
