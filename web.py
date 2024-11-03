from datetime import datetime
import time
import requests

class web_record:
    def __init__(self):
        self.url = "http://8.137.87.254:8002/gameRecords/import"
        self.txt_path = './web.txt'
        with open(self.txt_path, 'w', encoding='utf-8') as f:
            f.write('')
        self.outcome = 'Unknown'
        self.date = datetime.now().strftime("%Y/%m/%d")
        self.start_time = time.time()
        self.difficulty = '1'
        self.record = []

    def write_to_txt(self):
        last_time = int((time.time() - self.start_time)//60)
        with open(self.txt_path, 'w', encoding='utf-8') as f:
            f.write(f"{self.outcome}\n")
            f.write(f"{self.date}\n")
            f.write(f"{last_time}\n")
            f.write(f"{self.difficulty}\n")
            for item in self.record:
                f.write(f"{item}\n")
        print("web数据写入完成")

    def update_record(self, mv_str):
        result = ""
        for char in mv_str:
            if char.isalpha():  # 检查字符是否是字母
                result += char.upper()  # 如果是字母，则转换为大写并添加到结果字符串
            else:
                result += char  # 如果不是字母（即数字或其他字符），则直接添加到结果字符串

        self.record.append(result)
        print(f"记录更新：{result}")

    def send_txt_to_web(self):
        # 打开文件，并以form-data的形式发送请求
        with open(self.txt_path, 'rb') as file:
            files = {'file': (file.name, file, 'text/plain')}
            response = requests.post(self.url, files=files)

        # 打印响应内容
        print("网站响应:", response.text)