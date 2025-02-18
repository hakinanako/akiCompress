class bwt:
    @staticmethod
    def encode(s: bytes) -> (bytes, int):
        """对字节流进行BWT编码"""
        if not s:
            return b"", 0

        n = len(s)
        # 构建旋转矩阵
        matrix = []
        for i in range(n):
            rotation = s[i:] + s[:i]
            matrix.append((rotation, i))

        # 按字典序排序
        matrix.sort(key=lambda x: x[0])

        # 构建BWT结果和查找原始位置
        bwt = bytearray()
        for rot, _ in matrix:
            bwt.append(rot[-1])

        # 找到原始字符串的位置
        for i, (rot, orig_pos) in enumerate(matrix):
            if orig_pos == 0:
                return bytes(bwt), i

        return bytes(bwt), 0

    @staticmethod
    def decode(encoded: bytes, index: int) -> bytes:
        """从BWT编码恢复原始字节流"""
        if not encoded:
            return b""

        n = len(encoded)

        # 构建F列（第一列）
        f_col = sorted(encoded)

        # 构建L列到F列的映射
        rank = {}
        count = {}
        for i, c in enumerate(encoded):
            count[c] = count.get(c, 0)
            rank[i] = count[c]
            count[c] += 1

        # 构建F列中每个字符的起始位置
        first = {}
        curr_pos = 0
        for c in sorted(count.keys()):
            first[c] = curr_pos
            curr_pos += count[c]

        # 重建原始字符串
        result = bytearray()
        pos = index
        for _ in range(n):
            c = encoded[pos]
            result.append(c)
            pos = first[c] + rank[pos]

        return bytes(reversed(result))