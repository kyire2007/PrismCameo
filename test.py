import cv2

capture = cv2.VideoCapture(0)
encoding = cv2.cv.CV_FOURCC('I','4','2','0')
fps = 30
size = (int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
        int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
if fps == 0.0:
    fps = 30
videoWriter = cv2.VideoWriter('trail.avi', encoding, fps, size)
cv2.namedWindow('My video')
success, frame = capture.read()
while success and cv2.waitKey(1) == -1:
    cv2.imshow('My video', frame)
    success, frame = capture.read()
    videoWriter.write(frame)

cv2.destroyAllWindows()
