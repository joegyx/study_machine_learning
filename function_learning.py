import numpy as np
import  matplotlib.pyplot as plt
from sklearn import datasets
import plot_decision_boundary
def sigmoid(x,deriv=False):
    if deriv==True:
        return x*(1-x)
    return 1/(1+np.exp(-x))

def to_result(y):
    r=[]
    for i in y:
        if i == 0:
            r.append([1, 0])
        elif i == 1:
            r.append([0, 1])
        else:
            print "to_result_function_error"
            return 0
    return np.array(r)

hidden_num=4
study_rate=0.1

np.random.seed(1)
x,y=datasets.make_moons(200,noise=0.3)
syn0=2*np.random.random((2,hidden_num))-1
b0=np.zeros((1,hidden_num))
syn1=2*np.random.random((hidden_num,2))-1
b1=np.zeros((1,2))
r=to_result(y)

for i in xrange(500000):
    l0=x
    l1=sigmoid(np.dot(l0,syn0)+b0)
    l2=sigmoid(np.dot(l1,syn1)+b1)

    l2_error=r-l2

    if(i%10000==0):
        print "l2_error:{}".format(np.mean(np.abs(l2_error)))

    l2_delta=l2_error*sigmoid(l2,True)
    l1_error=np.dot(l2_delta,syn1.T)
    l1_delta=l1_error*sigmoid(l1,True)

    #study_rate=np.mean(np.abs(l2_error))

    syn1=syn1+study_rate*np.dot(l1.T,l2_delta)
    #b1=b1+l2_delta
    b1 = b1 +study_rate*np.mean(l2_delta,axis=0)
    syn0=syn0+study_rate*np.dot(l0.T,l1_delta)
    #b0=b0+l1_delta
    b0 = b0 +study_rate*np.mean(l1_delta,axis=0)

#print "b0:{},b1:{}".format(b0,b1)

def pridict(In,syn,b):
    In0=In
    In1=sigmoid(np.dot(In0,syn[0])+b[0])
    In2=sigmoid(np.dot(In1,syn[1])+b[1])
    Out=In2
    return np.argmax(Out, axis=1)

syn=[syn0,syn1]
b=[b0,b1]
plot_decision_boundary.draw(lambda x:pridict(x,syn,b),x,y)
plt.show()

