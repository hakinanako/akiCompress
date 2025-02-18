from sais import sais


class bwt:
    END = b'\x01'  # Use byte representation of 0x01 (must not appear in original string)

    @staticmethod
    def encode(s: bytes) -> bytes:
        """Perform Burrows-Wheeler Transform on byte sequence using SAIS"""
        s = s + bwt.END
        sa = sais(s)
        sa = sa[1:]  # Remove the first element which is the position of the end marker
        bwt_result = bytearray()
        for pos in sa:
            if pos == 0:
                bwt_result.append(s[-1])
            else:
                bwt_result.append(s[pos - 1])
        return bytes(bwt_result)

    @staticmethod
    def decode(r: bytes) -> bytes:
        n = len(r)
        table = [b''] * n
        for _ in range(n):
            table = sorted([r[i:i+1] + table[i] for i in range(n)])
        s = [row for row in table if row.endswith(bwt.END)][0]
        return s.rstrip(bwt.END)

# Example usage
if __name__ == '__main__':
    s = b'banana_apple_banana'
    bwt_encoded = bwt.encode(s)
    bwt_decoded = bwt.decode(bwt_encoded)
    assert bwt_decoded == s
    print('BWT test passed')