from sais import sais


class sais_bwt:
    @staticmethod
    def encode(s: bytes) -> (bytes, int):
        """使用SAIS加速的BWT编码"""
        if not s:
            return b"", 0

        # 后缀数组
        sa = sais(s)  # 256
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
        if not encoded:
            return b""

        n = len(encoded)

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

        # 还原
        result = bytearray()
        pos = index
        for _ in range(n):
            c = encoded[pos]
            result.append(c)
            pos = first[c] + rank[pos]

        return bytes(reversed(result))


# 测试
def test_sais_bwt():
    test_cases = [
        b"banana"*10+b"apple"+b"banana"*10,

    ]

    for s in test_cases:
        encoded, index = sais_bwt.encode(s)
        print(f"Encoded: {encoded}, Index: {index}")
        decoded = sais_bwt.decode(encoded, index)
        print(f"Decoded: {decoded}")
        assert s == decoded, f"Test failed for input: {s}"
        print("BWT test passed.")

if __name__ == '__main__':
    test_sais_bwt()
