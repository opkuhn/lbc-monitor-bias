#!/opt/anaconda/bin/python

import numpy as np
import string as str
import os
import sys
import time
from sys import argv, exit
import getopt

#----------------------------------------------------------------
#
# printUsage - print a simple usage message
#

def printUsage(): 
  #print ("\nUsage: getheadlist [gethead option] inlist keyword1 [keyword2 keyword3 ... keywordN]" )
  print ("\nUsage: getheadlist inlist keyword1 [keyword2 keyword3 ... keywordN]" )
  print ("\nWhere:")
  print ("  inlist = list of files for gethead" )
  #print ("  option = gethead options, e.g -p or -b")
  print ("  keyword 1...N = keywords to be queried" )

#
# Main Program starts here...
#

# Parse the command-line arguments (GNU-style getopt)
  
try:
  opts, files = getopt.gnu_getopt(argv[1:],'pb')
except getopt.GetoptError:
  printUsage()
  exit(2)

if len(opts)==0 and len(files)==0:
  printUsage()
  exit(1)

#for opt, arg in opts:
  #if opt in ('-p','--verbose'):
    #Verbose = True
  #elif opt in ('-V','--version'):
    #print ("mdisp.py v%s [%s]" % (versNum, versDate))
    #exit(0)

numFiles = len(files)
numkeys = len(files)-1
keyword = []

if numFiles < 2:
  printUsage()
  exit(1)
  
inlist = files[0]

for i in range(numkeys):
   keyword.append(files[i+1])

keylist =  " ".join(keyword)

afiles = []
with open(inlist,"r") as my_file:
   for line in my_file:
      if not line.startswith("#"):
         afiles.append(line)

for file in afiles:

   cmd = ("gethead -p -b %s %s" % (file.split()[0],keylist))

   os.system(cmd)
