#!/usr/bin/env python3

import os
import sys
from met_util import wav_split, segment

def main():
    bpm = int(sys.argv[1])
    sec = int(sys.argv[2])
    
    # sample data
    hdr, data = wav_split('s3.wav')
    metronome = segment(bpm, sec, data)

    # write to file
    outf = open('a.wav', 'wb')
    hdr.sub_chunk2_sz += len(metronome)
    outf.write( hdr.pack())
    outf.write(metronome)
    outf.close()

if __name__ == '__main__':
    main()
