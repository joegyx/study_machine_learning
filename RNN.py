#coding=UTF-8
import numpy as np

data=open("poem.txt","rw").read()
data=data.decode('utf-8')
chars=list(set(data))

data_size=len(data)
char_size=len(chars)

char_to_ix={ch:i for i,ch in enumerate(chars)}
ix_to_char={i:ch for i,ch in enumerate(chars)}


hidden_size=200
seq_length=25#number of steps to unroll the RNN for
rate=0.1

W_xh=np.random.randn(hidden_size,char_size)*0.01
W_hh=np.random.randn(hidden_size,hidden_size)*0.01
W_hy=np.random.randn(char_size,hidden_size)*0.01

bh=np.zeros((hidden_size,1))
by=np.zeros((char_size,1))

def sample(h,seed_ix,n):
    x=np.zeros((char_size,1))
    x[seed_ix]=1
    ixes=[]
    for t in xrange(n):
        h=np.tanh(np.dot(W_xh,x)+np.dot(W_hh,h)+bh)
        y=np.dot(W_hy,h)+by
        p=np.exp(y)/np.sum(np.exp(y))
        ix=np.random.choice(range(char_size),p=p.ravel())
        x=np.zeros((char_size,1))
        x[ix]=1
        ixes.append(ix)
    return ixes

def Lossfunction(inputs,targets,hprev):
    xs,hs,ys,ps={},{},{},{}
    hs[-1]=np.copy(hprev)
    loss=0

    for t in xrange(len(inputs)):
        xs[t]=np.zeros((char_size,1))
        xs[t][inputs[t]]=1
        hs[t]=np.tanh(np.dot(W_xh,xs[t])+np.dot(W_hh,hs[t-1])+bh)
        ys[t]=np.dot(W_hy,hs[t])+by
        ps[t]=np.exp(ys[t])/np.sum(np.exp(ys[t]))
        #loss=loss-np.log(ps[t][targets[t],0])
        loss += -np.log(ps[t][targets[t], 0])

    dWxh,dWhh,dWhy=np.zeros_like(W_xh),np.zeros_like(W_hh),np.zeros_like(W_hy)
    dbh,dby=np.zeros_like(bh),np.zeros_like(by)
    dhnext=np.zeros_like(hs[0])
    for t in reversed(xrange(len(inputs))):
        dy=np.copy(ps[t])
        dy[targets[t]]-=1
        dWhy+=np.dot(dy,hs[t].T)
        dby+=dy
        dh=np.dot(W_hy.T,dy)+dhnext
        dhraw=(1-hs[t]*hs[t])*dh
        dbh += dhraw
        dWxh+=np.dot(dhraw,xs[t].T)
        dWhh += np.dot(dhraw, hs[t - 1].T)
        dhnext=np.dot(W_hh.T,dhraw)

    for dparam in [dWxh,dWhh,dWhy,dbh,dby]:
        np.clip(dparam,-5,5,out=dparam)

    return loss, dWxh, dWhh, dWhy, dbh, dby, hs[len(inputs)-1]

n,p=0,0
#零矩阵
mW_xh,mW_hh,mW_hy=np.zeros_like(W_xh),np.zeros_like(W_hh),np.zeros_like(W_hy)
mbh,mby=np.zeros_like(bh),np.zeros_like(by)
smooth_loss=-np.log(1.0/char_size)*seq_length#???

for n in range(300000):
    if p+seq_length+1>=len(data) or n==0:
        hprev=np.zeros((hidden_size,1))#???
        p=0
        #载入输入和训练目标
    inputs=[char_to_ix[ch] for ch in data[p:p+seq_length]]
    targets=[char_to_ix[ch] for ch in data[p+1:p+seq_length+1]]

    if n%1000==0:
        sample_ix=sample(hprev,inputs[0],200)
        txt="".join(ix_to_char[ix] for ix in sample_ix)
        print "\n============================\n"+txt+"\n============================\n"

    loss, dWxh, dWhh, dWhy, dbh, dby, hprev=Lossfunction(inputs,targets,hprev)
    #loss, dWxh, dWhh, dWhy, dbh, dby, hprev = lossFun(inputs, targets, hprev)
    smooth_loss=smooth_loss*0.999+loss*0.001

    if n%100==0:
        print "iter:{},loss:{}".format(n,smooth_loss)

    for param,dparam,mem in zip([W_xh,W_hh,W_hy,bh,by],
                                [dWxh,dWhh,dWhy,dbh,dby],
                                [mW_xh,mW_hh,mW_hy,mbh,mby]):
        mem+=dparam*dparam
        param += -rate * dparam / np.sqrt(mem + 1e-8)

    p=p+seq_length
