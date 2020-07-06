import numpy as np
import cv2, win32gui, time, math, win32con, win32ui
from PIL import ImageGrab, Image
import pytesseract
import sys
from pathlib import Path
import ctypes
import ctypes.wintypes

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class MapleWindowNotFoundError(Exception):
    pass


MAPLESTORY_WINDOW_TITLE = "MapleStory"


class MapleScreenCapturer:
    """Container for capturing MS screen"""
    def __init__(self):
        self.hwnd = None

    def ms_get_screen_hwnd(self):
        window_hwnd = win32gui.FindWindow(0, MAPLESTORY_WINDOW_TITLE)
        if not window_hwnd:
            return 0
        else:
            return window_hwnd

    def ms_get_screen_rect(self, hwnd):
        """
        Added compatibility code from
        https://stackoverflow.com/questions/51786794/using-imagegrab-with-bbox-from-pywin32s-getwindowrect
        :param hwnd: window handle from self.ms_get_screen_hwnd
        :return: window rect (x1, y1, x2, y2) of MS rect.
        """
        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            f = None
        if f:  # Vista & 7 stuff
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(ctypes.wintypes.HWND(self.ms_get_screen_hwnd()),
              ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
              ctypes.byref(rect),
              ctypes.sizeof(rect)
              )
            size = (rect.left, rect.top, rect.right, rect.bottom)
        else:
            if not hwnd:
                hwnd = self.ms_get_screen_hwnd()
            size = win32gui.GetWindowRect(hwnd)
        return size  # returns x1, y1, x2, y2

    def capture(self, set_focus=True, hwnd=None, rect=None):
        """Returns Maplestory window screenshot handle(not np.array!)
        :param set_focus : True if MapleStory window is to be focusesd before capture, False if not
        :param hwnd : Default: None Win32API screen handle to use. If None, sets and uses self.hwnd
        :param rect : If defined, captures specificed ScreenRect area (x1, y1, x2, y2). Else, uses MS window ms_screen_rect.
        :return : returns Imagegrab of screen (PIL Image)"""
        if hwnd:
            self.hwnd = hwnd
        if not hwnd:
            self.hwnd = self.ms_get_screen_hwnd()
        if not rect:
            rect = self.ms_get_screen_rect(self.hwnd)
        # if set_focus:
        #     win32gui.SetForegroundWindow(self.hwnd)
        #     time.sleep(0.1)
        img = ImageGrab.grab(rect)
        img = np.array(img)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # cv2.imshow("Screen", img)
        # cv2.waitKey()
        return img

    def screen_capture(self,w, h, x=0, y=0, save=True, save_name=''):
        # hwnd = win32gui.FindWindow(None, None)
        hwnd = win32gui.GetDesktopWindow()
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (x, y), win32con.SRCCOPY)

        if save:
            dataBitMap.SaveBitmapFile(cDC, save_name)
        else:
            b = dataBitMap.GetBitmapBits(True)
            img = np.fromstring(b, np.uint8).reshape(h, w, 4)
            cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        if not save:
            return img

    def pil_image_to_array(self, img):
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

