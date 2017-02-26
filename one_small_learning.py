#coding:UTF-8
import numpy as np

def nonlin(x,deriv=False):
    if deriv==True:
        return x*(1-x)
    return 1/(1+np.exp(-x))

#input 四条数据，每条数据三个参数
x=np.array([[1,0,1,0],
            [0,1,1,0],
            [1,1,0,1],
            [0,0,1,1],
            [1,0,0,1],
            [0,1,1,1]])

#output 每条数据一个输出
y=np.array([[1,1,0,0,0,0]]).T

#random seed
np.random.seed(1)

syn0=2*np.random.random((4,1))-1#还不是很懂 3×1矩阵，每个数字代表每个参数的权重

for i in xrange(10000):
    l0=x
    l1=nonlin(np.dot(l0,syn0))

    l1_error=y-l1

    l1_delta=l1_error*nonlin(l1,True)

    syn0=syn0+np.dot(l0.T,l1_delta)

#print "l1:"
#print l1
#print "syn0:"
#print syn0
print nonlin(np.dot(np.array([1,1,0,0]),syn0))
