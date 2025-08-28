import cv2 as cv
img = cv.imread('ejemplo.jpeg', 0)
cv.imshow('Ejemplo', img)
cv.waitKey()
cv.destroyAllWindows()
