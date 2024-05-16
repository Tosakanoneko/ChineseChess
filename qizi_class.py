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

    def load_chesspiece_values(self):
        try:
            with open('chesspiece_config.txt', 'r') as file:
                values = file.read().split(',')
                # 30,30,17,25,31
                # 255,25,24,35,60
                self.param1, self.param2, self.minRadius, self.maxRadius, self.red_threshold = [int(v) for v in values]
        
        except FileNotFoundError:
            return [30, 30, 17, 25, 11]  # 默认值

    def merge_circles(self):
        if self.circles is None:
            return None
        self.circles = np.uint16(np.around(self.circles))
        filtered_circles = []
        merged = set()
        for i in range(len(self.circles[0])):
            if i in merged:
                continue
            x1, y1, r1 = self.circles[0][i]
            center1 = np.array([x1, y1])
            radius1 = r1
            merge_count = 1
            for j in range(i + 1, len(self.circles[0])):
                if j in merged:
                    continue
                x2, y2, r2 = self.circles[0][j]
                center2 = np.array([x2, y2])
                if np.linalg.norm(center1 - center2) < 15:
                    center1 = (center1 * merge_count + center2) / (merge_count + 1)
                    radius1 = (radius1 * merge_count + r2) / (merge_count + 1)
                    merge_count += 1
                    merged.add(j)
            filtered_circles.append((int(center1[0]), int(center1[1]), int(radius1)))
        return filtered_circles

    def count_red_pixels(self, img, x, y, radius):
        """计算圆内部的红色像素数量"""
        mask = np.zeros(img.shape[:2], dtype="uint8")
        cv2.circle(mask, (x, y), radius, 255, -1)
        masked = cv2.bitwise_and(img, img, mask=mask)
        # 定义红色的阈值，HSV颜色空间中的红色
        lower_red = np.array([119, 15, 140]) #[80, 33, 97]、[127, 115, 0]
        upper_red = np.array([255, 146, 255])#[179, 255, 255]、[255, 255, 255]
        red_mask = cv2.inRange(cv2.cvtColor(masked, cv2.COLOR_BGR2HSV), lower_red, upper_red)

        return cv2.countNonZero(red_mask)

    def detect_circles(self, img):
        self.black_circles = []  # 清空黑色圆列表
        self.red_circles = []    # 清空红色圆列表
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (9, 9), 2)
        # gray = cv2.equalizeHist(gray)
        self.circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 15, param1=self.param1, param2=self.param2, minRadius=self.minRadius, maxRadius=self.maxRadius)
        if self.circles is not None:
            self.circles = self.merge_circles()
        if self.circles:
            for x, y, r in self.circles:
                num_red_pixels = self.count_red_pixels(img, x, y, r)
                if num_red_pixels > self.red_threshold:
                    self.red_circles.append((x, y, r))
                else:
                    self.black_circles.append((x, y, r))

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

if __name__ == '__main__':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cp = chesspiece()
    cp.load_chesspiece_values()

    while True:
        ret, frame = cap.read()
        if ret:
            cp.detect_circles(frame)
            frame = cp.draw_circles(frame)
            cv2.imshow('detect', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
