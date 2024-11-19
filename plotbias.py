#!/usr/bin/env python3
# /opt/anaconda/bin/python

import numpy as np
import argparse
import datetime
from datetime import datetime, time
import matplotlib.pyplot as pl
import matplotlib.dates as mdates

parser = argparse.ArgumentParser(description = 'plot bias stats')
parser.add_argument('chip1', type=str, help = 'chip1')
parser.add_argument('chip2', type=str, help = 'chip2')
parser.add_argument('chip3', type=str, help = 'chip3')
parser.add_argument('chip4', type=str, help = 'chip4')
parser.add_argument('datefile', type=str, help = 'dates')
args = parser.parse_args()


chip1file = args.chip1
chip2file = args.chip2
chip3file = args.chip3
chip4file = args.chip4
datefile = args.datefile

root = chip1file.split(".")[0]
pngfile = root + ".png"

chip1 = np.genfromtxt(chip1file,dtype=str)
chip2 = np.genfromtxt(chip2file,dtype=str)
chip3 = np.genfromtxt(chip3file,dtype=str)
chip4 = np.genfromtxt(chip4file,dtype=str)
dates = np.genfromtxt(datefile,dtype=str)

mn1 = chip1[:,1].astype(float)
mn2 = chip2[:,1].astype(float)
mn3 = chip3[:,1].astype(float)
mn4 = chip4[:,1].astype(float)
rn1 = chip1[:,3].astype(float)
rn2 = chip2[:,3].astype(float)
rn3 = chip3[:,3].astype(float)
rn4 = chip4[:,3].astype(float)

dt = []
for i in range(len(dates)):
 dt.append(datetime.strptime(dates[i,1],"%Y-%m-%dT%H:%M:%S.%f"))

fig, ax = pl.subplots(2,1)

ax1=ax[0]
ax2=ax[1]

locator = mdates.AutoDateLocator()
formatter = mdates.AutoDateFormatter(locator)
ax1.xaxis.set_major_locator(locator)
ax1.xaxis.set_major_formatter(formatter)

ax1.plot(dt,mn1,'b*',label="bias_chip1")
ax1.plot(dt,mn2,'r*',label="bias_chip2")
ax1.plot(dt,mn3,'g*',label="bias_chip3")
ax1.plot(dt,mn4,'k*',label="bias_chip4")
ax1.plot(dt,mn1,c='b',ls=':')
ax1.plot(dt,mn2,c='r',ls=':')
ax1.plot(dt,mn3,c='g',ls=':')
ax1.plot(dt,mn4,c='k',ls=':')

ax1.legend()

ax2.xaxis.set_major_locator(locator)
ax2.xaxis.set_major_formatter(formatter)
ax2.plot(dt,rn1,'b*',label="RN_1")
ax2.plot(dt,rn2,'r*',label="RN_2")
ax2.plot(dt,rn3,'g*',label="RN_3")
ax2.plot(dt,rn4,'k*',label="RN_4")
ax2.plot(dt,rn1,c='b',ls=':')
ax2.plot(dt,rn2,c='r',ls=':')
ax2.plot(dt,rn3,c='g',ls=':')
ax2.plot(dt,rn4,c='k',ls=':')

ax2.set_xlabel("UT")
ax1.set_ylabel("Mean Bias [ADU]")
ax2.set_ylabel("Readnoise [ADU]") 

pl.savefig(pngfile)

pl.show()
