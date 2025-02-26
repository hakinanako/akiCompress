from utils.SAIS import SAIS


class BWT:
    END = b'\x01'

    @staticmethod
    def bwt_encode(s: bytes) -> bytes:
        s = s + BWT.END
        sa = SAIS.sais(s)
        sa = sa[1:]

        bwt_result = bytearray()
        for pos in sa:
            if pos == 0:
                bwt_result.append(s[-1])
            else:
                bwt_result.append(s[pos - 1])

        return bytes(bwt_result)

    @staticmethod
    def bwt_decode(s:bytes) -> bytes:
        freq = {}
        for c in s:
            if c in freq:
                freq[c] += 1
            else:
                freq[c] = 1

        sorted_chars = sorted(freq.keys())

        start = {}
        total = 0
        for c in sorted_chars:
            start[c] = total
            total += freq[c]

        lf = [0] * len(s)
        count = {}
        index = 0
        for c in s:
            if c not in count:
                count[c] = 0
            lf[index] = start[c] + count[c]
            count[c] += 1
            index += 1

        end_pos = s.find(BWT.END)

        result = bytearray()
        pos = end_pos
        for _ in range(len(s) - 1):
            pos = lf[pos]
            result.append(s[pos])

        return bytes(result[::-1])



if __name__ == '__main__':
    s = b"banana"
    encoded = BWT.bwt_encode(s)
    decoded = BWT.bwt_decode(encoded)
    assert s == decoded