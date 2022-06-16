import cv2

# Read the original image
# img = cv2.imread('images/edge_test.jpg')
# img = cv2.imread('images/full_scene2.png')
img = cv2.imread('images/full_scene.jpg')
# Display original image
cv2.imshow('Original', img)
cv2.waitKey(0)

# Convert to graycsale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Blur the image for better edge detection
# img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
img_blur = cv2.medianBlur(img_gray, 3, 0)

# # Sobel Edge Detection
# sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)  # Sobel Edge Detection on the X axis
# sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)  # Sobel Edge Detection on the Y axis
# sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)  # Combined X and Y Sobel Edge Detection
# # Display Sobel Edge Detection Images
# cv2.imshow('Sobel X', sobelx)
# cv2.waitKey(0)
# cv2.imshow('Sobel Y', sobely)
# cv2.waitKey(0)
# cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
# cv2.waitKey(0)


# Canny Edge Detection
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=220)  # Canny Edge Detection
# Display Canny Edge Detection Image
cv2.imshow('Canny Edge Detection', edges)
key = cv2.waitKey(0)

if key == ord('s'):
    cv2.imwrite('canny_test2.png', edges)

cv2.destroyAllWindows()
