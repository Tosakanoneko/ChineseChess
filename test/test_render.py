import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def draw_chess_board(board_state):
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
                text_size = draw.textsize(chinese_pieces[piece], font=font)
                text_x = center[0] - text_size[0] // 2
                text_y = (center[1] - text_size[1] // 2) - 3
                draw.text((text_x, text_y), chinese_pieces[piece], font=font, fill=color)

    # 在第5行（索引为4）和第6行（索引为5）之间的第2、3列，第3、4列，第6、7列，第7、8列中分别绘制“楚”，“河”，“汉”，“界”
    chu_he_han_jie = ["楚", "河", "汉", "界"]
    positions = [(2, 4), (3, 4), (6, 4), (7, 4)]  # (col, row) 位置

    for (col, row), text in zip(positions, chu_he_han_jie):
        text_x = (col * square_size + border_size - draw.textsize(text, font=font)[0] // 2) - (border_size // 2)
        text_y = row * square_size + border_size + (square_size - draw.textsize(text, font=font)[1]) // 2
        draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    # 转换回OpenCV图像
    board = np.array(pil_img)

    return board

# 定义棋盘状态
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

# 绘制并显示棋盘
frame = draw_chess_board(start_board)
cv2.imshow('Rendered Chess Board', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
