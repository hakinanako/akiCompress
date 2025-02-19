import heapq
from collections import defaultdict

class Huffman:
    @staticmethod
    def _build_tree(data: bytes):
        # 计算字符频率
        freq = defaultdict(int)
        for byte in data:
            freq[byte] += 1

        # 构建优先队列（最小堆）
        heap = [[weight, [byte, ""]] for byte, weight in freq.items()]
        heapq.heapify(heap)

        # 合并树节点，直到堆中只剩下一个节点
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

        # 返回编码字典
        return sorted(heap[0][1:], key=lambda p: (len(p[-1]), p))

    @staticmethod
    def encode(data: bytes) -> bytes:
        huff = Huffman._build_tree(data)
        huff_dict = {byte: code for byte, code in huff}

        # 将输入数据转化为二进制字符串
        encoded_data = ''.join(huff_dict[byte] for byte in data)

        # 将二进制字符串按字节（8位）填充成字节流
        padding = 8 - len(encoded_data) % 8
        encoded_data = '0' * padding + encoded_data
        byte_array = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte_array.append(int(encoded_data[i:i+8], 2))

        return bytes(byte_array), huff_dict, padding

    @staticmethod
    def decode(encoded_data: bytes, huff_dict: dict, padding: int) -> bytes:
        # 逆向构建哈夫曼树
        reverse_dict = {code: byte for byte, code in huff_dict.items()}

        # 将字节流解码成二进制字符串
        bit_string = ''.join(f'{byte:08b}' for byte in encoded_data)
        bit_string = bit_string[:-padding]  # 去掉填充的零

        # 使用哈夫曼树解码
        current_code = ''
        decoded_data = bytearray()
        for bit in bit_string:
            current_code += bit
            if current_code in reverse_dict:
                decoded_data.append(reverse_dict[current_code])
                current_code = ''

        return bytes(decoded_data)

# Example usage:
if __name__ == '__main__':
    s = '香蕉_苹果_香蕉'.encode('utf-8')  # Encode Chinese text into UTF-8 bytes
    huffman_encoded, huff_dict, padding = Huffman.encode(s)
    huffman_decoded = Huffman.decode(huffman_encoded, huff_dict, padding)
    print(huffman_decoded.decode('utf-8'))  # Decode back to UTF-8 text
