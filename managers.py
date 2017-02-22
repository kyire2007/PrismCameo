# abstract opencv functions to create a higher level interface
import cv2
import numpy as np
import time

# Capture manager
class CaptureManager(object):
    def __init__(self, capture, previewWindowManager = None,
                 shouldMirrorPreview = None):
        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview

        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

        self._startTime = 0
        self._framesElapsed = long(0)
        self._fpsEstimate = None

    @property
    def channel(self):
        return self._channel
    @channel.setter
    def channel(self,value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        if self._enteredFrame:
            _, self._frame = self._capture.retrieve(
                channel = self._channel)
            return self._frame

    @property
    def isWritingImage(self):
        return self._imageFilename is not None

    @property
    def isWritingVideo(self):
        return self._videoFilename is not None

    def videoEncoding(self,encoding):
        self._videoEncoding = encoding
        return self._videoEncoding

    def videoWriter(self):
        fps = self._capture.get(cv2.cv.CV_CAP_PROP_FPS)
        if fps == 0.0:
        # The capture fps is unknown so use an estimate
            if self._framesElapsed < 20:
                self._videoWriter = None
                return
            elif self._fpsEstimate < 15:
                fps = 15
            else:
                fps = self._fpsEstimate
        size = (int(self._capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
                int(self._capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
        self._videoWriter = cv2.VideoWriter(self._videoFilename, self._videoEncoding, fps, size)

    def enterFrame(self):
        # capture the next frame, if any
        # but first, check that the previous frame is exited
        assert not self._enteredFrame, \
        'previous enterFrame() had no matching exitFrame()'
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        # Draw to the window, write to files, release the frames
        # check whether any grabbed frame is retrieved
        # the getter might retrieve and cache the frame
        if self._frame is None:
            self._enteredFrame = False
            return

        # update the FPS estimate and relative variables
        if self._framesElapsed == 0:
            self.startTime = time.clock()
        else:
            timeElapsed = time.clock()-self.startTime
            self._fpsEstimate = self._framesElapsed/timeElapsed
        self._framesElapsed += 1

        # Draw to the window, if any
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirrorFrame = np.fliplr(self._frame).copy()
                self.previewWindowManager.show(mirrorFrame)
            else:
                self.previewWindowManager.show(self._frame)

        # Write to the image file , if any
        if self.isWritingImage:
            cv2.imwrite(self._imageFilename, self._frame)
            self._imageFilename = None

        # Write to the video file, if any
        if self._videoWriter is None:
            self.videoWriter()
        if self.isWritingVideo and self._videoWriter is not None:
            self._videoWriter.write(self._frame)

        # release the frame
        self._frame = None
        self._enteredFrame = False

    def writeImage(self, filename):
        # write the next exited frame to an image file
        self._imageFilename = filename

    def startWritingVideo(self,filename):
        # start writing exited frames to a video file
        self._videoFilename = filename
        #self._videoEncoding = encoding

    def stopWritingVideo(self):
        # stop writing exited frames to a video file
        self._videoFilename = None
        #self._videoWriter = None
        #self._videoEncoding = None






# Window Manager
class WindowManager(object):
    def __init__(self, windowName, keypressCallback):
        self.keypressCallback = keypressCallback

        self._windowName = windowName
        self._isWindowCreated = False

    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True

    def show(self, frame):
        cv2.imshow(self._windowName, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False

    def processEvent(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            keycode &= 0xFF
            self.keypressCallback(keycode)






