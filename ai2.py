import subprocess
import os
import select
import time

class XiangQiAI():
    def __init__(self):
        engine_path = "./ai/fstockfishb"
        # 启动象棋引擎
        self.engine = subprocess.Popen(engine_path, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # 用于存储棋局的走子
        self.moves_history = []
        self.engine_initialize()

    def engine_initialize(self):
        # 初始化引擎
        self.send_command("uci")
        self.send_command("setoption name UCI_Variant value xiangqi")
        self.send_command("isready")

        # # 等待直到接收到 'readyok'
        # time.sleep(0.5)
        while not self.receive_output_non_blocking():
            time.sleep(0.1)

    def send_command(self, command):
        self.engine.stdin.write(command + '\n')
        self.engine.stdin.flush()

    # 添加走子到历史，并更新引擎状态
    def add_move(self, move):
        self.moves_history.append(move)
        moves_command = ' '.join(self.moves_history)
        self.send_command(f"position startpos moves {moves_command}")
        self.send_command("go depth 1")

    # 非阻塞方式获取引擎的输出并打印，返回是否接收到readyok
    def receive_output_non_blocking(self):
        while True:
            output = self.engine.stdout.readline().strip()
            if output == '':
                break
            elif output.lower() == 'readyok':
                return True
            elif output is None:
                break
            else:
                # print(output)
                if output.startswith("bestmove"):
                    return output
                
        return False

# 初始化引擎

# 添加走子
#add_move("e7e5")

if __name__ == '__main__':
    # 持续获取引擎的输出并打印
    xq_ai = XiangQiAI()
    xq_ai.add_move("a1a2")
    try:
        while True:
            xq_ai.receive_output_non_blocking()
            time.sleep(0.1)  # 等待一段时间再继续获取输出
    finally:
        # 无论如何都确保关闭引擎
        xq_ai.send_command("quit")
