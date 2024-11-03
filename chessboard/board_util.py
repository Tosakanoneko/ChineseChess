import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os
import sys
sys.path.append('..')
from gpt import *
# from ai2 import *
import re
# 定义颜色
colors = {
    'r': (0, 0, 0), 'n': (0, 0, 0), 'b': (0, 0, 0), 'a': (0, 0, 0), 'k': (0, 0, 0), 'c': (0, 0, 0), 'p': (0, 0, 0),
    'R': (0, 0, 255), 'N': (0, 0, 255), 'B': (0, 0, 255), 'A': (0, 0, 255), 'K': (0, 0, 255), 'C': (0, 0, 255), 'P': (0, 0, 255)
}

# 定义棋子的中文字符
chinese_pieces = {
    'r': '車', 'n': '馬', 'b': '象', 'a': '士', 'k': '将', 'c': '炮', 'p': '卒',
    'R': '車', 'N': '馬', 'B': '相', 'A': '仕', 'K': '帥', 'C': '炮', 'P': '兵'
}
# chinese_pieces = {
#     'r': '车', 'n': '马', 'b': '象', 'a': '士', 'k': '将', 'c': '炮', 'p': '卒',
#     'R': '车', 'N': '马', 'B': '相', 'A': '仕', 'K': '帅', 'C': '炮', 'P': '兵'
# }

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

dic_CHN2ENG = {
    'bing': 'P',
    'red_shi': 'A',
    'black_shi': 'a',
    'red_xiang': 'B',
    'black_xiang': 'b',
    'jiang': 'k',
    'red_ju': 'R',
    'black_ju': 'r',
    'red_ma': 'N',
    'black_ma': 'n',
    'red_pao': 'C',
    'black_pao': 'c',
    'shuai': 'K',
    'zu': 'p'
}
dic_NUM2ENG = {
    0: 'P', 
    1: 'r', 
    2: 'n', 
    3: 'c', 
    4: 'a', 
    5: 'b', 
    6: 'k', 
    7: 'R', 
    8: 'N', 
    9: 'C', 
    10: 'A',
    11: 'B',
    12: 'K',
    13: 'p'
}
dic_NUM2CHN = {
    0: 'bing', 
    1: 'black_shi', 
    2: 'black_xiang', 
    3: 'jiang', 
    4: 'ju', 
    5: 'ma', 
    6: 'pao', 
    7: 'red_shi', 
    8: 'red_xiang', 
    9: 'shuai', 
    10: 'zu'
}


