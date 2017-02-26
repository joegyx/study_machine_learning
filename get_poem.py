#coding=UTF-8
import urllib2
from bs4 import BeautifulSoup
import time
Input=[]

for n in range(901):
    try:
        url="http://www.gushiwen.org/wen_"+str(n+1109)+".aspx"
        html=urllib2.urlopen(url).read()
        bs=BeautifulSoup(html, "html.parser")
        poem=bs.find("div",{"class":"authorShow"})
        txt=poem.get_text().encode("UTF-8")
        txt=txt.replace(' ','\n')
        Input.append(txt)
        print n
        time.sleep(0.5)
    except Exception as e:
        print e

f=open("poem.txt","w")
f.writelines(Input)
print "success"