class StaticImageProcessor:
    def __init__(self, img_handle=None):
        """
        :param img_handle: handle to MapleScreenCapturer
        """
        if not img_handle:
            raise Exception("img_handle must reference an MapleScreenCapturer class!!")
        # Pre-processing
        # Read the template
        self.template1 = cv2.imread('{}\\Git_Folder\\BotMaple\\CS_1280x920.JPG'.format(str(Path.home())), 0)
        self.template2 = cv2.imread('{}\\Git_Folder\\BotMaple\\CS_1024x768.JPG'.format(str(Path.home())), 0)
        # Pre-processing
        self.img_handle = img_handle
        self.bgr_img = None
        self.rbg_img = None
        self.bin_img = None
        self.gray_img = None
        self.processed_img = None
        self.minimap_area = 0
        self.minimap_rect = None
        self.chat_box_rgb_img = None
        self.chat_box_bgr_img = None

        self.maximum_minimap_area = 40000

        self.default_minimap_scan_area = [0, 60, 400, 300]  # x1, y1, x2, y2

        # Minimap player marker original BGR: 68, 221, 255
        # self.lower_player_marker = np.array([67, 220, 254])  # B G R
        # self.upper_player_marker = np.array([69, 222, 256])

        # Minimap player marker original BGR: 136, 255, 255
        self.lower_player_marker = np.array([0, 254, 254])  # B G R
        self.upper_player_marker = np.array([205, 256, 256])
        self.lower_rune_marker = np.array([254, 101, 220]) # B G R
        self.upper_rune_marker = np.array([255, 103, 222])

        self.hwnd = self.img_handle.ms_get_screen_hwnd()
        self.ms_screen_rect = None
        if self.hwnd:
            self.ms_screen_rect = self.img_handle.ms_get_screen_rect(self.hwnd)

        else:
            raise Exception("Could not find MapleStory window!!")



    def update_image(self, src=None, set_focus=False, update_rect=False):
        """
        Calls ScreenCapturer's update function and updates images.
        :param src : rgb image data from PIL ImageGrab
        :param set_focus : True if win32api setfocus shall be called before capturing"""
        if src:
            self.rgb_img = src
        else:
            if update_rect:
                self.ms_screen_rect = self.img_handle.ms_get_screen_rect(self.hwnd)

            if not self.ms_screen_rect:
                self.ms_screen_rect = self.img_handle.ms_get_screen_rect(self.hwnd)
            self.rgb_img = self.img_handle.capture(set_focus, self.hwnd, self.ms_screen_rect)

            # if not rgb_img:
            #     assert self.bgr_img != 0, "self.img_handle did not return img"

        self.bgr_img = cv2.cvtColor(np.array(self.rgb_img), cv2.COLOR_RGB2BGR)
        self.gray_img = cv2.cvtColor(self.bgr_img, cv2.COLOR_BGR2GRAY)
        self.rbg_img = np.array(self.rbg_img)

        h, w = self.rgb_img.shape[:-1]
        self.chat_box_rgb_img = self.rgb_img[int(h / 1.8):int(h / 1.12), 0:int(w / 1.6)]
        self.chat_box_bgr_img = self.bgr_img[int(h / 1.8):int(h / 1.12), 0:int(w / 1.6)]
        # cv2.imshow("RBG", np.array(self.rgb_img))
        # cv2.waitKey()

    def get_minimap_rect(self):
        """
        Processes self.gray images, returns minimap bounding box
        :return: Array [x,y,w,h] bounding box of minimap if found, else 0
        """
        cropped = self.gray_img[self.default_minimap_scan_area[1]:self.default_minimap_scan_area[3], self.default_minimap_scan_area[0]:self.default_minimap_scan_area[2]]
        blurred_img = cv2.GaussianBlur(cropped, (3,3), 3)
        morphed_img = cv2.erode(blurred_img, (7,7))
        # cv2.imshow("Map", cropped)
        # cv2.waitKey()
        canny = cv2.Canny(morphed_img, threshold1=180, threshold2=255)
        try:
            im2, contours, hierachy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        except:
            contours, hierachy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            biggest_contour = max(contours, key = cv2.contourArea)
            if cv2.contourArea(biggest_contour) >= 100 and cv2.contourArea(biggest_contour) >= self.minimap_area and cv2.contourArea(biggest_contour) <= self.maximum_minimap_area:
                minimap_coords = cv2.boundingRect(biggest_contour)
                if minimap_coords[0] > 0 and minimap_coords[1] > 0 and minimap_coords[2] > 0 and minimap_coords[2] > 0:
                    contour_area = cv2.contourArea(biggest_contour)
                    self.minimap_area = contour_area
                    minimap_coords = [minimap_coords[0], minimap_coords[1], minimap_coords[2], minimap_coords[3]]
                    minimap_coords[0] += self.default_minimap_scan_area[0]
                    minimap_coords[1] += self.default_minimap_scan_area[1]
                    self.minimap_rect = minimap_coords
                    return minimap_coords
                else:
                    pass
        return 0

    def reset_minimap_area(self):
        """
        Resets self.minimap_area which is used to reset self.get_minimap_rect search.
        :return: None
        """
        self.minimap_area = 0

    def find_player_minimap_marker(self, rect=None):
        """
        Processes self.bgr_image to return player coordinate on minimap.
        The player marker has exactly 12 pixels of the detection color to form a pixel circle(2,4,4,2 pixels). Therefore
        before calculation the mean pixel value of the mask, we remove "false positives", which are not part of the
        player color by finding pixels which do not have between 10 to 12 other pixels(including itself) of the same color in a
        distance of 3.
        :param rect: [x,y,w,h] bounding box of minimap in MapleStory screen. Call self.get_minimap_rect to obtain
        :return: x,y coordinate of player relative to ms_screen_rect if found, else 0
        """
        if not rect and not self.minimap_rect:
            rect = self.get_minimap_rect()
        else:
            rect = self.minimap_rect
        assert rect, "Invalid minimap coordinates"
        cropped = self.rgb_img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
        # cv2.imshow("Minimap", cropped)
        # cv2.waitKey()

        mask = cv2.inRange(cropped, self.lower_player_marker, self.upper_player_marker)

        # for i in range(len(mask)):
        #     if 255 in mask[i]:
        #         print(i)

        # print(mask)
        # cv2.imshow("Mask", mask)
        # cv2.waitKey()
        td = np.transpose(np.where(mask > 0)).tolist()

        # [y, x]
        if len(td) > 0:
            x_list = [x[1] for x in td]
            y_list = [x[0] for x in td]
            avg_x = int(sum(x_list) / len(x_list))
            avg_y = int(sum(y_list) / len(y_list))
            return avg_x, avg_y
            # print((avg_x, avg_y))

        return 0

    def find_other_player_marker(self, rect=None):
        """
        Processes self.bgr_image to return coordinate of other players on minimap if exists.
        Does not behave as expected when there are more than one other player on map. Use this function to just detect.
        :param rect: [x,y,w,h] bounding box of minimap. Call self.get_minimap_rect
        :return: x,y coord of marker if found, else 0
        """
        if not rect:
            rect = self.get_minimap_rect()
        assert rect, "Invalid minimap coordinates"
        cropped = self.bgr_img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
        mask = cv2.inRange(cropped, (0, 0, 255), (0, 0, 255))
        td = np.transpose(np.where(mask > 0)).tolist()
        if len(td) > 0:
            avg_x = 0
            avg_y = 0
            totalpoints = 0
            for coord in td:
                avg_y += coord[0]
                avg_x += coord[1]
                totalpoints += 1
            avg_y = int(avg_y / totalpoints)
            avg_x = int(avg_x / totalpoints)
            return avg_x, avg_y

        return 0

    def find_rune_marker(self, rect=None):
        """
        Processes self.bgr_image to return coordinates of rune marker on minimap.
        :param rect: [x,y,w,h] bounding box of minimap. Call self.get_minimap_rect
        :return: x,y of rune minimap coordinates if found, else 0
        """
        if not rect and not self.minimap_rect:
            rect = self.get_minimap_rect()
        else:
            rect = self.minimap_rect
        assert rect, "Invalid minimap coordinates"
        cropped = self.bgr_img[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
        mask = cv2.inRange(cropped, self.lower_rune_marker, self.upper_rune_marker)
        td = np.transpose(np.where(mask > 0)).tolist()
        if len(td) > 0:
            avg_x = 0
            avg_y = 0
            totalpoints = 0
            for coord in td:
                nearest_points = 0  # Points which are close to coord pixel
                for ref_coord in td:
                    # Calculate the range between every single pixel
                    if math.sqrt(abs(ref_coord[0] - coord[0]) ** 2 + abs(ref_coord[1] - coord[1]) ** 2) <= 6:
                        nearest_points += 1

                if nearest_points >= 20 and nearest_points <= 25:
                    avg_y += coord[0]
                    avg_x += coord[1]
                    totalpoints += 1

            if totalpoints == 0:
                return 0

            avg_y = int(avg_y / totalpoints)
            avg_x = int(avg_x / totalpoints)
            return avg_x, avg_y

        return 0

    def get_HP_percent(self):
        '''
        choices: 1024 x 768 (0) OR 1280 x 960 (1)
        '''
        h, w = self.rgb_img.shape[:-1]
        resOption = 1
        if h == 768:
            resOption = 0
        elif h == 960:
            resOption = 1

        x_start = [285, 356]
        x_end = [412, 508]
        y_start = [744, 936]
        y_end = [762, 954]

        im_np = self.gray_img[y_start[resOption]:y_end[resOption],
                                x_start[resOption]:x_end[resOption]]

        # pick an array to analyze current hp and full hp
        # print("HP: ", im_np[10])
        # cv2.imshow("HP", im_np)
        # cv2.waitKey()

        # return unique values and count of each unique value
        unique, counts = np.unique(im_np[10], return_counts=True)
        percent = counts[0] / (x_end[resOption] - x_start[resOption]) * 100
        print("Percent HP: ", percent)
        return percent

    def get_MP_percent(self):
        '''
        choices: 1024 x 768 (0) OR 1280 x 960 (1)
        '''

        h, w = self.rgb_img.shape[:-1]
        resOption = 1
        if h == 768:
            resOption = 0
        elif h == 960:
            resOption = 1

        x_start = [424, 530]
        x_end = [551, 682]
        y_start = [744, 936]
        y_end = [762, 954]

        im_np = self.gray_img[y_start[resOption]:y_end[resOption],
                                x_start[resOption]:x_end[resOption]]

        # pick an array to analyze current hp and full hp
        # print("MP: ", im_np[10])
        # print("Auto MP. Random percent: {}. Res Option: {}".format(percent, resOption))
        # cv2.imshow("MP", im_np)
        # cv2.waitKey()

        item = 0

        # 178 is empty - 1024x768
        # 134 is empty - 1280x960
        empty = [175, 130]
        for x in range(len(im_np[10])):
            if im_np[10][x] > empty[resOption]:
                item = x
                break
        # print("Percent MP: ", item / (x_end[resOption] - x_start[resOption]) * 100)
        percent = item / (x_end[resOption] - x_start[resOption]) * 100
        if percent == 0:
            return 100
        return percent

    def is_exist_chaos_scroll(self):
        try:
            # Store width and height of template in w and h
            w1, h1 = self.template1.shape[::-1]
            w2, h2 = self.template2.shape[::-1]

            # Perform match operations.
            res1 = cv2.matchTemplate(self.gray_img, self.template1, cv2.TM_CCOEFF_NORMED)
            res2 = cv2.matchTemplate(self.gray_img, self.template2, cv2.TM_CCOEFF_NORMED)

            # Specify a threshold
            threshold = 0.8

            # Store the coordinates of matched area in a numpy array
            loc1 = np.where(res1 >= threshold)
            loc2 = np.where(res2 >= threshold)
            if len(loc1[0]) > 0:
                return True

            if len(loc2[0]) > 0:
                return True

        except Exception as e:
            print("Check for CS scsroll exception: ", e)
            pass
        return False

    def is_exist_GM_dungeon(self):
        ###### Preprocessing (if needed)
        # gray = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)
        # gray_thresh = cv2.threshold(gray, 0, 255,
        #                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # # make a check to see if median blurring should be done to remove
        # # noise
        # gray_blur = cv2.medianBlur(gray, 3)
        #
        # text_bgr = pytesseract.image_to_string(im_np)
        # print("BGR", text_bgr)
        # # text_thresh = pytesseract.image_to_string(gray_thresh)
        # # print("Thresh", text_thresh)
        # text_blur = pytesseract.image_to_string(gray_blur)
        # print("Blur", text_blur)
        # cv2.imshow("Output Thresh", gray_thresh)
        # cv2.imshow("Output Blur", gray_blur)
        # cv2.waitKey(0)
        ###### Preprocessing (if needed)-----

        text_bgr = pytesseract.image_to_string(self.chat_box_bgr_img)
        text_rgb = pytesseract.image_to_string(self.chat_box_rgb_img)

        if "GM" or "Alex" or "GMAlex" in text_bgr:
            return True
        if "GM" or "Alex" or "GMAlex" in text_rgb:
            return True
        # cv2.imshow("img", test_img)
        # cv2.waitKey()

        return False

    def is_exist_GM_regular(self):
        return False

    def display_image_attr(self):
        cv2.imshow("BGR", self.bgr_img)
        cv2.imshow("RGB", self.rgb_img)
        cv2.imshow("Gray", self.gray_img)
        cv2.waitKey()

if __name__ == "__main__":
    dx = MapleScreenCapturer()
    hwnd = dx.ms_get_screen_hwnd()
    rect = dx.ms_get_screen_rect(hwnd)

    static = StaticImageProcessor(dx)
    static.update_image()
    print(static.get_MP_percent())
    x, y, w, h = static.get_minimap_rect()
    # print(rect)
    # dx.capture(rect=rect)
