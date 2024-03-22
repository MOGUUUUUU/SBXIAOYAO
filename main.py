import cv2
import numpy as np

def read_img(img_path):
    return cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

def main():
    img_path = 'img.jpg'
    
    img = read_img(img_path)
    
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    max_contour = max(contours, key=cv2.contourArea)
    
    M = cv2.moments(max_contour)
    
    center_x = int(M['m10']/M['m00'])
    center_y = int(M['m01']/M['m00'])
    
    print(len(contours))
    cv2.drawContours(img, contours, -1, (0,0,255), 1)
    cv2.drawContours(img, [max_contour], 0, (0, 0, 255, 3))
    cv2.circle(img, (center_x, center_y), 5, (0, 0, 255), -1)
    
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()