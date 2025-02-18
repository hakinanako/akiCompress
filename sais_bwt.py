from sais import sais


class sais_bwt:
    @staticmethod
    def encode(s: bytes) -> (bytes, int):
        """使用SAIS加速的BWT编码"""
        if not s:
            return b"", 0

        # 调用sais算法生成后缀数组
        sa = sais(s)  # 256 for byte values
        sa = sa[1:]
        print(f"Suffix Array: {sa}")

        # 生成BWT结果
        bwt = bytearray()
        original_index = 0
        for i, pos in enumerate(sa):
            if pos == 0:
                bwt.append(s[-1])
                original_index = i
            else:
                bwt.append(s[pos - 1])

        return bytes(bwt), original_index

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

