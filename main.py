import cv2
import numpy as np


class Image:
    def __init__(self, img) -> None:
        self.img = img
        _, self.thresh = cv2.threshold(self.img, 127, 255, cv2.THRESH_BINARY)

    def get_max_contour(self):
        contours, _ = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        max_contour = max(contours, key=cv2.contourArea)
        return max_contour
    
    def get_center(self, contour):
        M = cv2.moments(contour)
        xx = int(M['m10']/M['m00'])
        yy = int(M['m01']/M['m00'])
        return(xx, yy)

    def draw_contour(self, contour):
        cv2.drawContours(self.img, [contour], 0, (0, 0, 255, 3))
    
    def draw_center(self, center):
        xx, yy = center
        cv2.circle(self.img, (xx, yy), 5, (0, 0, 255), -1)
        
    def show(self):
        cv2.imshow('image', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def read_img_from_path(img_path):
    return cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

def main():
    img_path = 'img.jpg'
    
    img = read_img_from_path(img_path)
    
    IMG = Image(img)
    
    max_contour = IMG.get_max_contour()
    center = IMG.get_center(max_contour)
    IMG.draw_contour(max_contour)
    IMG.draw_center(center)
    IMG.show()
    
if __name__ == '__main__':
    main()