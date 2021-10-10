from networkHandle.NetHandle import MqttDevMonitor
from discern import detect_fire

import threading
import time
import cv2 as cv
import numpy as np

font = cv.FONT_HERSHEY_SIMPLEX
PI = 3.1415926


def contrast_brightness_demo(image, c, b):  # 其中c为对比度，b为每个像素加上的值（调节亮度）
    blank = np.zeros(image.shape, image.dtype)  # 创建一张与原图像大小及通道数都相同的黑色图像
    dst = cv.addWeighted(image, c, blank, 1 - c, b)  # c为加权值，b为每个像素所加的像素值
    ret, dst = cv.threshold(dst, 25, 255, cv.THRESH_BINARY)
    return dst


redThre = 150
saturationTh = 45


def discreen(frame):
    # cv.imshow("frame", frame)
    B = frame[:, :, 0]
    G = frame[:, :, 1]
    R = frame[:, :, 2]
    minValue = np.array(np.where(R <= G, np.where(G <= B, R, np.where(R <= B, R, B)), np.where(G <= B, G, B)))
    S = 1 - 3.0 * minValue / (R + G + B + 1)
    fireImg = np.array(np.where(R > redThre, np.where(R >= G, np.where(G >= B, np.where(S >= 0.2, np.where(
        S >= (255 - R) * saturationTh / redThre, 255, 0), 0), 0), 0), 0))
    gray_fireImg = np.zeros([fireImg.shape[0], fireImg.shape[1], 1], np.uint8)
    gray_fireImg[:, :, 0] = fireImg
    gray_fireImg = cv.GaussianBlur(gray_fireImg, (7, 7), 0)
    gray_fireImg = contrast_brightness_demo(gray_fireImg, 5.0, 25)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    gray_fireImg = cv.morphologyEx(gray_fireImg, cv.MORPH_CLOSE, kernel)
    dst = cv.bitwise_and(frame, frame, mask=gray_fireImg)
    canny = cv.Canny(gray_fireImg, 50, 150)  # 50是最小阈值,150是最大阈值

    contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    def cnt_area(cnt):
        area = cv.contourArea(cnt)
        return area

    contours.sort(key=cnt_area, reverse=True)
    # for i in range(0, len(contours)):
    #     (x, y, w, h) = cv.boundingRect(contours[i])
    #     cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2, cv.LINE_AA)
    #     cv.putText(frame, "No.%d" % (i + 1), (x, y - 5), font, 0.8, (255, 0, 0), 2)
    if len(contours) != 0:
        (x, y, w, h) = cv.boundingRect(contours[0])
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2, cv.LINE_AA)
        cv.putText(frame, "fire", (x, y - 5), font, 0.8, (255, 0, 0), 2)

        return True

    return False

class ServerMonitor:
    def __init__(self):
        self.m_discern_flag = False
        self.m_ready_img = None

        self.m_current_flag = False

        self.m_net_handle = MqttDevMonitor()

        self.discern_thread = threading.Thread(target=self.img_process, args=())
        self.discern_thread_lock = threading.RLock()

        self.discern_thread.start()

    def img_process(self):
        while True:
            self.discern_thread_lock.acquire()

            if self.m_net_handle.has_img():

                self.m_ready_img = self.m_net_handle.get_image()
                self.m_discern_flag = True

            self.discern_thread_lock.release()

            if self.m_discern_flag:
                #cv2.imshow("1", self.m_ready_img[1])
                #cv2.waitKey(1)
                #result = discreen(self.m_ready_img[1])

                result = detect_fire.detect(self.m_ready_img[1])

                print(self.m_ready_img[0])
                self.m_discern_flag = False
                if result:
                    if self.m_current_flag != result:
                        self.m_net_handle.publish_control_signal(self.m_ready_img[0], "open")
                else:
                    if self.m_current_flag != result:
                        self.m_net_handle.publish_control_signal(self.m_ready_img[0], "close")
                self.m_current_flag = result
            else:
                time.sleep(0.01)


def main():
    server = ServerMonitor()

    while True:
        time.sleep(0.1)

if __name__ == '__main__':
    main()
