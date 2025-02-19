from io import BytesIO


class LZ77:
    END = b'\x01'  # End-of-file marker (ASCII value 1)

    @staticmethod
    def encode(data: bytes, window_size=4096, lookahead_size=18) -> bytes:
        """
        使用 LZ77 算法压缩字节流。压缩后的数据以字节流的形式返回。

        :param data: 要压缩的字节流数据
        :param window_size: 滑动窗口的大小
        :param lookahead_size: 向前查看的窗口大小
        :return: 压缩后的字节流数据
        """
        i = 0
        compressed_stream = BytesIO()
        data_length = len(data)

        while i < data_length:
            match_length = 0
            match_offset = 0

            # 查找最大匹配的子串
            start = max(0, i - window_size)
            for j in range(start, i):
                k = 0
                while k < lookahead_size and (i + k) < data_length and data[j + k] == data[i + k]:
                    k += 1
                if k > match_length:
                    match_length = k
                    match_offset = i - j

            # 如果找到匹配，则输出(偏移量, 长度, 下一个字符)
            if match_length > 0:
                # 确保在访问 data[i + match_length] 时不会越界
                if i + match_length < data_length:
                    compressed_stream.write(match_offset.to_bytes(2, 'big'))  # 偏移量，占2字节
                    compressed_stream.write(match_length.to_bytes(2, 'big'))  # 长度，占2字节
                    compressed_stream.write(data[i + match_length:i + match_length + 1])  # 下一个字符
                else:
                    compressed_stream.write(match_offset.to_bytes(2, 'big'))  # 偏移量，占2字节
                    compressed_stream.write(match_length.to_bytes(2, 'big'))  # 长度，占2字节
                    compressed_stream.write(LZ77.END)  # 处理边界的情况
                i += match_length + 1
            else:
                # 没有找到匹配，则输出(0, 0, 当前字符)
                compressed_stream.write((0).to_bytes(2, 'big'))  # 偏移量，占2字节
                compressed_stream.write((0).to_bytes(2, 'big'))  # 长度，占2字节
                compressed_stream.write(data[i:i + 1])  # 当前字符
                i += 1

        return compressed_stream.getvalue()

    @staticmethod
    def decode(compressed_data: bytes) -> bytes:
        """
        使用 LZ77 算法解压字节流。解压后的数据以字节流的形式返回。

        :param compressed_data: 压缩后的字节流数据
        :return: 解压后的字节流
        """
        compressed_stream = BytesIO(compressed_data)
        decompressed_data = bytearray()

        while True:
            offset_bytes = compressed_stream.read(2)
            length_bytes = compressed_stream.read(2)

            if not offset_bytes or not length_bytes:
                break

            offset = int.from_bytes(offset_bytes, 'big')
            length = int.from_bytes(length_bytes, 'big')
            next_char = compressed_stream.read(1)

            if offset == 0 and length == 0:
                decompressed_data.append(next_char[0])
            else:
                start_index = len(decompressed_data) - offset
                for i in range(length):
                    decompressed_data.append(decompressed_data[start_index + i])
                if next_char != LZ77.END:
                    decompressed_data.append(next_char[0])

        return bytes(decompressed_data)


# 示例
if __name__ == '__main__':
    # 打开文件
    with open('test.txt', 'rb') as f:
        input_data = f.read()

    compressed = LZ77.encode(input_data)
    print("Compressed:", compressed)

    decompressed = LZ77.decode(compressed)
    print("Decompressed:", decompressed)

# 压缩率计算
    original_size = len(input_data)
    compressed_size = len(compressed)
    print("Original size:", original_size)
    print("Compressed size:", compressed_size)
    print("Compression ratio: {:.2f}".format(compressed_size / original_size))