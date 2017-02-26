import matplotlib.pyplot as plt
import numpy as np

def draw(function,x,y,printname=False):
    if printname==True:
        print "plot_decision_boundary"
        return 0

    x_max,x_min=x[:,0].max()+0.5,x[:,0].min()-0.5
    y_max,y_min=x[:,1].max()+0.5,x[:,1].min()-0.5
    h=0.01

    xx,yy=np.meshgrid(np.arange(x_min,x_max,h),np.arange(y_min,y_max,h))

    z=function(np.c_[xx.ravel(),yy.ravel()])
    z=z.reshape(xx.shape)

    plt.contourf(xx,yy,z,cmap=plt.cm.Spectral)
    plt.scatter(x[:,0],x[:,1],c=y,cmap=plt.cm.Spectral)


if __name__=='__main__':
    draw(printname=True)