import cv2

def crop_frame(point, frame):
    # 获取帧的高度和宽度
    half_a = 70
    # 指定中心坐标
    center_x = point[0]
    center_y = point[1]
    # 裁剪图像
    cropped_frame = frame[center_y - half_a:center_y + half_a, center_x - half_a:center_x + half_a]

    return cropped_frame

if __name__ == '__main__':
    # 示例使用
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    point = (621, 271)
    while(True):
        ret, frame = cap.read()

        # 裁剪图像
        cropped_frame = crop_frame(point, frame)

        # 显示裁剪后的图像
        cv2.imshow('Cropped Frame', cropped_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
