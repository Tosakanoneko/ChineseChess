import cv2
import socket
import numpy as np

HOST = '192.168.137.5'  # OpenMV的IP地址
PORT = 8080

def main():
    # 创建socket连接
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    # 发送HTTP请求
    request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(HOST)
    s.send(request.encode())
    
    data = b''
    while True:
        data += s.recv(4096)
        start = data.find(b'\xff\xd8')  # JPEG图像开始
        end = data.find(b'\xff\xd9')    # JPEG图像结束
        if start != -1 and end != -1:
            jpg = data[start:end+2]
            data = data[end+2:]
            img = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
            if img is not None:
                cv2.imshow("OpenMV Stream", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    s.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
