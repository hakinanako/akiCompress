from sais import sais
from collections import defaultdict

class bwt:
    END = b'\x01'  # End-of-file marker (ASCII value 1)

    @staticmethod
    def encode(s: bytes) -> bytes:
        s = s + bwt.END
        # Using SA-IS (Suffix Array Induced Sorting) to construct the suffix array
        sa = sais(s)
        sa = sa[1:]  # Remove the original string from the suffix array (we don't need to include it)

        bwt_result = bytearray()
        for pos in sa:
            # For each suffix, append the byte at position pos-1 (this is the BWT transformation)
            if pos == 0:
                bwt_result.append(s[-1])  # If the suffix starts at the beginning, we append the last character
            else:
                bwt_result.append(s[pos - 1])

        return bytes(bwt_result)

    @staticmethod
    def decode(r: bytes) -> bytes:
        # Create a frequency table of characters in the BWT result
        freq = defaultdict(int)
        for c in r:
            freq[c] += 1

        sorted_chars = sorted(freq.keys())

        # Calculate the starting index for each character in the sorted list
        start = {}
        total = 0
        for c in sorted_chars:
            start[c] = total
            total += freq[c]

        # The LF (Last-to-First) mapping
        lf = [0] * len(r)
        count = defaultdict(int)
        for i, c in enumerate(r):
            lf[i] = start[c] + count[c]
            count[c] += 1

        # Find the position of the END marker and reconstruct the original string
        end_pos = r.find(bwt.END)
        if end_pos == -1:
            raise ValueError("BWT decode: END marker not found")

        s = bytearray()
        pos = end_pos
        for _ in range(len(r) - 1):
            pos = lf[pos]
            s.append(r[pos])

        return bytes(s[::-1])  # Reverse the final result to get the original string

# Example usage:
# if __name__ == '__main__':
#     s = '香蕉_苹果_香蕉'.encode('utf-8')  # Encode Chinese text into UTF-8 bytes
#     bwt_encoded = bwt.encode(s)
#     bwt_decoded = bwt.decode(bwt_encoded)
#     print(bwt_decoded.decode('utf-8'))  # Decode back to UTF-8 text
