import subprocess
import os
import select
import time

# # 获取主目录路径
# home_dir = os.path.expanduser("~")

# # 构建包含XiangQIAI文件夹的路径
# folder_name = "XiangQiAI"
# engine_path = os.path.join(home_dir, folder_name, "fstockfishb")
engine_path = "./ai/fairy-stockfish-largeboard_x86-64-bmi2"

# 启动象棋引擎
engine = subprocess.Popen(engine_path, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# 发送命令给引擎
def send_command(command):
    engine.stdin.write(command + '\n')
    engine.stdin.flush()

# 非阻塞方式获取引擎的输出并打印
def receive_output_non_blocking():
    while True:
        output = engine.stdout.readline().strip()
        if output == '':
            break
        print(output)



# 与引擎进行交互示例
send_command("uci")  # 发送UCI协议初始化命令


send_command("setoption name UCI_Variant value xiangqi")  # 发送UCI协议初始化命令


send_command("isready")  # 发送isready命令，询问引擎是否准备就绪


send_command("position startpos ")
send_command("go depth 1")
# 持续获取引擎的输出并打印
while True:
    receive_output_non_blocking()
    time.sleep(0.1)  # 等待一段时间再继续获取输出

# 关闭引擎
send_command("quit")
