from typing import List

class SAIS:

    @staticmethod
    def sais(input_bytes: bytes) -> List[int]:
        num_list = list(set(input_bytes))
        num_list.sort()
        mapping = {}
        for i, e in enumerate(num_list):
            mapping[e] = i + 1
        mapping_bytes = []
        for i in input_bytes:
            mapping_bytes.append(mapping[i])
        return SAIS.get_sais_list(mapping_bytes, len(num_list))

    @staticmethod
    def get_sais_list(byte_list: List[int], num: int) -> List[int]:
        str_len: int = len(byte_list)

        '''
        对于小于2的情况，后缀数组显然即原数组加上一个0
        这里设的是尾标识的字典序最大
        '''
        if str_len < 2:
            return byte_list + [0]

        '''
        尾标0
        '''
        byte_list.append(0)
        str_len += 1

        '''
        初始化res和type数组
        '''
        res = [-1] * str_len
        type: List[int] = [1] * str_len

        '''
        判断type[i]是L还是S，逆序扫描
        满足条件 i小于他的后一个或者i等于他的后一个且i+1是L型，那么i是L型
        '''
        for i in range(str_len - 2, -1, -1):
            if (byte_list[i] < byte_list[i + 1]
                    or (byte_list[i] == byte_list[i + 1] and type[i + 1])):
                type[i] = 1
            else:
                type[i] = 0

        '''
        查找LSM/Xtype
        LSM即type[i-1] < type[i]，表现为最靠左的S型
        '''
        x_type: List[int] = []
        is_x_type: List[bool] = []

        for i in range(str_len):
            if type[i - 1] < type[i]:
                is_x_type.append(True)
            else:
                is_x_type.append(False)

        for i in range(1, str_len):
            if type[i - 1] < type[i]:
                x_type.append(i)

        x_cnt = len(x_type)

        '''
        对于输入串，统计每个字符出现的次数字典
        '''
        list_count_dict: dict = {}

        for i in byte_list:
            if i in list_count_dict:
                list_count_dict[i] += 1
            else:
                list_count_dict[i] = 1

        '''
        遍历字典，计算出每个字符的位置索引区间
        '''
        index_start: List[int] = [0] * (num + 1)
        index_end: List[int] = [0] * (num + 1)
        tmp = 0

        for key in range(num + 1):
            index_start[key] = tmp
            index_end[key] = tmp = tmp + list_count_dict[key]

        '''
        比如对于banana，编码后呈现为[2,1,3,1,3,1,0],
        字典为{1:3,3:2,2:1,0:1},
        那么就有:
        index_start=[0,1,4,5]，
        index_end=  [1,4,5,7]
        '''

        '''
        第一次诱导排序，从右向左处理Xtype子串，
        将后缀数组构造问题简化为排序LMS子字符串
        '''
        bucket_iter = []
        '''
        为每个可能的值（0 到 num）设置一个桶迭代器。
        index_start 和 index_end 定义了每个值在列表中的起始和结束位置范围。
        '''
        for start, end in zip(index_start, index_end):
            bucket_iter.append(iter(range(end - 1, start - 1, -1)))

        '''
        按逆序处理 X 类型位置列表。
        对于每个 X 类型位置 end，获取该位置的值 byte_list[end]，
        选择对应的桶迭代器，
        从中获取下一个可用位置 next_bucket，
        并将 end 填入结果数组 res 的该位置。
        '''
        for end in reversed(x_type):
            cur_bucket_iter = bucket_iter[byte_list[end]]
            next_bucket = next(cur_bucket_iter)
            res[next_bucket] = end

        '''
        处理L型后缀,即第二次诱导排序
        '''
        start_iter = []
        end_iter = []

        for start, end in zip(index_start, index_end):
            start_iter.append(iter(range(start, end)))
            end_iter.append(iter(range(end-1, start-1, -1)))

        for end in res:
            if end > 0 and not type[end - 1]:
                cur_iter = start_iter[byte_list[end - 1]]
                next_bucket = next(cur_iter)
                res[next_bucket] = end - 1

        '''
        处理S型后缀,即第三次诱导排序
        '''
        for end in reversed(res):
            if end > 0 and type[end - 1]:
                cur_iter = end_iter[byte_list[end - 1]]
                next_bucket = next(cur_iter)
                res[next_bucket] = end - 1

        '''
        处理LMS子串，重命名LSM
        '''
        name = 0
        prev = -1
        new_x_name: dict = {}

        for end in res:
            if is_x_type[end]:
                if prev == -1 or byte_list[end] != byte_list[prev]:
                    name += 1
                    prev = end
                else:
                    for i in range(1, str_len):
                        if byte_list[end + i] != byte_list[prev + i]:
                            name += 1
                            prev = end
                            break
                        if is_x_type[end + i] or is_x_type[prev + i]:
                            break
                new_x_name[end] = name - 1

        '''
        如果命名的LSM子串数量小于LSM子串数量，递归调用sais算法
        '''
        if name < x_cnt:
            not_tail_x = []
            for end in x_type:
                if end < str_len - 1:
                    not_tail_x.append(new_x_name[end])

            sub_problem_result = SAIS.get_sais_list(not_tail_x, name - 1)

            updated_x_type = []
            for i in reversed(sub_problem_result):
                updated_x_type.append(x_type[i])
            x_type = updated_x_type
        else:
            extracted_x = []
            for end in reversed(res):
                if is_x_type[end]:
                    extracted_x.append(end)
            x_type = extracted_x

        res = [-1] * str_len

        '''
        最终诱导排序的第一步：处理 X 子串，建立初始排序
        '''
        bucket_iter = []
        for start, end in zip(index_start, index_end):
            '''
            为每个值初始化桶迭代器，从大到小分配位置
            例如对于 "banana"（编码为 [2,1,3,1,3,1,0]），计数为 {0:1, 1:3, 2:1, 3:2}
            index_start = [0, 1, 4, 5], index_end = [1, 4, 5, 7]
            桶范围：0 -> [0, -1], 1 -> [3, 2, 1], 2 -> [4], 3 -> [6, 5]
            '''
            bucket_iter.append(iter(range(end - 1, start - 1, -1)))

        for end in x_type:
            '''
            根据 X 位置的值选择桶，从右向左放入结果
            例如 X 位置 [1, 3, 5]，值为 [1, 1, 1]，依次放入桶 1 的位置 [3, 2, 1]
            结果可能是 res[3] = 5, res[2] = 3, res[1] = 1
            '''
            cur_bucket_iter = bucket_iter[byte_list[end]]
            next_bucket = next(cur_bucket_iter)
            res[next_bucket] = end

        '''
        L 型后缀
        '''
        start_iter = []
        end_iter = []
        for start, end in zip(index_start, index_end):
            '''
            为 L 型初始化正向桶，为 S 型初始化逆向桶
            对于 "banana"：
            正向桶：0 -> [0], 1 -> [1, 2, 3], 2 -> [4], 3 -> [5, 6]
            逆向桶：0 -> [0], 1 -> [3, 2, 1], 2 -> [4], 3 -> [6, 5]
            '''
            start_iter.append(iter(range(start, end)))
            end_iter.append(iter(range(end - 1, start - 1, -1)))

        for end in res:
            if end > 0 and not type[end - 1]:
                '''
                检查前一个位置是否为 L 型，若是则加入其前缀
                例如 end = 5（"ana"），byte_list[4] = 3，放入桶 3 的正向位置 [5]
                更新 res[5] = 4，逐步构造 L 型后缀的排序
                '''
                cur_iter = start_iter[byte_list[end - 1]]
                next_bucket = next(cur_iter)
                res[next_bucket] = end - 1

        '''
        处理 S 型后缀
        '''
        for end in reversed(res):
            if end > 0 and type[end - 1]:
                '''
                检查前一个位置是否为 S 型，若是则加入其前缀
                例如 end = 6（""），byte_list[5] = 1，放入桶 1 的逆向位置 [1]
                更新 res[1] = 5；再如 end = 2（"nana"），byte_list[1] = 1，放入 [2]
                最终形成完整的后缀数组
                '''
                cur_iter = end_iter[byte_list[end - 1]]
                next_bucket = next(cur_iter)
                res[next_bucket] = end - 1

        return res


# 测试
if __name__ == '__main__':
    print(SAIS.sais(b"banana"))
