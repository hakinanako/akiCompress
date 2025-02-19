from sais import sais
from collections import defaultdict

class bwt:
    END = b'\x01'
    @staticmethod
    def encode(s: bytes) -> bytes:
        s = s + bwt.END
        # 通过sais生成后缀数组sa
        sa = sais(s)
        # 这里省略掉输入s本身
        sa = sa[1:]
        bwt_result = bytearray()
        # 迭带，将后缀数组的项作为索引查找输入中对应的byte添加到F串中
        # 对于pos-1，这是因为我们需要从该位置的“前一个字符”构建结果
        # for pos in sa:
        #     if pos == 0:
        #         bwt_result.append(s[-1])
        #     else:
        #         bwt_result.append(s[pos - 1])
        for pos in sa:
            bwt_result.append(s[pos - 1])

        return bytes(bwt_result)

    @staticmethod
    def decode(r: bytes) -> bytes:
        # 通过常数时间扫描构建频率表 排序O(n log n)
        freq = defaultdict(int)
        for c in r:
            freq[c] += 1

        sorted_chars = sorted(freq.keys())

        # 计算每个字符在排序后的字符数组中的起始索引
        # 比如对于nnbaaa freq = {n:2, b:1, a:3}，排序后的字符数组为['a', 'b', 'n']
        # 那么start = {
        #     'a': 0,
        #     'b': 3,
        #     'n': 4
        # }
        start = {}
        total = 0
        for c in sorted_chars:
            start[c] = total
            total += freq[c]

        # 对于每个字符 c 在 r 中的位置 i，
        # LF 映射的值 lf[i] 表示在经过排序后，
        # 当前字符 c 应该出现在的位置。
        # 具体来说，
        # lf[i] 等于字符 c 在排序字符集中的起始位置 start[c]，
        # 加上字符 c 在已经处理的字符中出现的次数（count[c]）。
        lf = [0] * len(r)
        count = defaultdict(int)
        for i, c in enumerate(r):
            lf[i] = start[c] + count[c]
            count[c] += 1

        # 从 END 字符的位置 end_pos 开始，
        # 通过不断根据 LF 映射（lf[pos]）找到下一个字符的位置，
        # 并将该字符加入 s 中。
        end_pos = r.find(bwt.END)
        if end_pos == -1:
            raise ValueError("BWT decode")
        s = bytearray()
        pos = end_pos
        for _ in range(len(r) - 1):
            pos = lf[pos]
            s.append(r[pos])

        return bytes(s[::-1])

# if __name__ == '__main__':
#     s = b'banana_apple_banana'
#     bwt_encoded = bwt.encode(s)
#     bwt_decoded = bwt.decode(bwt_encoded)
#     assert bwt_decoded == s
#     print('BWT test passed')