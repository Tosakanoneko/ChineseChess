import cv2
cap=cv2.VideoCapture(0, cv2.CAP_V4L2)  #调用摄像头�?’一般是打开电脑自带摄像头，�?’是打开外部摄像头（只有一个摄像头的情况）
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
width=640
height=480
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (width, height))
cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)#设置图像宽度
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)#设置图像高度
#显示图像
while True:
    ret,frame=cap.read()#读取图像(frame就是读取的视频帧，对frame处理就是对整个视频的处理)
    if not ret:
        continue
    out.write(frame)
    ########图像不处理的情况
    cv2.imshow("frame",frame)    
    
    input=cv2.waitKey(20)
    if input==ord('q'):#如过输入的是q就break，结束图像显示，鼠标点击视频画面输入字符
        break

out.release()
cap.release()#释放摄像�?cv2.destroyAllWindows()#销毁窗�? 
cv2.destroyAllWindows()