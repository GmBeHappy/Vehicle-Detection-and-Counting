import os
import sys
import glob
import cv2
import dlib
import itertools
class Rectangle:
    def intersection(self, other):
        a, b = self, other
        x1 = max(min(a.x1, a.x2), min(b.x1, b.x2))
        y1 = max(min(a.y1, a.y2), min(b.y1, b.y2))
        x2 = min(max(a.x1, a.x2), max(b.x1, b.x2))
        y2 = min(max(a.y1, a.y2), max(b.y1, b.y2))
        if x1<x2 and y1<y2:
            return type(self)(x1, y1, x2, y2)
    __and__ = intersection

    def difference(self, other):
        inter = self&other6
        if not inter:
            yield self
            return
        xs = {self.x1, self.x2}
        ys = {self.y1, self.y2}
        if self.x1<other.x1<self.x2: xs.add(other.x1)
        if self.x1<other.x2<self.x2: xs.add(other.x2)
        if self.y1<other.y1<self.y2: ys.add(other.y1)
        if self.y1<other.y2<self.y2: ys.add(other.y2)
        for (x1, x2), (y1, y2) in itertools.product(
            pairwise(sorted(xs)), pairwise(sorted(ys))
        ):
            rect = type(self)(x1, y1, x2, y2)
            if rect!=inter:
                yield rect
    __sub__ = difference
    def __init__(self, x1, y1, x2, y2):
        if x1>x2 or y1>y2:
            raise ValueError("Coordinates are invalid")
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
    def __iter__(self):
        yield self.x1
        yield self.y1
        yield self.x2
        yield self.y2
    def __eq__(self, other):
        return isinstance(other, Rectangle) and tuple(self)==tuple(other)
    def __ne__(self, other):
        return not (self==other)

    def __repr__(self):
        return type(self).__name__+repr(tuple(self))
def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
faces_folder = r'C:\Users\gmplk\Desktop\TrainHOG\TrainHOG\TrainHOG'
detector = dlib.simple_object_detector("detector.svm")
detector2 = dlib.simple_object_detector("detectorcarbig.svm")
win_det = dlib.image_window()
win_det.set_image(detector)
win_det2 = dlib.image_window()
win_det2.set_image(detector2)
cap = cv2.VideoCapture('DJI_0083.MP4')
i=0;
q=0
countmoto=0
countcar =0
win = dlib.image_window()
while(True):
	try:
		_,frame = cap.read()
		frame = cv2.resize(frame,(0,0),fx = 0.88,fy = 0.88)
		frame = frame[350:800,500:1300]
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		if(i==0):
			print(q)
			dets = detector(frame)
			print("Number of moto detected: {}".format(len(dets)))
			for k, d in enumerate(dets):
				newcentralI      = int((d.top()+d.bottom())/2)
				newcentral       = int((d.left()+d.right())/2)
				#cv2.line(frame,(450,10),(450,800),(0,255,0),5)
				cv2.circle(frame,(int((newcentral)),int((newcentralI))),2,(200,0,0),2)
				if(newcentralI<800 and 10<newcentralI and 430<newcentral and newcentral<470):
					countmoto    = countmoto+1
					cv2.circle(frame,(int((newcentral)),int((newcentralI))),20,(200,200,0),10)
			dets2 =detector2(frame)
			print("Number of car detected: {}".format(len(dets2)))
			for k, d in enumerate(dets2):
				newcentralI      = int((d.top()+d.bottom())/2)
				newcentral       = int((d.left()+d.right())/2)
				#cv2.line(frame,(500,10),(500,800),(0,0,255),5)
				cv2.circle(frame,(int((newcentral)),int((newcentralI))),2,(0,200,0),2)
				if( newcentral<500 and 490<newcentral and newcentralI<8000 and 10<newcentralI ):
					countcar     = countcar+1
					cv2.circle(frame,(int((newcentral)),int((newcentralI))),20,(0,200,0),10)
			font = cv2.FONT_HERSHEY_SIMPLEX
			yyy = ((3.138049*len(dets)) + (3.650786*len(dets2)) - 1.56418) 
			cv2.putText(frame,"moto : {}".format(len(dets)),(20,50), font, 1,(255,255,255),2,cv2.LINE_AA)
			cv2.putText(frame,"car  : {}".format(len(dets2)),(20,100), font, 1,(255,255,255),2,cv2.LINE_AA)
			#cv2.putText(frame,"CO   : {:.3}  ppm".format(yyy),(20,150), font, 1,(255,255,255),2,cv2.LINE_AA)
			win.clear_overlay()
			win.set_image(frame)
			win.add_overlay(dets)
			win.add_overlay(dets2)
			i=2
		else:
			i=i-1
	except:
		pass