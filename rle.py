class rle:
    MAX_COUNT = 255

    @staticmethod
    def encode(data: bytes) -> bytes:
        encoded = []
        count = 1

        for i in range(1, len(data)):
            if data[i] == data[i - 1]:
                count += 1
            else:
                while count > rle.MAX_COUNT:
                    encoded.append(rle.MAX_COUNT)
                    encoded.append(data[i - 1])
                    count -= rle.MAX_COUNT
                encoded.append(count)
                encoded.append(data[i - 1])
                count = 1

        while count > rle.MAX_COUNT:
            encoded.append(rle.MAX_COUNT)
            encoded.append(data[-1])
            count -= rle.MAX_COUNT
        encoded.append(count)
        encoded.append(data[-1])

        return bytes(encoded)

    @staticmethod
    def decode(data: bytes) -> bytes:
        decoded = bytearray()

        # Iterate through the encoded data by steps of 2 (count and byte)
        for i in range(0, len(data), 2):
            count = data[i]
            byte = data[i + 1]

            # Append the byte count times to the decoded data
            decoded.extend([byte] * count)

        return bytes(decoded)


if __name__ == '__main__':
    # 测试
    data = b"ABCD"
    encoded = rle.encode(data)
    print("Encoded data:", encoded)

    # 转成可读文本
    print("Encoded data (as latin1):", encoded.decode('latin1'))

    decoded = rle.decode(encoded)
    print("Decoded data:", decoded)

    # 计算压缩率
    original_size = len(data)
    compressed_size = len(encoded)
    compression_ratio = compressed_size / original_size

    print(f"Compression ratio: {compression_ratio:.2f}")
