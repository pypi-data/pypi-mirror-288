import pytest
from analyzemft import mft

def test_parse_record():
    
    options = mft.set_default_options()
    options.debug = False
    options.localtz = False

    # We begin by creating a MFT record

    mock_record = b'\x46\x49\x4C\x45' + b'\x00' * 1020 

    result = mft.parse_record(mock_record, options)

    assert result['magic'] == 0x454C4946 
    assert result['filename'] == ''
    assert result['fncnt'] == 0
    assert 'corrupt' not in result
    assert 'baad' not in result

    # We then test with a BAAD record
    baad_record = b'\x42\x41\x41\x44' + b'\x00' * 1020  
    baad_result = mft.parse_record(baad_record, options)
    assert baad_result['baad'] == True

    # Finally test with corrupt data
    corrupt_record = b'\x00' * 1024
    corrupt_result = mft.parse_record(corrupt_record, options)
    assert corrupt_result['corrupt'] == True
    pass

def test_mft_to_csv():
    # to do: Write tests for the mft_to_csv function
    pass

def test_decode_mft_header():
    # to do: Write tests for the test decodeMFTHeader function
    pass
