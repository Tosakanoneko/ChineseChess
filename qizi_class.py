import cv2
import numpy as np

class chesspiece():
    def __init__(self) -> None:
        self.circles = None
        self.black_circles = []
        self.red_circles = []
        
        self.param1 = 0
        self.param2 = 0
        self.minRadius = 0
        self.maxRadius = 0
        self.red_threshold = 0
        self.low_h = 0
        self.low_s = 0
        self.low_v = 0
        self.high_h = 0
        self.high_s = 0
        self.high_v = 0

        self.upper_edge = 300
        self.lower_edge = 1045

    def load_chesspiece_values(self):
        try:
            with open('chesspiece_config.txt', 'r') as file:
                values = file.read().split(',')
                self.param1, self.param2, self.minRadius, self.maxRadius, self.red_threshold, self.low_h, self.low_s, self.low_v, self.high_h, self.high_s, self.high_v, self.upper_edge, self.lower_edge = [int(v) for v in values]
        
        except FileNotFoundError:
            return [88,20,10,16,44,124,11,171,255,255,255,300,1045]  # 默认值

    def count_red_pixels(self, img, x, y, radius):
        """计算圆内部的红色像素数量"""
        mask = np.zeros(img.shape[:2], dtype="uint8")
        cv2.circle(mask, (x, y), radius, 255, -1)
        masked = cv2.bitwise_and(img, img, mask=mask)
        # 定义红色的阈值，HSV颜色空间中的红色
        lower_red = np.array([self.low_h, self.low_s, self.low_v])
        upper_red = np.array([self.high_h, self.high_s, self.high_v])
        red_mask = cv2.inRange(cv2.cvtColor(masked, cv2.COLOR_BGR2HSV), lower_red, upper_red)

        return cv2.countNonZero(red_mask)

    def detect_circles(self, img):
        self.black_circles = []  # 清空黑色圆列表
        self.red_circles = []    # 清空红色圆列表
        roi = img[self.upper_edge: self.lower_edge, :]
        roi = cv2.resize(roi, (roi.shape[1]//2, roi.shape[0]//2))
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        self.circles = cv2.HoughCircles(gray_roi, cv2.HOUGH_GRADIENT, 1, 20, param1=self.param1, param2=self.param2, minRadius=self.minRadius, maxRadius=self.maxRadius)
        if self.circles is not None:
            self.circles = np.round(self.circles[0, :]).astype("int")
            for (x, y, r) in self.circles:
                num_red_pixels = self.count_red_pixels(roi, x, y, r)
                if num_red_pixels > self.red_threshold:
                    self.red_circles.append((x*2, y*2+self.upper_edge, r*2))
                else:
                    self.black_circles.append((x*2, y*2+self.upper_edge, r*2))

    def draw_circles(self, img):
        
        if self.red_circles:
            for x, y, r in self.red_circles:
                cv2.circle(img, (x, y), 1, (255, 0, 0), 3)
                cv2.circle(img, (x, y), r, (255,0,0), 1)
        if self.black_circles:
            for x, y, r in self.black_circles:
                cv2.circle(img, (x, y), 1, (0, 255, 0), 3)
                cv2.circle(img, (x, y), r, (0,255,0), 1)
        return img

    def save_slider_values(self):
        with open('./chesspiece_config.txt', 'w') as file:
            file.write(f'{self.param1},{self.param2},{self.minRadius},{self.maxRadius},{self.red_threshold},{self.low_h},{self.low_s},{self.low_v},{self.high_h},{self.high_s},{self.high_v},{self.upper_edge},{self.lower_edge}')
            print('chesspiece config saved')

if __name__ == '__main__':
    cp = chesspiece()
    cp.load_chesspiece_values()
    
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

    cv2.namedWindow('circle_Sliders')
    cv2.createTrackbar('Param1', 'circle_Sliders', cp.param1, 300, lambda x: None)
    cv2.createTrackbar('Param2', 'circle_Sliders', cp.param2, 300, lambda x: None)
    cv2.createTrackbar('Min Radius', 'circle_Sliders', cp.minRadius, 30, lambda x: None)
    cv2.createTrackbar('Max Radius', 'circle_Sliders', cp.maxRadius, 50, lambda x: None)
    cv2.createTrackbar('Red Threshold', 'circle_Sliders', cp.red_threshold, 1000, lambda x: None)
    cv2.createTrackbar('Upper Edge', 'circle_Sliders', cp.upper_edge, 1280, lambda x: None)  # 新增红色像素阈值滑块
    cv2.createTrackbar('Lower Edge', 'circle_Sliders', cp.lower_edge, 1280, lambda x: None)  # 新增红色像素阈值滑块

    # 创建一个窗口
    cv2.namedWindow('hsv_Sliders')

    # 创建滑块，用于调整红色的HSV阈值
    cv2.createTrackbar('Low H', 'hsv_Sliders', cp.low_h, 255, lambda x: None)
    cv2.createTrackbar('High H', 'hsv_Sliders', cp.high_h, 255, lambda x: None)
    cv2.createTrackbar('Low S', 'hsv_Sliders', cp.low_s, 255, lambda x: None)
    cv2.createTrackbar('High S', 'hsv_Sliders', cp.high_s, 255, lambda x: None)
    cv2.createTrackbar('Low V', 'hsv_Sliders', cp.low_v, 255, lambda x: None)
    cv2.createTrackbar('High V', 'hsv_Sliders', cp.high_v, 255, lambda x: None)

    while True:
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        if ret:
            cp.param1 = cv2.getTrackbarPos('Param1', 'circle_Sliders')
            cp.param2 = cv2.getTrackbarPos('Param2', 'circle_Sliders')
            cp.minRadius = cv2.getTrackbarPos('Min Radius', 'circle_Sliders')
            cp.maxRadius = cv2.getTrackbarPos('Max Radius', 'circle_Sliders')
            cp.red_threshold = cv2.getTrackbarPos('Red Threshold', 'circle_Sliders')  # 获取红色像素阈值
            cp.upper_edge = cv2.getTrackbarPos('Upper Edge', 'circle_Sliders')  # 获取红色像素阈值
            cp.lower_edge = cv2.getTrackbarPos('Lower Edge', 'circle_Sliders')  # 获取红色像素阈值
            cp.detect_circles(frame)

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cp.low_h = cv2.getTrackbarPos('Low H', 'hsv_Sliders')
            cp.high_h = cv2.getTrackbarPos('High H', 'hsv_Sliders')
            cp.low_s = cv2.getTrackbarPos('Low S', 'hsv_Sliders')
            cp.high_s = cv2.getTrackbarPos('High S', 'hsv_Sliders')
            cp.low_v = cv2.getTrackbarPos('Low V', 'hsv_Sliders')
            cp.high_v = cv2.getTrackbarPos('High V', 'hsv_Sliders')
            lower_red = np.array([cp.low_h, cp.low_s, cp.low_v])
            upper_red = np.array([cp.high_h, cp.high_s, cp.high_v])
            red_mask = cv2.inRange(hsv, lower_red, upper_red)

            cv2.line(frame, (0,cp.upper_edge), (960-1, cp.upper_edge-1), (0,0,255), 1)
            cv2.line(frame, (0, cp.lower_edge), (960-1, cp.lower_edge-1), (0,0,255), 1)
            cv2.imshow('hsv_Sliders', cv2.resize(red_mask, (300, 480)))
            cv2.imshow('frame', cv2.resize(cp.draw_circles(frame), (400, 640)))

        if cv2.waitKey(1) == ord('q'):
            cp.save_slider_values()
            break

    cap.release()
    cv2.destroyAllWindows()