board1_1 = [
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
board1_2 = [
    ['r', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', 'c', '.', '.', '.', '.', '.', 'c', '.'],
    ['p', '.', 'p', '.', 'p', '.', 'p', '.', 'p'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'P', '.', '.'],
    ['P', '.', 'P', '.', 'P', '.', '.', '.', 'P'],
    ['.', 'C', '.', '.', '.', '.', '.', 'C', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['R', 'N', 'B', 'A', 'K', 'A', 'B', 'N', 'R']
]
board1_3 = [
    ['r', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', 'c', '.', '.', '.', '.', '.', 'c', '.'],
    ['p', '.', '.', '.', 'p', '.', 'p', '.', 'p'],
    ['.', '.', 'p', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'P', '.', '.'],
    ['P', '.', 'P', '.', 'P', '.', '.', '.', 'P'],
    ['.', 'C', '.', '.', '.', '.', '.', 'C', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['R', 'N', 'B', 'A', 'K', 'A', 'B', 'N', 'R']
]
board1_4 = [
    ['r', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', 'c', '.', '.', '.', '.', '.', 'c', '.'],
    ['p', '.', '.', '.', 'p', '.', 'p', '.', 'p'],
    ['.', '.', 'p', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'P', '.', '.'],
    ['P', '.', 'P', '.', 'P', '.', '.', '.', 'P'],
    ['.', 'C', 'N', '.', '.', '.', '.', 'C', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['R', '.', 'B', 'A', 'K', 'A', 'B', 'N', 'R']
]
board1_5 = [
    ['.', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
    ['r', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', 'c', '.', '.', '.', '.', '.', 'c', '.'],
    ['p', '.', '.', '.', 'p', '.', 'p', '.', 'p'],
    ['.', '.', 'p', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'P', '.', '.'],
    ['P', '.', 'P', '.', 'P', '.', '.', '.', 'P'],
    ['.', 'C', 'N', '.', '.', '.', '.', 'C', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['R', '.', 'B', 'A', 'K', 'A', 'B', 'N', 'R']
]
board1_6 = [
    ['.', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
    ['r', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', 'c', '.', '.', '.', '.', '.', 'c', '.'],
    ['p', '.', '.', '.', 'p', '.', 'p', 'C', 'p'],
    ['.', '.', 'p', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'P', '.', '.'],
    ['P', '.', 'P', '.', 'P', '.', '.', '.', 'P'],
    ['.', 'C', 'N', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['R', '.', 'B', 'A', 'K', 'A', 'B', 'N', 'R']
]
board1_7 = [
    ['.', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
    ['.', '.', '.', 'r', '.', '.', '.', '.', '.'],
    ['.', 'c', '.', '.', '.', '.', '.', 'c', '.'],
    ['p', '.', '.', '.', 'p', '.', 'p', 'C', 'p'],
    ['.', '.', 'p', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'P', '.', '.'],
    ['P', '.', 'P', '.', 'P', '.', '.', '.', 'P'],
    ['.', 'C', 'N', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['R', '.', 'B', 'A', 'K', 'A', 'B', 'N', 'R']
]
board1_8 = [
    ['.', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
    ['.', '.', '.', 'r', '.', '.', '.', '.', '.'],
    ['.', 'c', '.', '.', '.', '.', '.', 'c', '.'],
    ['p', '.', '.', '.', 'p', '.', 'p', 'C', 'p'],
    ['.', '.', 'p', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'P', '.', '.'],
    ['P', '.', 'P', '.', 'P', '.', '.', '.', 'P'],
    ['.', 'C', 'N', '.', '.', '.', 'N', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['R', '.', 'B', 'A', 'K', 'A', 'B', '.', 'R']
]
board1_9 = [
    ['.', '.', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
    ['.', '.', '.', 'r', '.', '.', '.', '.', '.'],
    ['.', 'c', 'n', '.', '.', '.', '.', 'c', '.'],
    ['p', '.', '.', '.', 'p', '.', 'p', 'C', 'p'],
    ['.', '.', 'p', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'P', '.', '.'],
    ['P', '.', 'P', '.', 'P', '.', '.', '.', 'P'],
    ['.', 'C', 'N', '.', '.', '.', 'N', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['R', '.', 'B', 'A', 'K', 'A', 'B', '.', 'R']
]

board1_list = [board1_1, board1_2, board1_3, board1_4, board1_5, board1_6, board1_7, board1_8, board1_9]
bestmv_list = ['6656', '3242', '9172', '0010', '7737', '1013', '9776', '0122']

  
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
            next_turn = '红方'
        elif old == 'b' and new == 'r':
            current_id = (i, j)
            eat_mark = 'r'
            next_turn = '黑方'
        if old != '.' and new == '.':
            # print(f"元素 '{old}' 从位置 ({i}, {j}) 移动了")
            former_id = (i, j)
        elif old == '.' and new != '.':
            # print(f"元素 '{new}' 出现在新位置 ({i}, {j})")
            current_id = (i, j)
            if new == 'b':
                next_turn = '红方'
            else:
                next_turn = '黑方'

    mapped_former = map_coordinates(former_id[0], former_id[1])
    mapped_current = map_coordinates(current_id[0], current_id[1])
    # if eat_mark:
    #     # print(f"chessman {former_id} eat {current_id}")
    #     print(f"chessman {mapped_former} eat {mapped_current}")
    # else:
    #     # print(f"chessman move from {former_id} to {current_id}")
    #     print(f"chessman move from {mapped_former} to {mapped_current}")
    mv_str = f"{mapped_former}{mapped_current}"
    if next_turn == '黑方':
        current_turn = '红方'
    else:
        current_turn = '黑方'
    return former_id, current_id, next_turn, current_turn, eat_mark, mv_str

def map_coordinates(row, col):
    col_mapping = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    row_mapping = ['10', '9', '8', '7', '6', '5', '4', '3', '2', '1']
    
    if 0 <= row < len(row_mapping) and 0 <= col < len(col_mapping):
        return col_mapping[col] + row_mapping[row]
    else:
        raise ValueError("Invalid row or column index")
    
def inverse_map_coordinates(coordinate):
    # if len(coordinate) > 6:
    #     raise ValueError("Invalid coordinate format")
    parts = re.findall(r'[a-zA-Z]+|\d+', coordinate)
    inversed_id1 = []
    inversed_id2 = []
    col_mapping = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    row_mapping = ['10', '9', '8', '7', '6', '5', '4', '3', '2', '1']

    col_char1 = parts[0]
    row_str1 = parts[1]
    col_char2 = parts[2]
    row_str2 = parts[3]

    if col_char1 not in col_mapping or row_str1 not in row_mapping or col_char2 not in col_mapping or row_str2 not in row_mapping:
        raise ValueError("Invalid coordinate")

    inversed_id1.append(row_mapping.index(row_str1))
    inversed_id1.append(col_mapping.index(col_char1))
    inversed_id2.append(row_mapping.index(row_str2))
    inversed_id2.append(col_mapping.index(col_char2))

    return inversed_id1, inversed_id2

def board_to_fen_pro(board, turn, turn_count, eat_mark, mv_str, not_eat = 0):
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

def board_to_fen(board):
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

    return fen[:-1]

def fen_to_board(fen):
    # 去除末尾可能存在的'/'
    if fen.endswith('/'):
        fen = fen[:-1]
    
    # 分割成行
    rows = fen.split('/')
    
    # 初始化棋盘，假设棋盘是8x8的
    board = [['.' for _ in range(9)] for _ in range(10)]
    
    # 遍历每一行
    for i, row_fen in enumerate(rows):
        pos = 0  # 当前在棋盘上的位置
        for char in row_fen:
            if char.isdigit():
                # 如果是数字，则跳过相应数量的空格
                pos += int(char)
            else:
                # 否则，放置棋子
                board[i][pos] = char
                pos += 1
    
    return board

def gen_ui_data(board, id1, id2):
    fen = board_to_fen(board)
    fen += f' {id1[0]}{id1[1]}{id2[0]}{id2[1]}'
    return fen

def print_board(board):
    for row in board:
        print('  '.join(row))

def render_chess_board(board_state):


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
                text_y = (center[1] - text_height // 2) - 7

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

def axis_convert(chess_color, x_origin, x_final):
    if chess_color == "red":
        return 9-x_origin, 9-x_final
    else:
        return 1+x_origin, 1+x_final

def cvt_pro_mv(board, y_origin, x_origin, y_final, x_final):
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

def gen_best_board_usr(board, y_origin, x_origin, y_final, x_final):
    board[y_final][x_final] = board[y_origin][x_origin]
    board[y_origin][x_origin] = '.'
    return board


def write_data(data, pipe_path='./mypipe'):
    # 写入命名管道
    with open(pipe_path, 'w') as pipe:
        pipe.write(data)

# if __name__ == "__main__":
#     best_mv_id_former = None
#     best_mv_id_after = None
#     count = 0
#     former_board = []
#     last_best_mv = ''
#     xq_ai = XiangQiAI()
#     # gpt = CC_GPT()
#     for idx, board in enumerate(board1_list):
#         # fen = board_to_fen(board)
#         cv2.imshow("board", render_chess_board(board))
#         if len(former_board) == 0:
#             former_board = board
#         else:
#             current_turn = "红方" if count % 2 == 0 else "黑方"
#             print("current_turn: ", current_turn)
#             changes = find_changes(former_board, board)
#             former_id, current_id, _, _, _, mv_str = get_changes(changes)
#             pro_mv = cvt_pro_mv(board, int(former_id[0]), int(former_id[1]), int(current_id[0]), int(current_id[1]))
#             xq_ai.add_move(mv_str)
#             ai_output = xq_ai.receive_output_non_blocking()
#             if ai_output.startswith("bestmove"):
#                 best_mv = ai_output[len('bestmove '):]
#                 if len(last_best_mv) == 0:
#                     last_best_mv = best_mv
#                 else:
#                     best_mv_id_former, best_mv_id_after = inverse_map_coordinates(last_best_mv)
#             if best_mv_id_former and best_mv_id_after is not None:
#                 best_board_usr = gen_best_board_usr(former_board, int(best_mv_id_former[0]), int(best_mv_id_former[1]), int(best_mv_id_after[0]), int(best_mv_id_after[1]))
#                 best_pro_mv = cvt_pro_mv(best_board_usr, int(best_mv_id_former[0]), int(best_mv_id_former[1]), int(best_mv_id_after[0]), int(best_mv_id_after[1]))
#             if current_turn == "黑方":
#                 print("黑方行棋：", pro_mv)
#                 if best_mv_id_former and best_mv_id_after is not None:
#                     print("黑方最佳行棋：", best_pro_mv)
#                     # gpt.chat(pro_mv, best_pro_mv, current_turn)
#             else:
#                 print("红方行棋：", pro_mv)
#                 # gpt.chat(pro_mv, '', current_turn)
#             former_board = board
#             count += 1
#             last_best_mv = best_mv
#         if cv2.waitKey(0) == ord('c'):
#             continue
#         elif cv2.waitKey(0) == ord('q'):
#             break

#     write_data("")

# board = fen_to_board('4k3R/2N2n3/5N3/9/9/9/9/9/9/3K5')
# cv2.imshow('1', render_chess_board(board))
# cv2.waitKey(0)
