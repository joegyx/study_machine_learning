#-*- coding:utf-8 -*-
import cv2
import math
import numpy as np

def getpoints():
    pointsArray=[]
    for n in range(1,7):
        points=[]
        for line in open(str(n)+".txt"):
            x,y=line.split(" ")
            points.append([int(x),int(y)])
        pointsArray.append(points)
    #print pointsArray
    #print len(pointsArray)
    return pointsArray

def getimg():
    imgArray=[]
    for n in range(1,7):
        img=cv2.imread("face"+str(n)+".jpg")
        img=np.float32(img)/255.0
        imgArray.append(img)
    #print imgArray
    #print len(imgArray)
    return imgArray

def similarityTransform(inPoints, outPoints) :
    s60 = math.sin(60*math.pi/180);
    c60 = math.cos(60*math.pi/180);

    inPts = np.copy(inPoints).tolist();
    outPts = np.copy(outPoints).tolist();

    xin = c60*(inPts[0][0] - inPts[1][0]) - s60*(inPts[0][1] - inPts[1][1]) + inPts[1][0];
    yin = s60*(inPts[0][0] - inPts[1][0]) + c60*(inPts[0][1] - inPts[1][1]) + inPts[1][1];

    inPts.append([np.int(xin), np.int(yin)]);

    xout = c60*(outPts[0][0] - outPts[1][0]) - s60*(outPts[0][1] - outPts[1][1]) + outPts[1][0];
    yout = s60*(outPts[0][0] - outPts[1][0]) + c60*(outPts[0][1] - outPts[1][1]) + outPts[1][1];

    outPts.append([np.int(xout), np.int(yout)]);

    tform = cv2.estimateRigidTransform(np.array([inPts]), np.array([outPts]), False);

    return tform

def rectContains(rect, point) :
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[2] :
        return False
    elif point[1] > rect[3] :
        return False
    return True

def calculateDelaunayTriangles(rect, points):
    subdiv=cv2.Subdiv2D(rect)

    for p in points:
        subdiv.insert((p[0],p[1]))

    triangleList = subdiv.getTriangleList()
    delaunayTri = []

    for t in triangleList:
        pt=[]
        pt.append((t[0],t[1]))
        pt.append((t[2],t[3]))
        pt.append((t[4],t[5]))

        pt1=(t[0],t[1])
        pt2=(t[2],t[3])
        pt3=(t[4],t[5])

        if rectContains(rect,pt1) and rectContains(rect,pt2) and rectContains(rect,pt3):
            ind=[]
            for j in xrange(0,3):
                for k in xrange(0,len(points)):
                    if (abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0):
                        ind.append(k)
            if len(ind)==3:
                delaunayTri.append((ind[0],ind[1],ind[2]))

    return delaunayTri

def constrainPoint(p, w, h):
    p = (min(max(p[0],0),w-1),min(max(p[1],0),h-1))
    return p

def applyAffineTransform(src, srcTri, dstTri, size) :
    warpMat = cv2.getAffineTransform(np.float32(srcTri), np.float32(dstTri))
    dst = cv2.warpAffine(src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT_101)
    return dst

def warpTriangle(img1, img2, t1, t2):
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    t1Rect=[]
    t2Rect=[]
    t2RectInt=[]
    for i in xrange(0,3):
        t1Rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
        t2RectInt.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))

    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2RectInt), (1.0, 1.0, 1.0), 16, 0)
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    size = (r2[2], r2[3])

    img2Rect = applyAffineTransform(img1Rect, t1Rect, t2Rect, size)
    img2Rect = img2Rect * mask
    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] * ((1.0, 1.0, 1.0) - mask)
    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] + img2Rect

w=600
h=600
allpoints=getpoints()
allimg=getimg()
eye=[ (np.int(0.3 * w ), np.int(h / 3)), (np.int(0.7 * w ), np.int(h / 3)) ]
boundary=np.array([(0,0), (w/2,0), (w-1,0), (w-1,h/2), ( w-1, h-1 ), ( w/2, h-1 ), (0, h-1), (0,h/2) ])
pointsAvg = np.array([(0,0)]* ( len(allpoints[0]) + len(boundary) ), np.float32())
#n=allpoints[0]
numimg=len(allimg)
imagesNorm = [];
pointsNorm = [];

for i in xrange(0,numimg):
    points1=allpoints[i]
    eyepoint=[allpoints[i][36],allpoints[i][45]]
    tform = similarityTransform(eyepoint, eye)
    img = cv2.warpAffine(allimg[i], tform, (w, h))

    points2 = np.reshape(np.array(points1), (68, 1, 2))
    points = cv2.transform(points2, tform)
    points = np.float32(np.reshape(points, (68, 2)))

    points = np.append(points, boundary, axis=0)
    pointsAvg= pointsAvg+points/numimg
    pointsNorm.append(points)
    imagesNorm.append(img)

rect=(0,0,w,h)
dt=calculateDelaunayTriangles(rect,np.array(pointsAvg))

output = np.zeros((h,w,3), np.float32())
for i in xrange(0,len(imagesNorm)):
    img = np.zeros((h, w, 3), np.float32())
    for j in xrange(0,len(dt)):
        tin=[]
        tout=[]
        for k in xrange(0,3):
            #print "i:{},j:{},k:{}".format(i,j,k)
            pin=pointsNorm[i][dt[j][k]]
            pin=constrainPoint(pin,w,h)

            pout=pointsAvg[dt[j][k]]
            pout=constrainPoint(pout,w,h)

            tin.append(pin)
            tout.append(pout)

        warpTriangle(imagesNorm[i], img, tin, tout)

    output=output+img
output = output / numimg

cv2.imshow('image', output)
output=output*255
cv2.imwrite('1.jpg',output, [int( cv2.IMWRITE_JPEG_QUALITY), 100])
cv2.waitKey(0)

