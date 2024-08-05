from abc import ABC, abstractmethod
import time
import cv2
import numpy as np
import pyautogui
import win32gui
from PIL import ImageGrab
import win32con
import mss


class ScreenCaptureInterface(ABC):
    @abstractmethod
    def screenCapture(self):
        pass

    def callback(self, hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and len(win32gui.GetWindowText(hwnd)) > 0:
            hwnds.append(hwnd)
        return True

    def find_windows_by_name(self, title):
        hwnds = []
        win32gui.EnumWindows(self.callback, hwnds)
        matching_hwnds = [hwnd for hwnd in hwnds if title.lower() in win32gui.GetWindowText(hwnd).lower()]
        return matching_hwnds
    
    #激活窗口
    def SetForegroundWindow(self, hwnd=0):
        if win32gui.IsIconic(hwnd):
            # 如果窗口最小化，恢复它
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)

class ScreenCapturePillow(ScreenCaptureInterface):
    def screenCapture(self, title):
        hwnds = self.find_windows_by_name(title)
        print(hwnds)
        if len(hwnds) > 0:
            for hwnd in hwnds:
                self.SetForegroundWindow(hwnd)
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                print(left,top,right,bottom)
                im = ImageGrab.grab((left, top, right, bottom))
                im.save(r"d:/screenshot.png")
                # 显示图片没反应
                # im.show()

                # 添加下面代码后图片为IDE的图片
                # 转换 PIL 图像为 OpenCV 格式
                # im_np = np.array(im)
                # im_cv2 = cv2.cvtColor(im_np, cv2.COLOR_RGB2BGR)

                # # 显示图像
                # cv2.imshow("Screenshot", im_cv2)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
        else :
            return

class ScreenCaptureAutoGui(ScreenCaptureInterface):
    def screenCapture(self, title):
        hwnds = self.find_windows_by_name(title)
        print(hwnds)
        if len(hwnds) > 0:
            for hwnd in hwnds:
                self.SetForegroundWindow(hwnd)
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                print(left,top,right,bottom)
                im = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
                im.save(r"d:/screenshot.png")

class ScreenCaptureMss(ScreenCaptureInterface):
    def screenCapture(self, title):
        hwnds = self.find_windows_by_name(title)
        if len(hwnds) > 0:
            for hwnd in hwnds:
                self.SetForegroundWindow(hwnd)
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                with mss.mss() as sct:
                    monitor = {"top": top, "left": left, "width": right - left, "height": bottom - top}
                    im = sct.grab(monitor)
                    img_np = np.array(im)

                    # 因为 mss 返回的是 BGRA 格式，需要转换为 BGR 格式
                    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)

                    # 保存图像
                    cv2.imwrite(r"d:/screenshot.png", img_bgr)
obj = ScreenCaptureMss()
obj.screenCapture("微信")  # 输出: Implementing my_method
