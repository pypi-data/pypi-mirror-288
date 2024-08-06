import pytest
from analyzemft import mftutils

def test_windows_time():
    
    wt = mftutils.WindowsTime(100, 200, False)
    assert wt.low == 100
    assert wt.high == 200
    assert isinstance(wt.unixtime, float)
    assert isinstance(wt.dtstr, str)

