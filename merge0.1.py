import cv2
import cchess
from qipan01 import *
from qizi_class import chesspiece
import time
from ai2 import XiangQiAI
from manipulator import *
import threading
from ui import *
from web import *
from model.hand_det import *

def handle_gpt_and_ui_comm(gpt, ui, ai):
    while True:
        if gpt.SendToUI_mark:
            ui.gpt_message = gpt.gpt_message
            gpt.SendToUI_mark = False
        if ui.set_diff:
            ai.send_command(ui.ai_diff)
            print("发送ai难度: ", ui.ai_diff)
        time.sleep(1)



if __name__ == '__main__':
# def main():
    # 初始化摄像头
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    # 创建一个窗口
    cv2.namedWindow('Chessboard and Circle Detector')
    
    cb = chessboard()
    cb.load_slider_values() 
    cp = chesspiece()
    cp.load_chesspiece_values()

    xq_ai = XiangQiAI()
    jxb = Manipulator()
    gpt = CC_GPT()
    ui = ui_comm()
    hand_det = hand_detector()
    web = web_record()

    last_list = []
    current_list = []
    temp_list = []
    last_detect_board = []
    current_board = []
    next_MovedId = []
    next_ToMoveId = []
    last_MovedId = []
    last_ToMoveId = []
    before_illegal_board = []
    illegal_judge_board = None

    change_intval = 3
    count_mark = False
    change_mark = False
    start_time = None
    detect_mark = False
    detect_count = 0
    next_eat_mark = False
    legal_mark = True
    send_mark = False # 是否发送给机械臂

    best_pro_mv = ''
    best_mv = ''
    current_pro_mv = ''

    cb_mode = 'start'
    if cb_mode == 'start':
        print_board(start_board)
        print('------------------------------------------------------------------------')
        # cv2.imshow('board', render_chess_board(start_board))

    gpt_thread = threading.Thread(target=read_gpt, args=(gpt,))
    gpt_thread.setDaemon(True)
    gpt_thread.start()

    uireq_thread = threading.Thread(target=ui.handle_req)
    uireq_thread.setDaemon(True)
    uireq_thread.start()

    transmit_uigpt_thread = threading.Thread(target=handle_gpt_and_ui_comm, args=(gpt, ui, xq_ai))
    transmit_uigpt_thread.setDaemon(True)
    transmit_uigpt_thread.start()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_cp = frame.copy()
        hand_det.run_hand_detect_frame(frame)

        if jxb.action_finish and not hand_det.hand_detected:
        # if jxb.action_finish:
            cp.detect_circles(frame_cp)
            frame = cb.get_chesspiece_point(frame, cp.red_circles, cp.black_circles)
            color_cb = cb.get_chess_board()
            first_det_time = time.time()
            if not all(all(element == '.' for element in sublist) for sublist in color_cb):
                if cb_mode == 'auto' and not detect_mark:
                    detected_board = cb.scan_board(frame_cp)
                    if len(last_detect_board) == 0:
                        last_detect_board = detected_board
                    else:
                        if last_detect_board == detected_board:
                            detect_count += 1
                            if detect_count > 0:
                                detect_mark = True
                                print_board(detected_board)
                                ui.fen = board_to_fen(detected_board)
                                ui.sendto_ui(first=True)
                                current_board = detected_board
                                cb.former_board = detected_board
                                cv2.imshow("board", cv2.resize(render_chess_board(current_board), (384, 480)))
                                print("扫描时间: ", time.time() - first_det_time)
                        else:
                            detect_count = 0
                    continue
                elif cb_mode == 'start' and not detect_mark:
                    detected_board = start_board
                    current_board = detected_board
                    cb.former_board = detected_board
                    ui.fen = board_to_fen(detected_board)
                    ui.sendto_ui(first=True)
                    cv2.imshow("board", cv2.resize(render_chess_board(current_board), (384, 480)))
                    detect_mark = True
                    continue

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
                                        former_id, current_id, next_turn, current_turn, last_eat_mark, mv_str = get_changes(changes)
                                        current_board[current_id[0]][current_id[1]] = current_board[former_id[0]][former_id[1]]
                                        current_board[former_id[0]][former_id[1]] = '.'
                                        print('------------------------------------------------------------------------')
                                        print_board(current_board)
                                        print('------------------------------------------------------------------------')
                                        rendered_cb = cv2.resize(render_chess_board(current_board), (384, 480))
                                        cv2.imshow('board', rendered_cb)

                                        # 非法判断
                                        if not legal_mark:
                                            if current_board == before_illegal_board:
                                                print("复原成功")
                                                legal_mark = True
                                                before_illegal_board = []
                                                ui.send_illegal_mark = False
                                                judge_fen = board_to_fen(current_board)
                                                illegal_judge_board = cchess.Board(judge_fen + ' ' + 'w')
                                            last_list = color_cb
                                            count_mark = False
                                            change_mark = False
                                            temp_list = []
                                            start_time = None
                                            continue
                                        else:
                                            ui.send_illegal_mark = False

                                        if next_turn == '红方':
                                            judge_fen = board_to_fen(current_board)
                                            illegal_judge_board = cchess.Board(judge_fen + ' ' + 'w')
                                        if current_turn == '红方' and illegal_judge_board is not None:
                                            cchess_mv_str = mv_str[0] + str(int(mv_str[1])-1) + mv_str[2] + str(int(mv_str[3])-1)
                                            legal_mark = illegal_judge_board.is_legal(cchess.Move.from_uci(cchess_mv_str))
                                            if not legal_mark:
                                                print("判断到非法行棋:", mv_str)
                                                ui.send_illegal_mark = True
                                                before_illegal_board = cb.former_board

                                        if legal_mark:
                                            ai_cmd = mv_str
                                            # print(f"{current_turn}移动: ", ai_cmd)
                                            xq_ai.add_move(ai_cmd)
                                            ai_output = xq_ai.receive_output_non_blocking()
                                            if ai_output.startswith("bestmove"):
                                                best_mv = ai_output[len('bestmove '):]
                                                # print(f"best_mv: ", best_mv)
                                                send_mark = True
                                            # print('------------------------------------')

                                            next_MovedId, next_ToMoveId = inverse_map_coordinates(best_mv)
                                            if current_board[next_ToMoveId[0]][next_ToMoveId[1]] != '.':
                                                next_eat_mark = True
                                            else:
                                                next_eat_mark = False

                                            if len(cb.last_best_mv) == 0:
                                                cb.last_best_mv = best_mv
                                            else:
                                                # print("last_best_mv: ", cb.last_best_mv)
                                                cb.best_mv_id_former, cb.best_mv_id_after = inverse_map_coordinates(cb.last_best_mv)

                                            current_pro_mv = cb.cvt_pro_mv(current_board, former_id, current_id)
                                            if current_turn == "红方":
                                                # print("红方行棋：", current_pro_mv)
                                                print("红方行棋：", former_id, current_id)
                                            else:
                                                # print("黑方行棋：", current_pro_mv)
                                                print("黑方行棋：", former_id, current_id)

                                            # 发送命令给gpt
                                            if cb.best_mv_id_former and cb.best_mv_id_after is not None:
                                                cb.gen_best_board_usr()
                                                best_pro_mv = cb.cvt_pro_mv(cb.best_board_usr, cb.best_mv_id_former, cb.best_mv_id_after)
                                            if current_pro_mv and best_pro_mv is not None:
                                                if current_turn == "红方":
                                                    if cb.best_mv_id_former and cb.best_mv_id_after is not None:
                                                        # print("红方最佳行棋：", best_pro_mv)
                                                        print("红方最佳行棋：", cb.best_mv_id_former, cb.best_mv_id_after)
                                                        # write_data(gen_ui_data(current_board, cb.best_mv_id_former, cb.best_mv_id_after), pipe_path="./chessboard/mypipe")
                                                        gpt.set_chat_msg(current_pro_mv, best_pro_mv, current_turn)
                                                else:
                                                    gpt.set_chat_msg(current_pro_mv, '', current_turn)

                                            # 设置ui发送信息
                                            ui.fen = board_to_fen(current_board)
                                            if len(last_MovedId) == 0:
                                                last_MovedId, last_ToMoveId = next_MovedId, next_ToMoveId
                                            else:
                                                ui.last_bp = f"{last_MovedId[0]}{last_MovedId[1]}{last_ToMoveId[0]}{last_ToMoveId[1]}"
                                            ui.next_bp = f"{next_MovedId[0]}{next_MovedId[1]}{next_ToMoveId[0]}{next_ToMoveId[1]}"
                                            ui.sendto_ui()
                                            print("next_turn:", next_turn)
                                            if next_turn == '红方':
                                                ui.send_remind = True

                                            # 发送命令给机械臂
                                            if current_turn == '红方' and send_mark is True:
                                                print(f"MovedId: {next_MovedId}")
                                                print(f"ToMoveId: {next_ToMoveId}")
                                                jxb.send_cmd(next_eat_mark, next_ToMoveId, next_MovedId)
                                                send_mark = False

                                            # web参数更新
                                            web.update_record(mv_str)

                                            cb.former_board = copy.deepcopy(current_board)
                                            cb.last_best_mv = best_mv
                                            last_MovedId, last_ToMoveId = next_MovedId, next_ToMoveId

                                    # 标志位清零
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

        if hand_det.hand_detected:
            cv2.putText(frame, "hand detected", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) , 2, cv2.LINE_AA)
        frame_resize = cv2.resize(frame, (320, 480))
        cv2.imshow('Chessboard and Circle Detector', frame_resize)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    web.write_to_txt()
    write_data("")
    cap.release()
    cv2.destroyAllWindows()
