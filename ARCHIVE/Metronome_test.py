import pytest
from Metronome import *

def test_bytes_for_test():
    assert( bytes_for_beat(88200) == 60 )
