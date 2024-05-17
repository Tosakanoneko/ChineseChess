import cv2
from qipan01 import *
from qizi_class import chesspiece
import time
from ai2 import XiangQiAI


if __name__ == '__main__':
    # 初始化摄像头
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    # 创建一个窗口
    cv2.namedWindow('Chessboard and Circle Detector')
    
    cb = chessboard()
    cb.load_slider_values() 
    cp = chesspiece()
    cp.load_chesspiece_values()

    last_list = []
    current_list = []
    temp_list = []

    change_intval = 5
    count_mark = False
    change_mark = False
    start_time = None

    turn_count = 0

    cb_mode = 'start'
    if cb_mode == 'start':
        print_board(start_board)
        print('------------------------------------')
        cv2.imshow('board', render_chess_board(start_board))

    xq_ai = XiangQiAI()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = cb.roi_cut(frame)
        cv2.imshow('roi', roi)
        cp.detect_circles(roi)
        cp.red_circles = cb.roi2ori(cp.red_circles)
        cp.black_circles = cb.roi2ori(cp.black_circles)
        frame = cb.get_chesspiece_point(frame, cp.red_circles, cp.black_circles)
        # print(cb.count_pieces())
        color_cb = cb.get_chess_board()
        if not all(all(element == '.' for element in sublist) for sublist in color_cb):
            if not last_list:
                last_list = color_cb
            else:
                if change_mark:
                    if color_cb == temp_list:
                        if not count_mark:
                            start_time = time.time()
                            count_mark = True
                        else:
                            last_time = time.time() - start_time
                            if last_time > change_intval:
                                current_list = color_cb
                                changes = find_changes(last_list, current_list)
                                if changes:
                                    former_id, current_id, next_turn, eat_mark, mv_str = get_changes(changes)
                                    start_board[current_id[0]][current_id[1]] = start_board[former_id[0]][former_id[1]]
                                    start_board[former_id[0]][former_id[1]] = '.'
                                    print_board(start_board)
                                    cv2.imshow('board', render_chess_board(start_board))
                                    turn_count += 1
                                    ai_cmd = board_to_fen(start_board, next_turn, turn_count, eat_mark, mv_str, 0)
                                    print("AI_CMD: ", ai_cmd)
                                    xq_ai.add_move(ai_cmd)
                                    # try:
                                    xq_ai.receive_output_non_blocking()
                                    # finally:
                                    #     # 无论如何都确保关闭引擎
                                    #     xq_ai.send_command("quit")

                                    print('------------------------------------')
                                last_list = color_cb
                                count_mark = False
                                change_mark = False
                                temp_list = []
                                start_time = None
                    else:
                        temp_list = color_cb
                        count_mark = False 

                elif color_cb != last_list:
                    temp_list = color_cb
                    change_mark = True


        frame_resize = cv2.resize(frame, (640, 960))
        cv2.imshow('Chessboard and Circle Detector', frame_resize)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cb.save_slider_values()
    cap.release()
    cv2.destroyAllWindows()
