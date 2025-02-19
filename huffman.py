import heapq
from collections import defaultdict

class HeapNode:
    def __init__(self, freq, byte=None, left=None, right=None):
        self.freq = freq
        self.byte = byte
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

class huffman:
    @staticmethod
    def _build_tree(data: bytes):
        frequency = defaultdict(int)
        for byte in data:
            frequency[byte] += 1

        heap = [HeapNode(freq, byte=byte) for byte, freq in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HeapNode(left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, merged)

        code_dict = {}
        if not heap:
            return code_dict

        root = heap[0]
        if root.byte is not None:
            code_dict[root.byte] = '0'
        else:
            def traverse(node, current_code):
                if node.byte is not None:
                    code_dict[node.byte] = current_code
                    return
                traverse(node.left, current_code + '0')
                traverse(node.right, current_code + '1')
            traverse(root, '')
        return code_dict

    @staticmethod
    def encode(data: bytes) -> bytes:
        if not data:
            return b''

        code_dict = huffman._build_tree(data)
        dict_bytes = bytearray()
        num_entries = len(code_dict)
        dict_bytes.extend(num_entries.to_bytes(2, 'big'))

        for byte_val, code_str in code_dict.items():
            code_length = len(code_str)
            code_bytes = huffman.bits_to_bytes(code_str)
            dict_bytes.append(byte_val)
            dict_bytes.append(code_length)
            dict_bytes.extend(code_bytes)

        binary_str = ''.join(code_dict[byte] for byte in data)
        total_bits = len(binary_str)
        pad_bits = (8 - (total_bits % 8)) % 8
        padded_str = binary_str + '0' * pad_bits
        data_bytes = huffman.bits_to_bytes(padded_str)
        data_part = bytearray([pad_bits]) + data_bytes

        return bytes(dict_bytes) + data_part

    @staticmethod
    def decode(encoded_data: bytes) -> bytes:
        if not encoded_data:
            return b''

        if len(encoded_data) < 2:
            raise ValueError("Invalid encoded data")

        num_entries = int.from_bytes(encoded_data[:2], 'big')
        ptr = 2
        code_dict = {}

        for _ in range(num_entries):
            if ptr + 2 > len(encoded_data):
                raise ValueError("Invalid encoded data")
            byte_val = encoded_data[ptr]
            code_length = encoded_data[ptr + 1]
            ptr += 2
            code_bytes_len = (code_length + 7) // 8
            if ptr + code_bytes_len > len(encoded_data):
                raise ValueError("Invalid encoded data")
            code_bytes = encoded_data[ptr: ptr + code_bytes_len]
            ptr += code_bytes_len
            code_str = ''.join(f"{byte:08b}" for byte in code_bytes)
            code_str = code_str[:code_length]
            code_dict[byte_val] = code_str

        if ptr >= len(encoded_data):
            raise ValueError("Invalid encoded data")
        pad_bits = encoded_data[ptr]
        ptr += 1
        data_bytes = encoded_data[ptr:]

        data_bits = ''.join(f"{byte:08b}" for byte in data_bytes)
        total_bits = len(data_bits) - pad_bits
        if total_bits < 0:
            raise ValueError("Invalid padding bits")
        data_bits = data_bits[:total_bits]

        reverse_dict = {v: k for k, v in code_dict.items()}
        decoded_data = bytearray()
        current_code = ''
        for bit in data_bits:
            current_code += bit
            if current_code in reverse_dict:
                decoded_data.append(reverse_dict[current_code])
                current_code = ''

        if current_code:
            raise ValueError("Invalid data: leftover bits")

        return bytes(decoded_data)

    @staticmethod
    def bits_to_bytes(bits: str) -> bytes:
        if not bits:
            return b''
        pad_len = (8 - len(bits) % 8) % 8
        padded = bits + '0' * pad_len
        byte_array = bytearray()
        for i in range(0, len(padded), 8):
            byte = int(padded[i:i+8], 2)
            byte_array.append(byte)
        return bytes(byte_array)

    # 测试
if __name__ == '__main__':
    # data = b"AAAABAAAAAAAAAAAAAAAAAAAAAAAAABBCCDAA"
    # 文本test.txt
    with open('test.txt', 'rb') as f:
        data = f.read()

    encoded = huffman.encode(data)
    print("Encoded data:", encoded)
    decoded = huffman.decode(encoded)
    print("Decoded data:", decoded)
    assert data == decoded

    # 压缩率
    original_size = len(data)
    compressed_size = len(encoded)
    compression_ratio = compressed_size / original_size
    print(f"Compression ratio: {compression_ratio:.2f}")