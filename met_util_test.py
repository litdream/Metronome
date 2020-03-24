import pytest
import met_util

def test_wavlength():
    h,d = met_util.wav_split('s3.wav')
    assert( len(h) == 13)
    assert( len(d) == 9998)
    
def test_wavheader():
    rd = open('s3.wav', 'rb')
    hdr = met_util.WavHeader(rd.read(44))
    rtn = hdr.pack()

    d = rtn[0:5].decode("utf-8") 
    assert( d == 'RIFF2')

def test_bytes_for_beat():
    assert( met_util.bytes_for_beat(60) == 88200)
    assert( met_util.bytes_for_beat(120) == 44100)
    assert( met_util.bytes_for_beat(30) == 176400)
    
