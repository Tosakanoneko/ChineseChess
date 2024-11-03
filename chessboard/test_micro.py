import os
import time


def read_data():
    tmp_msg = ''
    # 从命名管道读取数据
    while True:
        try:
            with open('./mypipe', 'r') as pipe:
                data = pipe.read()
                if data:
                    if tmp_msg is None:
                        tmp_msg = data
                    if tmp_msg != data:
                        print('Received:', data) 
                        tmp_msg = data
                    else:
                        pass
            time.sleep(1)
                    # return data
        except OSError:
            time.sleep(1)


read_data()

