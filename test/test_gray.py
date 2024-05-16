# 摄像头灰度识别
import cv2
import numpy as np
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.where(gray > 140, 240, 15).astype(np.uint8)
    cv2.imshow('Gray', gray)
    cv2.imshow('ori', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
