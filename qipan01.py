import cv2
import math
import collections
import numpy as np
from PIL import Image, ImageDraw, ImageFont
# 创建滑块回调函数
def nothing(x):
    pass


class chessboard():
    def __init__(self):
        self.width = 0
        self.height = 0
        self.x_pos = 0
        self.y_pos = 0

        self.rows, self.cols, self.depth = 9, 10, 8
        self.default_data = {
            'kind': '',
            'color': '',
            'id': None,
            'axis': None
            }
        self.points = [[self.default_data.copy() for _ in range(self.cols)] for _ in range(self.rows)]

        # 稳定器初始化
        self.red_stable_list = [[[None for _ in range(self.depth)] for _ in range(self.cols)] for _ in range(self.rows)]
        self.red_stable_list_round = 0
        self.black_stable_list = [[[None for _ in range(self.depth)] for _ in range(self.cols)] for _ in range(self.rows)]
        self.black_stable_list_round = 0
        # 储存并更新每次识别出的稳定结果
        self.red_stable_result = None
        self.black_stable_result = None
        
        self.mode = 'load'

    def init_chessboard(self):
        self.load_slider_values()
        self.devide_points(self.x_pos, self.y_pos)

    def init_start_chessboard(self):
        pass

    def load_slider_values(self):
        try:
            with open('slider_config.txt', 'r') as file:
                values = file.read().split(',')
                self.width, self.height, self.x_pos, self.y_pos = [int(v) for v in values]
        except FileNotFoundError:
            self.width, self.height, self.x_pos, self.y_pos = 348, 364, 91, 118  # 默认值
        self.devide_points(self.x_pos, self.y_pos)

    def adjust_chessboard(self, frame):
        if self.mode == 'debug':
            self.width = cv2.getTrackbarPos('Width', 'Degug button')
            self.height = cv2.getTrackbarPos('Height', 'Degug button')
            self.x_pos = cv2.getTrackbarPos('X Position', 'Degug button')
            self.y_pos = cv2.getTrackbarPos('Y Position', 'Degug button')

        top_left_x = self.x_pos
        top_left_y = self.y_pos

        self.devide_points(top_left_x, top_left_y)
        return frame

    def devide_points(self, top_left_x, top_left_y):
        self.points = [[self.default_data.copy() for _ in range(self.cols)] for _ in range(self.rows)]
        step_x = self.width // 8
        step_y = self.height // 9
        for i in range(9):  # 水平方向9等分
            for j in range(10):  # 垂直方向10等分
                x = top_left_x + i * step_x
                y = top_left_y + j * step_y
                self.points[i][j]['axis'] = (x, y)
                self.points[i][j]['id'] = (i, j)

    def draw_grid_point(self, frame):
        for i in range(9):  # 水平方向9等分
            for j in range(10):  # 垂直方向10等分
                cv2.circle(frame, self.points[i][j]['axis'], 2, (0, 0, 255), -1)
        return frame

    def save_slider_values(self):
        with open('slider_config.txt', 'w') as file:
            file.write(f'{self.width},{self.height},{self.x_pos},{self.y_pos}')
            print('chessboard config saved')

    def find_closest_point(self, x, y):
        min_distance = float('inf')
        closest_point = None
        closest_id = None
        for i in range(9):  # 水平方向9等分
            for j in range(10):  # 垂直方向10等分
                distance = math.sqrt((self.points[i][j]['axis'][0] - x) ** 2 + (self.points[i][j]['axis'][1] - y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_id = (i, j)

        closest_point = self.points[closest_id[0]][closest_id[1]]

        return closest_point
    
    def get_chesspiece_point(self, frame, red_points, black_points):
        '''
        得出稳定的棋子列表。格式：9*10-(x,y)
        '''
        closest_red_points = []
        closest_black_points = []
        for x, y, _ in red_points:
            closest_point = self.find_closest_point(x, y)
            closest_red_points.append(closest_point)
        red_stable_result = self.upload_stabler(closest_red_points, 'red')
        if red_stable_result:
            self.red_stable_result = red_stable_result
        if self.red_stable_result:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.red_stable_result[i][j]:
                        self.points[i][j]['color'] = 'r'
                        x = self.red_stable_result[i][j][0]
                        y = self.red_stable_result[i][j][1]
                        cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)
                    else:
                        if self.black_stable_result and not self.black_stable_result[i][j]:
                            self.points[i][j]['color'] = None

        for x, y, _ in black_points:
            closest_point = self.find_closest_point(x, y)
            closest_black_points.append(closest_point)
        black_stable_result = self.upload_stabler(closest_black_points, 'black')
        if black_stable_result:
            self.black_stable_result = black_stable_result
        if self.black_stable_result:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.black_stable_result[i][j]:
                        self.points[i][j]['color'] = 'b'
                        x = self.black_stable_result[i][j][0]
                        y = self.black_stable_result[i][j][1]
                        cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
                    else:
                        if self.red_stable_result and not self.red_stable_result[i][j]:
                            self.points[i][j]['color'] = None
        return frame
    
    def upload_stabler(self, points, color):
        '''
        将每次识别的每个位置上的棋子信息上传至稳定器，每7帧进行统计并得出最有可能的结果
        '''
        if color == 'red':
            self.red_stable_list_round += 1
            for point in points:
                id = point['id']
                axis = point['axis']
                self.red_stable_list[id[0]][id[1]][self.red_stable_list_round - 1] = axis
            if self.red_stable_list_round == self.depth:
                counter_result = self.find_most_common_element(self.red_stable_list)
                self.red_stable_list_round = 0
                self.red_stable_list = [[[None for _ in range(self.depth)] for _ in range(self.cols)] for _ in range(self.rows)]
                return counter_result
            return None
        else:
            self.black_stable_list_round += 1
            for point in points:
                id = point['id']
                axis = point['axis']
                self.black_stable_list[id[0]][id[1]][self.black_stable_list_round - 1] = axis
            if self.black_stable_list_round == self.depth:
                counter_result = self.find_most_common_element(self.black_stable_list)
                self.black_stable_list = [[[None for _ in range(self.depth)] for _ in range(self.cols)] for _ in range(self.rows)]
                self.black_stable_list_round = 0

                return counter_result
            return None

    def find_most_common_element(self, matrix):
        # 将三维稳定器的结果进行统计并得出最可能的结果，形成9*10-(x,y)的列表
        most_common_list = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                # 提取当前行和列所有深度的元素
                elements = [matrix[i][j][k] for k in range(self.depth)]
                # 统计元素出现频率
                counter = collections.Counter(elements)
                # 找到出现频率最高的元素，包括None
                most_common = counter.most_common(1)[0][0]
                most_common_list[i][j] = most_common
        return most_common_list

    def roi_cut(self,frame):
        top_left_x = self.x_pos - 40
        top_left_y = self.y_pos - 60
        bottom_right_x = self.x_pos + self.width + 40
        bottom_right_y = self.y_pos + self.height + 60
        roi = frame[top_left_y:bottom_right_y,top_left_x:bottom_right_x]
        return roi

    def roi2ori(self, roi_point):
        ori_point = []
        for x, y, r in roi_point:
            adj_x = x + self.x_pos - 20
            adj_y = y + self.y_pos - 40
            ori_point.append((adj_x, adj_y, r))
        return ori_point
    
    def count_pieces(self):
        count = 0
        # 遍历棋盘的每一行和每一列
        for row in self.points:
            for cell in row:
                if cell['color']:  # 检查棋子种类字段是否非空
                    count += 1
        return count

    def get_chess_board(self):
        color_cb = []
        for j in range(self.cols):  # 遍历列
            row = []
            for i in range(self.rows):  # 遍历行
                cell = self.points[i][j]
                row.append(cell['color'] if cell['color'] else '.')
            # print(' '.join(row))
            color_cb.append(row)
        # for row in color_cb:
        #     print('  '.join(row))
        # print('-----------------------------------')
        return color_cb

def find_changes(former, current):
    changes = []
    for i in range(len(former)):
        for j in range(len(former[i])):
            if former[i][j] != current[i][j]:
                changes.append(((i, j), former[i][j], current[i][j]))
    return changes

# 打印变化的函数
def get_changes(changes):
    former_id = None
    current_id = None
    eat_mark = None
    for change in changes:
        (i, j), old, new = change
        if old == 'r' and new == 'b':
            current_id = (i, j)
            eat_mark = 'b'
            next_turn = 'w'
        elif old == 'b' and new == 'r':
            current_id = (i, j)
            eat_mark = 'r'
            next_turn = 'b'
        if old != '.' and new == '.':
            # print(f"元素 '{old}' 从位置 ({i}, {j}) 移动了")
            former_id = (i, j)
        elif old == '.' and new != '.':
            # print(f"元素 '{new}' 出现在新位置 ({i}, {j})")
            current_id = (i, j)
            if new == 'b':
                next_turn = 'w'
            else:
                next_turn = 'b'

    mapped_former = map_coordinates(former_id[0], former_id[1])
    mapped_current = map_coordinates(current_id[0], current_id[1])
    if eat_mark:
        # print(f"chessman {former_id} eat {current_id}")
        print(f"chessman {mapped_former} eat {mapped_current}")
    else:
        # print(f"chessman move from {former_id} to {current_id}")
        print(f"chessman move from {mapped_former} to {mapped_current}")
    mv_str = f"{mapped_former[0]}{mapped_former[1]}{mapped_current[0]}{mapped_current[1]}"
    return former_id, current_id, next_turn, eat_mark, mv_str

def map_coordinates(row, col):
    col_mapping = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    row_mapping = ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0']
    
    if 0 <= row < len(row_mapping) and 0 <= col < len(col_mapping):
        return col_mapping[col] + row_mapping[row]
    else:
        raise ValueError("Invalid row or column index")

def board_to_fen(board, turn, turn_count, eat_mark, mv_str, not_eat = 0):
    ai_cmd = ''
    if eat_mark:
        fen = ""
        for row in board:
            empty_count = 0
            for piece in row:
                if piece == '.':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += piece
            if empty_count > 0:
                fen += str(empty_count)
            fen += "/"
        fen = fen[:-1]
        fen += f' {turn} - - {not_eat} {turn_count}'
        ai_cmd = fen
    else:
        ai_cmd = mv_str
    return ai_cmd

def print_board(board):
    for row in board:
        print('  '.join(row))

def render_chess_board(board_state):
    # 定义颜色
    colors = {
        'r': (0, 0, 0), 'n': (0, 0, 0), 'b': (0, 0, 0), 'a': (0, 0, 0), 'k': (0, 0, 0), 'c': (0, 0, 0), 'p': (0, 0, 0),
        'R': (0, 0, 255), 'N': (0, 0, 255), 'B': (0, 0, 255), 'A': (0, 0, 255), 'K': (0, 0, 255), 'C': (0, 0, 255), 'P': (0, 0, 255)
    }

    # 定义棋子的中文字符
    chinese_pieces = {
        'r': '車', 'n': '馬', 'b': '象', 'a': '士', 'k': '将', 'c': '炮', 'p': '卒',
        'R': '車', 'N': '馬', 'B': '相', 'A': '仕', 'K': '帅', 'C': '炮', 'P': '兵'
    }

    # 定义棋盘大小
    rows, cols = 10, 9
    square_size = 60
    width, height = cols * square_size - square_size, rows * square_size - square_size

    # 创建带有边框的空白图像
    border_size = square_size
    board = np.ones((height + 2 * border_size, width + 2 * border_size, 3), dtype=np.uint8) * np.array([113, 170, 207], dtype=np.uint8)

    # 绘制棋盘网格线
    for i in range(rows):
        cv2.line(board, (border_size, i * square_size + border_size), (width + border_size, i * square_size + border_size), (0, 0, 0), 1)
    for j in range(cols):
        # 跳过第5和第6行之间区域的第2到第8列的列线
        if j in range(1, 8):
            cv2.line(board, (j * square_size + border_size, border_size), (j * square_size + border_size, 4 * square_size + border_size), (0, 0, 0), 1)
            cv2.line(board, (j * square_size + border_size, 5 * square_size + border_size), (j * square_size + border_size, height + border_size), (0, 0, 0), 1)
        else:
            cv2.line(board, (j * square_size + border_size, border_size), (j * square_size + border_size, height + border_size), (0, 0, 0), 1)

    # 绘制九宫格对角线
    cv2.line(board, (3 * square_size + border_size, border_size), (5 * square_size + border_size, 2 * square_size + border_size), (0, 0, 0), 1)
    cv2.line(board, (5 * square_size + border_size, border_size), (3 * square_size + border_size, 2 * square_size + border_size), (0, 0, 0), 1)
    cv2.line(board, (3 * square_size + border_size, 7 * square_size + border_size), (5 * square_size + border_size, 9 * square_size + border_size), (0, 0, 0), 1)
    cv2.line(board, (5 * square_size + border_size, 7 * square_size + border_size), (3 * square_size + border_size, 9 * square_size + border_size), (0, 0, 0), 1)

    # 绘制圆环和覆盖棋盘线条的圆
    for i in range(rows):
        for j in range(cols):
            piece = board_state[i][j]
            if piece != '.':
                center = (j * square_size + border_size, i * square_size + border_size)
                color = colors[piece]
                # 在圆内部覆盖棋盘线条
                cv2.circle(board, center, square_size // 2 - 5, (155, 189, 212), -1)
                # 绘制圆环
                cv2.circle(board, center, square_size // 2 - 5, color, 2)

    # 使用PIL来绘制汉字
    pil_img = Image.fromarray(board)
    draw = ImageDraw.Draw(pil_img)
    font = ImageFont.truetype("./font/SIMLI.TTF", 34)  # 使用黑体字体，字体大小40

    for i in range(rows):
        for j in range(cols):
            piece = board_state[i][j]
            if piece != '.':
                center = (j * square_size + border_size, i * square_size + border_size)
                color = colors[piece]
                text_bbox = draw.textbbox((0, 0), chinese_pieces[piece], font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = center[0] - text_width // 2
                text_y = (center[1] - text_height // 2) - 3

                draw.text((text_x, text_y), chinese_pieces[piece], font=font, fill=color)

    # 在第5行（索引为4）和第6行（索引为5）之间的第2、3列，第3、4列，第6、7列，第7、8列中分别绘制“楚”，“河”，“汉”，“界”
    chu_he_han_jie = ["楚", "河", "汉", "界"]
    positions = [(2, 4), (3, 4), (6, 4), (7, 4)]  # (col, row) 位置

    for (col, row), text in zip(positions, chu_he_han_jie):
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (col * square_size + border_size - text_width // 2) - (border_size // 2)
        text_y = (row * square_size + border_size + (square_size - text_height) // 2) - 5
        draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    # 转换回OpenCV图像
    board = np.array(pil_img)

    return board

start_board = [
    ['r', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', 'c', '.', '.', '.', '.', '.', 'c', '.'],
    ['p', '.', 'p', '.', 'p', '.', 'p', '.', 'p'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['P', '.', 'P', '.', 'P', '.', 'P', '.', 'P'],
    ['.', 'C', '.', '.', '.', '.', '.', 'C', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['R', 'N', 'B', 'A', 'K', 'A', 'B', 'N', 'R']
]

if __name__ == '__main__':
    # 初始化摄像头
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

    # 创建一个窗口
    cv2.namedWindow('Degug button')
    cv2.namedWindow('Chessboard Detector')
    cv2.resizeWindow('Chessboard Detector', 480, 640)
    cv2.resizeWindow('Degug button', 640, 320)
    cb = chessboard()
    cb.load_slider_values()
    cb.mode = 'debug'
    if cb.mode == 'debug':
        cv2.createTrackbar('Width', 'Degug button', cb.width, 1000, nothing)
        cv2.createTrackbar('Height', 'Degug button', cb.height, 1000, nothing)
        cv2.createTrackbar('X Position', 'Degug button', cb.x_pos, 1000, nothing)
        cv2.createTrackbar('Y Position', 'Degug button', cb.y_pos, 1000, nothing)

    while True:
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        if not ret:
            continue
        cb.adjust_chessboard(frame)

        frame = cb.draw_grid_point(frame)
        frame = cv2.resize(frame, (480, 640))
        cv2.imshow('Chessboard Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # axis = cb.points[3][3]['axis']
            # print("axis:", axis) #(296,239)
            # cv2.circle(frame, (int(axis[0]/2), int(axis[1]/2)), 2, (0, 255, 0), -1)
            
            # cv2.imshow('Chessboard Detector', frame)
            # cv2.waitKey(0)
            break

    cb.save_slider_values()
    cap.release()
    cv2.destroyAllWindows()
