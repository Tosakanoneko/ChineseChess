import math
import serial
import time
from numpy import cos, sin, arccos, arctan2, sqrt
class Manipulator:
    def __init__(self):
        # 已知参数(cm)
        self.a = 29.8      #大臂长度
        self.b = 28.0      #小臂长度

        self.L_length = 8.8

        self.init_theta1 = 0
        self.init_theta2 = 0
        self.ToMoveCp_theta1 = 0
        self.ToMoveCp_theta2 = 0
        self.MovedCp_theta1 = 0
        self.MovedCp_theta2 = 0

        self.ser = serial.Serial(
            port="/dev/ttyAMA2", 
            baudrate=9600,
            timeout = 0.01
        )

        self.count = 0
        self.action_finish = True

    def cal_angle(self, x, y):
        x=-x
        q1 = arccos((x ** 2 + y ** 2 - self.a ** 2 - self.b ** 2) / (2 * self.a * self.b))#大臂
        q0 = arctan2(y, x) - arctan2(self.b * sin(q1), self.b * cos(q1) + self.a)#小臂
        return q0/3.14*180, q1/3.14*180-90

    def id2theta(self, id):
        row = id[0]
        col = id[1]
        if(row<=4):
            x_dis = 1.9 + (4-row)*3.75
        else:
            x_dis = -(1.9 + (row-5)*3.75)
        y_dis = self.L_length + 4 * (8 - col)
        print(f"计算距离{x_dis}, {y_dis}")
        theta1, theta2 =  self.cal_angle(x_dis, y_dis)
        print(f"计算角度{theta1}, {theta2}")

        return theta1, theta2
    
    def wait_switch(self):
        print("等待按钮")
        while True:
            try:
                msg = self.ser.readline().decode('utf-8').strip()
                if msg:
                    print(msg)
                if msg == 'Player Done':
                    print("按下按钮")
                    break
            except UnicodeDecodeError:
                # print(f"收到{msg}")
                continue
            time.sleep(0.5)
    
    def send_cmd(self, mark, ToMoveid, Movedid):
        print("mark:", mark)
        self.action_finish = False
        self.wait_switch()
        ToMoveid[0] = 9 - ToMoveid[0]
        ToMoveid[1] = 8 - ToMoveid[1]
        Movedid[0] = 9 - Movedid[0]
        Movedid[1] = 8 - Movedid[1]
        self.ToMoveCp_theta1, self.ToMoveCp_theta2 = self.id2theta(ToMoveid)
        self.MovedCp_theta1, self.MovedCp_theta2 = self.id2theta(Movedid)

        # 吃子
        if mark:
            relative_theta1 = self.ToMoveCp_theta1 - self.init_theta1
            relative_theta2 = self.ToMoveCp_theta2 - self.init_theta2
            relative_theta1 = round(relative_theta1, 6)
            relative_theta2 = round(relative_theta2, 6)
            cmd = f"{relative_theta1},{relative_theta2},2\n"
            self.ser.write(cmd.encode('utf-8'))
            msg = self.ser.readline().decode('utf-8').strip()
            print("waiting arduino..")
            while msg != "Arduino is ready":
                # print(f"msg : {msg}")
                time.sleep(0.5)
                msg = self.ser.readline().decode('utf-8').strip()
                continue
            print("arduino_ready_receive!")
            time.sleep(1)

            relative_theta1 = self.init_theta1 - self.ToMoveCp_theta1
            relative_theta2 = self.init_theta2 - self.ToMoveCp_theta2
            relative_theta1 = round(relative_theta1, 6)
            relative_theta2 = round(relative_theta2, 6)
            cmd = f"{relative_theta1},{relative_theta2},1\n"
            print("cmd4:",cmd)
            self.ser.write(cmd.encode('utf-8'))
            print("waiting arduino..")
            while self.ser.readline().decode('utf-8').strip() != "Arduino is ready":
                time.sleep(0.5)
                continue
            print("arduino_ready_receive!")

        
        # 移动
        relative_theta1 = self.MovedCp_theta1 - self.init_theta1
        relative_theta2 = self.MovedCp_theta2 - self.init_theta2
        relative_theta1 = round(relative_theta1, 6)
        relative_theta2 = round(relative_theta2, 6)
        cmd = f"{relative_theta1},{relative_theta2},2\n"
        print("cmd1:",cmd)
        self.ser.write(cmd.encode('utf-8'))
        msg = self.ser.readline().decode('utf-8').strip()
        print("waiting arduino..")
        while msg != "Arduino is ready":
            if msg is not None:
                print(f"msg: {msg}")
            time.sleep(0.5)
            msg = self.ser.readline().decode('utf-8').strip()
            continue
        print("arduino_ready_receive!")
        time.sleep(1)

        relative_theta1 = self.ToMoveCp_theta1 - self.MovedCp_theta1
        relative_theta2 = self.ToMoveCp_theta2 - self.MovedCp_theta2
        relative_theta1 = round(relative_theta1, 6)
        relative_theta2 = round(relative_theta2, 6)
        cmd = f"{relative_theta1},{relative_theta2},1\n"
        print("cmd2:",cmd)
        self.ser.write(cmd.encode('utf-8'))
        print("waiting arduino..")
        while self.ser.readline().decode('utf-8').strip() != "Arduino is ready":
            time.sleep(0.5)
            continue
        print("arduino_ready_receive!")
        time.sleep(1)

        relative_theta1 = self.init_theta1 - self.ToMoveCp_theta1
        relative_theta2 = self.init_theta2 - self.ToMoveCp_theta2
        relative_theta1 = round(relative_theta1, 6)
        relative_theta2 = round(relative_theta2, 6)
        cmd = f"{relative_theta1},{relative_theta2},0\n"
        self.ser.write(cmd.encode('utf-8'))
        print("cmd3:",cmd)
        print("waiting arduino..")
        while self.ser.readline().decode('utf-8').strip() != "Arduino is ready":
            time.sleep(0.5)
            continue
        print("arduino_ready_receive!")
        self.action_finish = True

    def read_data(self):
        while True:
            data = self.ser.read(1024)
            if data:
                self.count += 1
                if self.count % 2 == 1:
                    self.action_finish = False
                    print("机械臂开始操作，停止识别")
                else:
                    self.action_finish = True
                    print("机械臂停止操作，开始识别")
            time.sleep(1)

if __name__ == '__main__':
    # 66 56s
    jxb = Manipulator()
    # jxb.send_cmd(0,[2,2],[0,1])
    jxb.send_cmd(0,[5,0],[4,0])
    # theta1 = round(theta1, 6)
    # theta2 = round(theta2, 6)
    # theta1 = 58
    # theta2 = 58
    # print(f"{theta1}, {theta2}")
    # cmd = f"{theta1},{theta2},1\n"
    # print(cmd)
    # jxb.ser.write(cmd.encode('utf-8'))
    # print("sent")
    # jxb.send_cmd(False, [0,0])




