from sais import sais

# BWT Encoding for byte input
def BWT_encode_bytes(s: bytes) -> bytes:
    n = len(s)
    # Add a special delimiter (represented as a byte value) at the end of the string to mark the end of the input
    s += b'\0'  # Using null byte as the special character (equivalent to '$' in text)

    # Generate the suffix array using the sais algorithm
    sa = sais(s.decode())  # Decode to string for sais, and we will handle it as bytes again later

    # Construct the BWT byte sequence
    bwt = bytearray()
    for i in range(n + 1):
        index = sa[i] - 1
        if index == -1:
            bwt.append(s[n])  # Special end character
        else:
            bwt.append(s[index])

    return bytes(bwt)


# BWT Decoding for byte input
def BWT_decode_bytes(bwt: bytes) -> bytes:
    n = len(bwt)
    # Create a table of all the characters in the BWT string
    table = [''] * n
    for i in range(n):
        table = sorted([chr(bwt[i]) + table[i] for i in range(n)])

    # The original string will be the row that ends with the null byte
    for row in table:
        if row.endswith(chr(0)):  # Null byte
            return row[:-1].encode()  # Remove the end byte and return as bytes


# Test function to validate BWT encoding and decoding with byte streams
def test_bwt_bytes():
    # Test cases with different strings (encoded as bytes)
    test_cases = [
        (b"banana",),  # Example input string
    ]

    for i, (original,) in enumerate(test_cases):
        print(f"Running test case {i + 1} for string: '{original.decode()}'")

        # BWT Encoding Test
        encoded = BWT_encode_bytes(original)
        print(f"BWT Encoded: {encoded.decode(errors='ignore')}")

        # BWT Decoding Test
        decoded = BWT_decode_bytes(encoded)
        print(f"BWT Decoded: {decoded.decode()}")

        # Verify if encoding and decoding preserve the original data
        assert decoded == original, f"Test {i + 1} failed. The decoded data does not match the original data."

        print(f"Test case {i + 1} passed!\n")


# Run the test function
if __name__ == "__main__":
    test_bwt_bytes()
