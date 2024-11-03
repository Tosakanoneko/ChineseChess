import serial
import time

ser = serial.Serial(
            port="/dev/ttyS0", 
            baudrate=115200,
            timeout = 0.01
)

# while True:
#     try:
#         msg = ser.readline().decode('utf-8').strip()
#         if msg:
#             print(msg)
#     except UnicodeDecodeError:
#         print("UnicodeDecodeError")
#     except KeyboardInterrupt:
#         ser.close()
#         break
    
while True:
    try:
        ser.write(b'Hello\n')
        print("sents")
        time.sleep(0.5)
    except KeyboardInterrupt:
        ser.close()
        break

