import struct

empty_sound = struct.pack('bbbbbbbb', *( 4,0,0,0,6,0,6,0 ))
dryrun = False

class WavHeader:
    def __init__(self, rawdata:bytes):
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

    def pack(self) -> bytes:
        return struct.pack("iiiiihhiihhii",  self.chunk_id, self.chunk_sz,
                                             self.format  , self.sub_chunk1_id,
                                             self.sub_chunk1_sz , self.audio_format,
                                             self.num_channel   , self.sample_rate ,
                                             self.byte_rate     , self.block_align ,
                                             self.bits_per_sample, self.sub_chunk2_id,
                                             self.sub_chunk2_sz )
    def __len__(self) -> int:
        return len(self.tup)

ONE_SEC = 88200
sample_fname = 's3.wav'

def wav_split(fname: str) -> (WavHeader, bytes):
    rd = open(fname, "rb")
    sample_hdr = WavHeader(rd.read(44))
    sample_data = rd.read()
    rd.close()
    return sample_hdr, sample_data

def bytes_for_beat(bpm: int):
    ratio = bpm/60.0
    bytes_per_beep = ONE_SEC / ratio
    return int(bytes_per_beep)

def segment(tempo: int, dura_sec: int, wavdata: bytes) -> bytes:
    tot_beats = dura_sec * (tempo/60.0)
    bps = bytes_for_beat(tempo)

    rtn = b''
    for i in range( int(tot_beats)):
        rtn += wavdata
        for j in range( int((bps - len(wavdata)) / 8) ):
            rtn += empty_sound
    return rtn

