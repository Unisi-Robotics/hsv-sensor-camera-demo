import cv2 as cv

# img = cv.imread('/home/irizqyakbr/Documents/robot-camera/plane.png')
# print(type(img))
# print(img.shape)

# img = img[70:450, 100:700]

# cv.imshow('Test CV', img)
# print(cv.waitKey(0))
# print("\anui")


cap = cv.VideoCapture(2)

while True:
    _, frame = cap.read()

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    cv.imshow('Test Camera', frame)

cap.release()
cv.destroyAllWindows()
