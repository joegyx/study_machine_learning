#-*- coding:utf-8 -*-
#脸部68点
import dlib
import numpy
from skimage import io

tool68path="shape_predictor_68_face_landmarks.dat"
imgpath="face7.jpg"

tool=dlib.get_frontal_face_detector()
tool68=dlib.shape_predictor(tool68path)

win=dlib.image_window()
img=io.imread(imgpath)

win.clear_overlay()
win.set_image(img)

#dets=tool(img,1)
def point68(im):
    de=tool(im,1)
    shape=tool68(im,de[0])
    f = open("7.txt", 'w')
    for p in shape.parts():
        f.write(str(p.x)+" "+str(p.y)+"\n")
    #mix=numpy.matrix([[p.x,p.y]for p in shape.parts()])
    f.close()
    print "finish"
    win.add_overlay(shape)
    return 0
'''
for i,d in enumerate(dets):
    print "left:{} top:{} right:{} bottom:{}".format(d.left(),d.top(),d.right(),d.bottom())
    shape=tool68(img,d)
    win.add_overlay(shape)
win.add_overlay(dets)
'''
point68(img)
win.wait_until_closed()