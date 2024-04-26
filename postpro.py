import cv2
import os
import math
import numpy as np


debug_mode = False

class Vedio:
    def __init__(self) -> None:
        self.CAP_NUM = 0
        self.cap = cv2.VideoCapture()
        
    # def open_cap(self):
    #     self.cap.open(self.CAP_NUM)
        
    def open_cap(self):
        self.cap = cv2.VideoCapture('resource/test.mp4')
        success, _ = self.cap.read()
        return success
        
    def close_cap(self):
        if self.cap.isOpened:
            self.cap.release()
        
    def grey_postpro(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        max_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(max_contour)
        xx = int(M['m10']/M['m00'])
        yy = int(M['m01']/M['m00'])
        cv2.drawContours(gray, [max_contour], 0, (0, 0, 255, 3))
        cv2.circle(gray, (xx, yy), 5, (0, 0, 255), -1)
        return gray
        
    def postpro(self, frame):
        def adaptive_threshold(frame):
            thresh = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 2)
            
            if debug_mode:
                cv2.imshow('adaptive_threshold', thresh)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                
            return thresh
        
        def fit_ellipse(frame, thresh):
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19))
            dilated = cv2.dilate(thresh, kernel, iterations=2)
            closed = cv2.erode(dilated, kernel, iterations=2)
            contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            max_contour = max(contours, key=cv2.contourArea)
            ellipse = cv2.fitEllipse(max_contour)
            cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 1)
            cv2.ellipse(frame, ellipse, (255, 255, 0), 1)
            center = ellipse[0]
            cv2.circle(frame, (int(center[0]), int(center[1])), 5, (0, 0, 255), -1)
            
            if debug_mode:
                cv2.imshow('fit_ellipse', frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            
            return center, max_contour, closed
        
        def find_black_hole(frame, thresh, closed, contour):
            mask = np.zeros_like(thresh)
            cv2.drawContours(mask, [contour], 0, 255, cv2.FILLED)
            diff = cv2.absdiff(closed, mask)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
            dilated = cv2.dilate(diff, kernel, iterations=2)
            closed = cv2.erode(dilated, kernel, iterations=2)
            contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            max_contour = max(contours, key=cv2.contourArea)
            ellipse = cv2.fitEllipse(max_contour)
            cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 1)
            cv2.ellipse(frame, ellipse, (255, 255, 0), 1)
            center = ellipse[0]
            cv2.circle(frame, (int(center[0]), int(center[1])), 5, (0, 0, 255), -1)
                    
            if debug_mode:
                cv2.imshow('find_black_hole', frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            return center
                    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 6)
        thresh = adaptive_threshold(blurred)
        found1, found2 = True, True
        try:
            center1, contour, closed = fit_ellipse(frame, thresh)
        except:
            found1 = False
        try: 
            center2 = find_black_hole(frame, thresh, closed, contour)
        except:
            found2 = False
        if found1 and found2:
            x1, y1 = center1
            x2, y2 = center2
            print('({:.2f},{:.2f}) ({:.2f},{:.2f})'.format(x1, y1, x2, y2))
            print('dx:{:.2f} dy:{:.2f} dist:{:.2f}'.format(
                abs(x1-x2),
                abs(y1-y2),
                math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            ))
        if debug_mode:
            cv2.imshow('Result', frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return frame
    
    def read_cap(self, window):
        if not self.cap.isOpened():
            raise RuntimeError('must open cap first')
        success, frame = self.cap.read()
        if not success:
            return
        # frame = cv2.resize(frame, (384, 216))
        native = cv2.cvtColor(np.copy(frame), cv2.COLOR_BGR2RGB)
        post_pro = self.postpro(np.copy(frame))
        window.native_img = cv2.resize(native, (384, 216))
        window.postpro_img = cv2.resize(post_pro, (384, 216))
        
        

if __name__ == '__main__':
    vv = Vedio()
    image = cv2.imread('./resource/test_01.png')
    vv.postpro(image)