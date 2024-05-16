# 初始化棋盘数据结构
def initialize_chess_board():
    # 定义棋盘的大小
    rows, cols = 10, 9
    # 初始化棋盘列表
    chess_board = [[{'kind': '', 'color': '',} for _ in range(cols)] for _ in range(rows)]

    # 赋值棋子的种类和颜色，小写为黑方，大写为红方
    # 黑方
    placements = {
        (0, 0): ('r', 'black'), (0, 1): ('n', 'black'), (0, 2): ('b', 'black'),
        (0, 3): ('a', 'black'), (0, 4): ('k', 'black'), (0, 5): ('a', 'black'),
        (0, 6): ('b', 'black'), (0, 7): ('n', 'black'), (0, 8): ('r', 'black'),
        (2, 1): ('c', 'black'), (2, 7): ('c', 'black'),
        (3, 0): ('p', 'black'), (3, 2): ('p', 'black'), (3, 4): ('p', 'black'),
        (3, 6): ('p', 'black'), (3, 8): ('p', 'black'),
        # 红方
        (9, 0): ('R', 'red'), (9, 1): ('N', 'red'), (9, 2): ('B', 'red'),
        (9, 3): ('A', 'red'), (9, 4): ('K', 'red'), (9, 5): ('A', 'red'),
        (9, 6): ('B', 'red'), (9, 7): ('N', 'red'), (9, 8): ('R', 'red'),
        (7, 1): ('C', 'red'), (7, 7): ('C', 'red'),
        (6, 0): ('P', 'red'), (6, 2): ('P', 'red'), (6, 4): ('P', 'red'),
        (6, 6): ('P', 'red'), (6, 8): ('P', 'red')
    }

    # 将棋子放置到棋盘上
    for pos, (kind, _) in placements.items():
        i, j = pos
        chess_board[i][j]['kind'] = kind

    return chess_board


# 打印棋盘当前的状态（只显示棋子的种类）
def print_chess_board(board):
    for row in board:
        print('  '.join([cell['kind'] if cell['kind'] else '.' for cell in row]))

def count_pieces(chess_board):
    count = 0
    # 遍历棋盘的每一行和每一列
    for row in chess_board:
        for cell in row:
            if cell['color']:  # 检查棋子种类字段是否非空
                count += 1
    return count

# 创建棋盘并打印
chess_board = initialize_chess_board()

# 使用之前定义的棋盘来计算棋子总数
total_pieces = count_pieces(chess_board)
print(f"当前棋盘上的棋子总数为: {total_pieces}")


# 执行打印棋盘
print_chess_board(chess_board)
