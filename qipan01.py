import math
import collections
import copy
from chessboard.board_util import *
from detect_local.detect_rect import classify_piece
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

        self.best_mv_id_former = None
        self.best_mv_id_after = None
        self.former_board = []
        self.best_board_usr = []
        self.last_best_mv = ''

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
        for i in range(self.rows):
            for j in range(self.cols):
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
    
    def scan_board(self, frame):
        detected_board = []
        for j in range(10):  # 垂直方向10等分
            row = []
            for i in range(9):  # 水平方向9等分
                if self.points[i][j]['color'] is None:
                    row.append('.')
                    continue
                if self.points[i][j]['color'] == 'r':
                    x = self.red_stable_result[i][j][0]
                    y = self.red_stable_result[i][j][1]
                elif self.points[i][j]['color'] == 'b':
                    x = self.black_stable_result[i][j][0]
                    y = self.black_stable_result[i][j][1]
                piece = frame[max(0,y-48):y+48, max(0,x-48):x+48]
                # cv2.imwrite(f'./testimg/chess_piece{i}{j}.jpg', piece)
                detect_result = dic_NUM2ENG[classify_piece(piece)]
                # print(detect_result)
                row.append(detect_result)
            detected_board.append(row)
        return detected_board


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
        top_left_x = max(0, self.x_pos - 60)
        top_left_y = max(0, self.y_pos - 60)
        print(f"width {frame.shape[1]}")
        bottom_right_x = min(frame.shape[1], self.x_pos + self.width + 60)
        bottom_right_y = min(frame.shape[0], self.y_pos + self.height + 60)
        roi = frame[top_left_y:bottom_right_y,top_left_x:bottom_right_x]
        return roi

    def roi2ori(self, roi_point):
        ori_point = []
        for x, y, r in roi_point:
            adj_x = max(0, x + self.x_pos - 60)
            adj_y = max(0, y + self.y_pos - 60)
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
            color_cb.append(row)
        return color_cb

    def gen_best_board_usr(self):
        # print("-------------移动前-------------")
        # print_board(self.former_board)
        # print("-------------移动前-------------")
        self.best_board_usr = copy.deepcopy(self.former_board)
        self.best_board_usr[int(self.best_mv_id_after[0])][int(self.best_mv_id_after[1])] = self.best_board_usr[int(self.best_mv_id_former[0])][int(self.best_mv_id_former[1])]
        self.best_board_usr[int(self.best_mv_id_former[0])][int(self.best_mv_id_former[1])] = '.'
        # print("-------------best_board_usr-------------")
        # print_board(self.best_board_usr)
        # print("-------------best_board_usr-------------")
    
    def cvt_pro_mv(self, board, mv_id_former, mv_id_after):
        y_origin, x_origin = int(mv_id_former[0]), int(mv_id_former[1])
        print("y_origin: ", y_origin, "x_origin: ", x_origin)
        y_final, x_final = int(mv_id_after[0]), int(mv_id_after[1])
        print("y_final: ", y_final, "x_final: ", x_final)
        chess_word = board[y_final][x_final]
        chess_name = chinese_pieces[chess_word]
        chess_color = "red"
        if chess_word.islower():
            chess_color = "black"
        if chess_color == "red":
            if y_final < y_origin:
                movement = "进"
            elif y_final == y_origin:
                movement = "平"
            else:
                movement = "退"
            x_origin, x_final = axis_convert(chess_color, x_origin, x_final)
            if chess_word == 'N' or chess_word == 'B' or chess_word == 'A':
                expression = chess_name + str(x_origin) + movement + str(x_final)
            else:
                if movement == "进":
                    expression = chess_name + str(x_origin) + movement + str(y_origin-y_final)
                elif movement == "退":
                    expression = chess_name + str(x_origin) + movement + str(y_final - y_origin)
                else:
                    expression = chess_name + str(x_origin) + movement + str(x_final)
            return expression
        if chess_color == "black":
            if y_final > y_origin:
                movement = "进"
            elif y_final == y_origin:
                movement = "平"
            else:
                movement = "退"
            x_origin, x_final = axis_convert(chess_color, x_origin, x_final)
            if chess_word == 'n' or chess_word == 'b' or chess_word == 'a':
                expression = chess_name + str(x_origin) + movement + str(x_final)
            else:
                if movement == "进":
                    expression = chess_name + str(x_origin) + movement + str(y_final - y_origin)
                elif movement == "退":
                    expression = chess_name + str(x_origin) + movement + str(y_origin - y_final)
                else:
                    expression = chess_name + str(x_origin) + movement + str(x_final)
            return expression
  

# dic_NUM2ENG = {
#     0: 'p', 
#     1: 'a', 
#     2: 'b', 
#     3: 'k', 
#     4: 'r', 
#     5: 'n', 
#     6: 'c', 
#     7: 'A', 
#     8: 'B', 
#     9: 'K', 
#     10: 'P'
# }

if __name__ == '__main__':
    # 初始化摄像头
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
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
            break
        elif cv2.waitKey(1) & 0xFF == ord('s'):
            cb.scan_board(frame)

    cb.save_slider_values()
    cap.release()
    cv2.destroyAllWindows()
