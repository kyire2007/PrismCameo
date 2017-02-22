import cv2
import filter
from managers import CaptureManager, WindowManager

class Cameo(object):
    def __init__(self):
        self._windowManager = WindowManager('cameo',
                                            self.onKeyPress)
        self._captureManager = CaptureManager(
            cv2.VideoCapture(0), self._windowManager, False)

        self._curveFilter = filter.BGRPortaCurveFilter()

    def run(self):
        self._windowManager.createWindow()
        self._captureManager.videoEncoding(cv2.cv.CV_FOURCC('I','4','2','0'))

        while self._windowManager.isWindowCreated:
           # print self._captureManager._videoWriter
            self._captureManager.enterFrame()
            frame = self._captureManager.frame

            filter.strokeEdges(frame, frame)
            self._curveFilter.apply(frame, frame)


            self._captureManager.exitFrame()
            self._windowManager.processEvent()

    def onKeyPress(self, keycode):
        if keycode == 32:
            self._captureManager.writeImage('screenshot.png')
            print 'screen shot taken'
        elif keycode == 9:
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo('screenshot.avi')
                print 'video record on'
            else:
                self._captureManager.stopWritingVideo()
                print 'video record off'
        elif keycode == 27:
            self._windowManager.destroyWindow()
            print 'close all'

if __name__ == '__main__':
    Cameo().run()
