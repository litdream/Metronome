import struct

empty_sound = struct.pack('bbbbbbbb', *( 4,0,0,0,6,0,6,0 ))

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
        return struct.pack("iiiiihhiihhii", \
                           self.chunk_id, self.chunk_sz,
                           self.format  , self.sub_chunk1_id,
                           self.sub_chunk1_sz , self.audio_format,
                           self.num_channel   , self.sample_rate ,
                           self.byte_rate     , self.block_align ,
                           self.bits_per_sample, self.sub_chunk2_id,
                           self.sub_chunk2_sz )
    def __len__(self) -> int:
        return len(self.tup)

