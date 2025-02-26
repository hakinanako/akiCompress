from collections import deque


class MTF:
    @staticmethod
    def mtf_encode(data: bytes) -> bytes:
        symbols = deque(range(256))
        symbol_map = {i: symbols[i] for i in range(256)}

        result = bytearray()

        for byte in data:
            index = symbol_map[byte]
            result.append(index)
            # 移动
            symbols.remove(byte)
            symbols.appendleft(byte)

            # 更新哈希表
            for i in range(len(symbols)):
                symbol_map[symbols[i]] = i

        return bytes(result)

    @staticmethod
    def mtf_decode(data: bytes) -> bytes:
        symbols = deque(range(256))
        symbol_map = {i: symbols[i] for i in range(256)}

        result = bytearray()

        for index in data:
            byte = symbols[index]
            result.append(byte)
            symbols.remove(byte)
            symbols.appendleft(byte)

            for i in range(len(symbols)):
                symbol_map[symbols[i]] = i

        return bytes(result)
