import subprocess
import os
import time
import select
class XiangQiEngine:
    def __init__(self, engine_path):
        self.engine = subprocess.Popen(
            engine_path, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        self.moves = []  # 用于存储走子历史

    def send_command(self, command):
        self.engine.stdin.write(command + '\n')
        self.engine.stdin.flush()

    def receive_output_non_blocking(self, timeout=100):
        """非阻塞方式读取引擎输出，带有超时。"""
        end_time = time.time() + timeout
        while True:
            ready, _, _ = select.select([self.engine.stdout], [], [], timeout)
            if ready:
                output = self.engine.stdout.readline().strip()
                if output:
                    print(output)
                if output == 'readyok':
                    break
            if time.time() > end_time:
                print("Timeout waiting for engine response.")
                break

    def initialize_engine(self):
        self.send_command("uci")
        self.send_command("setoption name UCI_Variant value xiangqi")
        self.send_command("isready")

    def add_move(self, move):
        self.moves.append(move)
        moves_str = ' '.join(self.moves)
        self.send_command(f"position startpos moves {moves_str}")
        self.send_command("go depth 1")

    def close_engine(self):
        self.send_command("quit")
        self.engine.terminate()
        self.engine.wait()

# 示例使用
if __name__ == "__main__":
    # home_dir = os.path.expanduser("~")
    # folder_name = "XiangQiAI"
    # engine_path = os.path.join(home_dir, folder_name, "fstockfishb")
    engine_path = "./ai/fairy-stockfish-largeboard_x86-64-bmi2"
    engine = XiangQiEngine(engine_path)

    engine.initialize_engine()
    
    # 添加一些示例走子
    engine.add_move("e2e4")
    engine.add_move("e7e5")

    # 持续获取输出
    for _ in range(10):
        engine.receive_output_non_blocking()
        time.sleep(0.1)

    engine.close_engine()
