class rle:
    @staticmethod
    def encode(data: bytes) -> bytes:
        if not data:
            return b""

        encoded = bytearray()
        i = 0
        n = len(data)

        while i < n:
            # 找到连续相同字节的结束位置
            run_start = i
            run_byte = data[i]
            while i < n and data[i] == run_byte and i - run_start < 255:
                i += 1
            run_length = i - run_start

            # 如果重复次数少于3，直接存储原始字节
            if run_length < 3:
                encoded.append(0)  # 标记为未压缩块
                encoded.append(run_length)  # 未压缩块长度
                encoded.extend(data[run_start:i])
            else:
                # 压缩块：[标记(255), 长度, 字节值]
                encoded.append(255)  # 标记为压缩块
                encoded.append(run_length)
                encoded.append(run_byte)

        return bytes(encoded)

    @staticmethod
    def decode(data: bytes) -> bytes:
        if not data:
            return b""

        decoded = bytearray()
        i = 0

        while i < len(data):
            block_type = data[i]
            i += 1
            if i >= len(data):
                raise ValueError("Incomplete RLE block")

            length = data[i]
            i += 1

            if block_type == 255:  # 压缩块
                if i >= len(data):
                    raise ValueError("Incomplete RLE block")
                decoded.extend([data[i]] * length)
                i += 1
            else:  # 未压缩块
                if i + length > len(data):
                    raise ValueError("Incomplete RLE block")
                decoded.extend(data[i:i + length])
                i += length

        return bytes(decoded)