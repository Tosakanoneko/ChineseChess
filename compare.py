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

        self.ser = serial.Serial(port="/dev/ttyHS1", baudrate=9600)

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

    def send_cmd(self, mark, ToMoveid, Movedid):
        self.ToMoveCp_theta1, self.ToMoveCp_theta2 = self.id2theta(ToMoveid)
        self.MovedCp_theta1, self.MovedCp_theta2 = self.id2theta(Movedid)

        # 吃子
        if mark:
            relative_theta1 = self.MovedCp_theta1 - self.init_theta1
            relative_theta2 = self.MovedCp_theta2 - self.init_theta2
            relative_theta1 = round(relative_theta1, 6)
            relative_theta2 = round(relative_theta2, 6)
            cmd = f"{relative_theta1},{relative_theta2},2\n"
            self.ser.write(cmd.encode('utf-8'))
            while self.ser.readline().decode('utf-8').strip() != "Arduino is ready":
                print("waiting arduino..")
                time.sleep(0.5)
                continue
            print("arduino_ready_receive!")
            time.sleep(1)

            relative_theta1 = self.init_theta1 - self.MovedCp_theta1
            relative_theta2 = self.init_theta2 - self.MovedCp_theta2
            relative_theta1 = round(relative_theta1, 6)
            relative_theta2 = round(relative_theta2, 6)
            cmd = f"{relative_theta1},{relative_theta2},1\n"
            print("cmd4:",cmd)
            self.ser.write(cmd.encode('utf-8'))
            while self.ser.readline().decode('utf-8').strip() != "Arduino is ready":
                print("waiting arduino..")
                time.sleep(0.5)
                continue
            print("arduino_ready_receive!")

            cmd = f"0,0,0\n"
            print("cmd5:",cmd)
            self.ser.write(cmd.encode('utf-8'))
            while self.ser.readline().decode('utf-8').strip() != "Arduino is ready":
                print("waiting arduino..")
                time.sleep(0.5)
                continue
            print("arduino_ready_receive!")
        
        # 移动
        relative_theta1 = self.ToMoveCp_theta1 - self.init_theta1
        relative_theta2 = self.ToMoveCp_theta2 - self.init_theta2
        relative_theta1 = round(relative_theta1, 6)
        relative_theta2 = round(relative_theta2, 6)
        cmd = f"{relative_theta1},{relative_theta2},2\n"
        print("cmd1:",cmd)
        self.ser.write(cmd.encode('utf-8'))
        while self.ser.readline().decode('utf-8').strip() != "Arduino is ready":
            print("waiting arduino..")
            time.sleep(0.5)
            continue
        print("arduino_ready_receive!")
        time.sleep(1)

        relative_theta1 = self.MovedCp_theta1 - self.ToMoveCp_theta1
        relative_theta2 = self.MovedCp_theta2 - self.ToMoveCp_theta2
        relative_theta1 = round(relative_theta1, 6)
        relative_theta2 = round(relative_theta2, 6)
        cmd = f"{relative_theta1},{relative_theta2},1\n"
        print("cmd2:",cmd)
        self.ser.write(cmd.encode('utf-8'))
        while self.ser.readline().decode('utf-8').strip() != "Arduino is ready":
            print("waiting arduino..")
            time.sleep(0.5)
            continue
        print("arduino_ready_receive!")
        time.sleep(1)

        relative_theta1 = self.init_theta1 - self.MovedCp_theta1
        relative_theta2 = self.init_theta2 - self.MovedCp_theta2
        relative_theta1 = round(relative_theta1, 6)
        relative_theta2 = round(relative_theta2, 6)
        cmd = f"{relative_theta1},{relative_theta2},0\n"
        self.ser.write(cmd.encode('utf-8'))
        print("cmd3:",cmd)
        while self.ser.readline().decode('utf-8').strip() != "Arduino is ready":
            print("waiting arduino..")
            time.sleep(0.5)
            continue
        print("arduino_ready_receive!")



if __name__ == '__main__':
    jxb = Manipulator()
    jxb.send_cmd(1,[9,0],[0,0])




