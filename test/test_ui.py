import random
import time
import threading
import cv2

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
                

def get_changes(changes):
    former_id = None
    current_id = None
    for change in changes:
        (i, j), old, new = change
        if old == 'r' and new == 'b':
            current_id = (i, j)
        elif old == 'b' and new == 'r':
            current_id = (i, j)
        if old != '.' and new == '.':
            # print(f"元素 '{old}' 从位置 ({i}, {j}) 移动了")
            former_id = (i, j)
        elif old == '.' and new != '.':
            # print(f"元素 '{new}' 出现在新位置 ({i}, {j})")
            current_id = (i, j)

    return former_id, current_id

def find_changes(former, current):
    changes = []
    for i in range(len(former)):
        for j in range(len(former[i])):
            if former[i][j] != current[i][j]:
                changes.append(((i, j), former[i][j], current[i][j]))
    return changes

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


def write_data(data):
    # 写入命名管道
    with open('/tmp/mypipe', 'w') as pipe:
        pipe.write(data)

def clear_pipes():
    with open('/tmp/mypipe', 'w') as pipe1:
        pipe1.write('')
    with open('/tmp/mypipe1', 'w') as pipe2:
        pipe2.write('')
    with open('/tmp/mypipe2', 'w') as pipe3:
        pipe3.write('')

class ui_comm:
    def __init__(self):
        self.bp_mode = 0 # 0: 下一步模式，1: 上一步模式
        self.fen = ''
        self.gpt_message = ''
        self.last_bp = ''
        self.next_bp = ''
        clear_pipes()

    def handle_req(self):
        tmp_msg = ''
        # 从命名管道读取数据
        while True:
            try:
                with open('/tmp/mypipe1', 'r') as pipe:
                    data = pipe.read()
                    if data:
                        if tmp_msg is None or tmp_msg != data:
                            if data.startswith('bestpoint'):
                                self.bp_mode = 0
                                print("bp mode change to 0")
                                self.fen = self.fen.split(' ', 1)[0] + ' ' + self.next_bp
                                write_data(self.fen)
                            elif data.startswith('analysis'):
                                self.bp_mode = 1
                                print("bp mode change to 1")
                                self.fen = self.fen.split(' ', 1)[0] + ' ' + self.last_bp
                                write_data(self.fen)
                            elif data.startswith('message'):
                                print("send gpt message")
                                with open('/tmp/mypipe2', 'r') as pipe1:
                                    pipe1.write(self.gpt_message)
                            tmp_msg = data

                time.sleep(1)
            except OSError as e:
                print(f"error: {e}")
                time.sleep(1)

    def sendto_ui(self):
        if self.bp_mode == 0:
            self.fen += " " + self.next_bp
        elif self.bp_mode == 1:
            self.fen += " " + self.last_bp
        print(f"sendd to ui: {self.fen}")
        write_data(ui.fen)

msg = [
    "1一二三四五六七八九十",
    "2一二三四五六七八九十一二三四五六七八九十",
    "3一二三四五六七八九十",
    "4一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十",
    "5一二三四五六七八九十",
    "6一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十",
    "7一二三四五六七八九十",
    "8一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十",
    "9一二三四五六七八九十",
]

former_board = []
board_idx = 1
former_board = board1_list[0]

best_mv_list = ['6656', '3242', '9172', '0010', '7737', '1013', '9776', '0122']

if __name__ == '__main__':
    ui = ui_comm()

    uireq_thread = threading.Thread(target=ui.handle_req)
    uireq_thread.setDaemon(True)
    uireq_thread.start()

    while True:
        img = cv2.imread('./test.png') 
        cv2.imshow('img', img)
        if cv2.waitKey(30) == ord('q'):
            break
        elif cv2.waitKey(30) == ord('s'):
            ui.gpt_message = msg[board_idx]
            board = board1_list[board_idx]
            ui.fen = board_to_fen(board)
            ui.next_bp = best_mv_list[board_idx]
            ui.last_bp = best_mv_list[board_idx-1]

            ui.sendto_ui()
            former_board = board
            board_idx += 1


    write_data("")
