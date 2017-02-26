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
y=np.array([[1,1,0,0,0,0]]).T

np.random.seed(1)
#with mean 0
syn0=2*np.random.random((4,4))-1
syn1=2*np.random.random((4,1))-1

for i in xrange(100000):
    l0=x
    l1=sigmoid(np.dot(l0,syn0))
    l2=sigmoid(np.dot(l1,syn1))

    l2_error=y-l2

    if(i%10000==0):
        print "l2_error:{}".format(np.mean(np.abs(l2_error)))

    l2_delta=l2_error*sigmoid(l2,True)
    l1_error=np.dot(l2_delta,syn1.T)
    l1_delta=l1_error*sigmoid(l1,True)

    syn1=syn1+np.dot(l1.T,l2_delta)
    syn0=syn0+np.dot(l0.T,l1_delta)

#INPUT
def pridict(In,syn):
    In0=In
    In1=sigmoid(np.dot(In0,syn[0]))
    In2=sigmoid(np.dot(In1,syn[1]))
    Out=In2
    return Out

In=np.array([1,1,0,0])
syn=[syn0,syn1]
print pridict(In,syn)
