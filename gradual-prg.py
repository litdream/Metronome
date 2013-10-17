#!/usr/bin/env python

import os
import sys
import time

prgfile=sys.argv[1]
for line in open(prgfile):
    line = line.strip()
    if len(line) == 0: continue

    working, dura, rest = tuple(line.split())
    os.system("python Metronome.py -t %s --gradual-dura=%s" % (working, dura))
    print '''

WORKING : %s

''' % working
    os.system("mplayer a.wav > /dev/null")
    
    time.sleep( int(rest))
