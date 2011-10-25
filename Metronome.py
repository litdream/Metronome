#!/usr/bin/env python

import os
import sys
import struct
import getopt

empty_sound = struct.pack('bbbbbbbb', *( 4,0,0,0,6,0,6,0 ))
dryrun = False

class WavHeader(object):
    def __init__(self, rawdata):
        self.tup = struct.unpack("iiiiihhiihhii", rawdata)
        self.chunk_id        = self.tup[0]
        self.chunk_sz        = self.tup[1]
        self.format          = self.tup[2]
        self.sub_chunk1_id   = self.tup[3]
        self.sub_chunk1_sz   = self.tup[4]
        self.audio_format    = self.tup[5]
        self.num_channel     = self.tup[6]
        self.sample_rate     = self.tup[7]
        self.byte_rate       = self.tup[8]
        self.block_align     = self.tup[9]
        self.bits_per_sample = self.tup[10]
        self.sub_chunk2_id   = self.tup[11]
        self.sub_chunk2_sz   = self.tup[12]

    def pack(self):
        return struct.pack("iiiiihhiihhii",  self.chunk_id, self.chunk_sz,
                                             self.format  , self.sub_chunk1_id,
                                             self.sub_chunk1_sz , self.audio_format,
                                             self.num_channel   , self.sample_rate ,
                                             self.byte_rate     , self.block_align ,
                                             self.bits_per_sample, self.sub_chunk2_id,
                                             self.sub_chunk2_sz )

ONE_SEC = 88200

def bytes_for_beat(bpm):
    ratio = bpm/60.0
    bytes_per_beep = ONE_SEC / ratio
    return int(bytes_per_beep)

def make_section(fh, sample_hdr, tempo, dura, sample_data):
    tot_beats = dura * (tempo/60.0);
    bps = bytes_for_beat(tempo);
    tot_bytes = 0;
    for i in range( int(tot_beats)):
        fh.write( sample_data )
        tot_bytes += sample_hdr.sub_chunk2_sz;
        for j in range( (bps - sample_hdr.sub_chunk2_sz)/8):
            fh.write( empty_sound )
            tot_bytes += len(empty_sound)
    return tot_bytes

def usage():
    print '''\
%s [Options]

Options:
  -h, --help                 Help screen
      --dryrun               Don't make wav, but print the action.
  -s, --sample=FILENAME      Sample file name
  -t, --tempo=INT            Beginning tempo
      --tempo-step=INT       Step this BPM for the next tempo (default 4)

  -d, --duration=INT         limit the total duration.  Global limiter.
      --gradual-dura=INT     Duration for gradual step.  (default 10 sec)
      --gradual-steps=INT    How many gradual steps to practice.  
                              (default 1 time)
      --stay=BPM             Set the stay mode at this bpm. 
                             stay length is 10 times of regular gradual-dura.

'''

def main():
    global dryrun
    sample_fname = "s3.wav"
    tempo = 999
    dura = -1
    tempo_step = 4
    gra_dura = 10
    gra_stepn  = 1
    stay_bpm = 999

    sa = "hs:t:d:"
    la = ('help', 'dryrun', 'sample=', 'tempo=', 'duration=', 'tempo-step=', 'gradual-dura=', \
              'gradual-steps=', 'stay=' )
    o,a = getopt.getopt(sys.argv[1:], sa, la)
    if len(o) + len(a) == 0:
        usage()
        sys.exit(1)

    for k,v in o:
        if    k in ('-h', '--help')     : usage(); sys.exit(0)
        elif  k in ('-s', '--sample')   : sample_fname = v.strip()
        elif  k in ('-t', '--tempo')    : tempo = int(v)            
        elif  k in ('-d', '--duration') : dura =  int(v)
        elif  k == '--dryrun'           : dryrun = True
        elif  k == '--tempo-step'       : tempo_step = int(v)
        elif  k == '--gradual-dura'     : gra_dura = int(v)
        elif  k == '--gradual-steps'    : gra_stepn = int(v)
        elif  k == '--stay'             :  stay_bpm = int(v)

    if tempo < 40 or tempo > 250:
        print >> sys.stderr, "Invalid tempo (%d):    Make it between 40 - MAX" % tempo
        print >> sys.stderr, "   * longer the sample length, smaller the MAX"
        sys.exit(1)

    # Reading sample header
    if sys.platform == 'win32':
        rd = open(sample_fname, "rb")
    else:
        rd = open(sample_fname, "r")
    sample_hdr = WavHeader(rd.read(44))
    sample_data = rd.read()
    rd.close()

    # Generating Beat data as WAV, storing temp file 't.wav'
    if sys.platform == 'win32':
        bdata = open("t.wav", "wb")
    else:
        bdata = open("t.wav", "w")
    
    tot_bytes = 0
    if dura == -1:
        dura = gra_dura * gra_stepn
    for i in range(0, gra_stepn):
        loop_dura = gra_dura
        if tempo > stay_bpm:
            loop_dura = gra_dura * 10

        if dryrun:
            print "will make section of (tempo=%d, dura=%d)" % (tempo, loop_dura)
        else:
            tot_bytes += make_section(bdata, sample_hdr, tempo, loop_dura, sample_data)
        tempo += tempo_step
        dura -= loop_dura
        if dura < 0:
            break

    bdata.close()
    if dryrun:
        sys.exit(0)

    # Overwrite new size, and Generate output wav file 'a.wav'
    sample_hdr.sub_chunk2_sz = tot_bytes
    if sys.platform == 'win32':
        outf = open("a.wav", 'wb')
    else:
        outf = open("a.wav", 'w')
    outf.write( sample_hdr.pack() )
    if sys.platform == 'win32':
        outf.write( open('t.wav', 'rb').read() )
    else:
        outf.write( open('t.wav').read() )
    outf.close()
    print "a.wav is made"


if __name__ == '__main__':
    main()
