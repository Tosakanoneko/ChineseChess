import time

def write_data(data):
    # 写入命名管道
    with open('/tmp/mypipe', 'w') as pipe:
        pipe.write(data)
    if len(data) != 0:
        print(f"send to ui: {data}")

def clear_pipes():
    files = ['/tmp/mypipe', '/tmp/mypipe1', '/tmp/mypipe2', '/tmp/mypipe3', '/tmp/mypipe4', '/tmp/mypipe5', '/tmp/mypipe6', '/tmp/mypipe7']
    for file in files:
        try:
            with open(file, 'w') as pipe:
                pipe.write('')
        except Exception as e:
            print(e)

def address_str(s):
    # 初始化结果字符串为空
    result = ""
    # 遍历字符串中的每个字符
    for i in range(len(s)):
        # 如果当前字符的索引是16的倍数（除了最后一个字符，因为索引是从0开始的）
        # 或者我们已经处理完了字符串中的所有字符
        if (i + 1) % 16 == 0 or i == len(s) - 1:
            # 将当前字符添加到结果字符串
            result += s[i]
            # 如果不是字符串的最后一个字符，则添加换行符
            if i != len(s) - 1:
                result += "\n"
        else:
            # 否则，直接将当前字符添加到结果字符串
            result += s[i]
    return result

class ui_comm:
    def __init__(self):
        self.bp_mode = 0 # 0: 下一步模式，1: 上一步模式
        self.fen = ''
        self.gpt_message = ''
        self.last_bp = ''
        self.next_bp = ''
        self.ai_diff = '1'
        self.set_diff = False
        self.send_remind = False
        self.send_illegal_mark = False
        self.remind = '1'
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
                                print("bp mode change to next")
                                self.fen = self.fen.split(' ', 1)[0] + ' ' + self.next_bp
                                write_data(self.fen)
                            elif data.startswith('analysis'):
                                self.bp_mode = 1
                                print("bp mode change to last")
                                self.fen = self.fen.split(' ', 1)[0] + ' ' + self.last_bp
                                write_data(self.fen)
                            tmp_msg = data

                with open('/tmp/mypipe2', 'r') as pipe:
                    data = pipe.read()
                    if data and data.startswith('message'):
                        print("send gpt message")
                        with open('/tmp/mypipe3', 'w') as pipe:
                            pipe.write(address_str(self.gpt_message))

                if not self.set_diff:
                    with open('/tmp/mypipe4', 'r') as pipe:
                        data = pipe.read()
                        if data:
                            self.ai_diff = data
                            self.set_diff = True

                if self.send_remind:
                    with open('/tmp/mypipe5', 'w') as pipe:
                        pipe.write(self.remind)
                        print("send remind: ", self.remind)
                    time.sleep(3)
                    with open('/tmp/mypipe5', 'w') as pipe:
                        pipe.write('0')
                        print('clear remind')
                    self.send_remind = False

                if self.send_illegal_mark:
                    with open('/tmp/mypipe6', 'w') as pipe:
                        # pass
                        pipe.write('1')
                else:
                    with open('/tmp/mypipe6', 'w') as pipe:
                        # pass
                        pipe.write('0')
                time.sleep(1)
            except OSError as e:
                print(f"error: {e}")
                time.sleep(1)

    def sendto_ui(self, first=False):
        if not first:
            if self.bp_mode == 0:
                self.fen += " " + self.next_bp
            elif self.bp_mode == 1:
                self.fen += " " + self.last_bp
        else:
            self.fen += " " + '1122'
        print(f"send to ui: {self.fen}")
        write_data(self.fen)
    