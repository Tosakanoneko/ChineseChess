import cv2

# 打开摄像头
cap = cv2.VideoCapture(0)  # 0代表第一个摄像头，如果有多个摄像头，可以尝试不同的索引值

while True:
    # 读取摄像头图像
    ret, frame = cap.read()
    
    # 显示图像
    cv2.imshow('Camera', frame)
    
    # 等待按键事件，如果按下键盘上的q键，则退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源
cap.release()
# 关闭所有窗口
cv2.destroyAllWindows()
