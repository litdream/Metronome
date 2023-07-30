#!/usr/bin/env python

import os
import sys
import time
import getopt

bump_up = 0

sa = "hU:"
la = ('help', 'bump-up=')
o,argv = getopt.getopt(sys.argv[1:], sa, la)

def usage():    
    print '''\
USAGE: %s [options]  DAT_FILE
  -h, --help             help screen
  -U, --bump-up=INT      bump up speed
''' % sys.argv[0]

if len(o) + len(argv) == 0:  usage(); sys.exit(1)
for k,v in o:
    if k in ('-h','--help'):
        usage(); sys.exit(0)
    if k in ('-U','--bump-up'):
        bump_up = int(v)

prgfile=argv[0]
for line in open(prgfile):
    line = line.strip()
    if len(line) == 0: continue

    working, dura, rest = tuple(line.split())
    cur_speed = int(working) + bump_up
    os.system("python Metronome.py -t %d --gradual-dura=%s" % (cur_speed, dura))
    print '''

WORKING : %d

''' % cur_speed
    os.system("mplayer a.wav > /dev/null")
    
    time.sleep( int(rest))
