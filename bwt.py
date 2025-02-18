from sais import sais
from collections import defaultdict

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
        """Efficiently decode a BWT-transformed byte sequence using LF Mapping"""
        # Step 1: Create the LF mapping
        # Count the frequency of each character
        freq = defaultdict(int)
        for c in r:
            freq[c] += 1

        # Step 2: Build the sorted list of characters
        sorted_chars = sorted(freq.keys())

        # Step 3: Compute the starting index for each character in the sorted list
        start = {}
        total = 0
        for c in sorted_chars:
            start[c] = total
            total += freq[c]

        # Step 4: Build the LF mapping
        lf = [0] * len(r)
        count = defaultdict(int)
        for i, c in enumerate(r):
            lf[i] = start[c] + count[c]
            count[c] += 1

        # Step 5: Reconstruct the original string
        # Find the position of the END character
        end_pos = r.find(bwt.END)
        if end_pos == -1:
            raise ValueError("END character not found in BWT string")

        # Reconstruct the original string
        s = bytearray()
        pos = end_pos
        for _ in range(len(r) - 1):
            pos = lf[pos]
            s.append(r[pos])

        return bytes(s[::-1])  # Reverse the string to get the original

# Example usage
if __name__ == '__main__':
    s = b'banana_apple_banana'
    bwt_encoded = bwt.encode(s)
    bwt_decoded = bwt.decode(bwt_encoded)
    assert bwt_decoded == s
    print('BWT test passed')