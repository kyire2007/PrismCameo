import cv2
import numpy
import scipy.interpolate as fit

def createCurveFunc(points):
    if points is None:
        return None

    numPoints = len(points)
    if numPoints < 2:
        return None

    xs, ys = zip(*points)
    if numPoints < 4:
        kind = 'linear'
    else:
        kind = 'cubic'

    return fit.interp1d(xs, ys, kind, bounds_error = False)

def createLookupArray(func, length = 256):
    if func is None:
        return None
    lookupArray = numpy.empty(length)
    i = 0
    while i < length:
        func_i = func(i)
        lookupArray[i] = min(max(0, func_i), length-1)
        i += 1
    return lookupArray

def applyLookupArray(lookupArray, src, dst):
    if lookupArray is None:
        return
    dst[:] = lookupArray[src]

def createCompositeFunc(func0, func1):
    if func0 is None:
        return func1
    if func1 is None:
        return func0
    return lambda x: func0(func1(x))

def createFlatView(array):
    flatView = array.view()
    flatView.shape = array.size
    return flatView





