#!/usr/bin/env python

import sys
import os
import time
import shutil

print "USAGE: %s <plan_number>\n" % sys.argv[0]
inputfile="input.csv"
plan=sys.argv[1]

hsh={}
for l in open(inputfile):
    arr=l.split(',')
    hsh[ arr[0]] = arr

selected=hsh[plan]
os.system("./Metronome.py %s" % selected[2])
time.sleep(0.2)

base_file="%s_%s.wav" % (selected[0], selected[1])
shutil.move("a.wav", base_file)
time.sleep(0.2)

endure_param=selected[4] % int(selected[3])
os.system("./Metronome.py %s" % endure_param)
time.sleep(0.2)

endure_file="%s_%s_endure.wav" % (selected[0], selected[1])
shutil.move("a.wav", endure_file)
