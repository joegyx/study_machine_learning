#-*- coding:utf-8 -*-
#把脸框出来
import dlib
from skimage import io

tool=dlib.get_frontal_face_detector()

win=dlib.image_window()

img_path="face7.jpg"

img=io.imread(img_path)
dets=tool(img,1)
for i,d in enumerate(dets):
    print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(i, d.left(), d.top(), d.right(), d.bottom()))

win.set_image(img)
win.add_overlay(dets)

win.wait_until_closed()

