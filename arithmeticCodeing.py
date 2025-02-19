class ArithmeticCoding:
    SCALE = 1000000  # 定义缩放因子

    @staticmethod
    def encode(data: bytes, probability_map: dict) -> int:
        low = 0
        high = ArithmeticCoding.SCALE  # 高精度的上界

        for char in data:
            char = chr(char)  # Convert byte to character
            range_width = high - low
            high = low + (range_width * int(probability_map[char][1] * ArithmeticCoding.SCALE))  # Upper bound
            low = low + (range_width * int(probability_map[char][0] * ArithmeticCoding.SCALE))  # Lower bound

        return (low + high) // 2  # 返回整数类型

    @staticmethod
    def decode(encoded_value: int, length: int, probability_map: dict) -> str:
        result = []
        low = 0
        high = ArithmeticCoding.SCALE

        for _ in range(length):
            range_width = high - low
            # Check if range_width is zero
            if range_width == 0:
                break

            # Avoid division by float and keep it in integer operations
            value = (encoded_value - low) * ArithmeticCoding.SCALE // range_width  # Standardized value in [0, SCALE)

            for char, (low_prob, high_prob) in probability_map.items():
                if low_prob <= value < high_prob * ArithmeticCoding.SCALE:
                    result.append(char)
                    high = low + int(range_width * high_prob * ArithmeticCoding.SCALE)
                    low = low + int(range_width * low_prob * ArithmeticCoding.SCALE)
                    break

        return ''.join(result)



if __name__ == '__main__':
    # 字符的概率分布
    probability_map = {
        'A': (0.0, 0.4),
        'B': (0.4, 0.7),
        'C': (0.7, 0.9),
        'D': (0.9, 1.0)
    }

    # 示例数据
    data = b'ABCD' * 1000  # 假设超长字节流

    # 编码
    encoded_value = ArithmeticCoding.encode(data, probability_map)
    print("Encoded value:", encoded_value)

    # 解码
    decoded_data = ArithmeticCoding.decode(encoded_value, len(data), probability_map)
    print("Decoded data:", decoded_data)

    assert data == decoded_data.encode('utf-8')