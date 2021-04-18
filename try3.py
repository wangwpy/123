# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 16:54:23 2021

@author: zhoujingtao
"""
from imutils.video import VideoStream
import imutils
import cv2
import numpy as np
frameWidth = 960
frameHeight = 720
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)          #参数3：设置视频框宽度
cap.set(4, frameHeight)         #参数4：设置视频框高
cap.set(5,5)
cap.set(10, 300)                #参数10：对应亮度
img1 = cv2.imread('4.jpg', 0)
myColors = [[-10,100,100, 10,255,255]]  #HSV：前3个lower 后三个upper  红壶的HSV152  179

myColorValues = [[126, 0, 0]]           #BGR

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(imgResult, (x, y), 1, (255, 0, 0), thickness=-1)
        cv2.putText(imgResult, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 255, 0), thickness=1)
        cv2.imshow("image", imgResult)

def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)   #BGR变HSV
    count = 0     
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])   
        upper = np.array(color[3:6])         # 分别设置HSV颜色空间中，对应颜色的阈值
        mask = cv2.inRange(imgHSV, lower, upper)
        mask = cv2.erode(mask, None, iterations=1)  #腐蚀去毛刺（完善图片边角）
        mask = cv2.dilate(mask, None, iterations=4) #膨胀恢复图像（适当调整大小可以实现将图片中间的一些无用特征去掉)
        x, y = getContours(mask)
        #cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)
        if x!= 0 and y!= 0:
            newPoints.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]), mask)
        return newPoints

#def drawOnCanvas(myPoints, myColorValues):
    #for point in myPoints:
        #cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

def getContours(img):
    imagess,contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)   #得到轮廓点集
    x, y, w, h = 0, 0, 0, 0     #设置数据储存识别物体的位置
    i=0                         #壶数量变量定义
    shuliang = 0
    r=0
    bottle = []    #壶的数量
    for cnt in contours: 
        area = cv2.contourArea(cnt) #计算轮廓像素面积（详细看资料不是真实面积）
        if (area>600 and area<20000) : 
            shuliang = shuliang + 1
            peri = cv2.arcLength(cnt,True)                          #计算得到弧长，形状是闭合的（True）
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)           #传入轮廓的点集
            #approx = cv2.approxPolyDP(cnt,2.8,True)
            bian = len(approx)
            print(shuliang,":",bian)
            if (bian>=6):
                bottle.append(cnt) 
                i = i+1
    print("数量：",shuliang)
    print("结果：",i)
    if(i==1):
        if(r==0):
            cnt=bottle[r]
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)           #传入轮廓的点集
            bian = len(approx)
            print(bian)
            area = cv2.contourArea(cnt)
            if (area>600 and area<20000): 
                #cv2.drawContours(imgResult, cnt, -1, (0,255,0), 3)         #-1：表示全部框住，0-全部：可以依次框住需要识别图像的轮廓
                
                #cv2.putText(imgResult, str(i), ((i*100), (i*100)), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 25)
                peri = cv2.arcLength(cnt,True)                          #计算得到弧长，形状是闭合的（True）
                x, y, w, h = cv2.boundingRect(approx)                   #x，y是矩阵左上点的坐标，w，h是矩阵的宽和高
                cv2.rectangle(imgResult, (x,y), (x+w,y+h), (0,255,0), 2)
                print(int(x+w/2), int(y+h/2))
        if(r==1):
            cnt=contours[1]
            area = cv2.contourArea(cnt)
            if area>600 : 
                #cv2.drawContours(imgResult, cnt, -1, (0,255,0), 3)         #-1：表示全部框住，0-全部：可以依次框住需要识别图像的轮廓
                
                peri = cv2.arcLength(cnt,True)                          #计算得到弧长，形状是闭合的（True）
                approx = cv2.approxPolyDP(cnt,0.02*peri,True)           #传入轮廓的点集，
                x, y, w, h = cv2.boundingRect(approx)                   #x，y是矩阵左上点的坐标，w，h是矩阵的宽和高
                cv2.rectangle(imgResult, (x,y), (x+w,y+h), (0,255,0), 2)
                print(int(x+w/2), int(y+h/2))
        if(r==2):
            cnt=contours[2]
            area = cv2.contourArea(cnt)
            if area>600 : 
                #cv2.drawContours(imgResult, cnt, -1, (0,255,0), 3)         #-1：表示全部框住，0-全部：可以依次框住需要识别图像的轮廓
              
                peri = cv2.arcLength(cnt,True)                          #计算得到弧长，形状是闭合的（True）
                approx = cv2.approxPolyDP(cnt,0.02*peri,True)           #传入轮廓的点集
                bian = len(approx)
                print(bian)
                x, y, w, h = cv2.boundingRect(approx)                   #x，y是矩阵左上点的坐标，w，h是矩阵的宽和高
                cv2.rectangle(imgResult, (x,y), (x+w,y+h), (0,255,0), 2)
                print(int(x+w/2), int(y+h/2))
    return int(x+w/2), int(y+h/2)
        
while True:
    success, img = cap.read()   #布尔值和图像
    imgResult = img.copy()      #备份原图片
    newPoints = findColor(img, myColors, myColorValues)
            #for i in myPoints:
                #print("myPoints"+str(i))
    #if len(myPoints) !=0:
        #drawOnCanvas(myPoints, myColorValues)
    cv2.imshow("Result", imgResult)
    cv2.setMouseCallback("Result", on_EVENT_LBUTTONDOWN)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
    
