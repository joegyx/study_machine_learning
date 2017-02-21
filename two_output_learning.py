import numpy as np

def sigmoid(x,deriv=False):
    if deriv==True:
        return x*(1-x)
    return 1/(1+np.exp(-x))

#input
x=np.array([[1,0,1,0],
            [0,1,1,0],
            [1,1,1,1],
            [0,0,1,1],
            [1,0,0,1],
            [0,1,1,1]])

#output
y=np.array([[0,1],
           [0,1],
           [1,0],
           [1,0],
           [1,0],
           [1,0]])#1,1,0,0,0,0

np.random.seed(1)
#with mean 0
syn0=2*np.random.random((4,4))-1
b0=np.zeros((1,4))
syn1=2*np.random.random((4,2))-1
b1=np.zeros((1,2))

for i in xrange(100000):
    l0=x
    l1=sigmoid(np.dot(l0,syn0)+b0)
    l2=sigmoid(np.dot(l1,syn1)+b1)

    l2_error=y-l2

    if(i%10000==0):
        print "l2_error:{}".format(np.mean(np.abs(l2_error)))

    l2_delta=l2_error*sigmoid(l2,True)
    l1_error=np.dot(l2_delta,syn1.T)
    l1_delta=l1_error*sigmoid(l1,True)

    syn1=syn1+np.dot(l1.T,l2_delta)
    b1=b1+np.sum(l2_delta,axis=0)
    syn0=syn0+np.dot(l0.T,l1_delta)
    b0=b0+np.sum(l1_delta,axis=0)

print "b0:{},b1:{}".format(b0,b1)