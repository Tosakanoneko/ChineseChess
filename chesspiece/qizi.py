import cv2
import numpy as np

# 存储前一帧圆的信息
previous_circles = None
alpha = 0.8  # 平滑系数，用于帧间平滑

def detect_circles(img, param1, param2, minRadius, maxRadius, previous_circles):
    global alpha
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 2)
    gray = cv2.equalizeHist(gray) # 直方图均衡化
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 15,
                               param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

    current_circles = {}
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            current_circles[tuple(i[:2])] = i[2]  # 将当前帧的圆心和半径存储为键值对

    # 平滑处理逻辑：帧间平滑更新圆的位置和半径
    if previous_circles:
        for center, radius in previous_circles.items():
            new_info = next((i for i in current_circles.items() if np.linalg.norm(np.array(center) - np.array(i[0])) < 20), None)
            if new_info:
                new_center, new_radius = new_info
                # 平滑更新半径和圆心
                smooth_radius = int(alpha * radius + (1 - alpha) * new_radius)
                smooth_center = (int(alpha * center[0] + (1 - alpha) * new_center[0]), int(alpha * center[1] + (1 - alpha) * new_center[1]))
                cv2.circle(img, smooth_center, 1, (0, 100, 100), 3)
                cv2.circle(img, smooth_center, smooth_radius, (255, 0, 255), 1)
                current_circles[smooth_center] = smooth_radius  # 更新当前圆的信息为平滑后的信息
            else:
                # 如果当前圆不在上一帧检测到的圆中，直接绘制当前信息
                cv2.circle(img, center, 1, (0, 100, 100), 3)
                cv2.circle(img, center, radius, (255, 0, 255), 3)

    cv2.imshow('Detected Circles', img)
    return current_circles  # 返回当前帧的圆位置和半径

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
