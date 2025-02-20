from collections import deque


class mtf:
    @staticmethod
    def encode(data: bytes) -> bytes:
        # 使用deque作为双向链表
        symbols = deque(range(256))
        # 哈希表用于记录每个符号对应的节点
        symbol_map = {i: symbols[i] for i in range(256)}

        result = bytearray()

        for byte in data:
            # 查找符号
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
    def decode(data: bytes) -> bytes:
        # 使用deque作为双向链表
        symbols = deque(range(256))
        # 哈希表用于记录每个符号对应的节点
        symbol_map = {i: symbols[i] for i in range(256)}

        result = bytearray()

        for index in data:
            # 在O(1)时间查找字节
            byte = symbols[index]
            result.append(byte)
            # 将该符号移动到链表的前端
            symbols.remove(byte)
            symbols.appendleft(byte)

            # 更新哈希表
            for i in range(len(symbols)):
                symbol_map[symbols[i]] = i

        return bytes(result)
