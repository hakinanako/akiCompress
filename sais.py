from collections import Counter

def sais(bytes_seq):
    uniq = list(set(bytes_seq))
    uniq.sort()
    # 将字节流转换为数字列表，每个字节映射到一个唯一的数字
    return sais_rec(list(map({e: i + 1 for i, e in enumerate(uniq)}.__getitem__, bytes_seq)), len(uniq))


def sais_rec(lst, num):

    L = len(lst)
    # 如果字节流长度小于2，直接返回结果
    if L < 2:
        return lst + [0]

    # 在字节流末尾添加结束符0
    lst = lst + [0]
    L += 1
    res = [-1] * L
    t = [1] * L

    # 计算类型数组 t，t[i] 表示第 i 个位置是 L 型还是 S 型
    for i in range(L - 2, -1, -1):
        t[i] = 1 if (lst[i] < lst[i + 1]
                     or (lst[i] == lst[i + 1]
                         and t[i + 1])) else 0

    # 判断是否是 LMS 子串
    isLMS = [t[i - 1] < t[i] for i in range(L)]
    # 找到所有的 LMS 子串的起始位置
    LMS = [i for i in range(1, L) if t[i - 1] < t[i]]
    LMSn = len(LMS)

    # 统计每个字节出现的次数
    count = Counter(lst)
    tmp = 0
    cstart = [0] * (num + 1)
    cend = [0] * (num + 1)
    # 计算每个字节的起始和结束位置
    for key in range(num + 1):
        cstart[key] = tmp
        cend[key] = tmp = tmp + count[key]

    # 第一次诱导排序：从右向左处理 LMS 子串
    cc_it = [iter(range(e - 1, s - 1, -1)) for s, e in zip(cstart, cend)]
    for e in reversed(LMS):
        res[next(cc_it[lst[e]])] = e

    # 第二次诱导排序：从左向右处理 L 型后缀
    cs_it = [iter(range(s, e)) for s, e in zip(cstart, cend)]
    ce_it = [iter(range(e - 1, s - 1, -1)) for s, e in zip(cstart, cend)]
    for e in res:
        if e > 0 and not t[e - 1]:
            res[next(cs_it[lst[e - 1]])] = e - 1

    # 第三次诱导排序：从右向左处理 S 型后缀
    for e in reversed(res):
        if e > 0 and t[e - 1]:
            res[next(ce_it[lst[e - 1]])] = e - 1

    # 为 LMS 子串命名
    name = 0
    prev = -1
    pLMS = {}
    for e in res:
        if isLMS[e]:
            if prev == -1 or lst[e] != lst[prev]:
                name += 1
                prev = e
            else:
                for i in range(1, L):
                    if lst[e + i] != lst[prev + i]:
                        name += 1
                        prev = e
                        break
                    if isLMS[e + i] or isLMS[prev + i]:
                        break
            pLMS[e] = name - 1

    # 如果命名的数量小于 LMS 子串的数量，递归处理子问题
    if name < LMSn:
        sublst = [pLMS[e] for e in LMS if e < L - 1]
        ret = sais_rec(sublst, name - 1)

        LMS = list(map(LMS.__getitem__, reversed(ret)))
    else:
        LMS = [e for e in reversed(res) if isLMS[e]]

    res = [-1] * L

    # 再次进行诱导排序
    cc_it = [iter(range(e - 1, s - 1, -1)) for s, e in zip(cstart, cend)]
    for e in LMS:
        res[next(cc_it[lst[e]])] = e

    cs_it = [iter(range(s, e)) for s, e in zip(cstart, cend)]
    ce_it = [iter(range(e - 1, s - 1, -1)) for s, e in zip(cstart, cend)]

    for e in res:
        if e > 0 and not t[e - 1]:
            res[next(cs_it[lst[e - 1]])] = e - 1
    for e in reversed(res):
        if e > 0 and t[e - 1]:
            res[next(ce_it[lst[e - 1]])] = e - 1

    return res


# LCP
def LCP(bytes_seq, n, sa):
    lcp = [-1] * (n + 1)
    rank = [0] * (n + 1)
    for i in range(n + 1):
        rank[sa[i]] = i

    h = 0
    lcp[0] = 0
    for i in range(n):
        j = sa[rank[i] - 1]
        if h > 0:
            h -= 1
        while j + h < n and i + h < n and bytes_seq[j + h] == bytes_seq[i + h]:
            h += 1
        lcp[rank[i] - 1] = h
    return lcp


if __name__ == "__main__":
    # 处理字节流
    bytes_seq = b"banana"
    n = len(bytes_seq)

    sa = sais(bytes_seq)
    print("后缀数组:", sa)

    lcp = LCP(bytes_seq, n, sa)
    print("最长公共前缀数组:", lcp)
