from sais import sais

END = b'\x01'  # Use byte representation of 0x01 (must not appear in original string)

def bwt(s: bytes) -> bytes:
    """Perform Burrows-Wheeler Transform on byte sequence using SAIS"""
    s = s + END
    sa = sais(s)
    sa = sa[1:]  # Remove the first element which is the position of the end marker
    bwt_result = bytearray()
    for pos in sa:
        if pos == 0:
            bwt_result.append(s[-1])
        else:
            bwt_result.append(s[pos - 1])
    return bytes(bwt_result)

def ibwt(r: bytes) -> bytes:
    n = len(r)
    table = [b''] * n
    for _ in range(n):
        table = sorted([r[i:i+1] + table[i] for i in range(n)])
    s = [row for row in table if row.endswith(END)][0]
    return s.rstrip(END)

def test_bwt():
    s = b'banana_apple_banana'
    r = bwt(s)
    assert ibwt(r) == s

if __name__ == '__main__':
    test_bwt()
    print('bwt test passed')