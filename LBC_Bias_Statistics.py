#!/usr/bin/env python3
# /opt/anaconda/bin/python
# coding: utf-8


import numpy as np
from astropy.io import fits
from astropy import stats
import matplotlib.pyplot as plt
import argparse


# Enter the name of the list of biases

# In[4]:

parser = argparse.ArgumentParser(description = 'bias statistics')

parser.add_argument('blist', type=str, help = 'file list')
parser.add_argument('statreg', type=str, help = 'region for stats  [c1,c2,r1,r2]')

args = parser.parse_args()

blist = args.blist
statreg = args.statreg
sr = str.split(statreg,",")
dc1= int(str.split(sr[0],"[")[1]) 
dc2= int(sr[1])
dr1= int(sr[2])
dr2= int(str.split(sr[3],"]")[0])

title = blist + "_" + statreg

#blist = "LBCR.list"
#title = "LBCR 20200830"

outfile1 = blist + "_chip1"
outfile2 = blist + "_chip2"
outfile3 = blist + "_chip3"
outfile4 = blist + "_chip4"
resfile = blist + ".res"
pltfile = blist + ".png"

g = open(resfile,"w")

# overscan region
oc1 = 2151
#oc1 = 2099
oc2 = 2303
or1 = 0
or2 = 4607

# prescan region
pc1 = 0
pc2 = 49
pr1 = 0 
pr2 = 4607

# data region
#dc1 = 50
#dc2 = 2097
#dr1 = 0 
#dr2 = 4607
#dc1 = 601
#dc2 = 1600
#dr1 = 2501
#dr2 = 3500


with open(blist,"r") as my_file:
     b = my_file.readlines()


#fi = [fits.open(f.strip()) for f in b]


mean = np.zeros((len(b),4))
med = np.zeros((len(b),4))
sig = np.zeros((len(b),4))
omean = np.zeros((len(b),4))
omed = np.zeros((len(b),4))
osig = np.zeros((len(b),4))
td = []
next = []
i=0
for f in b:
   fi = fits.open(f.strip())
   n =  fi[0].header['NEXTEND']
   td.append((fi)[0].header['MJD_OBS'])
   for j in range(n):  
      # the 2D array data contains the pixel values for chip j+1 
      data = (fi[j+1].data)[dr1:dr2,dc1:dc2]
      oscan = (fi[j+1].data)[or1:or2,oc1:oc2]
      mms = stats.sigma_clipped_stats(data,sigma=3,maxiters=5)
      omms = stats.sigma_clipped_stats(oscan,sigma=3,maxiters=5)
      mean[i][j] = mms[0]
      med[i][j] = mms[1]
      sig[i][j]= mms[2]
      omean[i][j] = omms[0]
      omed[i][j] = omms[1]
      osig[i][j]= omms[2]
      print("%s %.2f %.2f %.2f \n" % (f,mean[i][j],med[i][j],sig[i][j]))
   i=i+1
            
newa = np.zeros((len(td),n,7))
for j in range(4):
   newa[:,j,0] = td
   newa[:,j,1] = mean[:,j]
   newa[:,j,2] = med[:,j]
   newa[:,j,3] = sig[:,j]
   newa[:,j,4] = omean[:,j]
   newa[:,j,5] = omed[:,j]
   newa[:,j,6] = osig[:,j]
np.savetxt(outfile1,newa[:,0,:],fmt="%f %.2f %.2f %.2f %.2f %.2f %.2f")
np.savetxt(outfile2,newa[:,1,:],fmt="%f %.2f %.2f %.2f %.2f %.2f %.2f")
np.savetxt(outfile3,newa[:,2,:],fmt="%f %.2f %.2f %.2f %.2f %.2f %.2f")
np.savetxt(outfile4,newa[:,3,:],fmt="%f %.2f %.2f %.2f %.2f %.2f %.2f")
            
plt.plot(td,mean[:,0],"b.",linestyle='',lw=3,label="chip1 mean")
plt.plot(td,mean[:,1],"r.",linestyle='',lw=3,label="chip2 mean")
plt.plot(td,mean[:,2],"g.",linestyle='',lw=3,label="chip3 mean")
plt.plot(td,mean[:,3],"k.",linestyle='',lw=3,label="chip4 mean")

plt.plot(td,omean[:,0],"b+",linestyle='',label="chip1 mean overscan")
plt.plot(td,omean[:,1],"r+",linestyle='',label="chip2 mean overscan")
plt.plot(td,omean[:,2],"g+",linestyle='',label="chip3 mean overscan")
plt.plot(td,omean[:,3],"k+",linestyle='',label="chip4 mean overscan")
#
#plt.errorbar(td,mean[:,0],yerr=sig[:,0],ecolor="b",linestyle='None')
#plt.errorbar(td,mean[:,1],yerr=sig[:,1],ecolor="r",linestyle='None')
#plt.errorbar(td,mean[:,2],yerr=sig[:,2],ecolor="g",linestyle='None')
#plt.errorbar(td,mean[:,3],yerr=sig[:,3],ecolor="k",linestyle='None')
#
#plt.plot(td,med[:,0],"b.",linestyle='-.')
#plt.plot(td,med[:,1],"r.",linestyle='-.')
#plt.plot(td,med[:,2],"g.",linestyle='-.')
#plt.plot(td,med[:,3],"k.",linestyle='-.')
#
plt.xlabel("Time [MJD]")
plt.ylabel("3-sigma clipped mean bias level [ADU]; mean overscan level (dotted)")
#plt.legend()

plt.title(title)

head = ("chip: mean rms   rdnoise rms\n")
g.write(head)

for i in range(4):
    mmean = np.mean(mean[:,i])
    mstd = np.std(mean[:,i],ddof=1)
    smean = np.mean(sig[:,i])
    sstd = np.std(sig[:,i],ddof=1)
    oscan_mmean = np.mean(omean[:,i])
    oscan_mstd = np.std(omean[:,i],ddof=1)
    oscan_smean = np.mean(osig[:,i])
    oscan_sstd = np.std(osig[:,i],ddof=1)

    print ("chip %d: mean=%.2f rms=%.2f readnoise: ssig=%.2f sstd=%.2f" % (i+1,mmean,mstd,smean,sstd))
    line = ("chip %d: mean=%.2f rms=%.2f readnoise: ssig=%.2f sstd=%.2f" % (i+1,mmean,mstd,smean,sstd))
    plt.hlines(mmean,min(td),max(td),"b",label=line)
    g.write(line)
    g.write("\n")
    oline = ("chip %d: omean=%.2f orms=%.2f noise: osig=%.2f ostd %.2f" % (i+1,oscan_mmean,oscan_mstd,oscan_smean,oscan_sstd))
    g.write(oline)
    g.write("\n")

g.close()
plt.legend()
plt.savefig(pltfile)
plt.show()
